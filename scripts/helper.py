from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from brownie.network.state import Chain
from brownie import web3
from web3 import Web3

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

def get_new_instance(level_id, player, value=0):
    print("---getting new instance---")
    ethernaut_address = config["networks"][network.show_active()]["ethernaut"]
    level_address = config["networks"][network.show_active()][f"level_{level_id}"]
    ethernaut = interface.IEthernaut(ethernaut_address)
    tx = ethernaut.createLevelInstance(level_address, {"from": player, "value": value})
    tx.wait(1)
    instance_address = tx.events['LevelInstanceCreatedLog']['instance']
    print(f'---deployed new instance at address {instance_address}---')
    print()
    return instance_address

def submit_instance(instance_address, player):
    print("---submitting instance---")
    ethernaut_address = config["networks"][network.show_active()]["ethernaut"]
    ethernaut = interface.IEthernaut(ethernaut_address)
    tx = ethernaut.submitLevelInstance(instance_address, {"from": player})
    tx.wait(1)
    print("Level completed!" if tx.events.count('LevelCompletedLog') else "Level not completed...")

def deploy_with_bytecode(abi, bytecode, deployer_account):
    contract = Web3(web3.provider).eth.contract(abi=abi, bytecode=bytecode)
    nonce = Web3(web3.provider).eth.getTransactionCount(str(deployer_account))
    transaction = contract.constructor().buildTransaction(
        {
            "chainId": Chain().id,
            "gasPrice": Web3(web3.provider).eth.gas_price,
            "from": str(deployer_account),
            "nonce": nonce,
        }
    )
    signed_txn = Web3(web3.provider).eth.account.sign_transaction(transaction, private_key=str(deployer_account.private_key))
    tx_hash = Web3(web3.provider).eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = Web3(web3.provider).eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt