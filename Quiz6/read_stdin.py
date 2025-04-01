#!/usr/bin/env python3
#Updated Read_stdin for hyperloglog

import sys
import time
import hashlib
import hyperloglog

# Initialize HyperLogLog with a small error rate for precise counting
hll = hyperloglog.HyperLogLog(0.01)
interval = 5

start_time = time.time()

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break

    try:
        sender_name = line.split(", sender ")[1].split(" ")[0]
    except IndexError:
        continue 

    hll.add(sender_name)

    current_time = time.time()
    elapsed_time = int(current_time - start_time) 

    if elapsed_time % interval == 0:
        estimated_users = len(hll)
        print(f"Elapsed time: {elapsed_time}s, Estimated unique users: {estimated_users}")
        
        time.sleep(1)
