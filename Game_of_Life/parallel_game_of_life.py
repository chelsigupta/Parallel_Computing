import time
start_time = time.time()
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from mpi4py import MPI
comm = MPI.COMM_WORLD    # Defines the default communicator


def generate_organism():
	org = random.random()
	if org > 0.2: 
		return 0
	return 1


def init_world():
	world = np.zeros((1024, 1024))
	for i in range(0,len(world),1):
		for j in range(0,len(world[i]),1):
			world[i,j] = generate_organism()
	return world


def give_chunk(data, chunk_no, size):
	lower_index= (chunk_no-1)*(len(data)//size)
	upper_index= chunk_no*(len(data)//size) -1
	if(chunk_no>1):
		lower_index-=1
	if(chunk_no<size):
		upper_index+=1

	return data[lower_index:upper_index+1]	


def survival(x, y, world):
	num_neighbours = np.sum(world[x - 1 : x + 2, y - 1 : y + 2]) - world[x, y]
	# The rules of Life
	if (world[x, y] == 1) and (num_neighbours not in (2,3)):
		return 0
	elif num_neighbours == 3:
		return 1
	return world[x, y]


def generation(world,rank,size):
	new_world = np.copy(world)
	# Apply the survival function to every cell in the universe
	for i in range(0,len(world),1):
		for j in range(0,len(world[i]),1):
			new_world[i, j] = survival(i, j, world)

	lower_index= 0
	upper_index= len(world)-1
	if(rank>1):
		lower_index=1
	if(rank<size-1):
		upper_index-=1
	
	return new_world[lower_index:upper_index+1]


size = comm.Get_size()  # Stores the number of processes in size.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process

if rank == 0:
	fig = plt.figure()
	ims = []
	world=init_world()
	im =plt.imshow(world, cmap='binary')
	ims.append([im])
	for iii in range(100):
		for i in range(1,size):
			chunk=give_chunk(world,i,size-1)
			comm.send(chunk,dest=i)
		
		world=[]		
		for i in range(1,size):
			chunk=comm.recv(source=i)
			world.append(chunk)			

		world = np.vstack(world)
		im =plt.imshow(world, cmap='binary')
		ims.append([im])
	ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=10)
	ani.save("Parallel_gof.gif", writer="imagemagick")
	print("--- %s seconds ---" % (time.time() - start_time))

else:
	for iii in range(100):
		chunk=comm.recv(source=0)
		chunk=generation(chunk,rank,size)
		comm.send(chunk,dest=0)
