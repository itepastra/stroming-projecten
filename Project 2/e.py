from matplotlib.backend_bases import LocationEvent
import numpy as np
import matplotlib.pyplot as plt
from numpy.ma import harden_mask

circleRadius = 1.12
circleOrigin = -0.1 + 0.22j


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
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
transformation = Joukowski(1)
wing = transformation(Circle(circleOrigin, circleRadius))

for gamma in [-2.65, -2.68, -2.72, -2.75]:
    potential = MakePotential(gamma, circleRadius, u, circleOrigin)
    Zs, data = PotentialData(potential, lower=0, upper=2.2)
    transformedZ = transformation(Zs)
    data = np.ma.array(
        data,
        mask=(np.where(
            (transformedZ.real <= 2.05) & (transformedZ.real >= 1.95) &
            (transformedZ.imag <= -0.3) & (transformedZ.imag >= 0.3), True,
            False)))
    transformedZ = np.ma.array(
        transformedZ,
        mask=(np.where(
            (transformedZ.real <= 2.05) & (transformedZ.real >= 1.95) &
            (transformedZ.imag <= -0.3) & (transformedZ.imag >= 0.3), True,
            False)))
    plt.figure()
    plt.plot(wing.real, wing.imag, color="red")
    plt.contour(transformedZ.real,
                transformedZ.imag,
                data.imag,
                levels=450,
                cmap='gist_rainbow')
    plt.xlim(1.95, 2.05)
    plt.ylim(-.3, .3)
    # plt.axis('equal')
    plt.tight_layout()
    plt.savefig(f"Einzoom_{gamma}.png")
    # plt.show()
    plt.figure()
    plt.plot(wing.real, wing.imag, color="red")
    plt.contour(transformedZ.real,
                transformedZ.imag,
                data.real,
                levels=450,
                cmap='gist_rainbow')
    plt.xlim(1.95, 2.05)
    plt.ylim(-.3, .3)
    # plt.axis('equal')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"Einzoompot_{gamma}.png")
    # plt.show()