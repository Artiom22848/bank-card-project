import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.transaction import Transaction
from typing import List, Dict
from datetime import datetime
import json


class TransactionHistory:
    """Класс для управления историей транзакций карты"""
    
    def __init__(self, transactions: List[Transaction] = None):
        self.transactions = transactions if transactions else []
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Добавить транзакцию в историю"""
        if not isinstance(transaction, Transaction):
            raise TypeError('Необходимо передать объект Transaction')
        self.transactions.append(transaction)
    
    def get_all(self) -> List[Transaction]:
        """Получить все транзакции"""
        return self.transactions
    
    def get_by_type(self, trans_type: str) -> List[Transaction]:
        """Получить транзакции по типу (Пополнение/Снятие)"""
        return [t for t in self.transactions if t.trans_type == trans_type]
    
    def get_by_date_range(self, start_date: str, end_date: str) -> List[Transaction]:
        """Получить транзакции за период (формат: YYYY-MM-DD HH:MM:SS)"""
        start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        result = []
        for t in self.transactions:
            trans_time = datetime.strptime(t.trans_time, "%Y-%m-%d %H:%M:%S")
            if start <= trans_time <= end:
                result.append(t)
        return result
    
    def get_by_amount_range(self, min_amount: int, max_amount: int) -> List[Transaction]:
        """Получить транзакции в диапазоне сумм"""
        return [t for t in self.transactions if min_amount <= t.amount <= max_amount]
    
    def get_total_by_type(self, trans_type: str) -> int:
        """Получить общую сумму по типу транзакции"""
        transactions = self.get_by_type(trans_type)
        return sum(t.amount for t in transactions)
    
    def get_balance_change(self) -> int:
        """Получить изменение баланса (пополнения - снятия)"""
        deposits = self.get_total_by_type('Пополнение')
        withdrawals = self.get_total_by_type('Снятие')
        return deposits - withdrawals
    
    def get_last_n(self, n: int) -> List[Transaction]:
        """Получить последние N транзакций"""
        return self.transactions[-n:] if n > 0 else []
    
    def search_by_amount(self, amount: int) -> List[Transaction]:
        """Найти транзакции по точной сумме"""
        return [t for t in self.transactions if t.amount == amount]
    
    def get_max_expense(self) -> Transaction | None:
        """Получить максимальное снятие"""
        expenses = self.get_by_type('Снятие')
        return max(expenses, key=lambda x: x.amount) if expenses else None
    
    def get_min_expense(self) -> Transaction | None:
        """Получить минимальное снятие"""
        expenses = self.get_by_type('Снятие')
        return min(expenses, key=lambda x: x.amount) if expenses else None
    
    def get_statistics(self) -> Dict:
        """Получить статистику по всем транзакциям"""
        if not self.transactions:
            return {
                'total_transactions': 0,
                'total_deposits': 0,
                'total_withdrawals': 0,
                'average_amount': 0,
                'balance_change': 0
            }
        
        amounts = [t.amount for t in self.transactions]
        deposits = [t.amount for t in self.get_by_type('Пополнение')]
        
        return {
            'total_transactions': len(self.transactions),
            'total_deposits': self.get_total_by_type('Пополнение'),
            'total_withdrawals': self.get_total_by_type('Снятие'),
            'average_amount': sum(amounts) / len(amounts),
            'max_amount': max(amounts),
            'min_amount': min(amounts),
            'max_deposit': max(deposits) if deposits else 0,
            'balance_change': self.get_balance_change()
        }
    
    def export_to_json(self, filename: str) -> None:
        """Экспортировать историю в JSON файл"""
        data = [
            {
                'type': t.trans_type,
                'amount': t.amount,
                'time': t.trans_time,
                'is_expense': t.is_expense
            }
            for t in self.transactions
        ]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'История экспортирована в {filename}')
    
    def clear_history(self) -> None:
        """Очистить историю"""
        self.transactions.clear()
        print('История очищена')
    
    def __len__(self) -> int:
        return len(self.transactions)
    
    def __repr__(self) -> str:
        return f'TransactionHistory(transactions={len(self.transactions)})'
    
    def __str__(self) -> str:
        if not self.transactions:
            return 'История транзакций пуста'
        return '\n'.join(str(t) for t in self.transactions)

