from web3 import Web3

RPC_URL = "https://rpc.testnet.arc.network"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

print("Connected:", w3.is_connected())

if w3.is_connected():
    print("Latest Block:", w3.eth.block_number)