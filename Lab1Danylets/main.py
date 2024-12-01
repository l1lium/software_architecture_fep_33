from customer import Customer
from myOperator import Operator
from bill import Bill

def main():
    operator1 = Operator(0, 1.5, 0.5, 0.1, 10)

    bill1 = Bill(100)

    customer1 = Customer(0, "Богдан", 20, operator1, bill1, 100)

    customer1.talk(10, customer1)
    customer1.message(5, customer1)
    customer1.connection(50)

if __name__ == "__main__":
    main()