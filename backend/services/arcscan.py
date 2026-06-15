import requests

BASE_URL = "https://testnet.arcscan.app/api/v2"


def get_address(address):
    url = f"{BASE_URL}/addresses/{address}"

    response = requests.get(url)

    return response.json()


def get_counters(address):
    url = f"{BASE_URL}/addresses/{address}/counters"

    response = requests.get(url)

    return response.json()

# def get_transactions(address):

#     url = (
#         f"{BASE_URL}/addresses/"
#         f"{address}/transactions"
#     )

#     return requests.get(url).json()

def get_transactions(address):

    url = f"{BASE_URL}/addresses/{address}/transactions"

    data = requests.get(url).json()

    return data.get("items", [])