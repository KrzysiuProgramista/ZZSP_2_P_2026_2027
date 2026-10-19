CHALLENGE 1: Two largest distinct values
EXPECTED: Funkcja zwraca dwie największe różne liczby — dla [10, 12, 11, 15] wynikiem jest (15, 12).
OBSERVED: Dla [10, 12, 11, 15] zwraca (15, 11), gubiąc 12, a dla [5, 5, 4] daje (5, 5) zamiast (5, 4).
BREAKPOINT: Na linijce if n > largest:.
FIRST WRONG STATE: Gdy n = 12 (a potem 15), linijka largest = n nadpisuje stare maksimum bez przepisania go wcześniej do second, a startowe second = numbers[0] blokuje zmianę, gdy największa liczba jest na początku listy.
HYPOTHESIS: Przy znalezieniu nowego maksimum trzeba najpierw przepisać stare largest do second, zacząć od -inf i sprawdzać n != largest.
VERIFICATION:
def two_largest(numbers):
    largest = float("-inf")
    second = float("-inf")
    for n in numbers:
        if n > largest:
            second = largest
            largest = n
        elif n > second and n != largest:
            second = n
    return largest, second

assert two_largest([10, 12, 11, 15]) == (15, 12)
assert two_largest([3, 9, 1, 7]) == (9, 7)
assert two_largest([5, 5, 4]) == (5, 4)
assert two_largest([-8, -2, -4]) == (-2, -4)
