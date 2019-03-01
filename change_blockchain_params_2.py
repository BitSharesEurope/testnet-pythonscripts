from grapheneapi.grapheneapi import GrapheneAPI
from graphenebase.transactions import formatTimeFromNow
from pprint import pprint

broadcast = True
proposer = "faucet"

client = GrapheneAPI("localhost", 8092, "", "")
obj = client.get_object("2.0.0")[0]
expiration = formatTimeFromNow(obj["parameters"]["committee_proposal_review_period"] + 300)

parameters = {
    "maintenance_interval": 60 * 5,
    "cashback_vesting_period_seconds": 60 * 60 * 24,
    "cashback_vesting_threshold": 10 ** 5,
}

tx = client.propose_parameter_change(
    proposer,
    expiration,
    parameters,
    broadcast
)
pprint(tx)

if not broadcast:
    print("=" * 80)
    print("Set broadcast to 'True' if the transaction shall be broadcast!")
