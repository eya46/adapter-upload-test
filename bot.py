import nonebot
from adapter.demo.adapter import Adapter as Demo_Adapter

nonebot.init()

app = nonebot.get_app()

driver = nonebot.get_driver()
driver.register_adapter(Demo_Adapter)

nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
