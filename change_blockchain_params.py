from grapheneapi.grapheneapi import GrapheneAPI
from graphenebase.transactions import formatTimeFromNow
from pprint import pprint

broadcast = True
proposer = "faucet"

client = GrapheneAPI("localhost", 8092, "", "")
obj = client.get_object("2.0.0")[0]
expiration = formatTimeFromNow(obj["parameters"]["committee_proposal_review_period"] + 30)

parameters = {
    "block_interval": 3,
    "maintenance_interval": 60 * 2,
    "maintenance_skip_slots": 3,
    "committee_proposal_review_period": 0,
    "maximum_transaction_size": 2048,
    "maximum_block_size": 2048000000,
    "maximum_time_until_expiration": 86400,
    "maximum_proposal_lifetime": 2419200,
    "maximum_asset_whitelist_authorities": 10,
    "maximum_asset_feed_publishers": 10,
    "maximum_witness_count": 1001,
    "maximum_committee_count": 1001,
    "maximum_authority_membership": 10,
    "reserve_percent_of_fee": 2000,
    "network_percent_of_fee": 2000,
    "lifetime_referrer_percent_of_fee": 3000,
    "cashback_vesting_period_seconds": 31536000,
    "cashback_vesting_threshold": 10000000,
    "count_non_member_votes": True,
    "allow_non_member_whitelists": True,
    "witness_pay_per_block": 1000000,
    "worker_budget_per_day": "50000000000",
    "max_predicate_opcode": 1,
    "fee_liquidation_threshold": 10000000,
    "accounts_per_fee_scale": 1000,
    "account_fee_scale_bitshifts": 4,
    "max_authority_depth": 2,
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
