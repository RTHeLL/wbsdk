"""Адаптивный rate limiter по доменам WB API."""

import threading
import time
from collections import deque
from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    """Конфигурация лимита для домена."""

    requests_per_period: int
    period_seconds: float
    min_interval_ms: float


# Конфигурации по доменам WB API
DEFAULT_LIMITS: dict[str, RateLimitConfig] = {
    "content": RateLimitConfig(100, 60.0, 600),
    "marketplace": RateLimitConfig(300, 60.0, 200),
    "prices": RateLimitConfig(10, 6.0, 600),
    "analytics": RateLimitConfig(3, 60.0, 20000),
    "advert": RateLimitConfig(5, 1.0, 200),
    "advert_media": RateLimitConfig(10, 1.0, 100),
    "dp_calendar": RateLimitConfig(10, 6.0, 600),
    "feedbacks": RateLimitConfig(3, 1.0, 333),
    "buyer_chat": RateLimitConfig(10, 10.0, 1000),
    "returns": RateLimitConfig(20, 60.0, 150),
}


class RateLimiter:
    """Ограничитель частоты запросов с поддержкой нескольких доменов."""

    def __init__(self, limits: dict[str, RateLimitConfig] | None = None):
        self._limits = limits or DEFAULT_LIMITS.copy()
        self._lock = threading.Lock()
        self._request_times: dict[str, deque[float]] = {}

    def _get_queue(self, domain: str) -> deque[float]:
        """Возвращает очередь времени запросов для домена."""
        if domain not in self._request_times:
            self._request_times[domain] = deque(maxlen=1000)
        return self._request_times[domain]

    def acquire(self, domain: str = "marketplace") -> None:
        """Блокирует до тех пор, пока запрос не будет разрешён по лимиту."""
        config = self._limits.get(domain, self._limits["marketplace"])
        min_interval_sec = config.min_interval_ms / 1000.0

        with self._lock:
            now = time.monotonic()
            queue = self._get_queue(domain)

            # Удаляем старые записи за пределами периода
            cutoff = now - config.period_seconds
            while queue and queue[0] < cutoff:
                queue.popleft()

            # Проверяем лимит запросов за период
            if len(queue) >= config.requests_per_period:
                sleep_time = queue[0] + config.period_seconds - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
                return self.acquire(domain)  # Рекурсивно после ожидания

            # Соблюдаем минимальный интервал между запросами
            if queue:
                last = queue[-1]
                elapsed = now - last
                if elapsed < min_interval_sec:
                    time.sleep(min_interval_sec - elapsed)

            queue.append(time.monotonic())
