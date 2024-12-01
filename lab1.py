class Customer:
    def __init__(self, ID, name, age, operators, bill):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators  # Список операторів
        self.bill = bill

    def talk(self, minute, other, operator_index):
        operator = self.operators[operator_index]
        if operator and self.bill.check(operator.calculate_talking_cost(minute, self)):
            cost = operator.calculate_talking_cost(minute, self)
            self.bill.add(cost)
            print(f"{self.name} talked to {other.name} for {minute} minutes using Operator {operator.ID}, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def message(self, quantity, other, operator_index):
        operator = self.operators[operator_index]
        if operator and self.bill.check(operator.calculate_message_cost(quantity, self, other)):
            cost = operator.calculate_message_cost(quantity, self, other)
            self.bill.add(cost)
            print(f"{self.name} sent {quantity} messages to {other.name} using Operator {operator.ID}, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def connection(self, amount, operator_index):
        operator = self.operators[operator_index]
        if operator and self.bill.check(operator.calculate_network_cost(amount)):
            cost = operator.calculate_network_cost(amount)
            self.bill.add(cost)
            print(f"{self.name} used {amount} MB of data using Operator {operator.ID}, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def add_operator(self, operator):
        self.operators.append(operator)
        print(f"{self.name} added Operator {operator.ID} to their account.")


class Operator:
    def __init__(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        self.ID = ID
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate

    def calculate_talking_cost(self, minute, customer):
        cost = minute * self.talking_charge
        if customer.age < 18 or customer.age > 65:
            cost -= cost * (self.discount_rate / 100)
        return cost

    def calculate_message_cost(self, quantity, customer, other):
        cost = quantity * self.message_cost
        if customer.operators[0] == other.operators[0]:  # Знижка, якщо клієнти мають одного оператора
            cost -= cost * (self.discount_rate / 100)
        return cost

    def calculate_network_cost(self, amount):
        return amount * self.network_charge


class Bill:
    def __init__(self, limiting_amount):
        self.limiting_amount = limiting_amount
        self.current_debt = 0.0

    def check(self, amount):
        return (self.current_debt + amount) <= self.limiting_amount

    def add(self, amount):
        if self.check(amount):
            self.current_debt += amount
            print(f"Added {amount:.2f} to the bill. Current debt is now {self.current_debt:.2f}")
        else:
            print("Exceeds limit, cannot add to the bill.")

    def pay(self, amount):
        self.current_debt -= amount
        print(f"Paid {amount:.2f}. Current debt is now {self.current_debt:.2f}")

    def change_the_limit(self, amount):
        self.limiting_amount = amount
        print(f"Changed bill limit to {self.limiting_amount:.2f}")


class Main:
    def __init__(self):
        self.customers = []
        self.operators = []

    def create_customer(self, ID, name, age, operators, bill_limit):
        bill = Bill(bill_limit)
        customer = Customer(ID, name, age, operators, bill)
        self.customers.append(customer)
        print(f"Created customer {name} with ID {ID}, age {age}, bill limit {bill_limit:.2f}")

    def create_operator(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        operator = Operator(ID, talking_charge, message_cost, network_charge, discount_rate)
        self.operators.append(operator)
        print(f"Created operator with ID {ID}, talking charge {talking_charge:.2f}, message cost {message_cost:.2f}, network charge {network_charge:.2f}, discount rate {discount_rate}%")

    def run(self):
        self.create_operator(0, 0.5, 0.1, 0.2, 10)
        self.create_operator(1, 0.7, 0.2, 0.3, 15)

        self.create_customer(0, "Mary", 30, [self.operators[0], self.operators[1]], 100.0)
        self.create_customer(1, "Ivan", 25, [self.operators[1]], 150.0)

        mary = self.customers[0]
        ivan = self.customers[1]

        # Використання першого оператора
        mary.talk(10, ivan, 0)
        mary.message(5, ivan, 0)
        mary.connection(50, 0)

        # Використання другого оператора
        mary.talk(5, ivan, 1)
        mary.connection(30, 1)

        mary.bill.pay(30)
        mary.bill.change_the_limit(200.0)


main = Main()
main.run()
