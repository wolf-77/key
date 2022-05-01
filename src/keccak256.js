const keccak = require('keccak256');
let key = process.argv[2];
let hash = keccak(key).toString('hex');
console.log(hash);