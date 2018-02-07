#!/usr/bin/env python

''' A coinbase trading application '''

from coinbase.wallet.client import Client
from credentials import *
import json

eth_total = 0
btc_total = 0

client = Client(api_key, api_secret)
user = client.get_current_user()
account = client.get_accounts()
eth_transactions = client.get_transactions(eth_id)
btc_transactions = client.get_transactions(btc_id)

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
            print 'Bought' , transaction['amount']['amount'] , 'ETH'
            eth_total += float(transaction['amount']['amount']) * float(client.get_sell_price(currency_pair = 'ETH-USD')['amount'])

    for transaction in btc_transactions['data']:
        if(transaction['type'] == 'buy'):
            print 'Bought ' , transaction['amount']['amount'], 'BTC'
            btc_total = float(transaction['amount']['amount']) * float(client.get_sell_price(currency_pair = 'BTC-USD')['amount'])

def account_totals():
    ''' Get account totals '''
    
    global eth_total, btc_total

    print '\n***** My Account Totals *****\n'
    print 'My ETH total: $' + str(round(eth_total,2))
    print 'My BTC total : $' + str(round(btc_total,2))

if __name__ == '__main__':
    current_prices()
    transaction_history()
    account_totals()
