import hashlib
from dataclasses import dataclass
from typing import List, Dict

# Define the CreditCard class with encryption and decryption for cvv

class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: int):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = self.encrypt(str(cvv))

    # Hash the cvv value
    def encrypt(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    # Mock decrypt
    def decrypt(self) -> str:
        return "Cannot decrypt hashed value."

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value: int):
        self._cvv = self.encrypt(str(value))

    # Return bank details in dictionary format with CVV hashed
    def give_bank_details(self) -> Dict[str, str]:
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self._cvv,  # Hashed CVV
        }

# Define BankInfo class

@dataclass
class BankInfo:
    bank_name: str
    holder_name: str
    accounts_number: List[str]
    credit_history: Dict[str, float]

    #Return an arbitrary list of transactions for demonstration.
    def transaction_list(self, account_number: str) -> List[str]:
        return ["Transaction 1", "Transaction 2", "Transaction 3"]

# Define PersonalInfo dataclass for BankCustomer class

@dataclass
class PersonalInfo:
    name: str
    age: int
    address: str

# Define the BankCustomer adapter class

class BankCustomer:
    def __init__(self, personal_info: PersonalInfo, credit_card: CreditCard):
        self.personal_info = personal_info
        self.credit_card = credit_card

    #Use the credit card's bank details to provide a formatted response
    def give_bank_details(self) -> Dict[str, str]:
        bank_details = self.credit_card.give_bank_details()
        return {
            "holder_name": self.personal_info.name,
            "age": self.personal_info.age,
            "address": self.personal_info.address,
            **bank_details,
        }


# Decorator for CreditCard
class GoldenCreditCard(CreditCard):
    def __init__(self, credit_card: CreditCard):
        super().__init__(
            credit_card.client,
            credit_card.account_number,
            credit_card.credit_limit * 1.5,
            credit_card.grace_period,
            0  # Placeholder, since we cannot decrypt
        )
        self._cvv = credit_card.cvv  # Preserve the hashed CVV

    def special_reward(self):
        return "Access to Golden Rewards Program."

# Decorator for BankCustomer
class VIPCustomer(BankCustomer):
    def __init__(self, personal_info: PersonalInfo, credit_card: CreditCard):
        super().__init__(personal_info, credit_card)

    def vip_access(self):
        return "Access to VIP Lounge and personalized banking services."

# Testing the implementation
if __name__ == "__main__":
    # Creating initial objects
    personal_info = PersonalInfo(name="Ivan Ivanenko", age=45, address="Holovna str")
    credit_card = CreditCard(client="Petro Karpenko", account_number="1234567890",
                             credit_limit=5000, grace_period=30, cvv=123)

    # Adapter usage
    customer = BankCustomer(personal_info, credit_card)
    print("Bank Details via Adapter:")
    print(customer.give_bank_details())

    # Decorator usage
    golden_card = GoldenCreditCard(credit_card)
    vip_customer = VIPCustomer(personal_info, golden_card)

    print("\nDecorated Bank Details:")
    print(vip_customer.give_bank_details())
    print("Golden Card Special Reward:", golden_card.special_reward())
    print("VIP Customer Access:", vip_customer.vip_access())

