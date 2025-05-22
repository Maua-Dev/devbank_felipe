from fastapi.exceptions import HTTPException
import pytest
import time
from src.app.entities.account import Account
from src.app.entities.transaction import Transaction
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.main import (
    get_account,
    make_deposit,
    make_withdraw,
    get_transactions
)
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock

class Test_Main:
    @pytest.fixture
    def mock_repositories(self, monkeypatch):
        account_repo = AccountRepositoryMock()
        transaction_repo = TransactionRepositoryMock()
        
        monkeypatch.setattr('src.app.main.account_repo', account_repo)
        monkeypatch.setattr('src.app.main.transaction_repo', transaction_repo)
        
        return account_repo, transaction_repo

    def test_get_account(self, mock_repositories):
        account_repo, _ = mock_repositories
        account_id = 1
        response = get_account(account_id=account_id)
        
        assert response == {
            'account_id': account_id,
            'account': account_repo.accounts.get(account_id).to_dict()
        }

    def test_get_account_not_found(self, mock_repositories):
        account_id = 999
        with pytest.raises(HTTPException) as err:
            get_account(account_id=account_id)
        assert err.value.status_code == 404

    def test_make_deposit(self, mock_repositories):
        account_repo, transaction_repo = mock_repositories
        account_id = 1
        initial_balance = account_repo.accounts[1].current_balance
        deposit_value = 200.0
        
        response = make_deposit(account_id, {'value': deposit_value})
        
        assert response['account']['current_balance'] == initial_balance + deposit_value
        assert response['transaction']['type'] == TransactionsType.DEPOSIT.value
        assert response['transaction']['value'] == deposit_value

    def test_make_deposit_invalid_value(self, mock_repositories):
        test_cases = [
            ({'value': None}, "Value is required"),
            ({'value': '200'}, "Value must be a float"),
            ({'value': -200.0}, "Value must be positive"),
            ({}, "Value is required"),
        ]
        
        for body, error_msg in test_cases:
            with pytest.raises(HTTPException) as err:
                make_deposit(1, body)
            assert err.value.status_code == 400
            assert error_msg in str(err.value.detail)

    def test_make_withdraw(self, mock_repositories):
        account_repo, transaction_repo = mock_repositories
        account_id = 1
        initial_balance = account_repo.accounts[1].current_balance
        withdraw_value = 200.0
        
        response = make_withdraw(account_id, {'value': withdraw_value})
        
        assert response['account']['current_balance'] == initial_balance - withdraw_value
        assert response['transaction']['type'] == TransactionsType.WITHDRAW.value
        assert response['transaction']['value'] == withdraw_value

    def test_make_withdraw_insufficient_funds(self, mock_repositories):
        account_repo, _ = mock_repositories
        account_id = 1
        initial_balance = account_repo.accounts[1].current_balance
        
        with pytest.raises(HTTPException) as err:
            make_withdraw(account_id, {'value': initial_balance + 100})
        assert err.value.status_code == 400
        assert "Insufficient funds" in str(err.value.detail)

    def test_get_transactions(self, mock_repositories):
        account_repo, transaction_repo = mock_repositories
        account_id = 1

        transaction_repo.transactions.clear()

        transaction_repo.create_transaction(
            transaction_type=TransactionsType.DEPOSIT,
            transaction_value=100.0,
            transaction_time=time.time(),
            curr_balance=1000.0 + 100.0
        )
        
        transaction_repo.create_transaction(
            transaction_type=TransactionsType.WITHDRAW,
            transaction_value=50.0,
            transaction_time=time.time(),
            curr_balance=1100.0 - 50.0
        )
    
        response = get_transactions(account_id)
    
        assert len(response['transactions']) == 2
        assert any(t['type'] == 'deposit' for t in response['transactions'])
        assert any(t['type'] == 'withdraw' for t in response['transactions'])