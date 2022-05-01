# Dogecoin key generate

import bitcoin as dogecoin
import secrets
import binascii as _bin
import subprocess

def dogecoin_main(network='mainnet'):
    if network == 'testnet' :
        np1 = 'ef'
        np2 = b'\xEF'

        anp1 = '6f'
        anp2 = b'\x6F'
    else:
        np1 = '9e'
        np2 = b'\x9E'

        anp1 = '1e'
        anp2 = b'\x1E'

    dogecoin_private = secrets.randbits(256)
    hex_dogecoin_private = hex(dogecoin_private)
    private_key = hex_dogecoin_private[2:]
    print(f'private key :> {private_key}')

    # mainnet and testnet WIF key
    extended = np1 + private_key + '01'
    extended_key = np2 + _bin.unhexlify(private_key) + b'\x01'
    extended = extended + dogecoin.checksum(extended_key)
    print(f'WIF :> {dogecoin.base58(extended)}')
    public_key = subprocess.run(['node', 'secp256k1.js', private_key], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split(':')
    print(f'public key uncompressed :> {public_key[0]}')
    print(f'public key compressed :> {public_key[1]}')

    print(f'public key hash uncompressed :> {dogecoin.hash160(public_key[0])}')
    print(f'public key hash compressed :> {dogecoin.hash160(public_key[1])}')

    key_hash = dogecoin.hash160(public_key[1])
    public_key_extended = anp2 + _bin.unhexlify(key_hash)
    public_extended = anp1 + key_hash + dogecoin.checksum(public_key_extended)
    address = dogecoin.base58(public_extended)

    print(f'address :> {address}')