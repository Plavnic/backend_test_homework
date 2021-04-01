import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.utcnow().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == dt.datetime.utcnow().date():
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_ago = dt.datetime.utcnow().date() - dt.timedelta(days=7)
        week_amount = 0
        for record in self.records:
            if dt.datetime.utcnow().date() >= record.date >= week_ago:
                week_amount += record.amount
        return week_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        cal_rem = self.limit - self.get_today_stats()
        if cal_rem > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_rem} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 75.90
    EURO_RATE = 88.90

    def get_today_cash_remained(self, currency):
        cash_dict = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (1, 'руб')
        }
        cdict = cash_dict[currency]
        cash_rem = round(((self.limit - self.get_today_stats()) / cdict[0]), 2)
        if self.get_today_stats() < self.limit:
            return (f'На сегодня осталось {cash_rem} {cdict[1]}')
        elif self.get_today_stats() == self.limit:
            return ('Денег нет, держись')
        else:
            cr_abs = abs(cash_rem)
            return (f'Денег нет, держись: твой долг - {cr_abs}'
                    f' {cdict[1]}')
