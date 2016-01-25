from grapheneapi import GrapheneClient
import json

class Config():
    wallet_host           = "localhost"
    wallet_port           = 8090
    wallet_user           = ""
    wallet_password       = ""


if __name__ == '__main__':
    graphene = GrapheneClient(Config)

    symbol = "PEG.FAKEUSD"
    producers = ["fakeusd-feed-producer"]

    tx = graphene.rpc.update_asset_feed_producers(symbol, producers, True)
    print(json.dumps(tx, indent=4))
