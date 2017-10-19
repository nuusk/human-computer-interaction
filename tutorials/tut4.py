import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [5, 4, 6, 7, 3, 7, 1, 5]


plt.scatter(x, y, label='skitscat', color='k', marker='x')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Tutorial 4')
plt.legend()
plt.show()
