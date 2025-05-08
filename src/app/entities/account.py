import re
from typing import Tuple
from ..errors.entity_errors import ParamNotValidated

class Account:
    name: str
    agency: str
    account_number: str
    current_balance: float
    
    def __init__(self, name: str=None, agency: str=None, account_number: str=None, current_balance: float=None):
        validation_name = self.validate_name(name)
        if validation_name[0] is False:
            raise ParamNotValidated("name", validation_name[1])
        self.name = name
        
        validation_agency = self.validate_agency(agency)
        if validation_agency[0] is False:
            raise ParamNotValidated("agency", validation_agency[1])
        self.agency = agency

        validation_account_number = self.validate_account_number(account_number)
        if validation_account_number[0] is False:
            raise ParamNotValidated("account_number", validation_account_number[1])
        self.account_number = account_number
        
        validation_current_balance = self.validate_current_balance(current_balance)
        if validation_current_balance[0] is False:
            raise ParamNotValidated("current_balance", validation_current_balance[1])
        self.current_balance = current_balance
        
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        return (True, "")
        
    @staticmethod
    def validate_agency(agency: str) -> Tuple[bool, str]:
        if agency is None:
            return (False, "Agency is required")
        if type(agency) != str:
            return (False, "Agency must be a string")
        if len(agency) != 4:
            return (False, "Agency must have 4 digits")
        
        return (True, "")
    
    @staticmethod
    def validate_account_number(account_number: str) -> Tuple[bool, str]:
        account_number_pattern = r'^\d{5}-\d$'
        if account_number is None:
            return (False, "Account number is required")
        if type(account_number) != str:
            return (False, "Account number type must be a string")
        if not bool(re.match(account_number_pattern, account_number)):
            return (False, "Account number format must be XXXXX-X")

        return (True, "")
    
    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
        if current_balance is None:
            return (False, "Current balance is required")
        if type(current_balance) != float:
            return (False, "Current balance must be a float")
        return (True, "")    
        
    def to_dict(self):
        return {
            "name": self.name,
            "agency": self.agency,
            "account": self.account_number,
            "current_balance": self.current_balance
        }
    
    def __eq__(self,other):
        return self.name == other.name and self.agency == other.agency and self.account_number == other.account_number and self.current_balance == other.current_balance
    
    def __repr__(self):
        return f"Account(name={self.name}, agency={self.agency}, account_number={self.account_number}, current_balance={self.current_balance})"