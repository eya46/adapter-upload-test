import os
from pathlib import Path

from nonebot import on_message, logger

from adapter.demo import MessageEvent, Bot

upload = on_message()

first = False

local = os.path.dirname(__file__)


@upload.handle()
async def upload_handle(bot: Bot, event: MessageEvent):
    logger.debug(event.message)
    global first
    if not first:
        first = not first
        img = Path(local, "pics/peach.png")
        await bot.upload_image(img)
