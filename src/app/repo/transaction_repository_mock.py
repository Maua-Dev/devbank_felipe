import time
from typing import Dict
from ..entities.account import Account
from ..entities.transaction import Transaction
from ..repo.transaction_repository_interface import ITransactionRepository


class TransactionRepositoryMock(ITransactionRepository):
    transactions: Dict[int, Transaction]
    transactions_counter: int

    def __init__(self):
        self.transactions = {}
        self.transactions_counter = 0

    def get_all_transactions(self):
        return [t.to_dict() for t in self.transactions.values()]
    
    def create_transaction(self, transaction_type, transaction_value, transaction_time, curr_balance):
        
        self.transactions_counter += 1
        transaction = Transaction(transaction_type, transaction_value, transaction_time, curr_balance)

        self.transactions[self.transactions_counter] = transaction

        return transaction



    

    