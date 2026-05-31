import sys
import os
from models.cards import BankCard
from models.user import User

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

class CardRepository:
    def __init__(self, user: User) -> None:
        self.user = user
        self.cards = user.cards
        if not self.cards:
            self.cards = []

    def get_by_id(self, card_id: str) -> BankCard | None:
        for card in self.cards:
            if card.id == card_id:
                return card
        return None

    def get_all(self) -> list[BankCard]:
        return self.cards

    def get_by_type(self, card_type: str) -> list[BankCard]:
        res = []
        for card in self.cards:
            if type(card).__name__ == card_type:
                res.append(card)
        return res

    def get_richest(self, n: int) -> list[BankCard]:
        return sorted(self.cards, key= lambda x: x.balance)[-n:]

    def get_frozen(self) -> list[BankCard]:
        return [card for card in self.cards if card.is_frozen]

    def total_balance(self) -> float:
        total = 0
        for card in self.cards:
            total += card.balance
        return total
