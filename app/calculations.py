def add(num1:int,num2:int):
    return num1 + num2

def subtract(num1:int,num2:int):
    return num1 - num2

def multiply(num1:int,num2:int):
    return num1 * num2

def divide(num1:int,num2:int):
    return num1 / num2

#We create our own class for the exception
class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0): #this sets a default of 0 if we dont provide one
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount
        
    def collect_interest(self):
        self.balance *= 1.1
    