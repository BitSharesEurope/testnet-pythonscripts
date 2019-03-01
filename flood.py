import threading
import time
import json
import random
from grapheneapi.grapheneapi import GrapheneAPI


def run(n=0):
    client = GrapheneAPI("localhost", 8092, "", "")
    while True:
        for i in range(0, random.randint(1, 100)):
            print(n, end="", flush=True)
            client.transfer("faucet", "init0", "0.00007", "TEST", "", True)
        time.sleep(random.randint(0, 3))

for i in range(0, 50):
    threading.Thread(target=run, args=(i,)).start()
