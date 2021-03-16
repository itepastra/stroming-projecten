import numpy as np
import matplotlib.pyplot as plt


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return origin + radius * np.exp(1j * thetas)


def Joukowski(b):
    return lambda z: z + b**2 / z


transformation = Joukowski(1)
circle = Circle(-0.1 + 0.22j, 1.12)
wingprofile = transformation(circle)

#plotting the circle
plt.scatter(circle.real,
            circle.imag,
            s=1,
            c=np.linspace(0, 2 * np.pi, len(circle), endpoint=False),
            cmap='gist_rainbow')
#plotting the transformation of the circle
plt.scatter(wingprofile.real,
            wingprofile.imag,
            s=1,
            c=np.linspace(0, 2 * np.pi, len(wingprofile), endpoint=False),
            cmap='gist_rainbow')
plt.axis("equal")
plt.show()