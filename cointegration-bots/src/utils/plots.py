# -*- encoding: utf-8 -*-
# src/utils/plots.py
# author: Mia Stein
# Methods to plot data.

import matplotlib.pyplot as plt
import src.utils.os as utils


def plot_cointegrated_pair(data: dict, coin1: str, coin2: str, env_vars: dict) -> None:
    """Plot cointegrated pairs."""

    ########################
    # create figure and axis
    ########################

    figure, axis = plt.subplots(3, figsize=(20, 20))
    figure.suptitle(
        f"Cointegration (timeframe: {env_vars['TIMEFRAME']})",
        fontsize=30,
        fontweight='bold',
        family='monospace',
    )


    ##############
    # plot series
    ##############

    series1 = data[f'{coin1}_perc']
    series2 = data[f'{coin2}_perc']
    axis[0].plot(series1, color='red', label=f'{coin1}', linewidth=2)
    axis[0].plot(series2, color='blue', label=f'{coin2}', linewidth=2)
    axis[0].set_xlim([0, len(series2)])
    axis[0].grid(color="grey", axis="x", linestyle="solid", linewidth=1)
    axis[0].grid(color="grey", axis="y", linestyle="dotted", linewidth=1)
    axis[0].set_title(
        f'Price series for {coin1} vs. {coin2} ', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[0].set_xlabel(
        'close prices data', 
        fontweight ='bold',
        fontsize=12,
    )
    axis[0].set_ylabel(
        '％ change', 
        fontweight ='bold',
        fontsize=12,
    )


    #############
    # plot spread
    #############

    axis[1].plot(data['spread'], color='green', linewidth=3)
    axis[1].set_xlim([0, len(data['spread'])])
    axis[1].grid(color="grey", axis="x", linestyle="solid", linewidth=1)
    axis[1].grid(color="grey", axis="y", linestyle="dotted", linewidth=1)
    axis[1].set_title(
        'Spread', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[1].set_ylabel(
        'series1 - (series2 * hedge ratio)', 
        fontweight ='bold',
        fontsize=12,
    )
    axis[1].set_xlabel(
        'close prices data', 
        fontweight ='bold',
        fontsize=12,
    )

    ###############
    # plot z-score
    ###############
    
    axis[2].plot(data['zscore'], color='magenta', linewidth=3)
    axis[2].grid(color="grey", axis="x", linestyle="solid", linewidth=1)
    axis[2].grid(color="grey", axis="y", linestyle="dotted", linewidth=1)
    axis[2].set_xlim([0, len(data['zscore'])])
    axis[2].set_title(
        'Z-score', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[2].set_xlabel(
        'close prices data', 
        fontweight ='bold',
        fontsize=12,
    )
    axis[2].set_ylabel(
        'σ (current price from mean price) ', 
        fontweight ='bold',
        fontsize=12,
    )

    
    ##############
    #  save plot
    ##############
    plot_name = f"{coin1}_{coin2}_{env_vars['TIMEFRAME']}_cointegration.png"
    plot_filename = utils.format_path(env_vars['OUTPUTDIR'], plot_name)
    plt.savefig(plot_filename)
    utils.log_info(f"Saving plot to {plot_filename}")
