from aiogram import Bot, Dispatcher

from common.log_config import LogConfig
from common.config import load_config

# Устанавливаем конфигурацию логгера
logger = LogConfig.setup_logging()

config = load_config()


bot = Bot(token=config.tg_bot.token.get_secret_value())
dp = Dispatcher()
