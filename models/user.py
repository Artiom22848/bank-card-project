import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from services.stats import CardStats
from dop_work.utils import *
import logging
from models.cards import BankCard
from models.transaction import Transaction



class User:
    
    def __init__(self, name: str):
        
        self.name = name
        self.cards = []

    def __repr__(self):
        return f'User(name = {self.name}, cards = {len(self.cards)})'


    def add_card(self, card: BankCard):

        self.cards.append(card)

    def get_total_balance(self) -> int:
        self.total_balance = 0
        
        for card in self.cards:
            self.total_balance += card.balance

        return self.total_balance

    
    def pay_everywhere(self, amount: int) -> None:
        
        if self.get_total_balance() < amount:
            logging.error("Ошибка: Недостаточно средств")
            raise ValueError(f'Ошибка, совсем нет денег')
            
        
        ostatok = amount

        for card in self.cards:
            if ostatok > 0:
                to_withdraw = min(card.balance, ostatok)
                try:
                    card.withdraw(to_withdraw, card.my_pin)
                    ostatok -= to_withdraw
                    logging.info(f"Списано {to_withdraw} с карты {card.id}. Осталось: {ostatok}")
                except Exception as e:
                    logging.warning(f"Не удалось списать с карты {card.id}: {e}")

            if ostatok <= 0:
                print(f'Оплатна успешно прошла')
                break
            else:
                print(f'Оплата не завершена, не хватило: {ostatok}')
        return None


    
    def show_all_bonuses(self):
        for card in self.cards:
            info = card.get_info_bonus()
            print(f'{card.owner} | {type(card).__name__}: {info}')


    def get_card_by_id(self, search_id):
        
        for card in self.cards:
            if card.id == search_id:
                return card
        print(f'Ошибка: карта с ID {search_id} не найдена')
        return None
    


    def compare_cards(self,card1_id: str, card2_id: str) -> None:
        card1 = self.get_card_by_id(card1_id)
        card2 = self.get_card_by_id(card2_id)
        card1_stats = CardStats(card1)
        card2_stats = CardStats(card2)
        
        
        print(f'Карта 1: {type(card1).__name__} | Баланс: {card1.balance}₽ | Транзакций: {len(card1_stats.history)}')
        print(f'Карта 2: {type(card2).__name__} | Баланс: {card2.balance}₽ | Транзакций: {len(card2_stats.history)}')
        print(f'\nПобедитель по балансу: {type(max(card1,card2, key= lambda x : x.balance)).__name__}')
        if not card1_stats.history and not card2_stats.history :
            print('История транзакций пуста у обеих карт')
            return
        print(f'Победитель по активности: {type(max(card1_stats,card2_stats, key= lambda x : len(x.history))).__name__}')
        avg1 = card1_stats.average_expense()
        avg2 = card2_stats.average_expense()
        if avg1 is not None and avg2 is not None:
            print(f'Средний чек карты 1: {avg1}₽')
            print(f'Средний чек карты 2: {avg2}₽')
        else:
            print('Недостаточно данных для среднего чека')