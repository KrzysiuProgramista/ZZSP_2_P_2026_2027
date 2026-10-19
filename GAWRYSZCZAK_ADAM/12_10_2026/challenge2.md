CHALLENGE 2: Stop at the one bad record
EXPECTED: Pętla przechodzi przez wszystkie 1000 rekordów i pomija uszkodzony rekord bez wywalania błędu.
OBSERVED: Program wysypuje się przy i == 737 z błędem TypeError, bo próbuje wykonać None + 1.
BREAKPOINT: Warunkowy breakpoint na linijce adjusted = record["value"] + 1 z warunkiem i == 737.
FIRST WRONG STATE: Linijka records[737]["value"] = None ustawia brak wartości, przez co dla i == 737 wyrażenie record["value"] + 1 próbuje dodać 1 do None.
HYPOTHESIS: Kod zakłada, że "value" to zawsze liczba — przed dodaniem 1 trzeba sprawdzić, czy record["value"] nie jest None.
VERIFICATION:
records = [
    {"id": i, "value": i * 2}
    for i in range(1000)
]
records[737]["value"] = None

for i, record in enumerate(records):
    if record["value"] is not None:
        adjusted = record["value"] + 1

assert records[737]["value"] is None
assert records[0]["value"] + 1 == 1
