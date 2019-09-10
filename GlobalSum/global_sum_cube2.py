import time
start_time = time.time()
from mpi4py import MPI
import math
import random
comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()
num = random.randint(1,5)


def cube(i, sendData):
	size = comm.Get_size()
	rank = comm.Get_rank()
	mask = 1
	mask = mask << i
	dest = rank ^ mask		
	#dest is the process we want to exchange the data with
	comm.send(sendData, dest=dest)
	recvData = comm.recv(source=dest)
	return recvData


global_sum = num

k = int(math.log2(size))
for i in range(0,k,1):
    rdata = cube(i,global_sum)
    global_sum += rdata

print ('I am process ',rank,' had: ',num," global sum: ",global_sum,' time: '," %s seconds " % (time.time() - start_time),'\n')
