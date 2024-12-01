class Customer:
    def __init__(self, ID, name, age, operators, bills, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators
        self.bills = bills
        self.limitingAmount = limitingAmount

    def talk(self, minute, other):
        print(f"{self.name} дзвонить до {other.name} на {minute} хвилин")

    def message(self, quantity, other):
        print(f"{self.name} надсилає {quantity} повідомлень до {other.name}")

    def connection(self, amount):
        print(f"{self.name} підключається до Інтернету з {amount} MB")

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def getOperators(self):
        return self.operators

    def setOperators(self, operators):
        self.operators = operators

    def getBills(self):
        return self.bills

    def setBills(self, bills):
        self.bills = bills