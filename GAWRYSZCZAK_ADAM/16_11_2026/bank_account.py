class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name cannot be empty.")

        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise TypeError("Balance must be a number.")

        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")

        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self._validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    @staticmethod
    def _validate_amount(amount: float) -> None:
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")