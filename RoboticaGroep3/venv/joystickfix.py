def test(x):
    x2 = round((x/100))
    if x2 < 8:
        x = x * 0,639375
    elif x2 > 8:
        x = (0,43597263 * (x - 800)) + 511,5
    else:
        x = 511,5
    return x










