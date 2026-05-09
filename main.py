from models.cards import *
from models.user import *

card1 = BankCard('vergil', 2000, '1333',NoComission)
card2 = GoldCard('vergil', 1000, '1333',50,NoComission)

card1.withdraw(500, '1333')
card2.withdraw(700, '1333')


me = User('vergil')
me.add_card(card1)
me.add_card(card2)
me.compare_cards(card1.id, card2.id)