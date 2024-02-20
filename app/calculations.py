def add(num1: int, num2: int) -> int:

    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def div(num1: int, num2: int) -> int:
    if num2 != 0:
        return num1 / num2
    else:
        return 0
    
def mult(num1: int, num2: int) -> int:
    return num1 * num2

class BankAccount():
    def __init__(self, initial_blc=0):
        self.blc = initial_blc
    
    def deposit(self, amount):
        self.blc += amount

    def withdraw(self, amount):
        if amount <= self.blc:
            self.blc -= amount
        else:
            print("Can't make a withdrawal, Not enought funds")
            return -1

    def collect_interest(self):
        self.blc *= 1.1