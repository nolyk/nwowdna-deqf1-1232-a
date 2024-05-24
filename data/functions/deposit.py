# © copyright by VoX DoX
from loguru import logger

from . import models


class DepositLogs(models.DepositLogs):

    @classmethod
    async def writeDepositLogs(cls,
                               user_id: int,
                               types: str,
                               amount: float) -> None:
        """
        Запись нового депозита в базу
        :param user_id: int
        :param types: str
        :param amount: float
        :return: None
        """
        logger.info(f"Новый депозит! {user_id} | {types} | {amount}")
        await DepositLogs(
            user_id=user_id,
            type=types,
            amount=amount
        ).save()

