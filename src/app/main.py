import time
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from .environments import Environments
from .repo.transaction_repository_interface import ITransactionRepository
from .repo.account_repository_interface import IAccountRepository
from .enums.transactions_type_enum import TransactionsType

app = FastAPI()

account_repo: IAccountRepository = Environments.get_account_repo()() 
transaction_repo: ITransactionRepository = Environments.get_transaction_repo()()

@app.get("/")
def get_account():
    account = account_repo.get_account(1)
    return account.to_dict()

@app.post("/deposit")
def post_deposit(request: dict):
    total = 0

    for (bill, qty) in request.items(): total += int(bill) * qty

    total = float(total)

    account = account_repo.get_account(1)
    account = account_repo.make_deposit(account, total)
    transaction = transaction_repo.create_transaction(TransactionsType.DEPOSIT, total,  round(time.time() * 1000, 3),account.current_balance)

    return {
        "current_balance": transaction.curr_balance,
        "timestamp": transaction.timestamp
    }

@app.post("/withdraw")
def post_withdraw(request: dict):
    total = 0

    for (bill, qty) in request.items(): total += int(bill) * qty

    account = account_repo.get_account(1)
    
    if account.current_balance < total: raise HTTPException(403, "Saldo insuficiente")

    total = float(total)

    account = account_repo.make_withdraw(account, total)
    transaction = transaction_repo.create_transaction(TransactionsType.WITHDRAW, total, round(time.time() * 1000, 3), account.current_balance)

    return {
        "current_balance": transaction.curr_balance,
        "timestamp": transaction.timestamp
    }

@app.get("/history")
def get_transactions():
    return {
        "all_transactions": transaction_repo.get_all_transactions()
    }


handler = Mangum(app, lifespan="off")