from web3 import Web3

RPC_URL = "https://rpc.testnet.arc.network"

w3 = Web3(Web3.HTTPProvider(RPC_URL))


def is_connected():
    return w3.is_connected()


def latest_block():
    return w3.eth.block_number


def get_balance(address):

    if not w3.is_address(address):
        raise ValueError(
            "Invalid wallet address"
        )

    checksum = w3.to_checksum_address(address)

    balance = w3.eth.get_balance(
        checksum
    )

    return float(
        w3.from_wei(balance, "ether")
    )