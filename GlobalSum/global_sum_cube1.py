import time
start_time = time.time()
from mpi4py import MPI
import math
import random
comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()
num = random.randint(1,5)
rdata = 0


def cube(i):
	size = comm.Get_size()
	rank = comm.Get_rank()
	mask = 1
	mask = mask << i
	dest = rank ^ mask		
	#dest is the process we want to exchange the data with
	return dest


global_sum = num
k = int(math.log2(size))

for i in range(0,k,1):
    dest = cube(i)
    if dest < rank:
       comm.send(global_sum, dest=dest)
    else:
       rdata = comm.recv(source=dest)
       global_sum += rdata

for i in range(k-1,-1,-1):
    dest = cube(i)
    if dest > rank:
       comm.send(global_sum, dest=dest)
    else:
       rdata = comm.recv(source=dest)
       global_sum = rdata

print ('I am process ',rank,' had: ',num," global sum: ",global_sum,' time: '," %s seconds " % (time.time() - start_time),'\n')
