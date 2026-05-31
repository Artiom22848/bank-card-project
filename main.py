from models.cards import BankCard


card1 = BankCard(228, 1488, 2000, '2212', 0)

card1.deposit(2000)
card1.withdraw(100, '2212')
print(card1.display_info())
print(card1.get_history())