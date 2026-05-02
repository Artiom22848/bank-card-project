from OOP_TRAIN.main import *
from atomic import AtomicPayment



user = User("Тест")
card1 = CardFactory.create_card('gold', 'Тест', 1000, '1234')
card2 = CardFactory.create_card('debit', 'Тест', 500, '5678')
user.add_card(card1)
user.add_card(card2)

