import asyncio
from aiogram import Bot, Dispatcher

from bot.handlers.commands import cmd_rt
from bot.handlers.callbacks import callback_rt

from db.database import init_db

from common.log_config import LogConfig
from common.config import load_config

# Устанавливаем конфигурацию логгера
logger = LogConfig.setup_logging()

config = load_config()


bot = Bot(token=config.tg_bot.token.get_secret_value())
dp = Dispatcher()


async def main():
    # Инициализация базы данных
    init_db()

    # Включение Роутеров в диспетчер
    dp.include_router(cmd_rt)
    dp.include_router(callback_rt)
    # Удаляем не обработанные запросы
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг сервера Telegram
    await dp.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info("Bot stopped!")
