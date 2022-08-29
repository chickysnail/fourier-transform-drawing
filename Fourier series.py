import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.widgets import Slider, Button


def dft(x):
    N = x.__len__()
    print(f'there will be {N} circles')
    X = np.array([])
    for k in range(N):
        re, im = 0, 0
        for n in range(N):
            phi = (np.pi * 2 * k * n) / N
            re += x[n] * np.cos(phi)
            im -= x[n] * np.sin(phi)
        re /= N
        im /= N

        freq = k
        amp = np.sqrt(re ** 2 + im ** 2)
        phase = np.arctan2(im, re)
        X = np.append(X, {'freq': freq, 'amp': amp, 'phase': phase})
    return X


fig = plt.figure()

# circle:
# x = 100*np.cos(np.arange(0, np.pi*2, 0.1))
# y = 100*np.sin(np.arange(0, np.pi*2, 0.1))

# custom:
data = np.loadtxt('coordinates/fourier_image_coords.txt')
x = data[0]-100
y = data[1]-100

amp_sort = lambda el: -el['amp']
fourierY = np.array(sorted(dft(y), key=amp_sort))
fourierX = np.array(sorted(dft(x), key=amp_sort))

num = fourierY.__len__()
# FOR NEXT LINE: lowering the amount of circles
# num = num-5
print(num)

ax = fig.add_subplot(111)
# ax = fig.add_subplot(111, xlim=[-15000, 15000], ylim=[-15000, 15000])
ax.set_aspect('equal')
plt.axis('off')

axcolor = 'lightgoldenrodyellow'
axWidth = plt.axes([0.15, 0.08, 0.6, 0.03], facecolor=axcolor)
axHeight = plt.axes([0.15, 0.03, 0.6, 0.03], facecolor=axcolor)

xSlide = Slider(axWidth, 'width', 0, 5000, valinit=213)
ySlide = Slider(axHeight, 'height', 0, 5000, valinit=230)
width = xSlide.val
height = ySlide.val
ax.set_xlim([-width, width])
ax.set_ylim([-height, height])

line1, = ax.plot([], [], lw=1)
line2, = ax.plot([], [], lw=1)
wave, = ax.plot([], [], lw=1)

wavex = np.array([])
wavey = np.array([])

mk_circle = lambda: plt.Circle((0, 0), 100, color=(0.1, 0.1, 0.1), fill=False,
                               linewidth=0.1)
circle_list = np.array([[mk_circle() for _ in range(num)],
                        [mk_circle() for _ in range(num)]])
for axis in range(2):
    fourier = fourierY
    if axis:
        fourier = fourierX
    for i in range(num):
        circle_list[axis][i].set_radius(fourier[i]['amp'])
        ax.add_artist(circle_list[axis][i])

time = 0
dt = np.pi * 2 / fourierY.__len__()

x1 = np.array([-120])
y1 = np.array([-120])
moveX1 = x1[0]
moveY1 = y1[0]

x2 = np.array([120])
y2 = np.array([120])
moveX2 = x2[0]
moveY2 = y2[0]


def update(val):
    width = xSlide.val
    height = ySlide.val
    ax.set_xlim([-width, width])
    ax.set_ylim([-height, height])


resetax = plt.axes([0.85, 0.025, 0.1, 0.04])
button = Button(resetax, 'Update', color=axcolor)
button.on_clicked(update)


def epiCycles(x, y, rotation, fourier, axis):
    xarr, yarr = np.array([x]), np.array([y])

    for i in range(num):
        circle_list[axis][i].set_center((x, y))

        freq = fourier[i]['freq']
        radius = fourier[i]['amp']
        phase = fourier[i]['phase']
        x = (radius * np.cos(freq * time + phase + rotation)) + x
        y = (radius * np.sin(freq * time + phase + rotation)) + y
        xarr, yarr = np.append(xarr, x), np.append(yarr, y)

    return xarr, yarr


def animate(t):
    global wavex, wavey, time
    global x1, x2, y1, y2
    time += dt
    if time > np.pi * 2:
        wavex = np.array([])
        wavey = np.array([])
        time = 0

    x1, y1 = epiCycles(moveX1, moveY1, (np.pi / 2), fourierY, 0)
    x2, y2 = epiCycles(moveX2, moveY2, 0, fourierX, 1)

    wavex = np.append(x2[-1], wavex)
    wavey = np.append(y1[-1], wavey)

    x2 = np.append(x2, wavex[0])
    y1 = np.append(y1, wavey[0])
    y2 = np.append(y2, y1[-1])
    x1 = np.append(x1, x2[-1])

    line1.set_data(x1, y1)
    line2.set_data(x2, y2)
    wave.set_data(wavex, wavey)


interval = 1
anim = animation.FuncAnimation(fig, animate, interval=interval)

save = True
show = False

#Here saving the results
if save:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    anim.save('results/letovo_medium_res.gif', writer=writer)

#here to display
if show:
    plt.show()
