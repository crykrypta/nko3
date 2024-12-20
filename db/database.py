import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession # noqa

from db.models import Base  # type: ignore

from common.config import load_config  # type: ignore

# Логирование
logger = logging.getLogger(__name__)
# Конфигурация с чувствительнымт данными
config = load_config()

# ссылка для подключения к Базе Данных PostgreSQL + asyncpg
db_url = config.db_url

# Создаем асинхронный движок для подключения к БД
engine = create_async_engine(db_url, echo=True)

# Создаем асинхронную сессию для работы с БД
asession = async_sessionmaker(bind=engine, class_=AsyncSession)


def init_db():
    logger.info('Сбрасываем все таблицы')
    Base.metadata.drop_all

    logger.info('Создаем новые таблицы')
    Base.metadata.create_all
