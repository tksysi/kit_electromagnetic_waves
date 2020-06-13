import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def start(f, df, k1, k2, dt):
    color = ['C0', 'C0', 'C1', 'C1']
    linestyle = ['solid', 'solid', 'solid', 'dotted']

    def update(n):
        plt.cla()
        
        dx = 0.1
        xmin = 0
        xmax = 40*np.pi
        x = np.arange(xmin, xmax, dx)
        t = n%200 * dt

        offset = np.array([1, -1, -3, 1])
        y = []
        for i in range(0,len(color)):
            y.append(np.zeros_like(x, dtype = 'float64'))

        y[1] = np.sin(2*np.pi*f*t - k1*x)
        y[2] = np.cos(2*np.pi*df*t - k2*x)

        y[3] = y[2]
        y[0] = y[2] * np.sin(2*np.pi*f*t - k1*x)

        for (yy, o, c, ls) in zip(y, offset, color, linestyle):
            plt.plot(x, yy + o, color = c, linestyle = ls)

        plt.axis('off')


    fig = plt.figure(figsize = (6,3))
    ani = animation.FuncAnimation(fig, update, interval = 20, save_count=int(1/(df*dt)))
    plt.show()


if __name__ == '__main__':
    f = 10
    df = 0.5
    k1 = 1
    k2 = 0.1 * k1
    dt = 0.01
    start(f, df, k1, k2, dt)
    
    
