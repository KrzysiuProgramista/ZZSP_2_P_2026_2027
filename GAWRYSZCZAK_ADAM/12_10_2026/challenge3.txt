CHALLENGE 3: The disappearing grades
EXPECTED: Funkcja usuwa ujemne punkty, a wyniki powyżej 100 zamienia na 100 — dla [-1, -2, 105, 80] zwraca [100, 80].
OBSERVED: Zwraca [-2, 105, 80] — ujemne -2 zostaje na liście (Bug A), a 105 nie zmienia się na 100 (Bug B).
BREAKPOINT: Na linijce if score < 0:.
FIRST WRONG STATE: scores.remove(score) przesuwa listę w lewo i pętla przeskakuje -2 (Bug A), a score = 100 nadpisuje tylko zmienną pętli zamiast elementu w liście (Bug B).
HYPOTHESIS: Modyfikowanie listy w trakcie iteracji psuje indeksy, a zmiana zmiennej pętli nie zmienia listy — trzeba zbierać poprawione wyniki do nowej listy.
VERIFICATION:
def normalize_scores(scores):
    result = []
    for score in scores:
        if score >= 0:
            if score > 100:
                score = 100
            result.append(score)
    return result

assert normalize_scores([-1, -2, 105, 80]) == [100, 80]
assert normalize_scores([]) == []
assert normalize_scores([10, 50]) == [10, 50]
assert normalize_scores([-1, 101]) == [100]
