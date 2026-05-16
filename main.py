from dop_work.logi import setup_logging
setup_logging()
from models.cards import BankCard
from dop_work.utils import *



card1 = BankCard('Артём', 1000, '1234', NoComission)
card2 = BankCard('Иван', 500, '5678', NoComission)

print(card1 > card2)       # ✅ True
print(card1 > 800)         # ✅ True
print(card2 < 1000)