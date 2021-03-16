from matplotlib.backend_bases import LocationEvent
import numpy as np
import matplotlib.pyplot as plt

U0 = 1


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return origin + radius * np.exp(1j * thetas)


def MakePotential(Gamma, r, U):
    return lambda z: U * z + U * r**2 / z -1j * Gamma / (2 * np.pi) * np.log(z)


def MakeStreamPlot(potential, r, Nr=2000, Name=0):
    k = np.linspace(-3, 3, Nr)
    xs, ys = np.meshgrid(k, k)
    Zs = xs + ys * 1j
    Ps = potential(Zs)
    Ps2 = np.ma.array(Ps, mask=np.where(np.absolute(Zs) > r, False, True))
    plt.figure()
    plt.contourf(Zs.real, Zs.imag, Ps2.imag, levels=50,cmap='gist_rainbow')
    plt.axis('equal')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"gamma-{Name}")

r = 1
u = 1

for gamma in [0, -3, -5, -69]:
    potential = MakePotential(gamma, r, u)
    MakeStreamPlot(potential, r, Name=gamma)