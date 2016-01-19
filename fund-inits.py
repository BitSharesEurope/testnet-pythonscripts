from grapheneapi import GrapheneClient
import json


class Config():
    wallet_host           = "localhost"
    wallet_port           = 8090
    wallet_user           = ""
    wallet_password       = ""

if __name__ == '__main__':
    graphene = GrapheneClient(Config)

    faucet = "faucet"
    inits = ["init0", "init1", "init2", "init3", "init4", "init5", "init6", "init7", "init8", "init9", "init10"]

    for i in inits:
        tx = graphene.rpc.transfer(faucet, i, 1000, "TEST", "", True)
        print(json.dumps(tx, indent=4))
