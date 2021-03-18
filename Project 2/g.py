import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as sp

circleRadius = 1.12
circleOrigin = -0.1 + 0.22j


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=True)
    return origin + radius * np.exp(1j * thetas)


def MakePotential(Gamma, r, U, origin):
    return lambda z: U * (z - origin) + U * r**2 / (
        z - origin) - 1j * Gamma / (2 * np.pi) * np.log(z - origin)


def Joukowski(b):
    return lambda z: z + b**2 / z


def IsInCircle(point, circleCentre, radius):
    return np.where(np.absolute(point - circleCentre) < radius, True, False)


def PotentialData(potential, Nr=2000, lower=-5, upper=5):
    x = np.linspace(lower, upper, Nr)
    y = np.linspace(-(upper - lower), upper - lower, Nr)
    xs, ys = np.meshgrid(x, y)
    Zs = xs + ys * 1j
    Ps = potential(Zs)
    return Zs, np.ma.array(Ps, mask=IsInCircle(Zs, circleOrigin, circleRadius))


u = 1
rho = 1
transformation = Joukowski(1)
circle = Circle(circleOrigin, circleRadius)
wing = transformation(circle)

for gamma in [-2.72, 5]:
    potential = MakePotential(gamma, circleRadius, u, circleOrigin)
    Zs, data = PotentialData(potential)
    #wing
    transformedZ = transformation(Zs)
    diffxt = np.diff(data, axis=1) / np.diff(transformedZ, axis=1)
    wingpress = rho / 2 * (u**2 - np.absolute(diffxt)**2)
    wingtree = sp.KDTree(np.array([(z.real, z.imag)
                                   for z in transformedZ.flatten()]))
    werrors, wpoints = wingtree.query(
        np.array([(x.real, x.imag) for x in wing]),
                         distance_upper_bound=0.1,
                         workers=-1)
    winglift = 1j * rho / 2 * sum([
        wingpress.flatten()[i]**2 *
        (transformedZ.flatten()[i + 1] - transformedZ.flatten()[i - 1]) / 2
        for i in wpoints
    ])
    print(winglift)
    plt.scatter(transformedZ.flatten()[wpoints].real,
             transformedZ.flatten()[wpoints].imag, s=np.absolute(4*wingpress.flatten()[wpoints]))
    plt.show()
    #circle
    diffx = np.diff(data, axis=1) / np.diff(Zs, axis=1)
    cylinderpress = rho / 2 * (u**2 - np.absolute(diffx)**2)
    circletree = sp.KDTree(np.array([(z.real, z.imag)
                                     for z in transformedZ.flatten()]))
    cerrors, cpoints = circletree.query(
        np.array([(x.real, x.imag) for x in circle]),
                         distance_upper_bound=0.1,
                         workers=-1)
    circlelift = 1j * rho / 2 * sum([
        cylinderpress.flatten()[i]**2 *
        (transformedZ.flatten()[i + 1] - transformedZ.flatten()[i - 1]) / 2
        for i in cpoints
    ])
    print(circlelift)
    plt.plot(transformedZ.flatten()[cpoints].real,
             transformedZ.flatten()[cpoints].imag)
    plt.show()
