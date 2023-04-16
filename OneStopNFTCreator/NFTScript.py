import hashlib
import json
import requests
import algosdk

#Kacy Adams
#mega-ace submission for onestop nft

def mintNFT(algod_client, creator_address, creator_private_key, asset_name, asset_unit_name, metadata_uri):
    metadata = {"name": asset_name, "decimals": 0, "image": f"ipfs://{metadata_uri}#arc3"}
    metadata_json = json.dumps(metadata)

    ipfs_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    ipfs_headers = {
        "pinata_api_key": "e6ec707b7c24fa0d401c",
        "pinata_secret_api_key": "5b921875e121139733afc757633c0d0c1d4928bfbe82e068eb56ca5f54647380",
        "Content-Type": "application/json"
    }
    ipfs_payload = {
        "pinataMetadata": {"name": asset_name},
        "pinataContent": metadata_json
    }
    ipfs_response = requests.post(ipfs_url, headers=ipfs_headers, json=ipfs_payload)
    metadata_cid = ipfs_response.json()["IpfsHash"]



    params = algod_client.suggested_params()
    txn = algosdk.future.transaction.AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=1,
        decimals=0,
        unit_name=asset_unit_name.lower(),
        asset_name=asset_name,
        manager=creator_address,
        reserve=creator_address,
        freeze=creator_address,
        clawback=creator_address,
        url=f"ipfs://{metadata_cid}#arc3",
        metadata_hash=hashlib.sha256(metadata_json.encode()).hexdigest()
    )

    signed_txn = txn.sign(creator_private_key)
    txid = algod_client.send_transaction(signed_txn)
    # print(f"Asset creation txid: {txid}")

    confirmed_txn = algod_client.pending_transaction_info(txid)
    asset_id = confirmed_txn["asset-index"]
    # print(f"Asset ID: {asset_id}")

    return asset_id


def transferNFT(algod_client, sender_address, sender_private_key, receiver_address, asset_id):
    params = algod_client.suggested_params()
    txn = algosdk.future.transaction.AssetTransferTxn(
        sender=sender_address,
        sp=params,
        receiver=receiver_address,
        amt=1,
        index=asset_id
    )
    # signed_txn = txn.sign(sender_private_key)
    # txid = algod_client.send_transaction(signed_txn)
    # print(f"NFT transfer txid: {txid}")
