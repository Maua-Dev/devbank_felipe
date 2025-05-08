import pytest
from src.app.entities.account import Account
from src.app.enums.transactions_type_enum import TransactionsType
from src.app.errors.entity_errors import ParamNotValidated


class Test_Account:
    def test_account(self):
        account = Account("Victor", "0000", "00000-0", 1000.0)
        assert account.name == "Victor"
        assert account.agency == "0000"
        assert account.account_number == "00000-0"
        assert account.current_balance == 1000.0
        
    def test_account_dict(self):
        account = Account("Victor", "0000", "00000-0", 1000.0)
        assert account.to_dict() == {
            "name": "Victor",
            "agency": "0000",
            "account": "00000-0",
            "current_balance": 1000.0
        }
    
    def test_account_name_is_none(self):
        with pytest.raises(ParamNotValidated):
            Account("0000", "00000-0", 1000.0)
            
    def test_account_name_is_too_short(self):
        with pytest.raises(ParamNotValidated):
            Account("Vi", "0000", "00000-0", 1000.0)
            
    def test_account_agency_is_none(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", "00000-0", 1000.0)
            
    def test_account_agency_is_not_string(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", 0000, "00000-0", 1000.0)
            
    def test_account_number_is_none(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", "0000", 1000.0)
            
    def test_account_number_dont_match(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", "0000", "000000", 1000.0)
            
    def test_account_current_balance_is_none(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", "0000", "000000")
        
    def test_account_current_balance_is_not_float(self):
        with pytest.raises(ParamNotValidated):
            Account("Victor", "0000", "000000", "1000.0")