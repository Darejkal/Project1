import random
import argparse
import math
import os
import time
import json
parser=argparse.ArgumentParser()
parser.add_argument("-n",default=3000000,type=int,required=False)
parser.add_argument("-b",default=1000,type=int,required=False)
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
        break
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
    print(f"Reading ({p},{i})")
    with open(os.path.join(db_dir,"db",str(p)),"r") as f:
        for j in range(i):
            next(f)
        print(f"Read {json.loads(f.readline())[1:5]}...")
    time.sleep(random.randint(0,5))