import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from services.transaction_service import *
from models.user import User
from typing import List


class TransactionHistory:
    '''Класс для работы с транзакциями'''

    def __init__(self, user: User) -> None:
        self.user = user
        self.all_transaction = TransactionAnalyzer(user)._collect()
        if not self.all_transaction:
            raise ValueError('транзакции отсутствуют')

    
    def filter_by_type(self, transaction_type: str) -> List[Transaction]:
        res = []
        for trans in self.all_transaction:
            if trans.trans_type == transaction_type:
                res.append(trans)
        if res:
            return res 
        else:
            raise ValueError('Отсутствуют подходящие транзакции')
    

    def filter_by_amount(self, min_amount: int, max_amount: int) -> List[Transaction]:
        res = []
        for trans in self.all_transaction:
            if min_amount <= trans.amount <= max_amount:
                res.append(trans)
        if res:
            return res 
        else:
            raise ValueError('Отсутствуют подходящие транзакции')
    
    def get_last(self, n: int) -> List[Transaction]:
        return self.all_transaction[-n:]
    
    def filter_by_date(self, date: str) -> List[Transaction]:
        res = []
        for trans in self.all_transaction:
            if trans.trans_time.startswith(date):
                res.append(trans)
        if res:
            return res 
        else:
            raise ValueError('Отсутствуют подходящие транзакции')
        

        