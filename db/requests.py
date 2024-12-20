import logging

from db.models import UsersOrm  # type: ignore
from db.database import asession  # type: ignore

logger = logging.getLogger(__name__)


async def insert_user(tg_id: int, username: str):
    async with asession() as session:
        session.add(
            UsersOrm(tg_id=tg_id, username=username)
        )
        await session.commit()


async def get_user_by_tg_id(tg_id: int) -> UsersOrm | None:
    """Получение пользователя по tg_id

    Args:
        tg_id (int): .from_user.id

    Returns:
        UsersOrm | None:
    """
    async with asession() as session:
        user = await session.get(UsersOrm, {'tg_id': tg_id})
        return user


async def create_new_user(tg_id: int, username: str) -> UsersOrm | None:
    """Создает нового пользователя

    Args:
        tg_id (int): .from_user.id
        username (str): .from_user.full_name

    Returns:
        UsersOrm - если такой пользователь уже существует
        None - если это новый пользователь
    """
    async with asession() as session:
        try:
            user = await session.get(UsersOrm, {'tg_id': tg_id})
        except Exception as e:
            logger.error('Не удалось получить пользователя по tg_id: %s | %s', tg_id, e) # noqa

        if user is None:
            logger.info('Создание нового пользователя tg_id: %s', tg_id)
            session.add(
                UsersOrm(tg_id=tg_id, username=username)
            )
            await session.commit()
            return None
        else:
            logger.info("Пользователь %s уже есть в базе", user.id)
            return user
