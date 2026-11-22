def _is_number(value) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)


class BankAccount:
    
    def __init__(self, owner: str, balance: float = 0):
        if not isinstance(owner, str) or owner.strip() == "":
            raise ValueError("Owner name must not be empty.")

        if not _is_number(balance):
            raise TypeError("Balance must be a number.")

        if balance < 0:
            raise ValueError("Opening balance must not be negative.")

        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self._check_amount(amount)
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        self._check_amount(amount)

        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount

    @staticmethod
    def _check_amount(amount: float) -> None:
        if not _is_number(amount):
            raise TypeError("Amount must be a number.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
