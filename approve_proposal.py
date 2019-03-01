from grapheneapi.grapheneapi import GrapheneAPI
from bitshares import BitShares
from bitshares.account import Account
from pprint import pprint
import sys
import click

@click.command()
def run():

#    testnet = BitShares("wss://node.testnet.bitshares.eu")
    testnet = BitShares("ws://this.uptick.rocks:18090")
    
    account = Account("committee-account", full=True, bitshares_instance=testnet)
    proposals = account["proposals"]
    client = GrapheneAPI("localhost", 8092, "", "")

    for proposal in proposals:
        pprint(proposal)
        if click.confirm("Approve proposal %s" % proposal["id"]):
            # Get current fees
            core_asset = client.get_asset("1.3.0")
            committee_account = client.get_account("committee-account")
            proposal = client.get_object(proposal["id"])[0]
            prop_op = proposal["proposed_transaction"]["operations"]

            tx = client.approve_proposal(
                "faucet",
                proposal["id"],
                {"active_approvals_to_add": [
                    "committee-member-1",
                    "committee-member-2",
                    "committee-member-3",
                    "committee-member-4",
                    "committee-member-5",
                    "committee-member-6",
                    "committee-member-7",
                    "committee-member-8",
                    "committee-member-9",
                    "committee-member-10"]
                },
                True)
            pprint(tx)

if __name__ == '__main__':
    run()
