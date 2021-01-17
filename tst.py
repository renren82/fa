
for x in range(0, 10000):
    if x % 2 == 0:
        x1 = x/2
    else:
        x1 = x + 3

    if x1 % 2 == 0:
        x2 = x1 / 2
    else:
        x2 = x1 + 3

    if x2 % 2 == 0:
        x3 = x2 / 2
    else:
        x3 = x2 + 3

    if x == x3:
        print(x)


