from mpi4py import MPI
import math
import random
comm = MPI.COMM_WORLD


def cube(i, sendData):
	size = comm.Get_size()
	rank = comm.Get_rank()
	mask = 1
	mask = mask << i
	dest = rank ^ mask		
	#dest is the process we want to exchange the data with
	comm.send(sendData, dest=dest)
	recvData = comm.recv(source=dest)
	return recvData, dest


def compare_ascending(rank,dst,rdata,rbuf):
	if(rank<dst and rdata<rbuf): 	
	#rdata is the data process received and rbuf is the data it has right now
		rbuf = rdata
	if(rank>dst and rdata>rbuf):
		rbuf = rdata
	return rbuf


def compare_descending(rank,dst,rdata,rbuf):
	if(rank<dst and rdata>rbuf): 	
	#rdata is the data process received and rbuf is the data it has right now
		rbuf = rdata
	if(rank>dst and rdata<rbuf):
		rbuf = rdata
	return rbuf


size = comm.Get_size()
rank = comm.Get_rank()
ListtoSort = []
if rank == 0:
	ListtoSort = random.sample(range(100), size)
	print ("The list to be sorted is: ",ListtoSort,"\n")
rbuf = comm.scatter(ListtoSort,root=0)

k = int(math.log2(size))
for i in range(0,k,1):
	for j in range(i,-1,-1):
		rdata,dst = cube(j,rbuf)
		x = 2**(i+1)
		if (rank//x)%2 == 0:
			rbuf = compare_ascending(rank,dst,rdata,rbuf)
		else:
			rbuf = compare_descending(rank,dst,rdata,rbuf)
		comm.Barrier()

sortedList = comm.gather(rbuf,root=0)
if rank == 0:
	print ("The sorted list is: ",sortedList,'\n')
