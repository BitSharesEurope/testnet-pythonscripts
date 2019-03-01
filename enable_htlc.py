import json
import click
from pprint import pprint
from grapheneapi.grapheneapi import GrapheneAPI
from bitsharesbase.operations import getOperationNameForId, operations
from bitshares.utils import formatTimeFromNow
from deepdiff import DeepDiff
from copy import deepcopy


@click.command()
@click.option("--rpchost", default="localhost")
@click.option("--rpcport", default=8092)
@click.option("--expiration", default=60 * 60 * 24 * 2)
@click.option("--broadcast/--no-broadcast", default=False)
@click.option("--proposer", default="xeroc")
def main(rpchost, rpcport, expiration, broadcast, proposer):
    rpc = GrapheneAPI(rpchost, rpcport)
    obj = rpc.get_object("2.0.0")[0]
    new_parameters = deepcopy(obj["parameters"])
    current_fees = obj["parameters"]["current_fees"]["parameters"]
    fees = obj["parameters"]["current_fees"]["parameters"]
    scale = obj["parameters"]["current_fees"]["scale"] / 1e4

    # General change of parameter
    changes = {}

    # Copy old fees
    for f in current_fees:
        changes[getOperationNameForId(f[0])] = f[1].copy()

    # New fees
    new_fee = {"fee": int(0.2 / scale * 1e5), "fee_per_day": int(0.2 / scale * 1e5)}
    changes["htlc_create"] = new_fee
    changes["htlc_redeem"] = new_fee
    changes["htlc_extend"] = new_fee

    tx = rpc.propose_fee_change(
        proposer, formatTimeFromNow(expiration), changes, broadcast
    )
    op = tx["operations"][0][1]["proposed_ops"][0]["op"]

    # New HTLC parameters are in extensions
    op[1]["new_parameters"]["extensions"] = {
        "updatable_htlc_options": {
            "max_preimage_size": 19200,
            "htlc_max_timeout_secs": 60 * 60 * 24 * 28,
        }
    }

    ops = [op]
    buildHandle = rpc.begin_builder_transaction()
    for op in ops:
        rpc.add_operation_to_builder_transaction(buildHandle, op)
    rpc.set_fees_on_builder_transaction(buildHandle, "1.3.0")
    params = rpc.get_object("2.0.0")[0]
    preview = params["parameters"]["committee_proposal_review_period"] or 10
    rpc.propose_builder_transaction2(
        buildHandle, proposer, formatTimeFromNow(expiration), preview, False
    )
    rpc.set_fees_on_builder_transaction(buildHandle, "1.3.0")

    # Sign and broadcast
    tx = rpc.sign_builder_transaction(buildHandle, broadcast)

    pprint(tx)


if __name__ == "__main__":
    main()
