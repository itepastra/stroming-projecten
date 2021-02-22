#want zien jullie t dan???

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi


def temp(y, t, k):
    r,p = y
    dydt= [p, -r/k]
    return dydt


k = 1e-5

y0 = [0, 1]

t = np.linspace(0,10,101)

sol = spi.odeint(temp, y0, t, args=(k,))

plt.plot(t, sol[:, 0], 'b', label='theta(t)')

plt.plot(t, sol[:, 1], 'g', label='omega(t)')

plt.legend(loc='best')

plt.xlabel('t')

plt.grid()

plt.show()