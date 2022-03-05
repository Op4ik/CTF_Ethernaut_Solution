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