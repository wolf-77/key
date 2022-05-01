// is cryptocurrency address valid ?

var WAValidator = require('multicoin-address-validator');

var valid = WAValidator.validate(
	'0xd898e44ba0be16381bf607d6b2ae42d03778ec65',
	'Ethereum'
);
if(valid)
	console.log('This is a valid address');
else
	console.log('Address INVALID');