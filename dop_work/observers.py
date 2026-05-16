from abc import ABC, abstractmethod

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

        
        