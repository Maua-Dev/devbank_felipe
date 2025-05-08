import time
from src.app.entities.transaction import Transaction
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.repo.account_repository_mock import AccountRepositoryMock


class ITransactionRepository:

    def test_get_account(self):

        repo = AccountRepositoryMock()
        account = repo.get_account(account_id=1)
        assert account == repo.accounts.get(1)

    def test_get_account_not_found(self):

        repo = AccountRepositoryMock()
        account = repo.get_account(account_id=10)
        assert account is None

    def test_make_deposit(self):

        repo = AccountRepositoryMock()
        account = repo.get_account(1)

        repo.make_deposit(account, 200.0)

        assert account.current_balance == 1200.0

    def test_make_withdraw(self):

        repo = AccountRepositoryMock()
        account = repo.get_account(1)

        repo.make_withdraw(account, 400.0)

        assert account.current_balance == 600.0

