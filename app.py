import os
from bech32 import bech32_encode, convertbits
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# Generate a seed phrase
seed_phrase = Bip39MnemonicGenerator().FromWordsNumber(12)
print("Seed Phrase: " + str(seed_phrase))

# Generate a seed buffer from the seed phrase
seed_buffer = Bip39SeedGenerator(seed_phrase).Generate()

# Generate a root node from the seed buffer using the bip32 library
root = Bip44.FromSeed(seed_buffer, Bip44Coins.BITCOIN)

# Derive the first account's node (m/44'/0'/0')
account = root.Purpose().Coin().Account(0)

# Derive the external chain node of this account (m/44'/0'/0'/0)
node = account.Change(Bip44Changes.CHAIN_EXT)

# Derive the first address from the external chain (m/44'/0'/0'/0/0)
child = node.AddressIndex(0)

# Get the public key for this address
public_key = child.PublicKey().RawCompressed()

# Convert public key to witness program format
witness_program = convertbits(public_key[1:], 8, 5)

# Generate a SegWit address using bech32 encoding
address = bech32_encode('bc', [0] + witness_program)
print("Address: " + address)
