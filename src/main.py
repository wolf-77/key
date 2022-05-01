from bitcoin import bitcoin_main as btc
from litecoin import litecoin_main as ltc
from dogecoin import dogecoin_main as doge
from bitcoincash import bch_main as bch
from ethereum import eth_main as ethereum
import sys

try:
    _argv = sys.argv
    print(_argv)
    coin_list = ['BTC', 'BCH', 'LTC', 'DOGE', 'ETH']
    if len(_argv) == 3:
        network = _argv[2]

    if len(_argv) >= 2:
        if _argv[1] == '--help':
            print(
                '''
                python main.py BTC [mainnet/testnet]
                python main.py BCH [mainnet/testnet]
                python main.py LTC [mainnet/testnet]
                python main.py DOGE [mainnet/testnet]
                python main.py ETH
                '''
            )
        elif _argv[1] in coin_list:
            coin = _argv[1]
            if coin == 'BTC':
                btc(network)
            elif coin == 'BCH':
                bch(network)
            elif coin == 'LTC':
                ltc(network)
            elif coin == 'DOGE':
                doge(network)
            elif coin == 'ETH':
                ethereum()
        else:
            print('run :> python main.py --help')
            
    else:
        print('run :> python main.py --help')
except:
    print('run :> python main.py --help')