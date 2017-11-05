from random import *

numbers = []

def beef():
    #print("running a function...")
    #print(int(random() * 3) + 2)
    numbers.append(int(random() * 3) + 2)

for i in range(20):
    beef()

for i in range(len(numbers)):
    if i in numbers:
        print(i)
