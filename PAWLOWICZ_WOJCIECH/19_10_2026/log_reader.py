"""
log_reader.py

Reads bank_app.log (produced by bank_audit.py) and prints:
  - how many operations succeeded and how many failed,
  - the total amount deposited,
  - the account with the most failed operations.
"""

import re
from collections import Counter

LOG_FILE = "bank_app.log"

LINE_RE = re.compile(
    r"^(?P<ts>\S+ \S+) \[(?P<level>\w+)\] "
    r"(?P<status>SUCCESS|FAILED) (?P<action>deposit|withdrawal): "
    r"account=(?P<account>\S+) amount=(?P<amount>[-\d.]+) balance=(?P<balance>[-\d.]+)"
)


def analyze(path: str = LOG_FILE) -> None:
    succeeded = 0
    failed = 0
    total_deposited = 0.0
    failures_by_account = Counter()

    with open(path, "r") as fh:
        for line in fh:
            match = LINE_RE.search(line)
            if not match:
                continue

            status = match.group("status")
            action = match.group("action")
            account = match.group("account")
            amount = float(match.group("amount"))

            if status == "SUCCESS":
                succeeded += 1
                if action == "deposit":
                    total_deposited += amount
            else:
                failed += 1
                failures_by_account[account] += 1

    print(f"Successful operations: {succeeded}")
    print(f"Failed operations:     {failed}")
    print(f"Total amount deposited: {total_deposited}")

    if failures_by_account:
        account, count = failures_by_account.most_common(1)[0]
        print(f"Account with most failed operations: {account} ({count} failures)")
    else:
        print("Account with most failed operations: none (no failures logged)")


if __name__ == "__main__":
    analyze()
