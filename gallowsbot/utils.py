def units(num, cases):
    num = abs(num)
    return (
        cases[0] if num % 10 == 1 and num % 100 != 11 else
        (cases[1] if 2 <= num % 10 <= 4 and not (10 <= num % 100 < 20) else cases[2])
    )
