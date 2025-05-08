from typing import Tuple
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.errors.entity_errors import ParamNotValidated


class Transaction:
    transaction_type: TransactionsType
    value: float
    curr_balance: float
    timestamp: float

    def __init__(self, transaction_type: TransactionsType=None, value: float=None, timestamp: float=None, curr_balance: float=None):

        validation_transaction_type = self.validate_type(transaction_type)
        if validation_transaction_type[0] is False:
            raise ParamNotValidated("type", validation_transaction_type[1])
        self.transaction_type = transaction_type

        validation_value = self.validate_value(value)
        if validation_value[0] is False:
            raise ParamNotValidated("value", validation_value[1])
        self.value = value

        validation_timestamp = self.validate_timestamp(timestamp)
        if validation_timestamp[0] is False:
            raise ParamNotValidated("timestamp", validation_timestamp[1])
        self.timestamp = timestamp

        validation_curr_balance = self.validate_curr_balance(curr_balance)
        if validation_curr_balance[0] is False:
            raise ParamNotValidated("curr_balance", validation_curr_balance[1])
        self.curr_balance = curr_balance

    @staticmethod
    def validate_type(transaction_type: TransactionsType)  -> Tuple[bool, str]:
        if transaction_type is None:
            return (False, "Transaction type is required")  
        if type(transaction_type) != TransactionsType:
            return (False, "The type of field Transaction type must be TransactionsType")
        return (True, "")
    
    @staticmethod
    def validate_value(value: float) -> Tuple[bool, str]:
        if value is None:
            return (False, "Transaction value is required")
        if type(value) != float:
            return (False, "Transaction value type must be float")
        if value < 0:
            return (False, "Transaction must be positive")
        return (True, "")
    
    @staticmethod
    def validate_timestamp(timestamp: float) -> Tuple[bool, str]:
        if timestamp is None:
            return (False, "Timestamp is required")
        if type(timestamp) != float:
            return (False, "Timestamp type must be float")
        if timestamp < 0:
            return (False, "Timestamp must be bigger than 0")
        return (True, "")
    
    @staticmethod
    def validate_curr_balance(curr_balance: float) -> Tuple[bool, str]:
        if curr_balance is None:
            return (False, "Transaction curr_balance is required")
        if type(curr_balance) != float:
            return (False, "Transaction curr_balance type must be float")
        if curr_balance < 0:
            return (False, "The curr_balance cannot be negative")
        return (True, "")

    def to_dict(self):
        return {
            "type": self.transaction_type.value,
            "value": self.value,
            "current_balance": self.curr_balance,
            "timestamp": self.timestamp
        }

    def __eq__(self, other):
        return self.transaction_type == other.transaction_type and self.value == other.value and self.curr_balance == other.curr_balance and self.timestamp == other.timestamp
    
    def __repr__(self):
        return f"Transaction(type={self.transaction_type}, value={self.value}, curr_balance={self.curr_balance}, timestamp={self.timestamp})"