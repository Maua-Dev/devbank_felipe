from fastapi.exceptions import HTTPException
import pytest
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.main import get_account, get_transactions, make_deposit, make_withdraw


class Test_Main:
    def test_get_account(self):
        expected = {
            'account': {
                'account': '11111-1',
                'agency': '1111',
                'current_balance': 1000.0,
                'name': 'Felipe Sakae'
        }
    }
        result = get_account()
        assert result == expected
         
    def test_make_deposit(self):
        request = {
            "2": 0,
            "5": 2,
            "10": 0,
            "20": 0,
            "50": 0,
            "100": 0,
            "200": 2
        }

        response = make_deposit(request=request)

        expected = {
            "current_balance": 1410.0,
            "timestamp": response["timestamp"]
        }

        assert response == expected

    def test_make_withdraw(self):
        request = {
            "2": 0,
            "5": 0,
            "10": 0,
            "20": 5,
            "50": 0,
            "100": 1,
            "200": 0
        }

        response = make_withdraw(request=request)

        expected = {
            "current_balance": 1210.0,
            "timestamp": response["timestamp"]
        }

        assert response == expected