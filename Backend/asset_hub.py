from substrateinterface import SubstrateInterface, Keypair

# Initialize the connection to the Polkadot AssetHub
def init_asset_hub():
    return SubstrateInterface(
        url="wss://polkadot-rpc.polkadot.io",  # Use the appropriate AssetHub endpoint
        ss58_format=0,
        type_registry_preset='polkadot'
    )

# Create keypair from mnemonic
def get_keypair(mnemonic):
    return Keypair.create_from_mnemonic(mnemonic)

# Mint tokens
def mint_tokens(substrate, keypair, asset_id, recipient_address, amount):
    call = substrate.compose_call(
        call_module='Assets',
        call_function='mint',
        call_params={
            'id': asset_id,
            'beneficiary': recipient_address,
            'amount': amount
        }
    )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    return result
