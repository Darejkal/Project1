import random
import argparse
import math
import os
import time
import logging
logging.basicConfig(filename="/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
parser=argparse.ArgumentParser()
parser.add_argument("-n",default=3000000,type=int,required=False)
parser.add_argument("-b",default=3000,type=int,required=False)
parser.add_argument("-d",type=str,required=True)
args=vars(parser.parse_args())
n=args["n"]
page_size=args["b"]
db_dir:StopAsyncIteration=args["d"]
num_page=math.ceil(n/page_size)
wait_time=1
wait_thres=60000
while True:
    print(f"wait {wait_time}s")
    time.sleep(wait_time)
    wait_time*=2
    if wait_time==wait_thres:
        wait_thres/=2
        break
    try:
        if os.path.isfile(os.path.join(db_dir,"safe.lock")):
            break 
        else:
            continue
    except:
        continue
while True:
    print(f"wait {wait_time}s")
    time.sleep(wait_time)
    wait_time+=1
    if wait_time==wait_thres:
        wait_thres/=2
    try:
        if os.path.isfile(os.path.join(db_dir,"safe.lock")):
            break 
        else:
            continue
    except:
        continue
while True:
    p=random.randint(0,num_page-1)
    if p<num_page-1:
        i=random.randint(0,page_size-1)
    else:
        i=random.randint(0,n-num_page*(page_size-1))
    logging.info(f"Reading ({p},{i})")
    with open(os.path.join(db_dir,"db",str(p)),"r") as f:
        for j in range(i):
            next(f)
        print(next(f," ")[:-1].split(" "))
    logging.info(f"Done ({p},{i})")
    time.sleep(random.randint(0,5))