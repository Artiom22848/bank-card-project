from models.cards import BankCard


card1 = BankCard(228, 1488, 200000, '2212', 0)

card1.withdraw(30000, '2212')
print(card1.display_info())
card1.withdraw(40000, '2212')
print(card1.get_history())