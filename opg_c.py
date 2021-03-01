import numpy as np
import matplotlib.pyplot as plt
import sys


Radius = 0.2
theta0 = 10
theta1 = 100
ks = 100e-4

dt = 0.0001
dr = 0.01

locked = True

Fo = np.array([0.05, 0.1, 1.0])
targetTs = (Fo*Radius**2)/ks

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
        if t%10 == 0:
            print(t)
        Temps = EuLeRfOrThEta(Temps, rs, tstep, lockedr0=lockedr0)
        
    return Temps

print(targetTs)
print(f"this should be *much* smaller than 1: {ks*dt/dr**2}")
rs = np.arange(0, Radius, dr)
endTemps = []
for t in targetTs:
    ts = np.arange(0, t, dt)
    endTemps = ThetaInternal(rs, ts, Temps=endTemps, lockedr0=locked)
    plt.plot(rs/Radius, (np.array(endTemps)-theta0)/(theta1-theta0))
    
plt.ylabel("$\\theta$ ($\degree$C)")
plt.xlabel("$r$ (m)")
plt.tight_layout()

plt.savefig(f"{theta0}-{theta1}_{ks}-{round(t, 3)}_{'locked' if locked else 'free' }.png")