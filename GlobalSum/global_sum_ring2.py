import time
start_time = time.time()
from mpi4py import MPI
import math
import random
comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()
num = random.randint(1,5)
global_sum = num
rdata = num

for i in range(1,size,1):
    comm.send(rdata,dest=(rank+1)%size)
    if rank != 0:
        rdata = comm.recv(source=rank-1)
    else:
        rdata = comm.recv(source=size-1)
    global_sum += rdata

print ('I am process ',rank,' had: ',num," global sum: ",global_sum,' time: '," %s seconds " % (time.time() - start_time),'\n')
