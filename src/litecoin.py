# litecoin key generate

import bitcoin as litecoin
import secrets
import binascii as _bin
import subprocess

def litecoin_main(network='mainnet'):
    if network == 'testnet' :
        np1 = 'ef'
        np2 = b'\xEF'

        anp1 = '6f'
        anp2 = b'\x6F'
    else:
        np1 = 'b0'
        np2 = b'\xB0'

        anp1 = '30'
        anp2 = b'\x30'

    litecoin_private = secrets.randbits(256)
    hex_litecoin_private = hex(litecoin_private)
    private_key = hex_litecoin_private[2:]
    print(f'private key :> {private_key}')

    # mainnet and testnet WIF key
    extended = np1 + private_key + '01'
    extended_key = np2 + _bin.unhexlify(private_key) + b'\x01'
    extended = extended + litecoin.checksum(extended_key)
    print(f'WIF :> {litecoin.base58(extended)}')
    public_key = subprocess.run(['node', 'secp256k1.js', private_key], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split(':')
    print(f'public key uncompressed :> {public_key[0]}')
    print(f'public key compressed :> {public_key[1]}')

    print(f'public key hash uncompressed :> {litecoin.hash160(public_key[0])}')
    print(f'public key hash compressed :> {litecoin.hash160(public_key[1])}')

    key_hash = litecoin.hash160(public_key[1])
    public_key_extended = anp2 + _bin.unhexlify(key_hash)
    public_extended = anp1 + key_hash + litecoin.checksum(public_key_extended)
    address = litecoin.base58(public_extended)

    print(f'address :> {address}')