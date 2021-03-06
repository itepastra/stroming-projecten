'''
OPGAVE B
Stromingsleer en Transportverschijnselen (NS-265B)
Deadline: 17:00, 1/3/2021

Authors:
- Thijs Aarts (6716776)
- Oussama Benchikhi (6930263)
- Martijn Brouwer (6859488)
- Victor Schyns (6550517)
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys


Radius = 0.2
theta0 = 20
theta1 = 100
ks = 98e-6

dt_list = [0.01, 0.001]
dr_list = [0.04, 0.004]
colors = ['red', 'blue']
for i in range(len(dt_list)):
    dt = dt_list[i]
    dr = dr_list[i]
    
    tend = 100
    locked = False
    
    def EulerOrTheta(temps, rs, tstep=dt, k=ks, lockedr0=False):
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
                print('t =', t)
            Temps = EulerOrTheta(Temps, rs, tstep, lockedr0=lockedr0)
        return Temps
    
    print(f"\nThis should be smaller than 0.1: {ks*dt/dr**2}")
    print(f"dr = {dr} and dt = {dt}")
    rs = np.arange(0, Radius, dr)
    n = 0
    endTemps = []
    while n < 4:
        ts = np.arange(tend*n, tend*(n+1), dt)
        endTemps = ThetaInternal(rs, ts, Temps=endTemps, lockedr0=locked)
        plt.plot(rs, endTemps, color=colors[i])
        n+=1
        
    # Ontzichtbare lijnen voor de legenda
    lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors]
    labels = [f'dt = {dt_list[i]}, dr = {dr_list[i]}' for i in range(len(dt_list))]
    plt.legend(lines, labels)
    
    plt.ylabel("$\\theta$ ($\degree$C)")
    plt.xlabel("$r$ (m)")
    plt.tight_layout()
    plt.show()