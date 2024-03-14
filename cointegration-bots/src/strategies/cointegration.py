# -*- encoding: utf-8 -*-
# src/strategies/cointegration.py
# author: Mia Stein
# Cointegration class.

import math
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

import src.utils.os as utils
import src.utils.plots as plots

class Cointegrator:

    def __init__(self, env_vars: dict, currency=None):

        self._env_vars = env_vars
        self.currency = currency or 'USDT'
        self._pvalue_limit = float(self._env_vars['PLIMIT'])
        self._outdir = self._env_vars['OUTPUTDIR']
        self._price_file = self._env_vars['PRICE_HISTORY_FILE'].format(self.currency)
        self._cointegration_file = self._env_vars['COINTEGRATION_FILE'].format(self.currency)
        self._zscore_file = self._env_vars['ZSCORE_FILE'].format(self.currency)
        self._backtest_file = self._env_vars['BACKTEST_FILE']
        self.zscore_list = []
        self.backtest_df = None
        self.cointegration_results = [] 

    #########################
    #   private methods     #
    #########################
    def _get_price_history(self) -> dict:
        """Get price history for a given derivative."""
        
        price_history = utils.open_price_history(self._outdir, self._price_file)
        if price_history is None:
            utils.exit_with_error(f'You need to generate price history first.')
        
        return price_history

    def _extract_close_prices(self, prices_list: list) -> list:
        """Extract all close prices info into a list."""

        close_prices = []

        for prices in prices_list:
            try:
                if not math.isnan(prices["close"]):
                    close_prices.append(prices["close"])
            except KeyError:
                utils.log_error(f'Could not find close price for {prices}')

        return close_prices

    def _calculate_spread(self, first_set: list, second_set: list, hedge_ratio: float) -> list:
        """Calculate spread."""

        return pd.Series(first_set) - (pd.Series(second_set) * hedge_ratio)

    def _calculate_hedge_ratio(self, first_set: list, second_set: list) -> float:
        """Calculate hedge ratio by fiting Ordinary Least Squares (OLS) model."""

        model = sm.OLS(first_set, second_set)
        return model.fit().params[0]

    def _calculate_zscore(self, spread: list) -> list:
        """Calculate zscore."""

        df = pd.DataFrame(spread)

        window = int(self._env_vars['ZSCORE_WINDOW'])
        mean = df.rolling(center=False, window=window).mean()
        std = df.rolling(center=False, window=window).std()
        x = df.rolling(center=False, window=1).mean()
        
        df["zscore"] = (x - mean) / std

        zscore = df["zscore"].astype(float).values
        self.zscore_list.append(zscore)
        return zscore

    def _get_pair_cointegration(self, first_set: list, second_set: list) -> dict:
        """Calculate co-integration for two tokens."""
        
        # calculate cointegration
        cointegration = coint(first_set, second_set)
        cointegration_value = cointegration[0]
        pvalue = cointegration[1]
        critical_value = cointegration[2][1]
        
        # calculate hedge ratio
        hedge_ratio = self._calculate_hedge_ratio(first_set, second_set)
        
        # calculate spread
        spread = self._calculate_spread(first_set, second_set, hedge_ratio)

        # calculate zero crossings
        zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])

        # calculate zscore
        self._calculate_zscore(spread)

        # calculate hot
        hot = False
        # if pvalue is less than 0.05, we can reject the null hypothesis
        if pvalue < self._pvalue_limit and cointegration_value < critical_value:
            hot = True

        return {
                "hot": hot,
                "pvalue": round(pvalue, 3),
                "cointegration_value": cointegration_value,
                "critical_value": critical_value,
                "hedge_ratio": hedge_ratio,
                "zero_crossings": zero_crossings
                }

    def _get_backtest_data(self, coin1: str, coin2: str) -> None:
        """Save backtest data to file."""

        # get price history
        price_history = self._get_price_history()

        # extract close prices
        try:
            first_set = self._extract_close_prices(price_history[coin1])
            second_set = self._extract_close_prices(price_history[coin2])
        except KeyError:
            utils.exit_with_error(f"Price history does not have {coin1} or {coin2}.")

        # fix if the two sets are not the same length
        if len(first_set) != len(second_set):
            first_set, second_set = self._create_equal_length_sets(first_set, second_set)

        # create dataframe
        df = pd.DataFrame()
        df[coin1] = first_set
        df[coin2] = second_set

        # calculate percentage change
        df[f'{coin1}_perc'] = (df[coin1] / first_set[0]).astype(float).values
        df[f'{coin2}_perc'] = (df[coin2] / second_set[0]).astype(float).values

        # calculate hedge ratio
        hedge_ratio = self._calculate_hedge_ratio(first_set, second_set)

        # calculate spread
        spread = self._calculate_spread(first_set, second_set, hedge_ratio)
        df['spread'] = spread

        # calculate zscore
        df['zscore'] = self._calculate_zscore(spread)

        # save results
        self.backtest_df = df
        outuput_file = self._backtest_file.format(coin1, coin2)
        utils.save_metrics(self.backtest_df, self._outdir, outuput_file)
        plots.plot_cointegrated_pair(df, coin1, coin2, self._env_vars)

    def _get_file_data(self, filepath) -> bool:
        """Check if a result file exists else calculates cointegration data."""

        if utils.file_exists(self._outdir, filepath):
            return utils.open_metrics(self._outdir, filepath)
        
        else:
            utils.log_info(f'Calculating cointegration first...')  
            self.get_cointegration()
            return None

    def _create_equal_length_sets(self, first_set: list, second_set: list) -> tuple:
        """Create equal length for two lists."""

        utils.log_info(f'Set lenghts are not equal: fixing it.')

        if len(first_set) > len(second_set):
            first_set = first_set[-len(second_set):]
        else:
            second_set = second_set[-len(first_set):]

        return first_set, second_set


    ###########################
    #      public methods     #
    ###########################

    def get_best_cointegrated_pairs(self, top: int) -> pd.DataFrame:
        """Get best cointegration pairs."""

        df = self._get_file_data(self._cointegration_file)
        if df is None:
            df = pd.DataFrame(self.cointegration_results)

        df.drop(columns=['hot', 'critical_value'], inplace=True)
        df.sort_values(by=['pvalue'], inplace=True, ascending=False)
        top_pairs = df.head(top)

        # get backtest data and plot for every top cointegrated pairs
        coin1_list = top_pairs['coin1'].tolist()
        coin2_list = top_pairs['coin2'].tolist()

        # plot backtest data for each top pair
        for coin1, coin2 in zip(coin1_list, coin2_list):
            self._get_backtest_data(coin1, coin2)

        return top_pairs

    def get_cointegration(self) -> pd.DataFrame:
        """Get and store price history for all available pairs."""

        if utils.file_exists(self._outdir, self._cointegration_file) and \
                    utils.file_exists(self._outdir, self._zscore_file):
            return utils.open_metrics(self._outdir, self._cointegration_file)
 
        hot_pairs = []
        price_history = self._get_price_history()

        for coin1 in price_history.keys():
            utils.log_info(f'Calculating cointegration for {coin1}...')

            for coin2 in price_history.keys():
                if coin1 != coin2:

                    this_symbol = "".join(sorted([coin1, coin2]))
                    if this_symbol in hot_pairs:
                        break
                    
                    # extract close prices f
                    first_set = self._extract_close_prices(price_history[coin1])
                    second_set = self._extract_close_prices(price_history[coin2])

                    # fix if the two sets are not the same length
                    if len(first_set) != len(second_set):
                        first_set, second_set = self._create_equal_length_sets(first_set, second_set)

                    # calculate co-integration
                    cointegration_dict = self._get_pair_cointegration(first_set, second_set)

                    # if the pair is cointegrated, add to hot pairs
                    if cointegration_dict['hot'] == True:
                        utils.log_info(f'   ✅ Found a hot pair: {coin1} and {coin1}')
                        hot_pairs.append(this_symbol)
                        cointegration_dict['coin1'] = coin1
                        cointegration_dict['coin2'] = coin2
                        self.cointegration_results.append(cointegration_dict)
        
        # save results
        utils.save_metrics(self.zscore_list, self._outdir, self._zscore_file)
        return utils.save_metrics(self.cointegration_results, self._outdir, \
                                self._cointegration_file, 'zero_crossings',)


    def get_zscore(self) -> pd.DataFrame:
        """Get z-score for a given window."""

        df = self._get_file_data(self._zscore_file)
        if df is None:
            df = pd.DataFrame(self.zscore_list)

        return df


    def get_backtests(self, coin1: str, coin2: str) -> pd.DataFrame:
        """Run backtests for all pairs, based on spread and zscore."""

        self._backtest_file = self._backtest_file.format(coin1, coin2)
        df = self._get_file_data(self._backtest_file)
        
        if df is None:
            self._get_backtest_data(coin1, coin2)
            df = self.backtest_df
        
        return df