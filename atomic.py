from __future__ import annotations
from typing import TYPE_CHECKING
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log"),
        logging.StreamHandler()         
    ]
) 


if TYPE_CHECKING:
    from osnova import User



class AtomicPayment:

    
    def __init__(self,user: User):
        self.user = user
    
    
    def __enter__(self):
        self.snapshot = {}
        for card in self.user.cards:
            self.snapshot[card.id] = card.balance
        logging.info(f'баланс карт запомнят, начала транцзации')
        return self.snapshot
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(f'произошла ошибка: {exc_val}.Начинаю откатывать балансы')

            for card in self.user.cards:
                if card.id in self.snapshot:
                    card._balance = self.snapshot[card.id]
            logging.info(f"откат завершен")
        else:
            logging.info(f'транцзации успешно прошла')
        
        return False