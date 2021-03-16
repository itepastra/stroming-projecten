import numpy as np
import matplotlib.pyplot as plt

U0 = 1


def Circle(origin, radius, n=1000):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return origin + radius * np.exp(1j * thetas)


circle = Circle(-0.1 + 0.22j, 1.12)

