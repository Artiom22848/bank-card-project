import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from dop_work.observers import *
from dop_work.utils import *
from dop_work.logi import *
from models.transaction import *
import json
from uuid import uuid4
import logging



class BankCard:

    def __init__(self,owner: str, balance: int, pin: str, comission: Comission) -> None:
        if BankCard.is_valid_amount(balance):
            self.daily_limit = 50000
            self.is_frozen = False
            self.owner = owner
            self._balance = balance
            self.__pin = pin
            self.history = []
            self.observers = []
            self.__id = str(uuid4())[:8]        
            self.comission = comission
            self.observers = [LogNotification()]

        else:
            raise ValueError('Неправильный начальный баланс')
            
    def __str__(self) -> str:
        return f'ID: {self.__id} {type(self).__name__} Владелец:{self.owner}, Баланс: {self.balance}'
    
    def __repr__(self):
        return f'BankCard(id = {self.id}, owner = {self.owner}, balance = {self.balance}, comission: {type(self.comission).__name__})'
    
    def __gt__(self, other) -> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        other_balance = other.balance if isinstance(other, BankCard) else other
        return self.balance > other_balance      
    
    def __lt__(self, other)-> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        other_balance = other.balance if isinstance(other, BankCard) else other
        return self.balance < other_balance

    def __eq__(self, value) -> bool:
        if  not isinstance(value, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        elif isinstance(value, BankCard):
            return value.balance == self.balance
        else:
            return self.balance == value
        
    def __add__(self, other):
        if  not isinstance(other, BankCard):
            raise TypeError('данные введены некоректно')
        else:
            summ_balance = self.balance + other.balance
            return type(self)(self.owner, summ_balance, self.my_pin, self.comission)
        
    def __len__(self) -> int:
        return len(self.history)               
        
   

    def  get_info_bonus(self) -> str:
        return("бонусов нету")
    
        
    def display_info(self) -> str:
        '''вывод информации'''
        print(f'Владелец: {self.owner}, Баланс: {self._balance}')
    

    def deposit(self,amount: int) -> None:
        if  self.is_frozen:
            raise PermissionError('карта заморожена')
        else:
            if BankCard.is_valid_amount(amount):
                self._balance += amount
                self._notify('Пополнение', amount)
                new_transaction = Transaction('Пополнение', amount)
                self.history.append(new_transaction)
                print(f'Счёт пополнен на {amount}')

    @trace_transaction
    def withdraw(self,amount: int, pin_code: str) -> None:
        if  self.is_frozen:
            raise PermissionError('карта заморожена')
        else:
            self.card_limit_checker.check_limit(self, amount)    
            if BankCard.is_valid_amount(amount):
                if pin_code != self.__pin:
                    raise InvalidPinError

                elif self.balance < amount:
                    logging.error("Ошибка: Недостаточно средств")
                    raise ValueError(f'Недостаточно средств')
                
                else:
                    com = self.comission.calculate(amount)
                    total = amount + com
                    new_transaction = Transaction('Снятие', amount)
                    self._balance -= total
                    self.history.append(new_transaction)
                    self._notify('Снятие', total)
                    print(f'Снято {amount}, Комиссия: {com}. Итог списания {total}')
            else:
                raise ValueError('Нельзя делать покупки на отрицательную сумму')


    def show_history(self) -> str:
        if len(self.history) == 0:
            print(f'История пуста')
        else:
            for trans in self.history:
                print(trans)

    def  add_observer(self, observer: CardObserver) -> None:
        if type(observer) in [type(o) for o in self.observers]:
            print(f'{type(observer).__name__} уже записан')
            return
        self.observers.append(observer)
    
    def remove_observer(self, observer: CardObserver) -> None:
        self.observers.remove(observer)
    
    def _notify(self, event: str, amount: int) -> None:
        for observer in self.observers:
            observer.update(event, amount, self.id)

    
    def get_observers_count(self) -> int:
        return len(self.observers)
    
    def list_observers(self) -> None:
        if not self.observers:
            print('Наблюдателей нету')
            return
        for i, obs in enumerate(self.observers):
            print(f'{i+1}. {type(obs).__name__}')
    
    @property
    def balance(self) -> int:
        '''геттер чтобы получать данные о балансе'''
        logging.info(f'[security] Запрос баланса.... доступ разрешен')
        return self._balance
        
    @balance.setter
    def balance(self, value: int) -> None:
        '''сеттер для изменния баланса'''
        if value < 0:
            raise ValueError('Баланс не может быть отрицательным')
        else:
            print(f'Баланс теперь: {value}')
            self._balance = value
        
    @property
    def owner_name(self):
        return self.owner.upper()

    @property
    def my_pin(self):
        return self.__pin

    @property
    def id(self):
        return self.__id
    
    
    
    def check_pin(self, code: str) -> bool:
        return self.__pin == code
    
    
    @staticmethod
    def is_valid_amount(amount: int) -> bool:
        '''валидация данных'''
        return isinstance(amount, (int, float)) and  amount > 0
    

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)

        return cls(owner = data['owner'],
            balance = data['balance'],
            pin = data['pin']
        )


