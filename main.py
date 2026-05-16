
from factory.card_factory import *

card = CardFactory.create_card('gold', 'Артём', 1000, '1234')
card.add_observer(SMSNotification())
card.add_observer(SMSNotification())  # дубликат — не добавится
card.list_observers()
print(card.get_observers_count())