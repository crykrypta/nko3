from pydantic import BaseModel, SecretStr
from environs import Env


class OpenAIScheme(BaseModel):
    token: SecretStr


class TGBotScheme(BaseModel):
    token: SecretStr


class Config(BaseModel):
    openai: OpenAIScheme
    tg_bot: TGBotScheme


def load_config() -> Config:
    """Загружает конфигурацию из переменных окружения"""
    env = Env()
    env.read_env()
    return Config(
        openai=OpenAIScheme(
            token=SecretStr(env.str("OPENAI_API_KEY"))
        ),
        tg_bot=TGBotScheme(
            token=SecretStr(env.str("TG_BOT_TOKEN"))
        )
    )
