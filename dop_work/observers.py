from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level= logging.INFO,
    format= '%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log", encoding= 'utf-8'),
        logging.StreamHandler()         
    ],
    force=True 
) 


class CardObserver(ABC):
    @abstractmethod
    def update(self, event: str, amount: int, card_id: str) -> None:
        pass


class SMSNotification(CardObserver):
    def update(self, event: str, amount: int, card_id: str) -> None:
        print (f'[SMS] Карта {card_id}: {event} на сумму {amount} ₽')

class EmailNotification(CardObserver):
    def update(self, event: str, amount: int, card_id: str) -> None:
        print (f'[Email] Карта {card_id}: {event} на сумму {amount} ₽')

        
class LogNotification(CardObserver):
    def update(self, event: str, amount: int, card_id: str) -> None:
        logging.info(f'[NOTIFICATION] Карта {card_id}: {event} на сумму {amount} ₽')

    