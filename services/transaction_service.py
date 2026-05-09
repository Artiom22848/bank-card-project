import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.transaction import Transaction
from models.transaction import Transaction
from collections import defaultdict
from typing import List
from models.user import User

class TransactionAnalyzer:
    """класс для работы с транзакциями сразу у нескольких карт"""
    
    def __init__(self,user: User):
        self.user = user
        self.trans = self._collect()
    
    def __repr__(self):
        return f'TransactionAnalyzer(user = {self.user}, trans = {len(self.trans)})'
    

    def _collect(self) -> List:
        res = []
        for card in self.user.cards:
            res.extend(card.history)
        return res


    def top_expenses(self, n: int) -> List[Transaction]:
        
        expenses = [trans for trans in self.trans if trans.type == 'Снятие']
        if len(expenses) == 0:
            return []
            
        sorted_ex = sorted(expenses, key=lambda x: x.amount, reverse= True)[:n] # сортирую транзакции по сумме и вывожу первые n из них
        return sorted_ex
    

        
    def total_by_type(self, type: str) -> int:
        totals = {}
        for transac in self.trans:
            totals[transac.type] = totals.get(transac.type,0) + transac.amount # для каждого вида транкзации добавлюю сумму 

        return totals.get(type,0)
    
    def most_active_card(self):
        if not self.user.cards:
            return None
        return max(self.user.cards, key= lambda x: len(x.history)) # возращаю максимум из карт по их  длине истории транкзаций 
        

    def average_transaction(self) -> float:
        if not self.trans:
            return 0
        return sum(t.amount for t in self.trans) / len(self.trans)
    

    def suspicious(self, target: int) -> List[Transaction]:
        return [t for t in self.trans if t.amount >= target]
    

    def monthly_report(self) -> dict:
        res = defaultdict(lambda: defaultdict(int))
        for t in self.trans:
            month = t.trans_time[:7]
            res[month][t.type] += t.amount
        for month, types in res.items():
            print(f'{month}')
            for type_name, amount in types.items():
                print(f'    {type_name}: {amount}₽')
                end = sum(am if tp == 'Пополнение' else -am
                for tp, am in types.items())
            print(f'    Итог: {end}₽')
        return dict(res)