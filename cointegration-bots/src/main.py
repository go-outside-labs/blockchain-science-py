#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: Mia Stein
# Entry point for cointbot.


import argparse

import src.utils.os as utils
from src.markets.bybit import BybitCex
from src.bots.bot1 import BbBotOne
from src.bots.bot2 import BbBotTwo
from src.strategies.cointegration import Cointegrator


def run_menu() -> argparse.ArgumentParser:
    """Run the menu for this module."""

    parser = argparse.ArgumentParser(description='🤖📉 cointbot 📈🤖')
    parser.add_argument('-c', dest='coin', nargs=1,
                        help='Get data for a derivative currency. \
                            Example: cointbot -d usdt')
    parser.add_argument('-p', dest='price', nargs=1,
                        help='Generates JSON price history for a derivative currency. \
                            Example: cointbot -p usdt')
    parser.add_argument('-i', dest='cointegration', nargs=1,
                        help='Generates CSV cointegration history data for a derivative \
                            currency. Example: cointbot -i usdt')
    parser.add_argument('-o', dest='top', nargs=2,
                        help='Get top <value> scoring cointegration pairs for a \
                            derivative currency. Example: cointbot -o usdt 10')
    parser.add_argument('-t', dest='test', nargs=3, 
                        help='Generates CSV and PNG backtests for a cointegrated pair \
                            and a currency. Example: cointbot -t ethusdt btcusdt usdt')
    parser.add_argument('-n', dest='network', nargs=3, 
                        help='Test websockets for orderbooks, for either spot, \
                            linear, or spot market, for a cointegrated pair. \
                            Example: cointbot -n ethusd btcusd inverse')
    parser.add_argument('-b', dest='bot', nargs=1, 
                        help='Deploy a trading bot using the cointegrated strategy, \
                            from a set of possible market and pairs strategies. \
                            Example: cointbot -b 1')

    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()
    
    env_vars = utils.load_config()
    cex = env_vars['CEX'].upper()


    ##########################################
    #     Get derivative currency info       #
    ##########################################
    if args.coin:
        currency = args.coin[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars, currency)
            data = b.get_derivative_currency_info()

            if data:
                utils.pprint(data)
            else:
                utils.exit_with_error(f'No data found for {currency}.')
        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get price history    #
    ############################
    elif args.price:
        currency = args.price[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars, currency)
            data = b.get_price_history()

            if data:
                outfile = env_vars['PRICE_HISTORY_FILE'].format(currency)
                outdir = env_vars['OUTPUTDIR']
                utils.save_price_history(data, outdir, outfile)
            else:
                utils.exit_with_error(f'Could not retrieve price history for {currency}')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get cointegration    #
    ############################
    elif args.cointegration:
        currency = args.cointegration[0].upper()

        if cex == 'BYBIT':
            s = Cointegrator(env_vars, currency)
            data = s.get_cointegration()

            if not data.empty:
                utils.log_info(data)
                
            else:
                utils.exit_with_error(f'No data found for {currency}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ################################
    #  Get top cointegrated pairs  #
    ################################
    elif args.top:
        currency = args.top[0].upper()
        top = int(args.top[1].upper())

        if cex == 'BYBIT':
            s = Cointegrator(env_vars, currency)
            data = s.get_best_cointegrated_pairs(top)

            if data is not None:
                utils.pprint(f'Top {top} cointegrated pairs for {currency}:')
                utils.pprint(data)
                
            else:
                utils.exit_with_error(f'No data found for {currency}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get backtests        #
    ############################
    elif args.test:
        coin1 = args.test[0].upper()
        coin2 = args.test[1].upper()
        currency = args.test[2].upper()

        if not coin1.endswith(currency) or not coin2.endswith(currency):
            utils.exit_with_error(f'{coin1}/{coin2} had wrong currency: {currency}')

        if cex == 'BYBIT':
            s = Cointegrator(env_vars, currency)
            data = s.get_backtests(coin1, coin2)

            if not data.empty:
                utils.log_info(data)
            else:
                utils.exit_with_error(f'Could not get backtests for {cex}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Test network         #
    ############################
    elif args.network:
        coin1 = args.network[0].upper()
        coin2 = args.network[1].upper()
        market = args.network[2].upper()

        if market not in ['INVERSE', 'LINEAR', 'SPOT']:
            utils.exit_with_error(f'Market not supported: {market}')

        if cex == 'BYBIT':
            b = BybitCex(env_vars, ws=True, market=market)
            b.open_orderbook_ws(coin1, coin2)
            
        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Deploy bot           #
    ############################
    elif args.bot:
        bot_number = args.bot[0].upper()
    
        if cex == 'BYBIT':

            if bot_number == '1':
                b = BbBotOne(env_vars)
                success = b.run()
                if not success:
                    utils.exit_with_error(f'Could not deploy bot for {cex}.')
            
            elif bot_number == '2':
                b = BbBotTwo(env_vars)
                success = b.run()
                if not success:
                    utils.exit_with_error(f'Could not deploy bot for {cex}.')
            else:
                utils.exit_with_error(f'Bot number not yet supported: {bot_number}')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 