#!/usr/bin/env python

''' A coinbase trading application '''

from coinbase.wallet.client import Client
from credentials import *
import sys
from time import sleep
import signal

# Global values for total amount of each
eth_total = 0
btc_total = 0

client = Client(api_key, api_secret)
user = client.get_current_user()
account = client.get_primary_account()
payment_method = client.get_payment_methods()[0]
eth_transactions = client.get_transactions(eth_id)
btc_transactions = client.get_transactions(btc_id)

# Max buy per run ($USD)
ETH_MAX_BUY = 50
BTC_MAX_BUY = 50


def current_prices():
    ''' Get current buy and sell prices '''

    print '\n***** Current Prices *****\n'
    print 'Etherem Buy Price: $' + client.get_buy_price(currency_pair='ETH-USD')['amount']
    print 'Etherem Sell Price: $' + client.get_sell_price(currency_pair='ETH-USD')['amount']
    print 'Bitcoin Buy Price: $' + client.get_buy_price(currency_pair='BTC-USD')['amount']
    print 'Bitcoin Sell Price: $' + client.get_sell_price(currency_pair='BTC-USD')['amount']


def transaction_history():
    ''' Get transaction history '''

    global eth_total, btc_total

    print '\n***** Transaction History *****\n'
    for transaction in eth_transactions['data']:
        if(transaction['type'] == 'buy'):
            print 'Bought', transaction['amount']['amount'], 'ETH on', transaction['created_at'][:10]
            eth_total += float(transaction['amount']['amount']) * float(
                client.get_sell_price(currency_pair='ETH-USD')['amount'])

    for transaction in btc_transactions['data']:
        if(transaction['type'] == 'buy'):
            print 'Bought', transaction['amount']['amount'], 'BTC on',  transaction['created_at'][:10]
            btc_total = float(transaction['amount']['amount']) * float(
                client.get_sell_price(currency_pair='BTC-USD')['amount'])


def account_totals():
    ''' Get account totals '''

    global eth_total, btc_total

    print '\n***** My Account Totals *****\n'
    print 'My ETH total: $' + str(round(eth_total, 2))
    print 'My BTC total : $' + str(round(btc_total, 2)), '\n'


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

    # Maximum threshold, set to $100 more than initial buying price
    eth_max_threshold = float(client.get_buy_price(
        currency_pair='ETH-USD')['amount']) + 100

    while True:

        # Get current ethereum buy and sell price
        eth_buy_price = float(client.get_buy_price(
            currency_pair='ETH-USD')['amount'])
        eth_sell_price = float(client.get_sell_price(
            currency_pair='ETH-USD')['amount'])

        # $10 worth of ethereum (including $1 fee)
        amount = (9 / eth_buy_price)

        # Buy if conditions match
        if eth_buy_price < eth_max_threshold and eth_total_buy != 10:
            # Buy
            print 'Buying', amount, 'ETH'
            account.buy(amount=amount, currency='ETH',
                        payment_method=payment_method.id)
            eth_total_buy += 10
            print 'ETH total buy:', eth_total_buy
            sleep(5) # sleep for 5 minutes

        # Sell if price goes over max threshold
        if eth_sell_price > eth_max_threshold:
            # Sell
            account.sell(amount=eth_total_buy, currency='ETH',
                         payment_method=payment_method.id)
            print 'Selling', float(eth_total_buy / eth_sell_price), 'ETH'
            sys.exit(1)


def trade_btc():
    ''' Start trading Bitcoin '''

    print 'Trading Bitcoin...'

    # Keep track of buys ($USD)
    btc_total_buy = 0

    # Maximum threshold, set to $100 more than initial buying price
    btc_max_threshold = float(client.get_buy_price(
        currency_pair='BTC-USD')['amount']) + 100

    while True:

        # Get current bitcoin buy and sell price
        btc_buy_price = float(client.get_buy_price(
            currency_pair='BTC-USD')['amount'])
        btc_sell_price = float(client.get_sell_price(
            currency_pair='BTC-USD')['amount'])

        # $10 worth of bitcoin (including $1 fee)
        amount = (9 / btc_buy_price)

        # Buy if conditions match
        if btc_buy_price < btc_max_threshold and btc_total_buy != BTC_MAX_BUY:
            # Buy
            print 'Buying', amount, 'BTC'
            account.buy(amount=amount, currency='BTC',
                        payment_method=payment_method.id)
            btc_total_buy += 10
            print 'BTC total buy:', btc_total_buy
            sleep(5) # Sleep for 5 minutes

        # Sell if price goes over max threshold
        if btc_sell_price > btc_max_threshold:
            # Sell
            account.sell(amount=btc_total_buy, currency='BTC',
                         payment_method=payment_method.id)
            print 'Selling', float(btc_total_buy / btc_sell_price), 'BTC'
            sys.exit(1)

# Quit gracefully with ctrl + c
def sigint_handler(signum, frame):
    print '\nQuitting...'
    sys.exit(1)


signal.signal(signal.SIGINT, sigint_handler)


if __name__ == '__main__':
    current_prices()
    transaction_history()
    account_totals()
    confirm_start()
