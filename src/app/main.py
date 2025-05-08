from fastapi import FastAPI, HTTPException
from mangum import Mangum

from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.errors.entity_errors import ParamNotValidated
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.entities.account import Account
from src.app.entities.transaction import Transaction

import time

app = FastAPI()

account_repo = AccountRepositoryMock()
transaction_repo = TransactionRepositoryMock()

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    account = account_repo.get_account(account_id)
    
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {
        "account_id": account_id,
        "account": account.to_dict()    
    }

@app.post("/accounts/{account_id}/deposit", status_code=201)
def make_deposit(account_id: int, request: dict):
    value = request.get("value")
    
    if value is None:
        raise HTTPException(status_code=400, detail="Value is required")
    if type(value) != float:
        raise HTTPException(status_code=400, detail="Value must be a float")
    if value <= 0:
        raise HTTPException(status_code=400, detail="Value must be positive")

    account = account_repo.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    updated_account = account_repo.make_deposit(account, value)

    transaction = transaction_repo.create_transaction(
        transaction_type=TransactionsType.DEPOSIT,
        transaction_value=value,
        transaction_time=time.time(),
        curr_balance=updated_account.current_balance
    )
    
    return {
        "account_id": account_id,
        "account": updated_account.to_dict(),
        "transaction": transaction.to_dict()
    }

@app.post("/accounts/{account_id}/withdraw", status_code=201)
def make_withdraw(account_id: int, request: dict):
    value = request.get("value")
    
    if value is None:
        raise HTTPException(status_code=400, detail="Value is required")
    if type(value) != float:
        raise HTTPException(status_code=400, detail="Value must be a float")
    if value <= 0:
        raise HTTPException(status_code=400, detail="Value must be positive")

    account = account_repo.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.current_balance < value:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    updated_account = account_repo.make_withdraw(account, value)
    
    transaction = transaction_repo.create_transaction(
        transaction_type=TransactionsType.WITHDRAW,
        transaction_value=value,
        transaction_time=time.time(),
        curr_balance=updated_account.current_balance
    )
    
    return {
        "account_id": account_id,
        "account": updated_account.to_dict(),
        "transaction": transaction.to_dict()
    }

@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: int):
    account = account_repo.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transactions = transaction_repo.get_all_transactions()
    account_transactions = [
        t for t in transactions 
        if t["current_balance"] == account.current_balance
    ]
    
    return {
        "account_id": account_id,
        "transactions": account_transactions
    }

@app.post("/accounts/create", status_code=201)
def create_account(request: dict):
    try:
        account = Account(
            name=request.get("name"),
            agency=request.get("agency"),
            account_number=request.get("account_number"),
            current_balance=request.get("current_balance", 0.0)
        )
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return {
        "account": account.to_dict()
    }

handler = Mangum(app, lifespan="off")