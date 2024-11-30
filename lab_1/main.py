# Файл main.py
from customer import Customer
from operator import Operator
from bill import Bill

# Приклад створення операторів, клієнтів та рахунків
def main():
    # Створюємо оператора
    operator1 = Operator(0, 1.5, 0.5, 0.1, 10)

    # Створюємо рахунок
    bill1 = Bill(100)

    # Створюємо клієнта
    customer1 = Customer(0, "Іван", 20, operator1, bill1, 100)

    # Дії клієнта
    customer1.talk(10, customer1)
    customer1.message(5, customer1)
    customer1.connection(50)

if __name__ == "__main__":
    main()