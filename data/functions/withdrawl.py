# © copyright by VoX DoX
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, List
from loguru import logger

from . import models


class WithdrawalLogs(models.WithdrawalLogs):

    @classmethod
    async def writeWithdrawalLogs(cls,
                                  user_id: int,
                                  wallet: str,
                                  amount: float) -> None:
        """
        Запись в базу лога о выводе
        :param user_id: int
        :param wallet: str
        :param amount: float
        :return: None
        """
        withdrawal = WithdrawalLogs(
            user_id=user_id,
            wallet=wallet,
            amount=amount
        )
        logger.info(
            f"Запись нового лога вывода: {withdrawal.id} | {withdrawal.user_id} | {withdrawal.amount} RUB")
        await withdrawal.save()


class Withdrawal(models.Withdrawal):

    @classmethod
    async def deleteWithdrawal(
            cls,
            w_id: int
    ) -> None:
        """
        Удаляет из базы данных запись о выводе
        по его айди
        :param w_id: int, id withdrawal
        :return: None
        """
        withdrawal = await cls.get(id=w_id)
        logger.info(
            f"Удаление активного вывода: {w_id} | {withdrawal.user_id} | {withdrawal.amount} RUB")
        await withdrawal.delete()

    @classmethod
    async def writeWithdrawal(
            cls,
            user_id: int,
            wallet: str,
            amount: float
    ) -> id:
        """
        Запись в базу данных данные вывода
        :param user_id: int
        :param wallet: str
        :param amount: float
        :return: None
        """
        withdrawal = Withdrawal(
            user_id=user_id,
            wallet=wallet,
            amount=amount
        )
        logger.info(
            f"Запись активного вывода: {withdrawal.id} | {withdrawal.user_id} | {withdrawal.amount} RUB")
        await withdrawal.save()

    @classmethod
    async def getWithdrawal(cls) -> Union[List[models.Withdrawal], bool]:
        """
        Получение из базы данных
        все выводы, которые там есть
        :return:
        """
        lists = await cls.all()

        if len(lists) > 0:
            return lists

        return False

    @classmethod
    async def getWithdrawalMarkup(cls,
                                  page_number: int = 1) -> Union[InlineKeyboardMarkup, bool]:
        """
        Инлайн клавиатура с выводами
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        data = await cls.getWithdrawal()
        markup = InlineKeyboardMarkup(row_width=2)
        if data:
            size = 8
            page = []
            pages = []

            for withdrawal in data:
                page.append(withdrawal)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(data) / size) not in range(16):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                markup.add(
                    InlineKeyboardButton(
                        text=f"🔰 {pages[page_number - 1][x1].user_id} | {pages[page_number - 1][x1].amount} RUB",
                        callback_data=f"user-withdrawal:{pages[page_number - 1][x1].id}")
                )
                x1 += 1

            if len(pages) > 1 and 0 < len(pages[1]):
                previous_page_number = page_number + 1 if page_number == 1 else page_number - 1
                next_page_number = page_number + 1 if len(pages) > page_number else page_number
                if page_number == len(pages):
                    previous_page_number = previous_page_number
                    next_page_number = 1

                markup.add(
                    InlineKeyboardButton(
                        text='ᐊ', callback_data=f'withdrawal-page:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'withdrawal-page:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            )

            return markup

        return False
