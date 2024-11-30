class Customer:
    def __init__(self, ID, name, age, operators, bills, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators
        self.bills = bills
        self.bill = Bill(limitingAmount)

    def talk(self, minute, other):
        cost = self.operators.calculateTalkingCost(minute, self)
        if self.bill.check(cost):
            self.bill.add(cost)
        else:
            print("Talk action denied. Bill limit exceeded.")

    def message(self, quantity, other):
        cost = self.operators.calculateMessageCost(quantity, self, other)
        if self.bill.check(cost):
            self.bill.add(cost)
        else:
            print("Message action denied. Bill limit exceeded.")

    def connection(self, amount):
        cost = self.operators.calculateNetworkCost(amount)
        if self.bill.check(cost):
            self.bill.add(cost)
        else:
            print("Internet connection denied. Bill limit exceeded.")

    # Getters and setters
    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def getOperator(self):
        return self.operators

    def setOperator(self, operator):
        self.operators = operator

    def getBill(self):
        return self.bill

    def setBill(self, bill):
        self.bill = bill


class Operator:
    def __init__(self, ID, talkingCharge, messageCost, networkCharge, discountRate):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute, customer):
        cost = minute * self.talkingCharge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateMessageCost(self, quantity, customer, other):
        cost = quantity * self.messageCost
        if customer.operators == other.operators:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateNetworkCost(self, amount):
        return amount * self.networkCharge

    # Getters and setters
    def getTalkingCharge(self):
        return self.talkingCharge

    def setTalkingCharge(self, charge):
        self.talkingCharge = charge

    def getMessageCost(self):
        return self.messageCost

    def setMessageCost(self, cost):
        self.messageCost = cost

    def getNetworkCharge(self):
        return self.networkCharge

    def setNetworkCharge(self, charge):
        self.networkCharge = charge

    def getDiscountRate(self):
        return self.discountRate

    def setDiscountRate(self, rate):
        self.discountRate = rate


class Bill:
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount):
        return (self.currentDebt + amount) <= self.limitingAmount

    def add(self, amount):
        self.currentDebt += amount

    def pay(self, amount):
        self.currentDebt -= amount

    def changeTheLimit(self, amount):
        self.limitingAmount = amount

    # Getters
    def getLimitingAmount(self):
        return self.limitingAmount

    def getCurrentDebt(self):
        return self.currentDebt


class Main:
    def __init__(self):
        self.customers = []
        self.operators = []
        self.bills = []

    def run(self, instructions):
        for instruction in instructions:
            action = instruction['action']
            if action == 'create_customer':
                self.create_customer(instruction)
            elif action == 'create_operator':
                self.create_operator(instruction)
            elif action == 'talk':
                self.handle_talk(instruction)
            elif action == 'message':
                self.handle_message(instruction)
            elif action == 'connect':
                self.handle_connection(instruction)
            elif action == 'pay_bill':
                self.handle_pay_bill(instruction)
            elif action == 'change_operator':
                self.handle_change_operator(instruction)
            elif action == 'change_bill_limit':
                self.handle_change_bill_limit(instruction)

    def create_customer(self, data):
        customer = Customer(
            data['ID'], data['name'], data['age'], 
            self.operators[data['operatorID']], 
            self.bills[data['billID']], 
            data['limitingAmount']
        )
        self.customers.append(customer)

    def create_operator(self, data):
        operator = Operator(
            data['ID'], data['talkingCharge'], 
            data['messageCost'], data['networkCharge'], 
            data['discountRate']
        )
        self.operators.append(operator)

    def handle_talk(self, data):
        customer = self.customers[data['customerID']]
        other = self.customers[data['otherCustomerID']]
        customer.talk(data['minute'], other)

    def handle_message(self, data):
        customer = self.customers[data['customerID']]
        other = self.customers[data['otherCustomerID']]
        customer.message(data['quantity'], other)

    def handle_connection(self, data):
        customer = self.customers[data['customerID']]
        customer.connection(data['amount'])

    def handle_pay_bill(self, data):
        customer = self.customers[data['customerID']]
        customer.bill.pay(data['amount'])

    def handle_change_operator(self, data):
        customer = self.customers[data['customerID']]
        customer.setOperator(self.operators[data['newOperatorID']])

    def handle_change_bill_limit(self, data):
        customer = self.customers[data['customerID']]
        customer.bill.changeTheLimit(data['newLimit'])
