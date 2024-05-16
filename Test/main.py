# main.py
from multiprocessing import Process, Queue
from server.write_data import Stage1
from server.read_data import Stage2

s1 = Stage1()
s2 = Stage2()

# S1 to S2 communication
queueS1 = Queue()  # s1.stage1() writes to queueS1

# S2 to S1 communication
queueS2 = Queue()  # s2.stage2() writes to queueS2

# start s2 as another process
s2 = Process(target=s2.stage2, args=(queueS1, queueS2))
s2.daemon = True
s2.start()  # Launch the stage2 process

s1.stage1(queueS1, queueS2)  # start sending stuff from s1 to s2
s2.join()  # wait till s2 daemon finishes