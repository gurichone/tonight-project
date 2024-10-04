# num1/num2をdigit桁で返す
def divide_round(num1, num2, digit):
    num1 *= 10 ** digit
    if (num1 / num2 - num1 // num2) >= 0.5:
        up = True
    else:
        up = False
    ans = num1 // num2
    if up:
        ans += 1
    ans /= 10 ** digit
    return ans