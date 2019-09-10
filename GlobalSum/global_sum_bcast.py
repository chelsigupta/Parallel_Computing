import time
start_time = time.time()
from mpi4py import MPI
import math
import random
comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()
num = random.randint(1,5)
global_sum = 0

for i in range(0,size,1):
    rbuf = comm.bcast(num,root=i)
    global_sum += rbuf

print ('I am process ',rank,' had: ',num," global sum: ",global_sum,' time: '," %s seconds " % (time.time() - start_time),'\n')
