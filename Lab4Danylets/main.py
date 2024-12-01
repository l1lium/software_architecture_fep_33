import hashlib
from typing import List, Dict
from dataclasses import dataclass


class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: int):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = None
        self.cvv = cvv  

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value: int):
        self._cvv = self.encrypt(str(value))

    def encrypt(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    def decrypt(self, value: str) -> str:
        return "Decryption is not feasible for one-way hashes"

    def give_bank_details(self, *args) -> Dict[str, str]:
        return {
            "Client": self.client,
            "Account Number": self.account_number,
            "Credit Limit": self.credit_limit,
            "Grace Period": self.grace_period,
            "CVV Hash": self._cvv,
        }

class BankInfo:
    def __init__(self, bank_name: str, holder_name: str):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = []
        self.credit_history = {}

    def transaction_list(self, account_number: str) -> List[str]:
        return ["Transaction 1", "Transaction 2", "Transaction 3"]  # Arbitrary example

@dataclass
class PersonalInfo:
    name: str
    age: int

class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, credit_card: CreditCard):
        self.personal_info = personal_info
        self.credit_card = credit_card

    def give_bank_details(self, *args) -> Dict[str, str]:
        details = self.credit_card.give_bank_details()
        details.update({"Holder Name": self.personal_info.name})
        return details


class CreditCardDecorator:
    def __init__(self, credit_card: CreditCard):
        self._credit_card = credit_card

    def give_bank_details(self, *args) -> Dict[str, str]:
        return self._credit_card.give_bank_details()

class GoldenCreditCard(CreditCardDecorator):
    def give_bank_details(self, *args) -> Dict[str, str]:
        details = super().give_bank_details()
        details["Card Type"] = "Golden"
        return details

class CorporateCreditCard(CreditCardDecorator):
    def give_bank_details(self, *args) -> Dict[str, str]:
        details = super().give_bank_details()
        details["Card Type"] = "Corporate"
        details["Corporate Benefits"] = "Priority Support, Higher Limits"
        return details

if __name__ == "__main__":
    personal_info = PersonalInfo(name="Alice", age=30)
    credit_card = CreditCard(client="Alice", account_number="1234567890", credit_limit=5000.0, grace_period=30, cvv=123)

    customer = BankCustomer(personal_info, credit_card)
    print("Adapter Pattern Test:")
    print(customer.give_bank_details())

    golden_card = GoldenCreditCard(credit_card)
    corporate_card = CorporateCreditCard(credit_card)

    print("\nDecorator Pattern Test:")
    print("Golden Credit Card:", golden_card.give_bank_details())
    print("Corporate Credit Card:", corporate_card.give_bank_details())