class GoldCard(BankCard):
        
    
    def __init__(self, owner: str, balance: int, pin: str, cashback_persent: int, comission: Comission ) -> None:
        super().__init__(owner, balance, pin, comission)
        
        self.cashback_persent = cashback_persent
        self.accumelated_cashback = 0

    
    def __repr__(self):
        return f'GoldCard(owner = {self.owner}, balance = {self.balance}, cashback_persent = {self.cashback_persent}, comission = {type(self.comission).__name__})'

    def deposit(self, amount: int) -> None:
        super().deposit(amount)
        
        self.accumelated_cashback += amount * (self.cashback_persent / 100)


    def get_info_bonus(self) -> str:
        return (f'У вас накопилось: {self.accumelated_cashback}')
    

    @classmethod
    def promo_card(cls, owner: str,comission: Comission) -> BankCard:
        promo = cls(owner, 500, '7777', 10, comission)
        return promo



class StudentCard(BankCard):

    def __init__(self, owner: str, balance: int, pin: str, food_points: int, comission: Comission) -> None:
        super().__init__(owner, balance, pin, comission)

        self.food_points = food_points
    
    def __repr__(self):
        return f'StudentCard(owner = {self.owner}, balance = {self.balance}, food_points = {self.food_points}, comission = {type(self.comission).__name__})'

    
    def get_info_bonus(self) -> str:
        return (f'Баллы столовой: {self.food_points}')



class CreditCard(BankCard):


    def __init__(self, owner: str, balance: int, pin: str, credit_limit: int, comission: Comission) -> None:
        super().__init__(owner, balance, pin, comission)
        
        self.credit_limit = credit_limit

    def __repr__(self):
        return f'CreditCard(owner = {self.owner}, balance = {self.balance}, credit_limit = {self.credit_limit}, comission = {type(self.comission).__name__})'
    
    
    @property
    def general_balance(self):
        return self.balance + self.credit_limit

    @property
    def balance(self):
        return self._balance
    

    @balance.setter
    def balance(self,value: int):
        if value < -self.credit_limit:
            logging.warning("Ошибка:Превышен кредитный лимит")
            raise ValueError('Превышен кредитный лимит')
        self._balance = value
    
    
    def withdraw(self, amount, pin_code: str) -> None:
        if not BankCard.is_valid_amount(amount):
            raise ValueError('Нельзя делать покупки на отрицательную сумму')
        
        if not self.check_pin(pin_code):
            raise InvalidPinError
            
        
        if amount <= self.general_balance:
            self.balance -= amount
            print(f'Снято {amount}')
        
        else:
            logging.error("Ошибка: Недостаточно средств")
            raise ValueError(f'Ошибка: Недостаточно средств')
        

    def get_info_bonus(self) -> str:
        if self.balance < 0:
            return (f'Долг по кредиту: {abs(self.balance)}')
         
        else:
            return (f'Долг отсутсвует')
        
    def display_info(self) -> str:
        print(f'Владелец: {self.owner}, Баланс: {max(0,self.balance)} Общий баланс: {self.general_balance} ')


class SecureGoldCard(SecurityMixin, LoggingMixn ,GoldCard):
    pass



class TeenCard(LimitMixin,NotificationMixin,BankCard):
    pass

