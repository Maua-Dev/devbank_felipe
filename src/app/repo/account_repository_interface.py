from abc import ABC, abstractmethod
from typing import Optional

from src.app.entities.account import Account
from src.app.entities.transaction import Transaction


class IAccountRepository(ABC):

    @abstractmethod
    def get_account(self, account_id: int) -> Optional[Account]:
        '''Retorna conta e id'''
        pass

    @abstractmethod
    def make_deposit(self, account: Account, value: float) -> Optional[Account]:
        '''Realiza depósito'''
        pass

    @abstractmethod
    def make_withdraw(self, account: Account, value: float) -> Optional[Account]:
        '''Realiza saque'''
        pass