import random
import argparse
import math
import os
import json
import multiprocessing
import time
import logging 
logging.basicConfig(filename="/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
parser=argparse.ArgumentParser()
# number of array
parser.add_argument("-n",default=3000000,type=int,required=False)
# array per file
parser.add_argument("-b",default=1000,type=int,required=False)
# DB_DIR
parser.add_argument("-d",type=str,required=True)
# number of worker
parser.add_argument("-w",default=10,type=int,required=False)
args=vars(parser.parse_args())

n=args["n"]
page_size=args["b"]
db_dir=args["d"]

safe_lock=os.path.join(db_dir,"safe.lock")
if os.path.isfile(safe_lock):
    exit()
pop=[i for i in range(n)]
num_page=math.ceil(n/page_size)
os.makedirs(os.path.join(db_dir,"db"),exist_ok=True)
class DBSampler:
    flag=False
    def __init__(self,worker_num,path,p_num,p_size) -> None:
        self.workers=[]
        worker_step=math.ceil(p_num/worker_num)
        for i in range(worker_num-1):
            self.workers.append(multiprocessing.Process(target=DBSampler.gen,args=(path,i*worker_step,(i+1)*worker_step,p_size),daemon=False))
            self.workers[-1].start()
        self.workers.append(multiprocessing.Process(target=DBSampler.gen,args=(path,p_num-worker_step,p_num,p_size),daemon=False))
        self.workers[-1].start()
    def close(self):
        for p in self.workers:
            p.terminate()
            p.join()
    @staticmethod
    def gen(path:str,begin:int,end:int,pageSize:int):
        for i in range(begin,end):
            logging.info(f"gen {i}")
            _p=os.path.join(path,str(i))
            last=0
            if os.path.isfile(_p):
                with open(_p,"r") as f:
                    for _ in f:
                        last+=1
            f=open(_p,"a")
            for _ in range(last,pageSize):
                leg=random.randint(100,10000)
                arr=random.choices(pop,k=leg)
                f.write(json.dumps(arr)+"\n")
            f.close()
            logging.info(f"done {i}")
sampler=DBSampler(args["w"],os.path.join(db_dir,"db"),num_page,page_size)
for i,worker in enumerate(sampler.workers):
    worker.join()
    print(f"Worker {i} has already done!")
with open(safe_lock,"a") as file:
    file.write("0")