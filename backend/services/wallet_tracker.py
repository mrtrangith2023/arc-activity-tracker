from web3 import Web3

RPC_URL = "https://rpc.testnet.arc.network"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_wallet_info(address):

    balance = w3.eth.get_balance(address)

    return {
        "address": address,
        "balance": balance
    }