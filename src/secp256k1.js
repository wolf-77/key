// ECDSA
const crypto = require('crypto');

let private_key = process.argv[2];
let ec = crypto.createECDH('secp256k1');
ec.setPrivateKey(private_key, 'hex');
let public_key_compressed = ec.getPublicKey('hex', 'compressed');
let public_key_uncompressed = ec.getPublicKey('hex', 'uncompressed');

console.log(`${public_key_uncompressed}:${public_key_compressed}`);