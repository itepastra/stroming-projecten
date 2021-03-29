import scipy.integrate as spint
import numpy as np
import matplotlib.pyplot as plt 

k = 1
Ra = 1
Pr = 1

s = Pr
r = Ra*k**2/(k**2+np.pi**2)**3
b = 4*np.pi**2/(k**2+np.pi**2)


def DiffEqs(s, r, b):
    return lambda t,V: (s * (V[1] - V[0]), r * V[0] - V[1] - V[0] * V[2], V[0]
                         * V[1] - b * V[2])


t = np.array((0,20))
tau = t * (k**2 + np.pi**2)
ts = np.linspace(t[0], t[1], 200)
taus = np.linspace(tau[0], tau[1], 200)

V0 = [1,1,1]

sol = spint.solve_ivp(DiffEqs(s,r,b),tuple(tau), V0, dense_output=True)

continousSol = sol.sol
ys = continousSol(taus)

plt.plot(ts, ys[0], ys[1], ys[2])
plt.legend()
plt.show()