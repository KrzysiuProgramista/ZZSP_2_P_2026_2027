ok = 0
fail = 0
deposited = 0.0
fails = {}

with open("app.log") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 5 or parts[0] not in ("OK", "FAIL"):
            continue
        status, op, acc, amt, bal = parts
        amt = float(amt)
        if status == "OK":
            ok += 1
            if op == "deposit":
                deposited += amt
        elif status == "FAIL":
            fail += 1
            fails[acc] = fails.get(acc, 0) + 1

print("Succeeded:", ok)
print("Failed:", fail)
print("Total deposited:", deposited)
print("Most failed account:", max(fails, key=fails.get) if fails else "None")