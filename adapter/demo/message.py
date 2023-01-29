from typing import Type, Iterable

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    def get_message_class(cls) -> Type["MessageSegment"]:
        return MessageSegment

    def __str__(self) -> str:
        return self.data["text"]

    def is_text(self) -> bool:
        return True

    @staticmethod
    def text(text: str):
        return MessageSegment("text", {"text": text})


class Message(BaseMessage[MessageSegment]):
    @classmethod
    def get_segment_class(cls) -> Type["MessageSegment"]:
        return MessageSegment

    @staticmethod
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
