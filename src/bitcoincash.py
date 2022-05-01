# Bitcoin Cash key generate

import bitcoin as bch
import secrets
import binascii as _bin
import subprocess

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def calculate_checksum(prefix, payload):
    poly = polymod(prefix_expand(prefix) + payload + [0, 0, 0, 0, 0, 0, 0, 0])
    out = list()
    for i in range(8):
        out.append((poly >> 5 * (7 - i)) & 0x1F)
    return out

def b32encode(inputs):
    out = ""
    for char_code in inputs:
        out += CHARSET[char_code]
    return out

def prefix_expand(prefix):
    return [ord(x) & 0x1F for x in prefix] + [0]

def polymod(values):
    chk = 1
    generator = [
        (0x01, 0x98F2BC8E61),
        (0x02, 0x79B76D99E2),
        (0x04, 0xF33E5FB3C4),
        (0x08, 0xAE2EABE2A8),
        (0x10, 0x1E4F43E470),
    ]
    for value in values:
        top = chk >> 35
        chk = ((chk & 0x07FFFFFFFF) << 5) ^ value
        for i in generator:
            if top & i[0] != 0:
                chk ^= i[1]
    return chk ^ 1

def bch_main(network='mainnet'):
    if network == 'testnet' :
        np1 = 'ef'
        np2 = b'\xEF'

        anp1 = '6f'
        anp2 = b'\x6F'

        prefix = 'bchtest'
    else:
        np1 = '80'
        np2 = b'\x80'

        anp1 = '00'
        anp2 = b'\x00'

        prefix = 'bitcoincash'

    bch_private = secrets.randbits(256)
    hex_bch_private = hex(bch_private)
    private_key = hex_bch_private[2:]
    print(f'private key :> {private_key}')

    # mainnet and testnet WIF key
    extended = np1 + private_key + '01'
    extended_key = np2 + _bin.unhexlify(private_key) + b'\x01'
    extended = extended + bch.checksum(extended_key)
    print(f'WIF :> {bch.base58(extended)}')
    public_key = subprocess.run(['node', 'secp256k1.js', private_key], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split(':')
    print(f'public key uncompressed :> {public_key[0]}')
    print(f'public key compressed :> {public_key[1]}')

    print(f'public key hash uncompressed :> {bch.hash160(public_key[0])}')
    print(f'public key hash compressed :> {bch.hash160(public_key[1])}')

    key_hash = bch.hash160(public_key[1])
    public_key_extended = anp2 + _bin.unhexlify(key_hash)
    public_extended = anp1 + key_hash + bch.checksum(public_key_extended)
    
    if network == 'testnet':
        address = bch.base58(public_extended)
    else:
        address = '1' + bch.base58(public_extended)

    print(f'legacy address :> {address}')

    version_byte_hex = b'\x00' + _bin.unhexlify(key_hash)
    payload = list(version_byte_hex)
    payload = convertbits(payload, 8, 5)
    checksum = calculate_checksum(prefix, payload)
    
    print(f'cashaddress :> {prefix}:{b32encode(payload + checksum)}')