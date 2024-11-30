import hashlib
from dataclasses import dataclass
from typing import List, Dict

# ====== CreditCard Class ======
class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: int):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv_hash = None
        self.cvv = cvv  # Set using the property to apply hashing

    @property
    def cvv(self):
        return self._cvv_hash

    @cvv.setter
    def cvv(self, value: int):
        self._cvv_hash = self.encrypt(value)

    def encrypt(self, value: int) -> str:
        """Hash the CVV value."""
        return hashlib.sha256(str(value).encode()).hexdigest()

    def decrypt(self, hash_value: str) -> str:
        """Decrypt is not possible with hashing. This is a placeholder."""
        raise NotImplementedError("CVV cannot be decrypted as it's hashed.")

    def give_bank_details(self) -> Dict[str, str]:
        """Return bank details as a dictionary."""
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": f"${self.credit_limit:.2f}",
            "grace_period": f"{self.grace_period} days",
            "cvv_hash": self._cvv_hash,
        }


# ====== BankInfo Class ======
class BankInfo:
    def __init__(self, bank_name: str, holder_name: str):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = []
        self.credit_history = {}

    def transaction_list(self, account_number: str) -> List[str]:
        """Return a list of arbitrary transactions for the account."""
        return [f"Transaction {i} for account {account_number}" for i in range(1, 6)]


# ====== PersonalInfo Dataclass ======
@dataclass
class PersonalInfo:
    name: str
    address: str
    phone_number: str


# ====== BankCustomer (Adapter) ======
class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, credit_card: CreditCard):
        self.personal_info = personal_info
        self.credit_card = credit_card

    def give_bank_details(self) -> Dict[str, str]:
        """Adapt CreditCard details to BankInfo format."""
        bank_details = self.credit_card.give_bank_details()
        return {
            "name": self.personal_info.name,
            "address": self.personal_info.address,
            "phone": self.personal_info.phone_number,
            "bank_details": bank_details,
        }


# ====== Decorator for CreditCard ======
class CreditCardDecorator:
    def __init__(self, credit_card: CreditCard):
        self._credit_card = credit_card

    def give_bank_details(self):
        return self._credit_card.give_bank_details()


class GoldenCreditCard(CreditCardDecorator):
    def get_rewards(self) -> str:
        return "Golden Credit Card: Enjoy 5% cashback on every purchase!"


class CorporateCreditCard(CreditCardDecorator):
    def get_corporate_benefits(self) -> str:
        return "Corporate Credit Card: Higher limits and access to exclusive lounges!"


# ====== Testing ======

def main():
    # Create personal info
    personal_info = PersonalInfo(name="John Doe", address="123 Main St", phone_number="555-5555")

    # Create a credit card
    credit_card = CreditCard(client="John Doe", account_number="123456789", credit_limit=5000.0, grace_period=30, cvv=123)

    # Create a bank customer (adapter)
    bank_customer = BankCustomer(personal_info=personal_info, credit_card=credit_card)
    print("Bank Customer Details:")
    print(bank_customer.give_bank_details())

    # Decorate the credit card
    golden_card = GoldenCreditCard(credit_card)
    corporate_card = CorporateCreditCard(credit_card)

    # Test decorators
    print("\nGolden Card Benefits:")
    print(golden_card.get_rewards())

    print("\nCorporate Card Benefits:")
    print(corporate_card.get_corporate_benefits())


if __name__ == "__main__":
    main()
