import json
from web3 import Web3
import time
import random
from termcolor import cprint

time_ot = 50
time_do = 200

# RPCs
polygon_rpc_url = 'https://rpc.ankr.com/polygon'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
# ABIs
abi = json.load(open('router_abi.json'))
contr_polygon_address = w3.to_checksum_address('0x8C531f965C05Fab8135d951e2aD0ad75CF3405A2')
nft_contract = w3.eth.contract(address=contr_polygon_address, abi=abi)

with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))
    random.shuffle(numbered_keys)
#counter = 0
wallets_prob = []
for wallet_number, PRIVATE_KEY in numbered_keys:
    account = w3.eth.account.from_key(PRIVATE_KEY)
    address = account.address

    print(time.strftime("%H:%M:%S", time.localtime()))
    print(f'[{wallet_number}] - {address}', flush=True)

    nonce = w3.eth.get_transaction_count(address)
    gas_price = w3.eth.gas_price
    data = 1
    try:
        swap_txn = nft_contract.functions.purchase(
            data
        ).build_transaction({
            'from': address,
            'value': w3.to_wei(1, 'wei'),
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(address),
        })
        gasLimit = w3.eth.estimate_gas(swap_txn)
        swap_txn['gas'] = int(gasLimit + gasLimit * 0.5)
        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE_KEY)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        print(f"Transaction: https://polygonscan.com/tx/{swap_txn_hash.hex()}")
        cprint("Success", "green")
        time.sleep(random.randint(time_ot, time_do))
    except:
        cprint("Failed", "red")
        wallets_prob.append(address)

if len(wallets_prob) > 0:
    cprint("Problems", "red")
    print(wallets_prob)
else:
    cprint("All done", "green")

