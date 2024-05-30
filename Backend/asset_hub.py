from substrateinterface import SubstrateInterface, Keypair

# Initialize the connection to the Polkadot AssetHub
def init_asset_hub():
    return SubstrateInterface(
        url="wss://westmint-rpc.polkadot.io",  # Use the appropriate AssetHub endpoint
        ss58_format=42,  # Westend's ss58 prefix
        type_registry_preset='westend'
    )

# Create keypair from mnemonic
def get_keypair(mnemonic):
    return Keypair.create_from_mnemonic(mnemonic)

# Transfer tokens
def transfer_tokens(substrate, keypair, asset_id, recipient_address, amount):
    call = substrate.compose_call(
        call_module='Assets',
        call_function='transfer',
        call_params={
            'id': asset_id,
            'target': recipient_address,
            'amount': amount
        }
    )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    return result
