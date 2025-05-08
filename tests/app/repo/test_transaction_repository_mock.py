import time
from src.app.entities.transaction import Transaction
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock


class Test_TransactionRepositoryMock:

    def test_create_transaction_deposit(self):

        value = 100.0
        curr_time = time.time()

        repo_account = AccountRepositoryMock()
        repo_transaction = TransactionRepositoryMock()

        account = repo_account.get_account(1)
        repo_account.make_deposit(account, value)

        transaction = repo_transaction.create_transaction(TransactionsType.DEPOSIT, value, curr_time, account.current_balance)

        assert repo_transaction.transactions.get(1) == transaction

    def test_create_transaction_withdraw(self):

        value = 500.0
        curr_time = time.time()

        repo_account = AccountRepositoryMock()
        repo_transaction = TransactionRepositoryMock()

        account = repo_account.get_account(1)
        repo_account.make_withdraw(account, value)

        transaction = repo_transaction.create_transaction(TransactionsType.WITHDRAW, value, curr_time, account.current_balance)

        assert repo_transaction.transactions.get(1) == transaction


    def test_get_all_transactions(self):

        curr_time = time.time()

        repo_account = AccountRepositoryMock()
        repo_transaction = TransactionRepositoryMock()

        account = repo_account.get_account(1)

        repo_account.make_deposit(account, 100.0)
        repo_transaction.create_transaction(TransactionsType.DEPOSIT, 100.0, curr_time, account.current_balance)

        repo_account.make_withdraw(account, 50.0)
        repo_transaction.create_transaction(TransactionsType.WITHDRAW, 50.0, curr_time + 1, account.current_balance)

        response = repo_transaction.get_all_transactions()

        expected = [
            {
                "type": "deposit",
                "value": 100.0,
                "current_balance": 1100.0,
                "timestamp": curr_time
            },
            {
                "type": "withdraw",
                "value": 50.0,
                "current_balance": 1050.0,
                "timestamp": curr_time + 1
            }   
        ]

        assert response == expected
