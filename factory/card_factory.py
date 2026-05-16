import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from models.cards import *





class CardFactory:
    
    @staticmethod
    def create_card (type_card: str, owner: str, balance: int, pin: str):
        if type_card == 'gold':
            print(f'Выпуск карты:{GoldCard.__name__}')
            return GoldCard(owner, balance, pin, 10, NoComission())
        
        elif type_card == 'debit':
            print(f'Выпуск карты: {BankCard.__name__}')
            return BankCard(owner, balance, pin, StandardComission())
        
        else:
            raise ValueError(f"Тип карты '{type_card}' не поддерживается")