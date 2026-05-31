import sys
import os
from models.cards import BankCard

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

class User:
    id: int
    name: str
    cards: list[BankCard]

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.cards = []

    def __repr__(self) -> str:
        return f'User(name = {self.name}, cards = {len(self.cards)})'

    def add_card(self, card: BankCard) -> None:
        self.cards.append(card)

    def get_total_balance(self, count_frozen: bool) -> int:
        total_balance = 0

        for card in self.cards:
            if count_frozen or not card.is_frozen:
                total_balance += card.balance

        return total_balance

    def freeze_card(self, card_id: int) -> None:
        card = self.get_card_by_id(card_id)
        if card is None:
            return

        card.is_frozen = True
        card._notify(f'Карта {type(card).__name__} заморожена', 0)

    def unfreeze_card(self, card_id: int) -> None:
        card = self.get_card_by_id(card_id)
        if card is None:
            return

        card.is_frozen = False
        card._notify(f'Карта {type(card).__name__} разморожена', 0)

    def show_all_bonuses(self) -> None:
        for card in self.cards:
            info = card.get_info_bonus()
            print(f'{card.owner_id} | {type(card).__name__}: {info}')


    def get_card_by_id(self, search_id: int) -> BankCard | None:
        for card in self.cards:
            if card.id == search_id:
                return card

        return None
