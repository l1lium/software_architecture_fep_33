from typing import List


class Customer:
    def __init__(self, ID: int, name: str, age: int, operators: List['Operator'], bills: List['Bill'], limitingAmount: float):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators
        self.bills = bills
        self.limitingAmount = limitingAmount
        print(f"Customer created: ID={ID}, Name={name}, Age={age}, LimitingAmount={limitingAmount}")

    def talk(self, minutes: int, other: 'Customer'):
        print(f"{self.name} is talking to {other.name} for {minutes} minutes.")

    def message(self, quantity: int, other: 'Customer'):
        print(f"{self.name} is sending {quantity} messages to {other.name}.")

    def connection(self, amount: float):
        print(f"{self.name} is using {amount} MB of internet.")

    def get_age(self):
        print(f"Getting age for {self.name}: {self.age}")
        return self.age

    def set_age(self, age: int):
        print(f"Setting age for {self.name} from {self.age} to {age}")
        self.age = age


class Operator:
    def __init__(self, ID: int, talkingCharge: float, messageCost: float, networkCharge: float, discountRate: int):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate
        print(f"Operator created: ID={ID}, TalkingCharge={talkingCharge}, MessageCost={messageCost}, NetworkCharge={networkCharge}, DiscountRate={discountRate}")

    def calculate_talking_cost(self, minutes: int, customer: Customer) -> float:
        discount = 1 - (self.discountRate / 100) if customer.age < 18 or customer.age > 65 else 1
        cost = minutes * self.talkingCharge * discount
        print(f"Calculating talking cost for {customer.name}: Minutes={minutes}, DiscountApplied={discount != 1}, Cost={cost}")
        return cost

    def calculate_message_cost(self, quantity: int, customer: Customer, other: Customer) -> float:
        discount = 1 - (self.discountRate / 100) if self.ID == other.operators[0].ID else 1
        cost = quantity * self.messageCost * discount
        print(f"Calculating message cost for {customer.name} to {other.name}: Quantity={quantity}, DiscountApplied={discount != 1}, Cost={cost}")
        return cost

    def calculate_network_cost(self, amount: float) -> float:
        cost = amount * self.networkCharge
        print(f"Calculating network cost: Amount={amount}, Cost={cost}")
        return cost


class Bill:
    def __init__(self, limitingAmount: float):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0
        print(f"Bill created: LimitingAmount={limitingAmount}, CurrentDebt={self.currentDebt}")

    def check(self, amount: float) -> bool:
        is_within_limit = self.currentDebt + amount <= self.limitingAmount
        print(f"Checking bill limit: Amount={amount}, CurrentDebt={self.currentDebt}, IsWithinLimit={is_within_limit}")
        return is_within_limit

    def add(self, amount: float):
        if self.check(amount):
            self.currentDebt += amount
            print(f"Added amount to bill: Amount={amount}, NewCurrentDebt={self.currentDebt}")
        else:
            print("Limit exceeded. Transaction denied.")

    def pay(self, amount: float):
        self.currentDebt -= amount
        print(f"Payment made: Amount={amount}, NewCurrentDebt={self.currentDebt}")

    def change_the_limit(self, amount: float):
        print(f"Changing bill limit from {self.limitingAmount} to {amount}")
        self.limitingAmount = amount


def main():
    customers = []
    operators = []
    bills = []

    operator1 = Operator(0, 0.5, 0.1, 0.05, 10)
    operators.append(operator1)

    bill1 = Bill(100)
    bills.append(bill1)

    customer1 = Customer(0, "Alice", 25, [operator1], [bill1], 100)
    customer2 = Customer(1, "Bob", 17, [operator1], [bill1], 50)
    customers.extend([customer1, customer2])

    customer1.talk(10, customer2)
    customer1.connection(50)
    customer2.message(5, customer1)

    cost = operator1.calculate_talking_cost(10, customer1)
    print(f"Talking cost: {cost}")
    bill1.add(cost)
    print(f"Current debt: {bill1.currentDebt}")

if __name__ == "__main__":
    main()
