import numpy as np
from instance.utils import simulateRgb


def points(num):
    # x = np.random.choice(range(100, 200), 1000)
    # y = np.random.choice(range(30, 120), 1000)
    x = np.random.randint(700, 2000, num)
    y = np.random.randint(300, 1200, num)
    # out = np.zeros_like(x)
    z = np.array(list(zip(x, y)))
    # mappings
    m = [{'speed': i[0], 'torque': i[1]} for i in z]
    return m


if __name__ == '__main__':
    num, r = (10325, 50)
    p = points(num)
    print('p', len(p))
    positions = simulateRgb(p, r)
    print('positions', len(positions))
    # self.assertIsNone(positions)
