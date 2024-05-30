import dotenv from "dotenv";
dotenv.config();
import assert from 'assert';
import Sdk from '@unique-nft/substrate-client';
import { KeyringProvider } from '@unique-nft/accounts/keyring';
import { COLLECTION_SCHEMA_NAME, CreateCollectionNewArguments } from '@unique-nft/substrate-client/tokens';
import { UniqueCollectionSchemaToCreate } from '@unique-nft/substrate-client/tokens';

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Dynamic imports
const uniqueDefinitions = await import(path.resolve(__dirname, 'node_modules/@unique-nft/unique-mainnet-types/unique/definitions.js'));
const appPromotionDefinitions = await import(path.resolve(__dirname, 'node_modules/@unique-nft/unique-mainnet-types/appPromotion/definitions.js'));
const povinfoDefinitions = await import(path.resolve(__dirname, 'node_modules/@unique-nft/unique-mainnet-types/povinfo/definitions.js'));
const defaultDefinitions = await import(path.resolve(__dirname, 'node_modules/@unique-nft/unique-mainnet-types/default/definitions.js'));

async function main() {
  const mnemonic = process.env.WALLET_SEED ?? "";
  const keyringOptions = {
    ss58Format: 42, // Adjust as necessary for your network
    type: 'sr25519',
  };
  const account = await KeyringProvider.fromMnemonic(mnemonic, keyringOptions);
  const address = account.instance.address;

  const sdk = new Sdk({
    baseUrl: 'https://rest.unique.network/opal/v1', // Replace with your base URL
    signer: account,
  });

  // Create collection schema
  const collectionSchema = {
    schemaName: COLLECTION_SCHEMA_NAME.unique,
    schemaVersion: "1.0.0",
    image: "QmfWMWnP8HjLrnxGsG7XCDfVVm2viRkL9BC8hyUz5XoxUQ"
    coverPicture: {
      ipfsCid: "QmfWMWnP8HjLrnxGsG7XCDfVVm2viRkL9BC8hyUz5XoxUQ",
    },
  };

  // Create collection arguments
  const args = {
    address: address,
    name: "My simple collection",
    description: "I've created my first NFT collection!",
    tokenPrefix: "MSC",
    schema: collectionSchema,
  };

  // Create collection
  const result = await sdk.collection.create.submitWaitResult(args);

  const { isCompleted } = result;

  if (isCompleted) {
    const {
      parsed: { collectionId },
    } = result;

    console.log(`Created new collection with id ${collectionId}`);

    // Now mint a token in the created collection
    const tokens = [
      {
        data: {
          attributes: {
            '0': "example-attribute-value",
          },
          image: {
            url: 'https://gateway.pinata.cloud/ipfs/QmfWMWnP8HjLrnxGsG7XCDfVVm2viRkL9BC8hyUz5XoxUQ',
            type: 'image'
          },
          name: {
            _: 'My First NFT',
          },
          description: {
            _: 'This is my first NFT',
          },
        },
      },
    ];

    assert(tokens.length < 35, "The safe limit is 35 NFTs minted at once.");

    const unsignedTxPayload = await sdk.token.createMultiple.build({
      address,
      collectionId,
      tokens: tokens,
    });

    const { signature } = await sdk.extrinsic.sign(unsignedTxPayload);
    const { hash } = await sdk.extrinsic.submit({
      signature,
      signerPayloadJSON: unsignedTxPayload.signerPayloadJSON,
    });
    const result = await sdk.extrinsic.waitResult({ hash });
    console.log('result', result);

    const mintedTokensCount = result?.parsed?.length;
    let currentTokenId;
    result.parsed?.forEach((token, index) => {
      currentTokenId = token?.tokenId;
      console.log(`Minted token ID #${currentTokenId}/${mintedTokensCount} in collection ${collectionId}`);
      console.log(`View this minted token at https://uniquescan.io/opal/tokens/${collectionId}/${currentTokenId}`);
    });

  } else {
    const {
      submittableResult: { dispatchError },
    } = result;

    console.warn("Something went wrong: ", dispatchError);
  }

  process.exit();
}

main().catch((error) => {
  console.error(error);
});
