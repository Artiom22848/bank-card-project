from dop_work import *
import json
import datetime
from logi import *
from uuid import uuid4
import logging
from typing import List
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log", encoding= 'utf-8'),
        logging.StreamHandler()         
    ],
    force=True 
) 


class BankCard:

    def __init__(self,owner: str, balance: int, pin: str, comission: Comission):
        if BankCard.is_valid_amount(balance):
            self.owner = owner
            self._balance = balance
            self.__pin = pin
            self.history = []
            self.__id = str(uuid4())[:8]        
            self.comission = comission

        else:
            raise ValueError('Неправильный начальный баланс')
            
    def __str__(self) -> str:
        return f'ID: {self.__id} {type(self).__name__} Владелец:{self.owner}, Баланс: {self.balance}'
    
    def __gt__(self, other) -> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        else:
           return self.balance > other.balance      
    
    def __lt__(self, other)-> bool:
        if  not isinstance(other, (int, BankCard )):
            raise TypeError('данные введены некоректно')
        else:
            return self.balance < other.balance

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
        
   

    def  get_info_bonus(self):
        return("бонусов нету")
    
        
    def display_info(self):
        '''вывод информации'''
        print(f'Владелец: {self.owner}, Баланс: {self._balance}')
    

    def deposit(self,amount: int):
        if BankCard.is_valid_amount(amount):
            self._balance += amount
            new_transaction = Transaction('Пополнение', amount)
            self.history.append(new_transaction)
            print(f'Счёт пополнен на {amount}')

    @trace_transaction
    def withdraw(self,amount: int, pin_code: str):
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
                self.history.append(new_transaction)
                self._balance -= total
                print(f'Снято {amount}, Комиссия: {com}. Итог списания {total}')
        else:
            raise ValueError('Нельзя делать покупки на отрицательную сумму')


    def show_history(self) -> str:
        if len(self.history) == 0:
            print(f'История пуста')
        else:
            for trans in self.history:
                print(trans)


    @property
    def balance(self) -> int:
        '''геттер чтобы получать данные о балансе'''
        logging.info(f'[security] Запрос баланса.... доступ разрешен')
        return self._balance
        
    @balance.setter
    def balance(self, value: int):
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
        
    
    def __init__(self, owner: str, balance: int, pin: str, cashback_persent: int, comission: Comission ):
        super().__init__(owner, balance, pin, comission)
        
        self.cashback_persent = cashback_persent
        self.accumelated_cashback = 0

    
    def deposit(self, amount: int):
        super().deposit(amount)
        
        self.accumelated_cashback += amount * (self.cashback_persent / 100)


    def get_info_bonus(self):
        return (f'У вас накопилось: {self.accumelated_cashback}')
    

    @classmethod
    def promo_card(cls, owner: str,comission: Comission) :
        promo = cls(owner, 500, '7777', 10, comission)
        return promo



class StudentCard(BankCard):

    def __init__(self, owner: str, balance: int, pin: str, food_points: int, comission: Comission):
        super().__init__(owner, balance, pin, comission)

        self.food_points = food_points

    
    def get_info_bonus(self):
        return (f'Баллы столовой: {self.food_points}')



class CreditCard(BankCard):


    def __init__(self, owner: str, balance: int, pin: str, credit_limit: int, comission: Comission):
        super().__init__(owner, balance, pin, comission)
        
        self.credit_limit = credit_limit

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
    
    
    def withdraw(self, amount, pin_code: str):
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
        

    def get_info_bonus(self):
        if self.balance < 0:
            return (f'Долг по кредиту: {abs(self.balance)}')
         
        else:
            return (f'Долг отсутсвует')
        
    def display_info(self):
        print(f'Владелец: {self.owner}, Баланс: {max(0,self.balance)} Общий баланс: {self.general_balance} ')


class SecureGoldCard(SecurityMixin, LoggingMixn ,GoldCard):
    pass



class TeenCard(LimitMixin,NotificationMixin,BankCard):
    pass




class User:
    
    def __init__(self, name: str):
        
        self.name = name
        self.cards = []

    
    def add_card(self, card: BankCard):

        self.cards.append(card)

    def get_total_balance(self) -> int:
        self.total_balance = 0
        
        for card in self.cards:
            self.total_balance += card.balance

        return self.total_balance

    
    def pay_everywhere(self, amount: int):
        
        if self.get_total_balance() < amount:
            logging.error("Ошибка: Недостаточно средств")
            raise ValueError(f'Ошибка, совсем нет денег')
            
        
        ostatok = amount

        for card in self.cards:
            if ostatok > 0:
                to_withdraw = min(card.balance, ostatok)
                try:
                    card.withdraw(to_withdraw, card.my_pin)
                    ostatok -= to_withdraw
                    card.new_transaction = Transaction('Снятие', ostatok)
                    logging.info(f"Списано {to_withdraw} с карты {card.id}. Осталось: {ostatok}")
                except Exception as f:
                    logging.warning(f"Не удалось списать с карты {card.id}: {f}")

            if ostatok <= 0:
                print(f'Оплатна успешно прошла')
                break
            else:
                print(f'Оплата не завершена, не хватило: {ostatok}')
        return


    
    def show_all_bonuses(self):
        for card in self.cards:
            info = card.get_info_bonus()
            print(f'{card.owner} | {type(card).__name__}: {info}')


    def get_card_by_id(self, search_id):
        
        for card in self.cards:
            if card.id == search_id:
                return card
        print(f'Ошибка: карта с ID {search_id} не найдена')
        return None
        
        

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



class CardFactory:
    
    @staticmethod
    def create_card (type_card: str, owner: str, balance: int, pin: str):
        if type_card == 'gold':
            print(f'Выпуск карты:{GoldCard}')
            return GoldCard(owner, balance, pin, 10, NoComission())
        
        elif type_card == 'debit':
            print(f'Выпуск карты: {BankCard}')
            return BankCard(owner, balance, pin, StandardComission())
        
        else:
            raise ValueError(f"Тип карты '{type_card}' не поддерживается")
        

class PaymentSystem:
    _instance = None
    _total_volume = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def transfer(self, from_card: BankCard, to_card: BankCard, amount: int, pin: str):
        if  not from_card.check_pin(pin):
            raise InvalidPinError
        try:
            from_card.withdraw(amount, pin)

            try:
                to_card.deposit(amount)
            except Exception as e:
                from_card.deposit(amount)
                raise RuntimeError(f'Ошибка зачисления: {e}: Деньги вовзращены')
            else:
                self._total_volume += amount
                print(f'Перевод успешно сделан')
        except ValueError as e:
            print(f'Перевод невозможен: {e}')
        
    
    @classmethod
    def get_stats(cls):
        print(f'Через систему прошло всего: {cls._total_volume}')



class TransactionAnalyzer:
    """класс для работы с транзакциями сразу у нескольких карт"""
    
    def __init__(self,user: User):
        self.user = user
        self.trans = self._collect()
    

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
    

