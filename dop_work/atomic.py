from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from typing import TYPE_CHECKING, Dict
import logging



if TYPE_CHECKING:
    from OOP_TRAIN.models import User



class AtomicPayment:

    
    def __init__(self,user: User) -> None:
        self.user = user
    
    
    def __enter__(self) -> Dict:
        self.snapshot = {}
        for card in self.user.cards:
            self.snapshot[card.id] = card.balance
        logging.info(f'баланс карт запомнят, начала транцзации')
        return self.snapshot
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            logging.error(f'произошла ошибка: {exc_val}.Начинаю откатывать балансы')

            for card in self.user.cards:
                card.balance = self.snapshot.get(card.id, card.balance)
            logging.info(f"откат завершен")
        else:
            logging.info(f'транцзации успешно прошла')
        
        return False