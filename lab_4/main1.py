import hashlib
from dataclasses import dataclass
from typing import List, Dict

# CreditCard class
class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: int):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = None
        self.cvv = cvv  # Use setter for encryption
    
    @property
    def cvv(self):
        return self._cvv
    
    @cvv.setter
    def cvv(self, value):
        self._cvv = self.encrypt(str(value))
    
    def encrypt(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
    
    def decrypt(self, value: str) -> None:
        raise NotImplementedError("Hash cannot be decrypted. Use secure comparison instead.")
    
    def give_bank_details(self) -> Dict:
        return {
            "Client": self.client,
            "Account Number": self.account_number,
            "Credit Limit": self.credit_limit,
            "Grace Period": self.grace_period,
            "CVV (Hashed)": self._cvv
        }


# BankInfo class
class BankInfo:
    def __init__(self, bank_name: str, holder_name: str, accounts: List[str]):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts = accounts
        self.credit_history = {}
    
    def transaction_list(self, account_number: str) -> List[str]:
        # Arbitrary implementation
        return self.credit_history.get(account_number, ["No transactions found"])


# Adapter: BankCustomer
@dataclass
class PersonalInfo:
    name: str
    age: int
    address: str

class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, credit_card: CreditCard):
        self.personal_info = personal_info
        self.credit_card = credit_card
    
    def give_bank_details(self) -> Dict:
        details = self.credit_card.give_bank_details()
        details.update({
            "Personal Name": self.personal_info.name,
            "Address": self.personal_info.address
        })
        return details


# Client Code for Adapter Pattern
if __name__ == "__main__":
    personal_info = PersonalInfo(name="John Doe", age=30, address="123 Main St")
    credit_card = CreditCard(client="John Doe", account_number="1234567890123456", credit_limit=5000.0, grace_period=30, cvv=123)
    customer = BankCustomer(personal_info=personal_info, credit_card=credit_card)

    print("Bank Details:")
    print(customer.give_bank_details())



    # Decorators for CreditCard
class GoldenCreditCard:
    def __init__(self, credit_card: CreditCard):
        self.credit_card = credit_card
    
    def get_gold_benefits(self):
        return "Access to airport lounges, cashback offers, and more."

    def give_bank_details(self):
        details = self.credit_card.give_bank_details()
        details["Card Type"] = "Golden Credit Card"
        details["Benefits"] = self.get_gold_benefits()
        return details


class CorporateCreditCard:
    def __init__(self, credit_card: CreditCard):
        self.credit_card = credit_card
    
    def get_corporate_benefits(self):
        return "Higher credit limits and extended payment periods."

    def give_bank_details(self):
        details = self.credit_card.give_bank_details()
        details["Card Type"] = "Corporate Credit Card"
        details["Benefits"] = self.get_corporate_benefits()
        return details


# Client Code for Decorator Pattern
if __name__ == "__main__":
    credit_card = CreditCard(client="Jane Smith", account_number="9876543210987654", credit_limit=10000.0, grace_period=45, cvv=456)

    # Applying decorators
    golden_card = GoldenCreditCard(credit_card)
    corporate_card = CorporateCreditCard(credit_card)

    print("Golden Credit Card Details:")
    print(golden_card.give_bank_details())

    print("\nCorporate Credit Card Details:")
    print(corporate_card.give_bank_details())