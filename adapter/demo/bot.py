import json
from pathlib import Path
from typing import Union, Any, Optional

import httpx
from nonebot import logger
from nonebot.adapters import Bot as BaseBot
from nonebot.internal.driver import Request

from .event import *
from .message import *


class Bot(BaseBot):
    async def send(self, event: "Event", message: Union[str, "Message", "MessageSegment"], **kwargs: Any) -> Any:
        pass

    def get_self_id(self) -> int:
        return int(self.self_id)

    async def call_api(self, api: str, **data: Any) -> Any:
        data = (await super().call_api(api, **data)).content
        try:
            return json.loads(data)
        except Exception as e:
            logger.exception(e)
            logger.error("解析api失败")
            return data

    async def get_token(self, *, account: Optional[str] = None, password: Optional[str] = None):
        data = await self.call_api("tokens", method="POST", email="test@eya46.com", password="thisisatestaccount")
        logger.debug(data)
        return data["data"]["token"]

    async def upload_image(self, data: Path) -> dict:
        def _get_file():
            return open(data,"rb")

        token = await self.get_token()

        args = {
            "headers": {
                "Authorization": f"Bearer {token}",
                "Accept": f"application/json"
            }, "files": {"file": _get_file()}
        }

        req = Request(
            "POST", "https://pic.eya46.com/api/v1/upload", **args
        )
        logger.debug(req.files)
        result = json.loads((await self.adapter.request(req)).content)
        logger.debug("调用驱动器~httpx")
        logger.debug(result)

        result = httpx.post("https://pic.eya46.com/api/v1/upload",**args).json()
        logger.debug("直接调用httpx")
        logger.debug(result)

        return result
