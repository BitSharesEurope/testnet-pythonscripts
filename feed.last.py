from grapheneapi import GrapheneClient
from grapheneexchange import GrapheneExchange

import json
import fractions


class Config():
    wallet_host           = "localhost"
    wallet_port           = 8090
    wallet_user           = ""
    wallet_password       = ""
    witness_url           = "ws://localhost:11011"
    witness_user          = ""
    witness_password      = ""

    watch_markets = ["PEG.LAST:TEST"]
    market_separator = ":"

if __name__ == '__main__':
    config = Config
    graphene = GrapheneClient(config)
    dex = GrapheneExchange(config)

    asset_symbol = "PEG.LAST"
    producers = ["init0", "init1", "init2", "init3", "init4", "init5", "init6", "init7", "init8", "init9", "init10"]

    ticker = None
    try:
        ticker = dex.returnTicker()
    except :
        pass

    if not ticker or config.watch_markets[0] not in ticker:
        price = 1
    else :
        price = ticker[config.watch_markets[0]]["last"]

    for producer in producers:
        account = graphene.rpc.get_account(producer)
        asset = graphene.rpc.get_asset(asset_symbol)
        core_price  = fractions.Fraction.from_float(price).limit_denominator(1e5)
        denominator = core_price.denominator
        numerator   = core_price.numerator
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

