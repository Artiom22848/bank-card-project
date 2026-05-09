import datetime
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log", encoding= 'utf-8'),
        logging.StreamHandler()         
    ],
    force=True 
) 



class Transaction:

    def __init__(self, type: str, amount: int):
        self.type = type
        self.amount = amount
        logging.info(f'Записываю в историю транкзакцию')
        self.trans_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        return f'Transaction(type ={self.type}, amount ={self.amount}, time = {self.trans_time})'
    
    
    
    def __str__(self) -> str:
        return f'{self.type} | Сумма: {self.amount}, Время и дата: {self.trans_time}'
    
    
    def __eq__(self, tran) -> bool:
        if not isinstance(tran,Transaction):
            raise ValueError(f'Данные введены неккоректно')
        return tran.type == self.type and tran.amount == self.amount
        
    
    @property
    def sh_trans(self) -> str:
        return f'{self.type} | Сумма: {self.amount}, Время и дата: {self.trans_time}'
    
    @property
    def is_expense(self) -> bool:
        if self.type == 'Пополнение':
            return False
        return True

    @property
    def formatted_amount(self) -> str:
        if self.type == 'Снятие':
            return f'-{self.amount} ₽'
        
        return f"+{self.amount} ₽"

