from typing import Union, List
from loguru import logger
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from . import models


class BlackList(models.BlackList):

    @classmethod
    async def checkingUser(
            cls,
            user_id: int = None,
            username: str = None
    ) -> Union[models.BlackList, bool]:
        """
        Проверка пользователя в блеклисте
        :param user_id: int
        :param username: str
        :return:
        """
        if user_id is not None:
            user = await cls.exists(user_id=user_id)
        else:
            user = await cls.exists(username=username)

        if user:
            data = await cls.get(user_id=user_id) if user_id is not None \
                else await cls.get(username=username)

            return data

        return False

    @classmethod
    async def writeUser(
            cls,
            user_id: int,
            username: str,
            amount: float,
            desc: str
    ) -> int:
        """
        Запись пользователя в блеклист
        :param user_id: int
        :param username: str
        :param amount: float
        :param desc: str
        :return: int
        """
        logger.info(
            f"Запись нового блеклиста: {user_id} | {username} | {amount} RUB")
        black = await BlackList(
            user_id=user_id,
            username=username,
            amount=amount,
            description=desc
        )
        await black.save()

        return black.id

    @classmethod
    async def deleteUser(
            cls,
            bl_id: int
    ) -> None:
        """
        Удаление пользователя с блеклиста
        :param bl_id: int
        :return: None
        """
        black = await cls.get(id=bl_id)
        await black.delete()

    @classmethod
    async def updateStatus(
            cls,
            bl_id: int,
            status: str = "ACTIVE"
    ) -> None:
        """
        Обновление статуса юзера в блеклисте
        :param bl_id: int
        :param status: str
        :return: None
        """
        print(bl_id)
        black = await cls.get(id=bl_id)
        black.status = status
        await black.save()

    @classmethod
    async def getAllScammers(
            cls,
            status: str = "ACTIVE"
    ) -> Union[List[models.BlackList], bool]:
        """
        Получаем массив BlackList из базы
        :param status: str
        :return: []BlackList
        """
        lists = await cls.filter(status=status)
        if len(lists) > 0:
            return lists

        return False

    @classmethod
    async def getMarkup(
            cls,
            page_number: int = 1
    ) -> Union[InlineKeyboardMarkup, bool]:
        """
        Получаем инлайн-клаву
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        markup = InlineKeyboardMarkup(row_width=2)
        backlist = await cls.getAllScammers()

        if backlist:
            size = 6
            page = []
            pages = []

            for bl in backlist:
                page.append(bl)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(backlist) / size) not in range(12):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                markup.add(
                    InlineKeyboardButton(
                        text=f"🛡 @{pages[page_number - 1][x1].username} | {pages[page_number - 1][x1].user_id}",
                        callback_data=f"blacklist-scammer:{pages[page_number - 1][x1].id}")
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
                        text='ᐊ', callback_data=f'blacklist-page:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'blacklist-page:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text="« Вернуться назад", callback_data='return-menu:default')
            )

            return markup

        return False

    @classmethod
    async def getAdminMarkup(
            cls,
            page_number: int = 1
    ) -> Union[InlineKeyboardMarkup, bool]:
        """
        Получаем инлайн-клаву
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        markup = InlineKeyboardMarkup(row_width=2)
        backlist = await cls.getAllScammers()

        if backlist:
            size = 8
            page = []
            pages = []

            for bl in backlist:
                page.append(bl)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(backlist) / size) not in range(16):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                markup.add(
                    InlineKeyboardButton(
                        text=f"🛡 @{pages[page_number - 1][x1].username} | {pages[page_number - 1][x1].user_id}",
                        callback_data=f"admin-blacklist-scammer:{pages[page_number - 1][x1].id}")
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
                        text='ᐊ', callback_data=f'admin-blacklist-page:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'admin-blacklist-page:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text="🔙 Закрыть", callback_data='close-message')
            )

            return markup

        return False
