import datetime
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from OOP_TRAIN.models import BankCard




class DailyLimitExceededError(Exception):
    pass

class CardLimit:
    """Проверяет и отслеживает дневной лимит расходов"""
    def __init__(self):
        self.card_limit = {}

    def check_limit(self, card: 'BankCard', amount: int) -> None:
        if amount > card.daily_limit:
            raise ValueError('Слишком большая сумма')
        date = datetime.date.today()
        if card.id not in self.card_limit:
            self.card_limit[card.id] = {"date":date, 'spent': amount}
        else:
            if self.card_limit[card.id]['date'] != date:
                self.card_limit[card.id] = {"date":date, 'spent': amount}

            elif self.card_limit[card.id]['spent'] + amount > card.daily_limit:
                remaining = card.daily_limit - self.card_limit[card.id]['spent']
                card._notify('Превышение лимита', amount, card.id)
                raise DailyLimitExceededError(f'Дневной лимит {card.daily_limit} ₽ исчерпан. Доступно: {remaining} ₽')
            else:
                self.card_limit[card.id]['spent'] += amount
