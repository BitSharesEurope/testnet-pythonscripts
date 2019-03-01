from pprint import pprint
import time
import json
import random
from grapheneapi.grapheneapi import GrapheneAPI
import threading


def run(n=0):
    client = GrapheneAPI("localhost", 8092, "", "")
    transfer = client.get_prototype_operation("transfer_operation")
    from_account = client.get_account("faucet")
    to_account = client.get_account("xeroc")
    transfer[1]["to"] = to_account["id"]
    transfer[1]["from"] = from_account["id"]
    transfer[1]["amount"]["amount"] = 3

    while True:
        builder = client.begin_builder_transaction()

        for i in range(0, random.randint(100, 500)):
            print(n, end="", flush=True)
            client.add_operation_to_builder_transaction(builder, transfer)
        client.set_fees_on_builder_transaction(builder, "1.3.0")
        print("\nTransfer!")
        client.sign_builder_transaction(builder, True)
        time.sleep(random.randint(0, 3))

for i in range(0, 10):
    threading.Thread(target=run, args=(i,)).start()
    time.sleep(random.randint(0, 10))
