import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import random


x = np.arange(-10, 11, 1)
y = np.random.uniform(-10, 10, size=len(x))
cs = CubicSpline(x, y)

#cs_vals = cs(x)

plt.plot(x, y, 'o', label='real data')

step = 0.01
start = -10
end = 10
cur_point = start
cs_x = []
cs_y = []
while cur_point <= end:
    cs_x.append(cur_point)
    cs_y.append( cs(cur_point) * random.uniform(0.95, 1.05) )
    cur_point += step
plt.plot(cs_x, cs_y, label='Cubic Spline')
plt.legend()
plt.savefig('cubic_spline_example.png')
print(len(x), len(cs_x), len(cs_y))