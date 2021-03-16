from matplotlib.backend_bases import LocationEvent
import numpy as np
import matplotlib.pyplot as plt

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


def PotentialData(potential, Nr=2000):
    k = np.linspace(-5, 5, Nr)
    xs, ys = np.meshgrid(k, k)
    Zs = xs + ys * 1j
    Ps = potential(Zs)
    return Zs, np.ma.array(Ps, mask=IsInCircle(Zs, circleOrigin, circleRadius))


u = 1
transformation = Joukowski(1)
wing=transformation(Circle(circleOrigin, circleRadius))

for gamma in [0, -3]:
    potential = MakePotential(gamma, circleRadius, u, circleOrigin)
    Zs, data = PotentialData(potential)
    transformedZ = transformation(Zs)
    plt.figure()
    plt.scatter(wing.real, wing.imag, color="red")
    plt.contour(transformedZ.real,
                 transformedZ.imag,
                 data.imag,
                 levels=500,
                 cmap='gist_rainbow')
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    # plt.axis('equal')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"C_{gamma}")
    # plt.show()