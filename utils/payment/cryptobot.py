from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Tuple
from aiocryptopay import AioCryptoPay

from utils import config
from ..cbrf import CentralBankAPI


class Cryptobot:
    def __init__(self):
        self._cryptocurrency = [
            'USDT', 'BUSD', 'BTC', 'ETH', 'TON'
        ]
        self.crypto = AioCryptoPay(
            token=config.config("crypto_api")
        )
        self.cbrf = CentralBankAPI()

    async def getAmount(self,
                        amount: float,
                        currency: str) -> float:
        """
        Получение суммы для оплаты по курсу крипты
        :param amount: float
        :param currency: str
        :return:
        """
        courses = await self.crypto.get_exchange_rates()
        await self.crypto.close()

        for course in courses:
            if course.source == currency and course.target == 'USD':
                return amount / course.rate

    async def createInvoice(self,
                            asset: str,
                            amount: float) -> Tuple[int, str, float]:
        """
        Создание инвойса на оплату
        :param asset: str (монета)
        :param amount: float (сумма)
        :return:
        """
        data = await self.crypto.create_invoice(
            asset=asset,
            amount=await self.getAmount(
                amount=amount,
                currency=asset
            ),
            description="Пополнение Garant • EW"
        )
        await self.crypto.close()

        rub_currency = float(self.cbrf.getCurrency()) * amount

        return data.invoice_id, data.pay_url, rub_currency

    async def paidInvoice(self,
                          invoice_id: int) -> bool:
        """
        Проверка, имеется ли пополнение
        :param invoice_id: int
        :return: bool
        """
        invoice = await self.crypto.get_invoices(
            invoice_ids=invoice_id
        )
        print(invoice[0])
        await self.crypto.close()
        if invoice[0].status == "paid":
            return True

        return False

    def getCurrencyMarkup(self) -> InlineKeyboardMarkup:
        """
        Инлайн-клава с криптой для пополнения
        :return: InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup(row_width=3)
        for currency in self._cryptocurrency:
            markup.insert(
                InlineKeyboardButton(
                    text=currency, callback_data=f'crypto-pay-currency:{currency}'
                )
            )
        markup.add(
            InlineKeyboardButton(
                text='🔙 Назад в кабинет', callback_data='return-menu:cabinet'
            )
        )
        return markup

    @staticmethod
    def geyCryptoPayMarkup(invoice_url: str,
                           invoice_id: int,
                           amount: float,
                           asset: str) -> InlineKeyboardMarkup:
        """
        Инлайн-клава на оплату и проверку пополнения
        :param invoice_url: str
        :param invoice_id: int
        :param amount: float
        :param asset: str
        :return: InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Оплатить', url=invoice_url
                    ),
                    InlineKeyboardButton(
                        text='♻️ Проверить', callback_data=f'check-crypto-pay:{invoice_id}:{amount}:{asset}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='🔙 Назад в кабинет', callback_data='return-menu:cabinet'
                    )
                ]
            ]
        )
        return markup
