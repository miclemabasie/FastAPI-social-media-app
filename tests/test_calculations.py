import pytest
from app.calculations import add, subtract, div, mult, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, res", [
    (1, 2, 3),
    (4, 5, 9),
    (2, 45, 47)
])
def test_add(x, y, res):
    assert add(x, y) == res


def test_subtract():
    assert subtract(3, 5) == -2


def test_div():
    assert div(8, 2) == 4
    assert div(8,0) == 0


def test_mult():
    assert mult(3, 5) == 15


# def test_bank_set_initial_amount():
#     bank_account = BankAccount(50)
#     assert bank_account.blc == 50

def test_bank_default_amount_works():
    bank_account = BankAccount()
    assert bank_account.blc == 0

def test_bank_account_withdraw():
    bank_account = BankAccount(100)
    bank_account.withdraw(39)
    assert bank_account.blc == 61
    assert bank_account.withdraw(100) == -1

def test_bank_deposit_works():
    bank_account = BankAccount(10)
    bank_account.deposit(44)
    
    assert bank_account.blc == 54

def test_bank_interest_collected():
    bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert int(bank_account.blc) == 110


# Using fixtures to run test cases
    
def test_bank_initial_balance_is_zero(zero_bank_account):
    assert zero_bank_account.blc == 0