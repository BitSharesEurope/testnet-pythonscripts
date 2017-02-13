from grapheneapi.grapheneapi import GrapheneAPI
import json

class Config():
    wallet_host           = "localhost"
    wallet_port           = 8090
    wallet_user           = ""
    wallet_password       = ""


if __name__ == '__main__':
    rpc = GrapheneAPI("localhost", 8092)

    symbol = "CNY"
    producers = ["fakeusd-feed-producer"]

    tx = rpc.update_asset_feed_producers(symbol, producers, True)
    print(json.dumps(tx, indent=4))
