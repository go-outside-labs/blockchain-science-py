# -*- encoding: utf-8 -*-
# src/bots/bot1.py
# author: Mia Stein
# Class for trading bot1.
# 
# Strategy:
#   1. set leverage
#   2. start a loop
#       3. check positions
#       4. check active orders
#       5. manage new trades
#           a. check latest z-score signal:
#               if hot:
#                   i. get ticker liquidity
#                   ii. confirm short vs. long tickers
#                   iii. confirm initial capital
#           b. in any case:
#                   i. average in Limit PostOnly orders
#                   ii. or place Market orders
#                   iii. monitor z-score for close signal
#       6. close existing trades
#

import asyncio
import src.utils.os as utils
from src.markets.bybit import BybitCex

class BbBotOne:
    """Deploy trading bot one."""

    def __init__(self, env_vars):

        self._env_vars = env_vars
        self._market = env_vars["BOT1_MARKET_TYPE"].upper()

        try:
            coins = env_vars["BOT1_COINS"]
            self._coin1 = coins.split(',')[0].strip()
            self._coin2 = coins.split(',')[1].strip()
        except IndexError:
            utils.exit_with_error(f'Error obtaining coins for bot1: {coins}')
    
        self._session = BybitCex(self._env_vars, ws=True, market=self._market)

    #########################
    #   private methods     #
    #########################

    def _set_leverage(self):
        """Set leverage for Bot1 to 1, for both buy and sell."""

        self._session.set_leverage(self._coin1, is_isolated=True, buy=1, sell=1)
        self._session.set_leverage(self._coin2, is_isolated=True, buy=1, sell=1)


    #########################
    #   public methods      #
    #########################
    
    def run(self):
        """Start bot1 loop execution."""

        utils.log_info(f"Starting Bot1...")

        utils.log_info(f"Setting leverage for {self._coin1} and {self._coin2}...")
        self._session._change_session(is_public=False)
        self._set_leverage()

        utils.log_info(f"Start seeking for trades...")
        self._session._change_session(is_public=True, ws=True)

        # TODO: finish moving old code to new structure
        try:
            asyncio.get_event_loop().run_until_complete(
                        self._session.orderbook_ws(
                                self._coin1, self._coin2
                            )
                        )
            
            return True

        except KeyboardInterrupt as e:
            utils.log_error(f"Bot1 is stopped: {e}")
            return False

