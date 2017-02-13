from grapheneapi.grapheneapi import GrapheneAPI

import json
import random
import math


if __name__ == '__main__':
    rpc = GrapheneAPI("localhost", 8092)

    asset_symbol = "GOLD"
    producers = ["fakeusd-feed-producer"]

    price = random.normalvariate(134, 0.1)
    price = math.fabs(price)

    asset = rpc.get_asset(asset_symbol)
    base = rpc.get_asset("1.3.0")
    price = price * 10 ** asset["precision"] / 10 ** base["precision"]
    denominator = 1e5
    numerator = round(price * 1e5)

    for producer in producers:
        account = rpc.get_account(producer)
        price_feed = {"settlement_price": {
                      "quote": {"asset_id": "1.3.0",
                                "amount": denominator
                                },
                      "base": {"asset_id": asset["id"],
                               "amount": numerator
                               }
                      },
                      "maintenance_collateral_ratio": 1200,
                      "maximum_short_squeeze_ratio": 1100,
                      "core_exchange_rate": {
                      "quote": {"asset_id": "1.3.0",
                                "amount": int(denominator * 1.05)
                                },
                      "base": {"asset_id": asset["id"],
                               "amount": numerator
                               }}}
        handle = rpc.begin_builder_transaction()
        op = [19,  # id 19 corresponds to price feed update operation
              {"asset_id": asset["id"],
               "feed": price_feed,
               "publisher": account["id"]
               }]
        rpc.add_operation_to_builder_transaction(handle, op)
        rpc.set_fees_on_builder_transaction(handle, "1.3.0")
        tx = rpc.sign_builder_transaction(handle, True)
        print(json.dumps(tx, indent=4))
