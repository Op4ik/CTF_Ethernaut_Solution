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


def main():
    player = get_account()
    instance_address = get_new_instance(level_id=0, player=player)
    contract = interface.IHelloEthernaut(instance_address)
    
    tx = contract.authenticate("ethernaut0", {"from": player})
    tx.wait(1)

    submit_instance(instance_address, player)