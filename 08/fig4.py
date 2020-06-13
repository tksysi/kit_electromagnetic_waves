import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def start(f, df, k1, k2, dt):
    color = ['C0', 'C2', 'C3', 'C1']

    def update(n):
        plt.cla()
        
        dx = 0.1
        xmin = 0
        xmax = 40*np.pi
        x = np.arange(xmin, xmax, dx)
        t = n%(2/(df*dt)) * dt

        offset = np.array([-1, -3, -5, 1])
        y = []
        for i in range(0,len(color)):
            y.append(np.zeros_like(x, dtype = 'float64'))

        for j in range(0,len(color)-1):
            m = 2*j + 1
            y[j] = np.sin(2*np.pi*(m**1.1)*df*t - m*k2*x) / m
            y[len(color)-1] += y[j]

        for (yy, o, c) in zip(y, offset, color):
            plt.plot(x, yy + o, color = c)

        plt.axis('off')


    fig = plt.figure(figsize = (6,3))
    ani = animation.FuncAnimation(fig, update, interval = 20, save_count=int(2/(df*dt)))
    plt.show()


if __name__ == '__main__':
    f = 10
    df = 0.5
    k1 = 1
    k2 = 0.1 * k1
    dt = 0.01
    start(f, df, k1, k2, dt)
    
    
