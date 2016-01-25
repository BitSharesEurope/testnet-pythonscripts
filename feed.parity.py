from grapheneapi import GrapheneClient
from grapheneexchange import GrapheneExchange

import json
import fractions


class Config():
    wallet_host           = "localhost"
    wallet_port           = 8090
    wallet_user           = ""
    wallet_password       = ""

if __name__ == '__main__':
    graphene = GrapheneClient(Config)

    asset_symbol = "PEG.PARITY"
    producers = ["init0", "init1", "init2", "init3", "init4", "init5", "init6", "init7", "init8", "init9", "init10"]

    price = 1

    asset = graphene.rpc.get_asset(asset_symbol)
    base = graphene.rpc.get_asset("1.3.0")
    price = price * 10 ** asset["precision"] / 10 ** base["precision"]
    denominator = 1e5
    numerator   = round(price*1e5)

    for producer in producers:
        account = graphene.rpc.get_account(producer)
        price_feed  = {"settlement_price": {
                       "quote": {"asset_id": "1.3.0",
                                 "amount": denominator
                                 },
                       "base": {"asset_id": asset["id"],
                                "amount": numerator
                                }
                       },
                       "maintenance_collateral_ratio" : 1200,
                       "maximum_short_squeeze_ratio"  : 1100,
                       "core_exchange_rate": {
                       "quote": {"asset_id": "1.3.0",
                                 "amount": int(denominator * 1.05)
                                 },
                       "base": {"asset_id": asset["id"],
                                "amount": numerator
                                }}}
        handle = graphene.rpc.begin_builder_transaction()
        op = [19,  # id 19 corresponds to price feed update operation
              {"asset_id"  : asset["id"],
               "feed"      : price_feed,
               "publisher" : account["id"]
               }]
        graphene.rpc.add_operation_to_builder_transaction(handle, op)
        graphene.rpc.set_fees_on_builder_transaction(handle, "1.3.0")
        tx = graphene.rpc.sign_builder_transaction(handle, True)
        print(json.dumps(tx, indent=4))

