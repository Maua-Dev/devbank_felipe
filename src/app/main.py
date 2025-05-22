from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .repo.transaction_repository_mock import TransactionRepositoryMock
from .repo.account_repository_mock import AccountRepositoryMock
from .repo.transaction_repository_interface import ITransactionRepository
from .repo.account_repository_interface import IAccountRepository
from .errors.entity_errors import ParamNotValidated
from .enums.transactions_type_enum import TransactionsType
from .entities.account import Account
from .entities.transaction import Transaction
from .environments import Environments

import time

app = FastAPI()

account_repo: IAccountRepository = Environments.get_account_repo()
transaction_repo: ITransactionRepository = Environments.get_transaction_repo()

@app.get("/")
def get_account(account_id: int):
    account = account_repo.get_account(account_id)
    
    return {
        "account": account.to_dict()    
    }

@app.post("/deposit")
def make_deposit(request: dict):
    total = 0

    for (bill, qty) in request.items():
        total += int(bill) * qty

    total = float(total)
    account = account_repo.get_account(1)
    account = account_repo.make_deposit(account, total)
    transaction = transaction_repo.create_transaction(TransactionsType.DEPOSIT, total,  round(time.time() * 1000, 3),account.current_balance)

    return {
        "current_balance": transaction.curr_balance,
        "timestamp": transaction.timestamp
    }

@app.post("/withdraw")
def make_withdraw(account_id: int, request: dict):
    total = 0

    for (bill, qty) in request.items():
        total += int(bill) * qty

    account = account_repo.get_account(1)

    if account.current_balance < total:
        raise HTTPException(403, "Saldo insuficiente")

    total = float(total)
    account = account_repo.make_withdraw(account, total)
    transaction = transaction_repo.create_transaction(TransactionsType.WITHDRAW, total, round(time.time() * 1000, 3), account.current_balance)

    return {
        "current_balance": transaction.curr_balance,
        "timestamp": transaction.timestamp
    }

@app.get("/history")
def get_transactions():
    transactions = transaction_repo.get_all_transactions()
    return {
        "transactions": transactions
    }

handler = Mangum(app, lifespan="off")