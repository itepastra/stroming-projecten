from matplotlib.backend_bases import LocationEvent
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp

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
circle = Circle(circleOrigin, circleRadius)
wing = transformation(circle)

for gamma in [-2.72, 5]:
    potential = MakePotential(gamma, circleRadius, u, circleOrigin)
    Zs, data = PotentialData(potential)
    transformedZ = transformation(Zs)
    diffxt = np.diff(data, axis=1)/np.diff(transformedZ, axis=1)
    plt.figure()
    plt.plot(wing.real, wing.imag, color="red")
    plt.contour(transformedZ.real[:,:-1], transformedZ.imag[:,:-1], np.absolute(diffxt), levels=90)
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    # plt.axis('equal')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"F-wing_{gamma}.png")
    diffx = np.diff(data, axis=1)/np.diff(Zs, axis=1)
    plt.figure()
    plt.plot(circle.real, circle.imag, color="red")
    plt.contour(Zs.real[:,:-1], Zs.imag[:,:-1], np.absolute(diffx), levels=90)
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    # plt.axis('equal')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"F-cyl_{gamma}.png")
