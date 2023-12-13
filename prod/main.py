import random
import argparse
import math
import os
import json
import multiprocessing
import time
parser=argparse.ArgumentParser()
parser.add_argument("-n",default=3000000,type=int,required=False)
parser.add_argument("-b",default=1000,type=int,required=False)
parser.add_argument("-d",type=str,required=True)
args=vars(parser.parse_args())
n=args["n"]
page_size=args["b"]
db_dir:StopAsyncIteration=args["d"]
safe_lock=os.path.join(db_dir,"safe.lock")
if os.path.isfile(safe_lock):
    exit()
pop=[i for i in range(n)]
num_page=math.ceil(n/page_size)
os.makedirs(os.path.join(db_dir,"db"),exist_ok=True)
last_arr=list(map(int,next(os.walk(os.path.join(db_dir,"db")))[2]))
if  last_arr:
    lastp=max(last_arr)
    lasti=len(list(open(os.path.join(db_dir,"db",str(lastp)),"r+")))
else:
    lastp,lasti=0,0
del last_arr
class Sampler:
    def __init__(self,worker_num,sampler,*args) -> None:
        self.queue=multiprocessing.Queue(maxsize=20)
        self.workers=[]
        for _ in range(worker_num):
            self.workers.append(multiprocessing.Process(target=sampler,args=(self.queue,*args),daemon=True))
            self.workers[-1].start()
    def next(self):
        return self.queue.get(block=True)
    def close(self):
        for p in self.workers:
            p.terminate()
            p.join()
print(f"Starting from ({lastp},{lasti})")
def rand_arr(queue:multiprocessing.Queue):
    while True:
        leg=random.randint(100,10000)
        arr=random.choices(pop,k=leg)
        queue.put(json.dumps(arr)+"\n")
sampler=Sampler(4,rand_arr)
with open(os.path.join(db_dir,"db",str(lastp)),"a") as file:
    for i in range(lasti,page_size):
        file.write(sampler.next())
    file.close()
for p in range(lastp+1,num_page):
    print(f"Gen page {p}")
    file=open(os.path.join(db_dir,"db",str(p)),"a")
    for i in range(0,page_size):
        file.write(sampler.next())
    file.close()
sampler.close()
with open(safe_lock,"a") as file:
    file.write("0")