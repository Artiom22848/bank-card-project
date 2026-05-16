
from factory.card_factory import *

card = CardFactory.create_card('gold', 'Артём', 1000, '1234')
card.add_observer(SMSNotification())
card.deposit(500)
card.withdraw(200, '1234')