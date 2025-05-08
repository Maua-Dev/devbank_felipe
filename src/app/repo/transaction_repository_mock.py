import time
from typing import Dict
from src.app.entities.account import Account
from src.app.entities.transaction import Transaction
from src.app.repo.transaction_repository_interface import ITransactionRepository


class TransactionRepositoryMock(ITransactionRepository):
    transactions: Dict[int, Transaction]
    transactions_counter: int

    def __init__(self):
        self.transactions = {}
        self.transactions_counter = 0

    def get_all_transactions(self):
        arr_to_return = []
        for transaction in self.transactions.values():
            arr_to_return.append(transaction.to_dict())

        return arr_to_return
    
    def create_transaction(self, transaction_type, transaction_value, transaction_time, curr_balance):
        
        self.transactions_counter += 1
        transaction = Transaction(transaction_type, transaction_value, transaction_time, curr_balance)

        self.transactions[self.transactions_counter] = transaction

        return transaction



    

    