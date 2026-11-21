import logging

logging.basicConfig(filename="app.log", filemode="w", level=logging.INFO, format="%(message)s")

accounts = {"1": 100.0, "2": 50.0}


def deposit(acc, amt):
    if acc not in accounts or amt <= 0:
        logging.info(f"FAIL deposit {acc} {amt} {accounts.get(acc, 0.0)}")
        return
    accounts[acc] += amt
    logging.info(f"OK deposit {acc} {amt} {accounts[acc]}")


def withdraw(acc, amt):
    if acc not in accounts or amt <= 0 or amt > accounts[acc]:
        logging.info(f"FAIL withdraw {acc} {amt} {accounts.get(acc, 0.0)}")
        return
    accounts[acc] -= amt
    logging.info(f"OK withdraw {acc} {amt} {accounts[acc]}")


deposit("1", 25.0)
withdraw("1", 10.0)
withdraw("2", 200.0)
withdraw("2", 100.0)
deposit("1", -5.0)