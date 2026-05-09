import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from dop_work.utils import *
import logging
from models.cards import BankCard
from models.transaction import Transaction
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log", encoding= 'utf-8'),
        logging.StreamHandler()         
    ],
    force=True 
) 


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

    
    def pay_everywhere(self, amount: int):
        
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
                    card.new_transaction = Transaction('Снятие', ostatok)
                    logging.info(f"Списано {to_withdraw} с карты {card.id}. Осталось: {ostatok}")
                except Exception as f:
                    logging.warning(f"Не удалось списать с карты {card.id}: {f}")

            if ostatok <= 0:
                print(f'Оплатна успешно прошла')
                break
            else:
                print(f'Оплата не завершена, не хватило: {ostatok}')
        return


    
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