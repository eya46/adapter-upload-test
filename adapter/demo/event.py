from datetime import datetime

from nonebot import escape_tag
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    self_uid: int
    post_type: str

    def get_type(self) -> str:
        return self.post_type

    def get_event_name(self) -> str:
        return self.post_type

    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    def get_user_id(self) -> str:
        return str(self.self_uid)

    def get_session_id(self) -> str:
        raise ValueError("Event has no session id!")

    def get_message(self) -> "Message":
        raise ValueError("Event has no message!")

    def is_tome(self) -> bool:
        return False

class MessageEvent(Event):
    post_type: str = "message"
    message: Message

    def get_message(self) -> Message:
        return self.message

    def get_event_description(self) -> str:
        return str(self.message)

