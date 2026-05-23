import logging

"""Настройка логирования для всего"""
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bank.log", encoding='utf-8'),
        logging.StreamHandler()         
    ],
    force=True 
    )




class LimitMixin:

    max_withdraw_limit = 1000

    def withdraw(self, amount: int, pin: str):
        if amount > self.max_withdraw_limit:
            raise ValueError(f'Слишком большая сумма')
        else:
            super().withdraw(amount, pin)


class NotificationMixin:
    def withdraw(self, amount: int, pin: str):
        super().withdraw(amount, pin)
        print(f'[SMS-Уведомление]: С вашей карты списано {amount} руб')
    


class SecurityMixin:
    def withdraw(self, amount: int, pin_code):
        print(f'Проверка безопасности')
        if self.check_pin(pin_code):
            super().withdraw(amount, pin_code)
        else:
            raise ValueError
        

class LoggingMixn:
    def withdraw(self, amount: int, pin_code):
        logging.exception("выполняю сбор информации")
        super().withdraw(amount, pin_code)