numbersTaken = [2, 5, 12, 13, 17]

print("Here are the numbers taken: ")
for i in range(20):
    if i in numbersTaken:
        continue
    print(i)
