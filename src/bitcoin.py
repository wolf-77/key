# https://github.com/wolf-77
# cryptocurrency address generator cli-based application

import secrets
import hashlib
import binascii as _bin
import subprocess

def checksum(key):
    sha1 = hashlib.sha256(key).digest()
    sha2 = hashlib.sha256(sha1).digest()
    return _bin.hexlify(sha2)[0:8].decode('utf-8')

def base58(_hash):
    char = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int(_hash, 16)
    base58 = ""
    while num > 0:
        num , i = divmod(num, 58)
        base58 = char[i] + base58
    
    return base58

def hash160(public_key):
    _public_key = _bin.unhexlify(public_key)
    sha1 = hashlib.sha256(_public_key).digest()
    ripemd1 = hashlib.new('ripemd160')
    ripemd1.update(sha1)
    return ripemd1.hexdigest()

def bitcoin_main(network='mainnet'):
    if network == 'testnet' :
        np1 = 'ef'
        np2 = b'\xEF'

        anp1 = '6f'
        anp2 = b'\x6F'
    else:
        np1 = '80'
        np2 = b'\x80'

        anp1 = '00'
        anp2 = b'\x00'

    bitcoin_private = secrets.randbits(256)
    hex_bitcoin_private = hex(bitcoin_private)
    private_key = hex_bitcoin_private[2:]
    print(f'private key :> {private_key}')

    # mainnet and testnet WIF key
    extended = np1 + private_key + '01'
    extended_key = np2 + _bin.unhexlify(private_key) + b'\x01'
    extended = extended + checksum(extended_key)
    print(f'WIF :> {base58(extended)}')
    public_key = subprocess.run(['node', 'secp256k1.js', private_key], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split(':')
    print(f'public key uncompressed :> {public_key[0]}')
    print(f'public key compressed :> {public_key[1]}')

    print(f'public key hash uncompressed :> {hash160(public_key[0])}')
    print(f'public key hash compressed :> {hash160(public_key[1])}')

    key_hash = hash160(public_key[1])
    public_key_extended = anp2 + _bin.unhexlify(key_hash)
    public_extended = anp1 + key_hash + checksum(public_key_extended)
    if network == 'testnet':
        address = base58(public_extended)
    else:
        address = '1' + base58(public_extended)

    print(f'address :> {address}')