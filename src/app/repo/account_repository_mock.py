from typing import Dict
from ..entities.account import Account
from ..repo.account_repository_interface import IAccountRepository


class AccountRepositoryMock(IAccountRepository):
    accounts: Dict[int, Account]

    def __init__(self):
        self.accounts = {
            1: Account(name="Felipe Sakae", agency="1111", account_number="11111-1", current_balance=1000.0)
        }

    def get_account(self, account_id):
        return self.accounts.get(account_id, None)
    
    def make_deposit(self, account, value):
        if account is not None:

            account.current_balance += value

        return account
    
    def make_withdraw(self, account, value):
        if account is not None:
             
            if account.current_balance >= value:
                 
                account.current_balance -= value

        return account

    
    