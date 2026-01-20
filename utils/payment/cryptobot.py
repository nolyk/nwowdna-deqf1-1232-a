from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Tuple
from aiocryptopay import AioCryptoPay, Networks
import ssl
import certifi

from utils import config


class Cryptobot:
    def __init__(self):
        self._cryptocurrency = [
            'USDT', 'BUSD', 'BTC', 'ETH', 'TON'
        ]
        
        token = config.config("crypto_api")
        
        # Создаем SSL контекст для aiohttp
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Инициализируем CryptoPay с TOKEN для MAIN сети
        self.crypto = AioCryptoPay(
            token=token,
            network=Networks.MAIN_NET
        )
        
    async def getUsdt_Rub_Rate(self) -> float:
        """
        Получить актуальный курс USDT к RUB через API Cryptobot
        :return: float (1 USDT = ? RUB)
        """
        try:
            rates = await self.crypto.get_exchange_rates()
            for rate in rates:
                # Ищем курс USDT к RUB или через USD
                if rate.source == 'USDT' and rate.target == 'RUB':
                    return float(rate.rate)
            # Если нет прямого курса, пытаемся через USD
            for rate in rates:
                if rate.source == 'USDT' and rate.target == 'USD':
                    usdt_usd = float(rate.rate)
                    # Теперь ищем USD к RUB
                    for rate2 in rates:
                        if rate2.source == 'USD' and rate2.target == 'RUB':
                            return usdt_usd * float(rate2.rate)
        except Exception as e:
            print(f"Ошибка получения курса USDT/RUB: {e}")
        
        # По умолчанию примерно 100 RUB за 1 USD
        return 100.0

    async def rubToUsd(self, amount: float) -> float:
        """
        Конвертирование RUB в USD через средние курсы
        Используется актуальный курс: 1 USD ≈ 100 RUB
        :param amount: float (сумма в РУБ)
        :return: float (сумма в USD)
        """
        return amount / 100.0

    async def getExchangeRate(self) -> float:
        """
        Получить актуальный курс USDT к USD
        :return: float (курс USDT/USD)
        """
        try:
            rates = await self.crypto.get_exchange_rates()
            for rate in rates:
                if rate.source == 'USDT' and rate.target == 'USD':
                    return float(rate.rate)
        except Exception as e:
            print(f"Ошибка получения курса USDT: {e}")
        return 1.0  # По умолчанию 1:1

    async def createInvoice(
            self,
            amount: float
    ) -> Tuple[int, str, float]:
        """
        Создание инвойса на оплату в RUB
        Конвертирует РУБ → USDT по актуальному курсу
        
        :param amount: float (сумма в РУБ)
        :return: (invoice_id, pay_url, amount_rub)
        """
        try:
            # Получаем актуальный курс USDT к RUB
            usdt_rub_rate = await self.getUsdt_Rub_Rate()
            print(f"📊 Курс USDT/RUB: 1 USDT = {usdt_rub_rate} RUB")
            
            # Конвертируем РУБ в USDT по актуальному курсу
            # amount (RUB) / usdt_rub_rate = amount (USDT)
            usdt_amount = amount / usdt_rub_rate
            # Округляем до 6 знаков для точности (не 2!)
            usdt_amount = round(usdt_amount, 6)
            
            print(f"💳 Создание инвойса: {amount} RUB → {usdt_amount} USDT (по курсу {usdt_rub_rate})")
            
            # Описание с исходной суммой в RUB
            description = f"Пополнение {int(amount)} RUB"
            
            invoice = await self.crypto.create_invoice(
                asset='USDT',
                amount=usdt_amount,
                description=description
            )
            
            # Получаем URL для оплаты
            pay_url = invoice.pay_url if hasattr(invoice, 'pay_url') else invoice.bot_invoice_url
            
            return (
                invoice.invoice_id,
                pay_url,
                amount
            )
        except Exception as e:
            print(f"❌ Ошибка создания инвойса: {e}")
            raise Exception(f"Не удалось создать инвойс: {str(e)}")

    async def paidInvoice(self,
                          invoice_id: int) -> bool:
        """
        Проверка, оплачен ли инвойс
        :param invoice_id: int
        :return: bool (True если оплачен, False если нет)
        """
        try:
            invoices = await self.crypto.get_invoices(invoice_ids=invoice_id)
            if invoices and len(invoices) > 0:
                status = invoices[0].status
                print(f"📊 Статус инвойса {invoice_id}: {status}")
                if status == 'paid':
                    return True
            return False
        except Exception as e:
            print(f"❌ Ошибка проверки платежа: {e}")
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
                text='« Вернуться назад', callback_data='return-menu:cabinet'
            )
        )
        return markup

    @staticmethod
    def geyCryptoPayMarkup(invoice_url: str,
                           invoice_id: int,
                           amount: float,
                           # asset: str
                           ) -> InlineKeyboardMarkup:
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
                        text='♻️ Проверить', callback_data=f'check-crypto-pay:{invoice_id}:{amount}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='« Вернуться назад', callback_data='return-menu:cabinet'
                    )
                ]
            ]
        )
        return markup
