def addNumbers(*args):
    sum = 0
    sentence = ''
    for i in args:
        sum += i
        sentence += str(i) + " + "
    print(sentence[:-1], "=", sum)

addNumbers(50, 6, 4, 2)
