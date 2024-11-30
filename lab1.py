class Customer:
    def __init__(self, ID, name, age, operators, limits_per_operator):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = {op.ID: op for op in operators}  # Associate operators by ID
        self.bills = {op.ID: Bill(limits_per_operator[op.ID]) for op in operators}  # Separate bills for each operator

    @property
    def tracking(self):
        return self.bills

    def get_bill(self, operator_id):
        """Get the bill associated with a specific operator."""
        return self.bills.get(operator_id)

    def set_tracking(self, operator_id, limit):
        """Dynamically create a bill for an operator if it doesn't exist."""
        if operator_id not in self.bills:
            self.bills[operator_id] = Bill(limit)
            print(f"Created a new bill for operator ID {operator_id} with limit {limit}")

    def talk(self, minute, other, operator_id):
        """Handle talking action using a specific operator."""
        operator = self.operators.get(operator_id)
        bill = self.get_bill(operator_id)

        if operator and bill and bill.check(operator.calculate_talking_cost(minute, self)):
            cost = operator.calculate_talking_cost(minute, self)
            bill.add(cost)
            print(f"{self.name} talked to {other.name} for {minute} minutes, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no valid operator assigned.")

    def message(self, quantity, other, operator_id):
        """Handle messaging action using a specific operator."""
        operator = self.operators.get(operator_id)
        bill = self.get_bill(operator_id)

        if operator and bill and bill.check(operator.calculate_message_cost(quantity, self, other)):
            cost = operator.calculate_message_cost(quantity, self, other)
            bill.add(cost)
            print(f"{self.name} sent {quantity} messages to {other.name}, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no valid operator assigned.")

    def connection(self, amount, operator_id):
        """Handle network connection using a specific operator."""
        operator = self.operators.get(operator_id)
        bill = self.get_bill(operator_id)

        if operator and bill and bill.check(operator.calculate_network_cost(amount)):
            cost = operator.calculate_network_cost(amount)
            bill.add(cost)
            print(f"{self.name} used {amount} MB of data, costing {cost:.2f}")
        else:
            print("Exceeds bill limit or no valid operator assigned.")


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
        if customer.operators.get(self.ID) == other.operators.get(self.ID):
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
        self.customers = {}
        self.operators = {}

    def create_customer(self, ID, name, age, operators, limits_per_operator):
        customer = Customer(ID, name, age, operators, limits_per_operator)
        self.customers[ID] = customer
        print(f"Created customer {name} with ID {ID}, age {age}")

    def create_operator(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        operator = Operator(ID, talking_charge, message_cost, network_charge, discount_rate)
        self.operators[ID] = operator
        print(f"Created operator with ID {ID}, talking charge {talking_charge:.2f}, message cost {message_cost:.2f}, "
              f"network charge {network_charge:.2f}, discount rate {discount_rate}%")

    def run(self):
        # Create operators
        operator1 = Operator(0, 0.5, 0.1, 0.2, 10)
        operator2 = Operator(1, 0.6, 0.15, 0.25, 15)
        self.operators[0] = operator1
        self.operators[1] = operator2

        # Assign separate limits for each operator
        limits_per_operator = {0: 100.0, 1: 200.0}

        # Create customers with multiple operators and separate limits
        customer1 = Customer(0, "Mary", 30, [operator1, operator2], limits_per_operator)
        customer2 = Customer(1, "Ivan", 25, [operator1], {0: 150.0})
        self.customers[0] = customer1
        self.customers[1] = customer2

        # Simulate interactions
        customer1.talk(10, customer2, 0)
        customer1.talk(5, customer2, 1)
        customer1.message(10, customer2, 0)
        customer1.connection(50, 0)


# Run the program
main = Main()
main.run()