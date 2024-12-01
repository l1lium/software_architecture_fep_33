class Bill:
    # Ініціалізація класу Bill з параметром ліміту та початковим боргом
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    # Метод для перевірки, чи перевищено ліміт
    def check(self, amount):
        return (self.currentDebt + amount) <= self.limitingAmount

    # Метод для додавання боргу
    def add(self, amount):
        if self.check(amount):
            self.currentDebt += amount
            return True
        return False

    # Метод для оплати рахунку
    def pay(self, amount):
        self.currentDebt -= amount

    # Метод для зміни ліміту
    def changeTheLimit(self, amount):
        self.limitingAmount = amount