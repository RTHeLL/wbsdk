"""API вопросов, отзывов, чатов и претензий (feedbacks-api)."""

from typing import Any

from wbsdk.api.base import BaseAPI


class CommunicationsAPI(BaseAPI):
    """API общения с покупателями: вопросы, отзывы, пины, чаты, претензии."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="feedbacks")

    # --- Вопросы ---

    def get_new_feedbacks_questions(self) -> Any:
        """Есть ли непросмотренные вопросы и отзывы."""
        return self.get("/api/v1/new-feedbacks-questions")

    def get_questions_count_unanswered(self) -> Any:
        """Количество неотвеченных вопросов."""
        return self.get("/api/v1/questions/count-unanswered")

    def get_questions_count(
        self,
        date_from: int,
        date_to: int,
        *,
        is_answered: bool | None = None,
    ) -> Any:
        """Количество вопросов за период."""
        params: dict[str, Any] = {"dateFrom": date_from, "dateTo": date_to}
        if is_answered is not None:
            params["isAnswered"] = is_answered
        return self.get("/api/v1/questions/count", params=params)

    def get_questions(self, payload: dict[str, Any]) -> Any:
        """Список вопросов."""
        return self.post("/api/v1/questions", json=payload)

    def get_question(self, question_id: int) -> Any:
        """Один вопрос по ID."""
        return self.get("/api/v1/question", params={"id": question_id})

    # --- Отзывы ---

    def get_feedbacks_count_unanswered(self) -> Any:
        """Количество неотвеченных отзывов."""
        return self.get("/api/v1/feedbacks/count-unanswered")

    def get_feedbacks_count(
        self,
        date_from: int,
        date_to: int,
        *,
        is_answered: bool | None = None,
    ) -> Any:
        """Количество отзывов за период."""
        params: dict[str, Any] = {"dateFrom": date_from, "dateTo": date_to}
        if is_answered is not None:
            params["isAnswered"] = is_answered
        return self.get("/api/v1/feedbacks/count", params=params)

    def get_feedbacks(self, payload: dict[str, Any]) -> Any:
        """Список отзывов."""
        return self.post("/api/v1/feedbacks", json=payload)

    def answer_feedback(self, payload: dict[str, Any]) -> Any:
        """Ответить на отзыв."""
        return self.patch("/api/v1/feedbacks/answer", json=payload)

    def feedback_order_return(self, payload: dict[str, Any]) -> Any:
        """Заявка на возврат по отзыву."""
        return self.post("/api/v1/feedbacks/order/return", json=payload)

    def get_feedback(self, feedback_id: str) -> Any:
        """Один отзыв по ID."""
        return self.get("/api/v1/feedback", params={"id": feedback_id})

    def get_feedbacks_archive(self, payload: dict[str, Any]) -> Any:
        """Архив отзывов."""
        return self.post("/api/v1/feedbacks/archive", json=payload)

    # --- Закреплённые отзывы ---

    def get_pins(self, payload: dict[str, Any]) -> Any:
        """Закреплённые отзывы."""
        return self.post("/api/feedbacks/v1/pins", json=payload)

    def get_pins_count(self) -> Any:
        """Количество закреплённых отзывов."""
        return self.get("/api/feedbacks/v1/pins/count")

    def get_pins_limits(self) -> Any:
        """Лимиты на закрепление."""
        return self.get("/api/feedbacks/v1/pins/limits")

    # --- Чат с покупателями ---

    def get_seller_chats(self, payload: dict[str, Any]) -> Any:
        """Список чатов."""
        return self.post("/api/v1/seller/chats", json=payload)

    def get_seller_events(self, payload: dict[str, Any]) -> Any:
        """События чата."""
        return self.post("/api/v1/seller/events", json=payload)

    def send_seller_message(self, payload: dict[str, Any]) -> Any:
        """Отправить сообщение."""
        return self.post("/api/v1/seller/message", json=payload)

    def get_seller_download(self, file_id: str) -> Any:
        """Скачать файл из чата."""
        return self.get(f"/api/v1/seller/download/{file_id}")

    # --- Претензии ---

    def get_claims(self, payload: dict[str, Any]) -> Any:
        """Список претензий."""
        return self.post("/api/v1/claims", json=payload)

    def get_claim(self, claim_id: int) -> Any:
        """Одна претензия по ID."""
        return self.get("/api/v1/claim", params={"id": claim_id})
