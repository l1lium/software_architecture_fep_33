class Bill:
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount):
        return (self.currentDebt + amount) <= self.limitingAmount

    def add(self, amount):
        if self.check(amount):
            self.currentDebt += amount
            return True
        return False

    def pay(self, amount):
        self.currentDebt -= amount

    def changeTheLimit(self, amount):
        self.limitingAmount = amount