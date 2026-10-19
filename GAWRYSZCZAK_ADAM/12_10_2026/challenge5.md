CHALLENGE 5: A transfer that partially succeeds
EXPECTED: Odrzucony przelew nie zmienia stanu żadnego konta — dla "X" słownik accounts zostaje jako {"A": 100, "B": 40}.
OBSERVED: Wyskakuje KeyError: 'X' na accounts[recipient] += amount, ale z konta "A" ubyło już 30 i w słowniku jest {"A": 70, "B": 40}.
BREAKPOINT: Na linijce accounts[sender] -= amount.
FIRST WRONG STATE: Linijka accounts[sender] -= amount zabiera 30 z konta "A", zanim program sprawdzi, czy konto "X" istnieje.
HYPOTHESIS: Funkcja zmienia saldo nadawcy przed sprawdzeniem wszystkich warunków (czy oba konta są w słowniku i czy kwota jest dodatnia).
VERIFICATION:
def transfer(accounts, sender, recipient, amount):
    if sender not in accounts or recipient not in accounts:
        return False
    if amount <= 0 or accounts[sender] < amount:
        return False
    accounts[sender] -= amount
    accounts[recipient] += amount
    return True

accounts = {"A": 100, "B": 40}
assert transfer(accounts, "A", "X", 30) == False
assert transfer(accounts, "A", "B", -10) == False
assert transfer(accounts, "B", "A", 100) == False
assert accounts == {"A": 100, "B": 40}
assert transfer(accounts, "A", "B", 30) == True
assert accounts == {"A": 70, "B": 70}
