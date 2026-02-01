# Руководство по участию в разработке

Спасибо за интерес к проекту **WB SDK** — Python SDK для работы с [API Wildberries](https://dev.wildberries.ru/). Ниже описано, как настроить окружение, соблюдать стиль кода и отправить изменения.

---

## Требования и окружение

- **Python 3.10+** (см. [pyproject.toml](pyproject.toml)).
- Клонируйте репозиторий и установите пакет в режиме разработки.

**С помощью pip:**

```bash
git clone https://github.com/RTHeLL/wbsdk.git
cd wbsdk
pip install -e ".[dev]"
```

**С помощью uv:**

```bash
git clone https://github.com/RTHeLL/wbsdk.git
cd wbsdk
uv sync --all-extras
```

После установки будут доступны dev-зависимости: pytest, respx, ruff, mypy и др.

---

## Структура проекта

| Каталог / файл | Описание |
|----------------|----------|
| `src/wbsdk/` | Исходный код пакета |
| `src/wbsdk/api/` | Модули API: content, prices, marketplace, warehouses, analytics |
| `src/wbsdk/schemas/` | Pydantic-схемы ответов API |
| `tests/` | Тесты; общие фикстуры (`token`, `client`) заданы в [conftest.py](tests/conftest.py) |

---

## Стиль кода и линтинг

Настройки заданы в [pyproject.toml](pyproject.toml).

- **Ruff**: длина строки 100, целевая версия Python 3.10, правила `E`, `F`, `I`, `N`, `W`, `UP`.
- Перед коммитом и перед отправкой PR рекомендуется запускать:

```bash
ruff check src/ tests/
ruff format src/ tests/
```

- **mypy**: проверка типизации:

```bash
mypy src/
```

Убедитесь, что линтеры и типы проходят без ошибок перед созданием Pull Request.

---

## Тесты

Запуск тестов (как в CI):

```bash
pytest tests/ -v --tb=short
```

- Тесты используют **respx** для моков HTTP-запросов.
- Общие фикстуры (`token`, `client`) описаны в [tests/conftest.py](tests/conftest.py).
- При добавлении или изменении функциональности добавляйте или обновляйте тесты.

---

## Процесс внесения изменений

1. Создайте ветку от `main` (или текущей основной ветки).
2. Вносите изменения, соблюдая стиль кода и при необходимости добавляя/обновляя тесты.
3. **Сообщения коммитов** — только на **русском языке**.
4. Откройте Pull Request с понятным описанием изменений.
5. Убедитесь, что CI проходит (в [.github/workflows/publish.yml](.github/workflows/publish.yml) перед публикацией выполняются тесты).

---

## Дополнительно

- [Документация API Wildberries](https://dev.wildberries.ru/)
- [README](README.md) — установка, быстрый старт и описание модулей
- Лицензия: **MIT**. Участвуя в проекте, вы соглашаетесь с тем, что ваш вклад будет распространяться под той же лицензией (см. [LICENSE](LICENSE)).
