import numpy as np
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(100)

Radius = 10
theta0 = 273
theta1 = 293
ks = 1e-4

dt = 0.01
dr = 0.001
tend = 100


def EuLeRfOrThEta(temps, rs, tstep=dt, k=ks):
    newTemps = []
    for i, temp in enumerate(temps[:-1]):
        if i == 0:
            newTemps.append(temps[0])
        else:
            newTemps.append(temp + (k * tstep / (rs[i] - rs[i - 1])**2) *
                            (temps[i - 1] + temps[i + 1] - 2 * temp))
    newTemps.append(temps[-1])
    return newTemps


def ThetaInternal(rs, ts, Temps=[], tstep=dt):
    if len(Temps) == 0:
        Temps = [theta0 if i != len(rs) - 1 else theta1 for i in range(len(rs))]
    for _ in ts:
        Temps = EuLeRfOrThEta(Temps, rs, tstep)
    return Temps


rs = np.arange(0, Radius, dr)
ts = np.arange(0, tend, dt)
endTemps = ThetaInternal(rs, ts)

plt.plot(rs, endTemps)
plt.show()
