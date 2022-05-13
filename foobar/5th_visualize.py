import matplotlib.pyplot as plt


sqrt2 = 2**(1./2)
x = range(30)
y = [sqrt2*i/2 for i in range(50)]
z = [(2-sqrt2)*i/2 for i in range(100)]

plt.scatter(x, [0]*len(x), marker='^', color='g', s=0.001, label='sqrt2') 
plt.scatter(y, [0]*len(y), marker='o', color='r', s=0.001, label='sqrt2') 
plt.scatter(z, [0]*len(z), marker='x', color='b', s=0.001, label='2-sqrt2') 
plt.ylim(-0.0001, 0.0001)
plt.savefig('visualize.pdf')