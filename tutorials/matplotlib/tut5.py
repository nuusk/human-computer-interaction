import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5]

sleeping =  [6,     7,      7,    9,      6]
eating =    [2,     2,      3,      1.5,        2]
studying =  [7,     8,      7,      7,      8]
playing =   [9,     7,      7,      6.5,        8]

plt.stackplot(days, sleeping, eating, studying, playing, colors=['m', 'c', 'r', 'k'])

plt.xlabel('x')
plt.ylabel('y')
plt.title('Tutorial 4')
plt.show()
