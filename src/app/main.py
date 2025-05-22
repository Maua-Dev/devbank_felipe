from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.errors.entity_errors import ParamNotValidated
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.entities.account import Account
from src.app.entities.transaction import Transaction
import time
import json
import traceback

app = FastAPI()

account_repo = AccountRepositoryMock()
transaction_repo = TransactionRepositoryMock()

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {str(exc)}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc),
            "type": exc.__class__.__name__
        },
    )

@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "Account API"
    }

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    try:
        account = account_repo.get_account(account_id)
        
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return {
            "success": True,
            "account_id": account_id,
            "account": account.to_dict()    
        }
    except Exception as e:
        print(f"Error in get_account: {str(e)}")
        raise

@app.post("/accounts/{account_id}/deposit", status_code=201)
def make_deposit(account_id: int, request: dict):
    try:
        value = request.get("value")
        
        if value is None:
            raise HTTPException(status_code=400, detail="Value is required")
        if type(value) not in (float, int):
            raise HTTPException(status_code=400, detail="Value must be a number")
        if value <= 0:
            raise HTTPException(status_code=400, detail="Value must be positive")

        account = account_repo.get_account(account_id)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")

        updated_account = account_repo.make_deposit(account, float(value))

        transaction = transaction_repo.create_transaction(
            transaction_type=TransactionsType.DEPOSIT,
            transaction_value=float(value),
            transaction_time=time.time(),
            curr_balance=updated_account.current_balance
        )
        
        return {
            "success": True,
            "account_id": account_id,
            "account": updated_account.to_dict(),
            "transaction": transaction.to_dict()
        }
    except Exception as e:
        print(f"Error in make_deposit: {str(e)}")
        raise

@app.post("/accounts/{account_id}/withdraw", status_code=201)
def make_withdraw(account_id: int, request: dict):
    try:
        value = request.get("value")
        
        if value is None:
            raise HTTPException(status_code=400, detail="Value is required")
        if type(value) not in (float, int):
            raise HTTPException(status_code=400, detail="Value must be a number")
        if value <= 0:
            raise HTTPException(status_code=400, detail="Value must be positive")

        account = account_repo.get_account(account_id)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.current_balance < float(value):
            raise HTTPException(status_code=400, detail="Insufficient funds")

        updated_account = account_repo.make_withdraw(account, float(value))
        
        transaction = transaction_repo.create_transaction(
            transaction_type=TransactionsType.WITHDRAW,
            transaction_value=float(value),
            transaction_time=time.time(),
            curr_balance=updated_account.current_balance
        )
        
        return {
            "success": True,
            "account_id": account_id,
            "account": updated_account.to_dict(),
            "transaction": transaction.to_dict()
        }
    except Exception as e:
        print(f"Error in make_withdraw: {str(e)}")
        raise

@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: int):
    try:
        account = account_repo.get_account(account_id)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        transactions = transaction_repo.get_all_transactions()
        
        return {
            "success": True,
            "account_id": account_id,
            "transactions": [t.to_dict() for t in transactions]
        }
    except Exception as e:
        print(f"Error in get_transactions: {str(e)}")
        raise

@app.post("/accounts/create", status_code=201)
def create_account(request: dict):
    try:
        account = Account(
            name=request.get("name"),
            agency=request.get("agency"),
            account_number=request.get("account_number"),
            current_balance=request.get("current_balance", 0.0)
        )
        
        return {
            "success": True,
            "message": "Account created successfully",
            "account": account.to_dict()
        }
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as e:
        print(f"Error in create_account: {str(e)}")
        raise

def lambda_handler(event, context):
    print("Lambda event received:", json.dumps(event))
    
    try:
        asgi_handler = Mangum(app, lifespan="off")
        response = asgi_handler(event, context)
        
        print("Lambda response:", json.dumps(response))
        return response
    except Exception as e:
        print(f"Lambda handler error: {str(e)}")
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }

handler = Mangum(app, lifespan="off")