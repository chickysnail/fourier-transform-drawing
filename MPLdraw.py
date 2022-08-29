import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib as mpl
import numpy as np


def drawing(imagePath):
    img = np.flip(plt.imread(imagePath), axis=0)
    print(img.shape)

    fig = plt.figure()
    border = 1/10
    shape = (img.shape[1], img.shape[0])
    ax = fig.add_subplot(111, xlim=[0-shape[0]*border, shape[0]+shape[0]*border], ylim=[0-shape[1]*border, shape[1]+shape[1]*border])
    ax.set_aspect('equal')
    line, = ax.plot([], [], lw=1.8)
    global arr
    arr = np.empty((0,2))
    ax.imshow(img)

    def update(x, y):
        line.set_data(x, y)
        fig.canvas.draw()

    def onclick(event):
        if event.key == ' ':
            print('done')
            plt.close(fig)
            return

        global arr
        x = event.xdata
        y = event.ydata

        if event.key == 'c':
            arr = np.empty((0,2))

        elif event.key == 'r':
            arr = arr[:-1]

        elif event.inaxes!=None:
            arr = np.append(arr, [[x, y]], axis=0)

        allx = arr.transpose()[0]
        ally = arr.transpose()[1]

        update(allx, ally)


    fig.canvas.mpl_connect('key_press_event', onclick)
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return arr.transpose()




