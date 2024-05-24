from aerich import Command
from tortoise import Tortoise
from loguru import logger

from .user import Users
from .channel import ChannelSub
from .deals import Reviews, Deals
from .withdrawl import WithdrawalLogs, Withdrawal
from .blacklist import BlackList
from .deposit import DepositLogs
from .admin import Admin


async def createModel(config: dict):
    command = Command(tortoise_config=config, app="models")
    await command.init()
    await command.init_db(safe=True)
    await command.upgrade(True)


async def migrate_models(config: dict):
    command = Command(tortoise_config=config, app="models")
    await command.init()
    await command.migrate("update")
    await command.upgrade(False)


async def init_orm(config: dict) -> None:
    await Tortoise.init(config=config, use_tz=True, timezone="UTC+3")
    await Tortoise.generate_schemas()
    logger.info(f"Tortoise-ORM started, {Tortoise.apps}")


async def close_orm() -> None:
    await Tortoise.close_connections()
    logger.info("Tortoise-ORM shutdown")
