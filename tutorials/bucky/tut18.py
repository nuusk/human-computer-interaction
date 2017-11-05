def calculateExp(rat, boar, demon):
    result = rat + 2*boar + 10*demon
    print("You killed\n", rat, "rats (", rat, "exp )\n", boar, "boars (", boar*2, "exp )\n", demon, "demons (", demon*10, "exp )\n")
    print("You got", result, "exp in total")

minionsData = [10, 2, 5]
#calculateExp(minionsData[0], minionsData[1], minionsData[2])
calculateExp(*minionsData)
