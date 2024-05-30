from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

# Connect to the Opal by Unique network
substrate = SubstrateInterface(
    url="wss://ws-opal.unique.network",
    ss58_format=42,  # Update this as per the Unique network's configuration
    type_registry_preset='unique'
)

# Your mnemonic phrase
mnemonic = "embody vivid region bright forum clay boost horror deal escape spider path"

# Create keypair
keypair = Keypair.create_from_mnemonic(mnemonic)

# Collection parameters
collection_name = "My NFT Collection"
collection_description = "A description of my NFT collection."
collection_properties = {"property1": "value1", "property2": "value2"}

# Function to create an NFT collection
def create_nft_collection():
    call = substrate.compose_call(
        call_module='Unique',
        call_function='create_collection',
        call_params={
            'name': collection_name,
            'description': collection_description,
            'properties': collection_properties
        }
    )

    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    try:
        result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return result
    except SubstrateRequestException as e:
        print(f"Failed to create collection: {e}")
        return None

# Mint the collection
result = create_nft_collection()
if result:
    print("Collection created successfully:", result)
else:
    print("Failed to create collection.")
