import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.cards import *



class CardFactory:
    
    @staticmethod
    def create_card (type_card: str, owner: str, balance: int, pin: str):
        if type_card == 'gold':
            print(f'Выпуск карты:{GoldCard}')
            return GoldCard(owner, balance, pin, 10, NoComission())
        
        elif type_card == 'debit':
            print(f'Выпуск карты: {BankCard}')
            return BankCard(owner, balance, pin, StandardComission())
        
        else:
            raise ValueError(f"Тип карты '{type_card}' не поддерживается")