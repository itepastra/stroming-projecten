import numpy as np
import matplotlib.pyplot as plt
import sys


Radius = 10
theta0 = 273
theta1 = 293
ks = 0.026

dt = 0.01
dr = 0.1
tend = 100
locked = True

def EuLeRfOrThEta(temps, rs, tstep=dt, k=ks, lockedr0=False):
    newTemps = []
    for i, temp in enumerate(temps[:-1]):
        if i == 0:
            if lockedr0:
                newTemps.append(temps[0])
            else:
                newTemps.append(temps[0] + (k*tstep/(rs[1]-rs[0])**2)*(temps[1]-temps[0]))
        else:
            newTemps.append(temp + (k * tstep / (rs[i] - rs[i - 1])**2) *
                            (temps[i - 1] + temps[i + 1] - 2 * temp))
    newTemps.append(temps[-1])
    return newTemps


def ThetaInternal(rs, ts, Temps=[], tstep=dt, lockedr0=False):
    if len(Temps) == 0:
        Temps = [theta0 if i != len(rs) - 1 else theta1 for i in range(len(rs))]
    for t in ts:
        if t%1 == 0:
            print(t)
        Temps = EuLeRfOrThEta(Temps, rs, tstep, lockedr0=lockedr0)
    return Temps

print(f"this should be *much* smaller than 1: {ks*dt/dr**2}")
rs = np.arange(0, Radius, dr)
n = 0
endTemps = []
while n <= 15:
    ts = np.arange(tend*n, tend*(n+1), dt)
    endTemps = ThetaInternal(rs, ts, Temps=endTemps, lockedr0=locked)
    plt.plot(rs, endTemps)
    plt.savefig(f"{ks}-{n}_{'locked' if locked else 'free' }.png")
    n+=1