import matplotlib.pyplot as plt

x = [2, 4, 6, 8, 10]
y = [6, 5, 4, 7, 3]

x2 = [1, 3, 5, 7, 9]
y2 = [7, 5, 1, 6, 8]

plt.bar(x, y, label='Bars', color='#ab2434')
plt.bar(x2, y2, label='Bars2', color='#34adad')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Tutorial 3')

plt.legend()
plt.show()
