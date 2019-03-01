from grapheneapi.grapheneapi import GrapheneAPI
from graphenebase.transactions import formatTimeFromNow
from pprint import pprint

broadcast = True
proposer = "faucet"

client = GrapheneAPI("localhost", 8092, "", "")
obj = client.get_object("2.0.0")[0]
expiration = formatTimeFromNow(obj["parameters"]["committee_proposal_review_period"] + 30)
TX_HEADER = 14
TRANSFER_OP = 22

phases = [{
    "maximum_transaction_size": 1 * 1024,   # 1 kb
    "maximum_block_size": 1 * 1024 * 1024,  # 1 MB
    "block_interval": 3,                    # 3 secs
},{
    "maximum_transaction_size": 1 * 1024,   # 1 kb
    "maximum_block_size": 5 * 1024 * 1024,  # 5 MB
    "block_interval": 3,                    # 3 secs
},{
    "maximum_transaction_size": 10 * 1024,  # 10 kb
    "maximum_block_size": 5 * 1024 * 1024,  # 5 MB
    "block_interval": 3,                    # 3 secs
},{
    "maximum_transaction_size": 100 * 1024, # 100 kb
    "maximum_block_size": 5 * 1024 * 1024,  # 10 MB
    "block_interval": 3,                    # 3 secs
},{
    "maximum_transaction_size": 1 * 1024,   # 1 kb
    "maximum_block_size": 10 * 1024 * 1024, # 10 MB
    "block_interval": 3,                    # 3 secs
},{
    "maximum_transaction_size": 10 * 1024 * 1024,   # 10 Mb
    "maximum_block_size": 1024 * 1024 * 1024, # 1 GB
    "block_interval": 3,                      # 3 secs
},{
    "maximum_transaction_size": 100 * 1024,   # 100 kB
    "maximum_block_size": 1 * 1024 * 1024, # 1 MB
    "block_interval": 2,                    # 2 secs
},{
    "maximum_transaction_size": 10 * 1024 * 1024,   # 10 Mb
    "maximum_block_size": 1024 * 1024 * 1024, # 1 GB
    "block_interval": 10,                      # 10 secs
},{
    "maximum_transaction_size": 10 * 1024 * 1024,   # 10 Mb
    "maximum_block_size": 1024 * 1024 * 1024, # 1 GB
    "block_interval": 1,                      # 1 secs
}]

tx = client.propose_parameter_change(
    proposer,
    expiration,
    phases[0],   # Pick Phase!
    broadcast
)
pprint(tx)

if not broadcast:
    print("=" * 80)
    print("Set broadcast to 'True' if the transaction shall be broadcast!")
