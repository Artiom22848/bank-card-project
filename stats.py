import datetime
from main import BankCard, Transaction

class CardStats:

    def __init__(self,card: BankCard):
        self.card = card
        self.history = card.history

    def max_expense(self) -> Transaction | None:
        if  not self.valid(self.history):
            return None
        arr_expense = [x for x in self.history if x.type == 'Снятие']
        if  not self.valid(arr_expense):
            return None
        return max(arr_expense, key= lambda x: x.amount)
    
    def min_expense(self) ->  Transaction | None:
        if not self.valid(self.history):
            return None
        arr_expense = [x for x in self.history if x.type == 'Снятие']
        if  not self.valid(arr_expense):
            return None
        return min(arr_expense, key= lambda x: x.amount)
    

    def average_expense(self) -> float | None:
        if  not self.valid(self.history):
            return None
        arr_expense = [x for x in self.history if x.type == 'Снятие']
        if  not self.valid(arr_expense):
            return None
        return sum(t.amount for t in arr_expense) / len(arr_expense)

    def most_active_weekday(self) -> str:
        res = {}
        for t in self.history:
            dt = datetime.datetime.strptime(t.trans_time, "%Y-%m-%d %H:%M:%S")
            weekday = dt.strftime("%A")
            res[weekday] = res.get(weekday,0) + 1
        return max(res, key = res.get)

    def expense_ratio(self) -> float:
        if  not self.valid(self.history):
            return None
        arr_expense = [x for x in self.history if x.type == 'Снятие']
        if  not self.valid(arr_expense) :
            return None
        return (len(arr_expense) / len(self.history)) * 100
    
    @staticmethod
    def valid(arr: list) -> bool:
        if len(arr) == 0:
            return False
        return True
    
