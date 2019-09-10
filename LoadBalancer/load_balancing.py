import time
start_time = time.time()
import random
import queue
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD    # Defines the default communicator
ANY = MPI.ANY_SOURCE  

size = comm.Get_size()  # Stores the number of processes in size.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process


def fill_queue(task_queue):
	count = 0
	while(count < 5):
		i = random.randint(1,1024)
		count += 1
		task_queue.put(i)

	return task_queue


def determine_random_destination(rank, size):
	r1 = range(0,size)
	r2 = [rank]
	r = list(set(r1) - set(r2))
	dst = random.choice(r)
	return dst


task_queue = queue.Queue(maxsize=16)
task_queue = fill_queue(task_queue)

recv_task = np.zeros(1)
token = 0
recv_token = np.zeros(1)

while True:
	req_token = comm.Irecv(recv_token, source=ANY, tag=0)
	req_task = comm.Irecv(recv_task, source=ANY, tag=1)

	while req_task.Get_status()==False:
		
		if task_queue.qsize() > 7:
			random_dest = determine_random_destination(rank, size)
			if random_dest < rank:
				token = 1

			sTask = task_queue.get()		
			comm.Isend(np.array(sTask), dest=random_dest, tag=1)
		
		if task_queue.qsize() > 0:
			do_task = task_queue.get()
			time.sleep(do_task/1000)
			print('Process ',rank,' performed ',do_task,' units of work.')

		if random.randint(0, 10) < 5:
			for _ in range(2):
				x = random.randint(1,1024)
				task_queue.put(x)

		if task_queue.empty():
			comm.Isend(np.array([token]), dest=(rank+1)%size, tag=0)

			req_token.wait()
		
			if recv_token[0] == 0:
				print('Process ',rank,' all done.')
				print("--- %s seconds ---" % (time.time() - start_time))
				quit()

	print("Process ",rank," received work.")
	req_task.wait()
	task_queue.put(recv_task[0])	
