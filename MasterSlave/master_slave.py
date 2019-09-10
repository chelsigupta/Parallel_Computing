from mpi4py import MPI
comm = MPI.COMM_WORLD   # Defines the default communicator

listToSort = [9,5,3,8,2,6,1,7,4,0,11,34,23]
sortedList = []
size = comm.Get_size()  # Stores the number of processes in size.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process

numSlaves = size-1
chunk_size = len(listToSort)//numSlaves
l = 0
r = chunk_size

if rank == 0: # I am the master
    print ("The list to be sorted is: ",listToSort,'\n')
    for i in range(1,size,1):
        if len(listToSort) % numSlaves!= 0 and i == size-1:
            lstChunk =  listToSort[l:]
            comm.send(lstChunk, dest=i, tag=0)
            print ("The master process is directing slave process ",i," to sort",lstChunk,'\n')
        else:
            lstChunk =  listToSort[l:r]
            print ("The master process is directing slave process ",i," to sort",lstChunk,'\n')
            comm.send(lstChunk, dest=i, tag=0)
            l += chunk_size
            r += chunk_size

    while numSlaves>0:
        lstChunk = comm.recv(source=MPI.ANY_SOURCE, tag=0)
        for i in lstChunk:
            sortedList.append(i)
        sortedList.sort()
        numSlaves -= 1
    
    print ("The sorted list is ",sortedList,'\n')
    
else: # I am a slave
    lstChunk = comm.recv(source=0, tag=0)
    print ("Slave process %s is sorting its chunk" %rank,'\n')
    lstChunk.sort()
    comm.send(lstChunk, dest=0, tag=0)
