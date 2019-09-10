import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation


def generateOrganism():
    org = random.random()
    if org > 0.2: return 0
    return 1


def survival(x, y, world):
    num_neighbours = np.sum(world[x - 1 : x + 2, y - 1 : y + 2]) - world[x, y]
    # The rules of Life
    if (world[x, y] == 1) and (num_neighbours not in (2,3)):
        return 0
    elif num_neighbours == 3:
        return 1
    return world[x, y]


def generation(world):
    new_world = np.copy(world)
    # Apply the survival function to every cell in the universe
    for i in range(0,len(world),1):
        for j in range(0,len(world[i]),1):
            new_world[i, j] = survival(i, j, world)
    return new_world


world = np.zeros((1024, 1024))
for i in range(0,len(world),1):
        for j in range(0,len(world[i]),1):
            world[i,j] = generateOrganism()

fig = plt.figure()
ims = []
for i in range(4):
    im = plt.imshow(world, cmap='binary')
    ims.append([im])
    world = generation(world)

ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=10)
ani.save("game_of_life.gif", writer="imagemagick")
