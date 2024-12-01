class Customer:
    def __init__(self, ID, first_name, second_name, age, operator, bill):
        self.ID = ID
        self.first_name = first_name
        self.second_name = second_name
        self.age = age
        self.operator = operator
        self.bill = bill
        self.cust_history = []

    def talk(self, duration, other):
        bill = self.operator.get_bill(self)
        cost = self.operator.calculate_talking_cost(duration, self)
        
        if bill.check(cost):
            bill.add(cost)
            print(f"{self.first_name} talked to {other.first_name} for {duration} minutes, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def message(self, quantity, other):
        bill = self.operator.get_bill(self)
        cost = self.operator.calculate_message_cost(quantity, self, other)
        
        if bill.check(cost):
            bill.add(cost)
            print(f"{self.first_name} sent {quantity} messages to {other.first_name}, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def connection(self, amount):
        bill = self.operator.get_bill(self)
        cost = self.operator.calculate_network_cost(amount)
        
        if bill.check(cost):
            bill.add(cost)
            print(f"{self.first_name} used {amount} MB of data, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no operator assigned.")

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age
        
    def get_operator(self):
        return self.operator

    def set_operator(self, operator):
        self.operator = operator

    def get_bill(self):
        return self.bill

    def set_bill(self, bill):
        self.bill = bill


class Operator:
    def __init__(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        self.ID = ID 
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate
        self.operator_bills= {}
        
    def get_bill(self, customer):
        if customer.ID not in self.operator_bills:
            self.operator_bills[customer.ID] = Bill(100.0)
            print(f"Created new bill for customer {customer.ID} under operator {self.ID}")
        return self.operator_bills[customer.ID]

    def calculate_talking_cost(self, minute, customer):
        cost = minute * self.talking_charge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discount_rate / 100)
        return cost

    def calculate_message_cost(self, quantity, customer, other):
        cost = quantity * self.message_cost
        if customer.operator.ID == other.operator.ID:
            cost *= (1 - self.discount_rate / 100)
        return cost

    def calculate_network_cost(self, amount):
        return amount * self.network_charge

    def get_talking_charge(self):
        return self.talking_charge

    def set_talking_charge(self, charge):
        self.talking_charge = charge

    def get_message_cost(self):
        return self.message_cost

    def set_message_cost(self, cost):
        self.message_cost = cost

    def get_network_charge(self):
        return self.network_charge

    def set_network_charge(self, charge):
        self.network_charge = charge

    def get_discount_rate(self):
        return self.discount_rate

    def set_discount_rate(self, rate):
        self.discount_rate = rate


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

    def change_limit(self, amount):
        self.limiting_amount = amount
        print(f"Changed bill limit to {self.limiting_amount:.2f}")


class Main:
    def __init__(self):
        self.customers = {}  # {customer_ID: Customer}
        self.operators = {}  # {operator_ID: Operator}

    def create_customer(self, ID, first_name, second_name, age, operator, bill_limit):
        bill = Bill(bill_limit)
        customer = Customer(ID, first_name, second_name, age, operator, bill)
        self.customers[ID] = customer
        print(f"Created customer {first_name} {second_name} with ID {ID}, age {age}")

    def create_operator(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        operator = Operator(ID, talking_charge, message_cost, network_charge, discount_rate)
        self.operators[ID] = operator
        print(f"Created operator {ID} with talking charge {talking_charge:.2f}")

    def run(self):
        self.create_operator(0, 0.5, 0.1, 0.2, 10)
        self.create_operator(1, 0.4, 0.15, 0.25, 15)

        self.create_customer(0, "Solomiia", "Krasovska", 19, self.operators[0], 100.0)
        self.create_customer(1, "Mary", "Scripinets", 12, self.operators[1], 150.0)

        solomiia = self.customers[0]
        mary = self.customers[1]

        solomiia.talk(10, mary)
        mary.message(3, solomiia)
        mary.connection(40)

        for operator_id, operator in self.operators.items():
            print(f"Operator {operator_id} bills:")
            for customer_id, bill in operator.operator_bills.items():
                print(f"  Customer {customer_id}: Current debt {bill.current_debt:.2f}")


main = Main()
main.run()
