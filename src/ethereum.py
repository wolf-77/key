# ethereum key generate

import secrets
import subprocess

def eth_main():
    ethereum_private = secrets.randbits(256)
    hex_ethereum_private = hex(ethereum_private)
    print(f'private key :> {hex_ethereum_private}')
    # private_key = hex_ethereum_private[2:]
    private_key = subprocess.run(['node', 'keccak256.js', hex_ethereum_private], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
    print(f'keccak256 private key :> {private_key}')

    public_key_uncompressed = subprocess.run(['node', 'secp256k1.js', private_key], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split(':')[0]
    print(f'public key uncompressed :> {public_key_uncompressed}')

    public_key = public_key = subprocess.run(['node', 'keccak256.js', public_key_uncompressed], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
    print(f'address :> 0x{public_key[-40:]}')