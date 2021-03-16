import numpy as np
import matplotlib.pyplot as plt
import sys


Radius = 0.2
theta0 = 20
theta1 = 100
ks = 103e-6

dt = 0.001
dr = 0.001
tend = 100
locked = False

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
        if Temps[0] >= 85: 
            print(t, Temps[0])
            while True:
                pass
    return Temps

print(f"this should be *much* smaller than 1: {ks*dt/dr**2}")
rs = np.arange(0, Radius, dr)
n = 0
endTemps = []
while n < 4:
    ts = np.arange(tend*n, tend*(n+1), dt)
    if len(endTemps) > 1:
        print(endTemps[0])
    endTemps = ThetaInternal(rs, ts, Temps=endTemps, lockedr0=locked)
    plt.plot(rs, endTemps)
    n+=1
    

plt.ylabel("$\\theta$ ($\degree$C)")
plt.xlabel("$r$ (m)")
plt.tight_layout()
plt.savefig(f"{ks}-{n}_{'locked' if locked else 'free' }.png")
