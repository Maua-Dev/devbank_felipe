import time

import pytest
from src.app.entities.transaction import Transaction
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.errors.entity_errors import ParamNotValidated


class Test_Transaction:
    def test_transaction(self):
        curr_timestamp = time.time()
        transaction = Transaction(TransactionsType.DEPOSIT, 100.0, curr_timestamp, 1100.0)
        assert transaction.transaction_type == TransactionsType.DEPOSIT
        assert transaction.value == 100.0
        assert transaction.timestamp == curr_timestamp
        assert transaction.curr_balance == 1100.0

    def test_transaction_dict(self):
        curr_timestamp = time.time()
        transaction = Transaction(TransactionsType.WITHDRAW, 100.0, curr_timestamp, 1100.0)
        assert transaction.to_dict() == {
            "type": "withdraw",
            "value": 100.0,
            "current_balance": 1100.0,
            "timestamp": curr_timestamp
        }

    def test_transaction_type_is_none(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(100.0, curr_timestamp)

    def test_transaction_type_is_not_from_enum(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction('eu nao existo' , 100.0, curr_timestamp)

    def test_transaction_value_is_none(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(transaction_type=TransactionsType.WITHDRAW, timestamp=curr_timestamp)

    def test_transaction_value_is_not_float(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(TransactionsType.WITHDRAW, '100.0', curr_timestamp)

    def test_transaction_value_is_negative(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(TransactionsType.WITHDRAW, -100.0, curr_timestamp)

    def test_transaction_timestamp_is_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(transaction_type=TransactionsType.WITHDRAW, value=100.0)

    def test_transaction_timestamp_is_not_float(self):
        with pytest.raises(ParamNotValidated):
            Transaction(TransactionsType.WITHDRAW, 100.0, 'tempo em string')

    def test_transaction_timestamp_is_negative(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(TransactionsType.WITHDRAW, 100.0, -100)

    def test_transaction_curr_balance_is_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(transaction_type=TransactionsType.WITHDRAW, value=100.0, timestamp=time.time())

    def test_transaction_timestamp_is_not_float(self):
        with pytest.raises(ParamNotValidated):
            Transaction(transaction_type=TransactionsType.WITHDRAW, value=100.0, timestamp=time.time(), curr_balance='meu saldo')

    def test_transaction_timestamp_is_negative(self):
        curr_timestamp = time.time()
        with pytest.raises(ParamNotValidated):
            Transaction(transaction_type=TransactionsType.WITHDRAW, value=100.0, timestamp=time.time(), curr_balance=-10.0)