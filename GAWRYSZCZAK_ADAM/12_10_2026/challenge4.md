CHALLENGE 4: The same room is booked twice
EXPECTED: Każdy dzień ma własny słownik i listę, więc rezerwacja sali "A" w "Mon" nie rezerwuje jej w "Tue".
OBSERVED: Po dopisaniu "10:00" do poniedziałku, godzina pojawia się też we wtorek, a schedule["Mon"] is schedule["Tue"] w Watch daje True.
BREAKPOINT: Na linijce schedule["Mon"]["A"].append("10:00").
FIRST WRONG STATE: W drugim obrocie pętli (day = "Tue") linijka schedule[day] = empty_day przypisuje wtorkowi ten sam słownik empty_day, który wcześniej dostał poniedziałek.
HYPOTHESIS: empty_day jest tworzony raz przed pętlą — wystarczy przenieść tę linijkę do środka pętli for, żeby każdy dzień dostawał nowy słownik.
VERIFICATION:
def create_schedule(days, rooms):
    schedule = {}
    for day in days:
        empty_day = {room: [] for room in rooms}
        schedule[day] = empty_day
    return schedule

schedule = create_schedule(["Mon", "Tue"], ["A"])
schedule["Mon"]["A"].append("10:00")
assert schedule["Mon"]["A"] == ["10:00"]
assert schedule["Tue"]["A"] == []
assert (schedule["Mon"] is schedule["Tue"]) == False
