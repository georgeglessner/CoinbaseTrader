#!/usr/bin/env python

''' A coinbase trading application '''

from coinbase.wallet.client import Client
from credentials import *
import sys

# Global values fo total amount of each
eth_total = 0
btc_total = 0

client = Client(api_key, api_secret)
user = client.get_current_user()
accounts = client.get_accounts()
payment_methods = client.get_payment_methods()
eth_transactions = client.get_transactions(eth_id)
btc_transactions = client.get_transactions(btc_id)

# Max buy per run ($USD)
ETH_MAX_BUY = 10
BTC_MAX_BUY = 10

def current_prices():
    ''' Get current buy and sell prices '''

    print '\n***** Current Prices *****\n'
    print 'Etherem Buy Price: $' + client.get_buy_price(currency_pair = 'ETH-USD')['amount']
    print 'Etherem Sell Price: $' + client.get_sell_price(currency_pair = 'ETH-USD')['amount']
    print 'Bitcoin Buy Price: $' + client.get_buy_price(currency_pair = 'BTC-USD')['amount']
    print 'Bitcoin Sell Price: $' + client.get_sell_price(currency_pair = 'BTC-USD')['amount']

def transaction_history():
    ''' Get transaction history '''

    global eth_total, btc_total

    print '\n***** Transaction History *****\n'
    for transaction in eth_transactions['data']:
        if(transaction['type'] == 'buy'):
            print 'Bought' , transaction['amount']['amount'] , 'ETH on', transaction['created_at'][:10]
            eth_total += float(transaction['amount']['amount']) * float(client.get_sell_price(currency_pair = 'ETH-USD')['amount'])

    for transaction in btc_transactions['data']:
        if(transaction['type'] == 'buy'):
            print 'Bought' , transaction['amount']['amount'], 'BTC on',  transaction['created_at'][:10]
            btc_total = float(transaction['amount']['amount']) * float(client.get_sell_price(currency_pair = 'BTC-USD')['amount'])

def account_totals():
    ''' Get account totals '''

    global eth_total, btc_total

    print '\n***** My Account Totals *****\n'
    print 'My ETH total: $' + str(round(eth_total,2))
    print 'My BTC total : $' + str(round(btc_total,2)), '\n'

def confirm_start():
    ''' Confirm start of trading '''

    while True:
        answer = raw_input('Do you want to start trading? [y/n]: ')

        if answer == 'y' or answer == 'Y':
            while True:
                currency = raw_input('For which currency? [eth/btc]: ')
                if currency == 'eth' or currency == 'ETH':
                    trade_eth()
                    return
                if currency == 'btc' or currency == 'BTC':
                    trade_btc()
                    return
                else:
                    print 'Invalid currency. Please enter [eth/btc].'

        if answer == 'n' or answer == 'N':
            print 'Ending session...'
            sys.exit(1)
        else:
            print 'Invalid input. Valid input is [y/n]'

def trade_eth():
    ''' Start trading Etherem '''

    print 'Trading Ethereum...'

    # Keep track of buys ($USD)
    eth_total_buy = 0

    # Set amound of ethereum to buy (low to test with)
    amount = '.000001'

    #TODO: implement logic for buying and selling

def trade_btc():
    ''' Start trading Bitcoin '''

    print 'Trading Bitcoin...'

    # Keep track of buys ($USD)
    btc_total_buy = 0

    # Set amount of bitcoin to buy (low to test with)
    amount = '.000001'

    #TODO: implement logic for buying and selling




if __name__ == '__main__':
    current_prices()
    transaction_history()
    account_totals()
    confirm_start()
