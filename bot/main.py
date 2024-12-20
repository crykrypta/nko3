import asyncio
from aiogram import Bot, Dispatcher

from bot.handlers.commands import cmd_rt

from common.log_config import LogConfig
from common.config import load_config

# Устанавливаем конфигурацию логгера
logger = LogConfig.setup_logging()

config = load_config()


bot = Bot(token=config.tg_bot.token.get_secret_value())
dp = Dispatcher()


async def main():
    dp.include_router(cmd_rt)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info("Bot stopped!")
