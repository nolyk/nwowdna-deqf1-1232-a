# © copyright by VoX DoX
import datetime

from . import Users, WithdrawalLogs, Deals


class Admin:
    def __init__(self):
        super().__init__()
        self.amount_user_hour = 0
        self.amount_user_day = 0
        self.amount_users_all = 0
        self.all_users_balance = 0

        self.all_amount = 0
        self.day_amount = 0
        self.all_with = 0

        self.day_deals_amount = 0
        self.all_deals = 0
        self.deals_day = 0
        self.all_deals_amount = 0

        self.day = datetime.timedelta(days=1)
        self.hour = datetime.timedelta(hours=1)
        self.date = datetime.datetime.now()

    async def getUsers(self):
        users = await Users.all()

        for user in users:
            if self.date - datetime.datetime.fromisoformat(str(user.date).split("+")[0]) <= self.day:
                self.amount_user_day += 1
            if self.date - datetime.datetime.fromisoformat(str(user.date).split("+")[0]) <= self.hour:
                self.amount_user_hour += 1

            self.amount_users_all += 1
            self.all_users_balance += user.balance

    async def getWithdrawLogs(self):
        withdrawals = await WithdrawalLogs.all()
        for i in withdrawals:
            if self.date - datetime.datetime.fromisoformat(str(i.date).split("+")[0]) <= self.day:
                self.day_amount += i.amount

            self.all_amount += i.amount
            self.all_with += 1

    async def getDealsLogs(self):
        deals = await Deals.all()

        for i in deals:
            if i.status != "Отменена":
                if self.date - datetime.datetime.fromisoformat(str(i.date).split("+")[0]) <= self.day:
                    self.day_deals_amount += i.amount
                    self.deals_day += 1

                self.all_deals_amount += i.amount
                self.all_deals += 1

    async def getStatistic(self) -> str:
        await self.getUsers()
        await self.getWithdrawLogs()
        await self.getDealsLogs()

        text = f"""
<b>💈 Информация о пользователях:</b>
❕ За все время: <b>{self.amount_users_all}</b>
❕ За день: <b>{self.amount_user_day}</b>
❕ За час: <b>{self.amount_user_hour}</b>
❕ Общий баланс юзеров: <b>{self.all_users_balance} RUB</b>

<b>💈 Информация о выводах:</b>
❕ Всего выводов: <b>{self.all_with} </b>
❕ Сумма всех выводов: <b>{self.all_amount} RUB</b>
❕ Сумма выводов за день: <b>{self.day_amount} RUB</b>  
        
<b>💈 Информация о сделках:</b>
❕ Всего сделок: <b>{self.all_deals} </b>
❕ Сделок за день: <b>{self.deals_day}</b>
❕ Сумма всех сделок: <b>{self.all_deals_amount} RUB</b>
❕ Сумма сделок за день: <b>{self.day_deals_amount} RUB</b>   
                """

        return text
