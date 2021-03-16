import numpy as np
import matplotlib.pyplot as plt


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0,2*np.pi,n, endpoint=False)
    return origin + radius*np.exp(1j*thetas)

def Joukowski(b):
    return lambda z : z + b**2/z

transformation = Joukowski(1)
circle = Circle(-0.1 + 0.22j, 1.12)
wingprofile = transformation(circle)

plt.scatter(wingprofile.real, wingprofile.imag)
plt.axis("equal")
plt.show()