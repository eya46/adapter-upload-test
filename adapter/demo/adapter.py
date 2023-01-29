import asyncio
import time
from typing import Any, Optional, List
from urllib.parse import urljoin

from nonebot import Driver, logger
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.internal.driver import ForwardDriver, Request, Response
from nonebot.message import handle_event

from . import MessageEvent
from .bot import Bot


class Adapter(BaseAdapter):
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.tasks: List["asyncio.Task"] = []
        self._setup()

    @classmethod
    def get_name(cls) -> str:
        return "Demo01"

    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Response:
        url = urljoin("https://pic.eya46.com/api/v1/", api)
        logger.debug(url)
        if (method := data.pop("method")) == "GET":
            return await self.request(Request(
                method, url, params=data, headers={
                    "Accept": "application/json"
                }
            ))
        else:
            return await self.request(Request(
                method, url, json=data, headers={"Accept": "application/json"}
            ))

    @staticmethod
    async def _run(bot: Bot):
        while True:
            await handle_event(bot, MessageEvent.parse_obj(
                {"message": str(int(time.time())), "self_uid": int(bot.self_id)}
            ))
            await asyncio.sleep(10)

    async def _start_forward(self):
        bot: Optional[Bot]

        bot = Bot(
            self, self_id=str(int(time.time()))
        )
        logger.debug("link")
        self.bot_connect(bot)
        try:
            self.tasks.append(asyncio.create_task(self._run(bot)))
        finally:
            if bot:
                self.bot_disconnect(bot)

    async def _stop_forward(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

    def _setup(self) -> None:
        if isinstance(self.driver, ForwardDriver):
            self.driver.on_startup(self._start_forward)
            self.driver.on_shutdown(self._stop_forward)
        else:
            logger.error(f"{self.get_name()} 需要ForwardDriver!")
