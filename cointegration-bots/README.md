## 🤖✨ cointegration trading bots

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/1130416/210929847-12a60847-954e-4d4e-a1eb-da5215e14ffb.jpeg" width="42%" align="center" style="padding:1px;border:1px solid black;"/>
 </p>
 



<br>

### tl; dr

<br>

* `coitnbot` is a **CLI tool and a set of trading bots** that i’ve written to detect **profitable cryptocurrency pairs to be shorted or longed** on trading exchanges.
* these statistical algorithmic strategies are named **cointegration**, which has been around for a long time, for either traditional or decentralized finances.
* 📚 for more details, check **[my mirror post, bot #2: cointbot, a cointegration trader](https://mirror.xyz/Mia Stein.eth/KQ0basHaclOCDDtOhz3NgKQhHdHqaqOtU89Sr4QO5L4)**.
* 🚨 **disclaimer**: i open-source my projects because i am a believer in the oss ethos. you might or might not profit from it, but this is not my problem. in the mev world, nobody is going to (explicitly) handle you alphas. i am not responsible for anything you do with my free code.

<br>

----


### 🧘🏻‍♀️✨ cointegration strategy for pair trading

<br>


![annotely_image](https://user-images.githubusercontent.com/1130416/210931729-01e831a9-a6b4-465d-9c52-1524219aabd7.png)


<br>

* pair trading is a classic example of a strategy based on mathematical analysis.
* put it simply, when two or more **non-stationary series can be combined to make a stationary series, they are said to be cointegrated**.
* in other words, this strategy allows you to find evidence of an underlying economic link for a pair of securities (say, A and B) within a timeframe. it also allows you to mathematically model this link, so that you can make trades on it.

> 💡 *a **series** are said to be stationary when the parameters of the data-generating process do not change over time.*

<br>

#### modeling a pair of securities with math

<br>

* let’s take two random crypto assets, say, **A and B futures**. let’s model each of their returns by drawing their **normal distributions** (aka the **[bell curve](https://www.investopedia.com/terms/b/bell-curve.asp)**). 

> 💡 ***crypto derivatives** are financial contracts that derive their values from underlying assets. futures are financial contracts that bet on a cryptocurrency's future price, allowing exposure without purchasing.*

* if these two series are cointegrated, there exists some **linear combination between them varying around a mean**. in other words, their combination should be related to the **same probability distribution**.


<br>



#### the beauty of p-values

<br>

* **correlation and cointegration are similar but not the same**. for example, correlated series could just diverge together without being cointegrated.
* how do we infer cointegration? we do like the scientists do: a **p-value** is the probability of obtaining results at least as extreme as the results of a hypothesis test, assuming that the **[null hypothesis](https://www.investopedia.com/terms/n/null_hypothesis.asp)** is correct.
* a **p-value of 0.05 or lower** is generally considered statistically **significant**.
* cointegrated series can show very small p-values but still not be correlated.


<br>




#### the trick of pair trading


<br>

* the **coefficients that define stationary combinations of two series are called hedge ratios**. in practical terms, the hedge ratio describes the suggested **amount of B to buy or sell for every of A**.
* because both securities drift towards and apart from each other, sometimes the distance is high, and sometimes the distance is low.
* the magick comes from **maintaining a hedged position across A and B**. if both go down or up, you neither make nor lose money. **profit comes from the spread of them reverting to the mean**:

```
- when A and B are far apart, you short B and long A: when the spread is small, you expect it to become larger.
- when A and B are close, you long B and short A: when the spread is large, you expect it to become larger.
```

<br>


#### spread and z-score


<br>


* we apply a **linear regression** to calculate the spread of these two series, which is simply defined by:

```
spread = first series - (hedge ratio * second series)  
```


* this gives us that linear combination coefficient, the hedge ratio (this is known as the **[engle-granger method](https://www.statisticshowto.com/engle-granger-test/)**).
* however, the spread does not give you an immediate signal for trading. the signal still needs to be normalized so it can be treated as a **z-score**, which is the number of **[standard deviations](https://www.investopedia.com/terms/s/standarddeviation.asp)** separating the **current price from the mean price**.
* traders can look at the **momentum of the average z-score** and takes a contrarian approach to trade, to generate **buy and sell signals**. graphically, **positive z-scores lie to the right** of the mean, and **negative z-scores lie to the left** of the mean.
* here is an example of a strategy:

```
- whenever the z-score < -1, you long the spread.
- whenever the z-score > 1, you short the spread.
- exit positions when the z-score ~ 0.
``` 

<br>

#### “there are three types of lies: lies, damn lies, and statistics”

<br>

* math is awesome, but obviously, any trading strategy comes with advantages and shortcomings:

<br>

| 😎 **PROS** 😎                           | 😭 **CONS** 😭                                             |
| -----------                              | -----------                                            |
| profit in up, down, or sideways markets  | behaviors are not guaranteed to continue               |
| use rebates on two assets                | high entry barrier 🧠                                   |
| clear signals for entry and exit         | involves shorting                                      |
| mathematical edge                        | market-based orders, costs double                      |
| scale for larger capital                 | entry and exit in parallel with limit-orders is tricky |

<br>



---



### 🧘🏾✨ the `cointbot` package

<br>

* the `cointbot` package consists of a CLI and a set of libraries for cointegration pair trading, with support for different market types, parameters, and bots designs:

<br>


```
📂 cointegration-bots
    ┣ 📂 src
        ┣ main.py
        ┣ 📂 markets
            ┣ bybit.py
            ┣ (...)
        ┣ 📂 bots
            ┣ bot1.py
            ┣ (...)
        ┣ 📂 strategies
            ┣ cointegration.py
            ┣ (...)
        ┣ 📂 utils
            ┣ os.py
            ┣ (...)
    ┣ 📂 results
    ┣ 📂 docker
```

<br>



* for example, `Bot1` has the following strategy:

```
1️⃣ search for all possible crypto perpetual derivative contracts in a cex that can be longed or shorted
2️⃣ retrieve their price history for a given timeframe
3️⃣ calculate all the pairs that cointegrated by looking at p-values smaller than a certain threshold
4️⃣ calculate their spread and their latest z-score signal
5️⃣ backtest to long when z-score < 0
6️⃣ if the asset is hot, confirm tokens to be longed and shorted, within the initial capital
7️⃣ with these close signals, average in limit orders or place market orders
```


<br>



#### setting up `cointbot`

<br>

* to test `cointbot`, you will need a testnet account from some cex. we currently have full support for **[bybit](https://testnet.bybit.com/en-US/)**. if you want to use any other cex, the code is free (or wait until i have time to implement them).
* after cloning `cointbot`, add system and trading config to a `.env` file:

<br>

```
cp .env.example .env
vim .env
```

<br>

* then, install with:

```
virtualenv venv
source venv/bin/activate
make install_deps
make install
cointbot
```

<br>


> ✅ you are now all set to explore `cointbot`:

<br>

<img width="765" alt="Screen Shot 2023-01-05 at 7 59 57 PM" src="https://user-images.githubusercontent.com/1130416/210927413-cdd0e66d-dde7-4bed-bb60-bb7825e10ca1.png">


<br>

---


### 🧘🏿‍♀️✨ fetching a perpetual currency’s data

<br>

> 💡 *a **perpetual contract** is a contract that can be held in perpetuity, i.e., indefinitely until the trader closes their position.*


* let’s start testing `cointbot` by running the simplest option, which is simply calling bybit’s API to query the market data for all derivatives (symbols) for a given currency (*e.g.*, `USDT`):

```
cointbot -c usdt
```


* here is an example of the output:

<br>

<img width="562" alt="Screen Shot 2023-01-05 at 8 00 30 PM" src="https://user-images.githubusercontent.com/1130416/210927475-55cc7ef3-6262-447d-91b5-5d8d6b975094.png">


<br>

---


### 🧘🏼✨ fetching price history for a derivative currency

<br>


* the second menu option queries the market price k-lines for all symbols above in a given `TIMEFRAME` and `KLINE-LIMIT`, not only printing them to `STDOUT` but also saving them as `JSON` to `OUTPUTDIR/PRICE_HISTORY_FILE`:

```
cointbot -p usdt
```

> 💡 *in the context of trading, a **k-line** represents the **fluctuation of asset prices** in a given time frame. It shows the **close price, open price, high price, and low price**. if the close price > open price, the k-line has a positive line. otherwise, it is a negative line.*


* here is an example of output:

<br>

<img width="569" alt="Screen Shot 2023-01-05 at 8 02 00 PM" src="https://user-images.githubusercontent.com/1130416/210927617-c2a1ff3b-1556-41b3-a922-747f952d1b9b.png">


<br>


>💡 *bybit employs a **[dual-price mechanism](https://www.bybit.com/en-US/help-center/bybitHC_Article/?id=360039261074&language=en_US)** to prevent market manipulations (when the market price on a futures exchange deviates from the spot price, causing mass liquidation of traders' positions). the dual-price mechanism consists of mark price and last traded price. "mark price" refers to a global spot price index plus a decaying funding basis rate, and it's used as a trigger for liquidation and to measure unrealized profit and loss. "last traded price" is the current market price, anchored to the spot price using the funding mechanism.*



<br>

---


### 🧘🏽‍♀️✨ calculating cointegration for the history data

<br>

* with the price history data from the previous step, we can now calculate cointegration for each symbol (for the desired `PLIMIT` , the chosen p-value that defines a "hot" pair:

```
cointbot -i usdt
```

* here is an example of output:

<br>

<img width="640" alt="Screen Shot 2023-01-05 at 8 54 14 PM" src="https://user-images.githubusercontent.com/1130416/210932784-dc780e9c-5aeb-423e-aa0b-1dc189bfa6c8.png">




<br>

* this step will also calculate **p-values**, **hedge ratios**, and **zero crossings**. the resulting Pandas' `DataFrame` is then saved at `OUTPUTDIR/COINTEGRATION_FILE`, sorted by `zero_crossing`.

> 💡 *in statistics, **zero crossing** is a point where the sign of function changes. In the context of trading, it determines an entry point (using the price in relation to the moving average as a direction confirmation).*


<br>

---


### 🧘🏼‍♀️✨ backtesting a cointegrated pair

<br>

> 💡 *in the context of crypto trading, **backtesting** is accomplished by reconstructing, with historical data, trades that would have occurred in the past using rules defined by a given strategy, gauging the effectiveness of the strategy.*


* select your favorite asset pair from the previous step, and let’s backtest their cointegration by testing the success of the hypothesis (and making some cool plots for their series’ spreads and z-score).

```
cointbot -t usdt bnbusdt algousdt usdt
```

* example of output for `BNBUSDT` vs. `ALGOUSDT`:

<br>

<img width="565" alt="Screen Shot 2023-01-05 at 8 04 51 PM" src="https://user-images.githubusercontent.com/1130416/210927908-0b1872f1-eb9c-48e9-ad01-a92f76acf873.png">


<br>


* by the way, this command also generates their cointegration plots and backtest data, and saves them at `OUTPUTDIR/`.


> 💡 *lil tip: if you are starting an entirely new run, clean up the current setup with `make clean_data`.*


<br>

---


### 🧘🏽‍♂️✨ looking at the top cointegrated pairs

<br>


* once we have all data from the previous step, we can look at the top cointegrated securities for the given `TIMEFRAME` and `NUMBER`:

```
cointbot -o usdt 10
```

* example of output:

<br>

<img width="567" alt="Screen Shot 2023-01-05 at 8 05 52 PM" src="https://user-images.githubusercontent.com/1130416/210928004-1341af1b-8fe1-4b6f-8090-3b7bbdc279bb.png">


<br>


* note that this command automatically generates the backtesting data and plots (similar to the previous option).

> ✅ congrats, you now understand cointegration pair trading. it’s time to move to our trading bots.

<br>

---


### 🧘🏾‍♀️✨ testing orderbooks websockets

<br>


* our bot will be connecting to bybit’s through both REST APIs and websockets endpoints. let’s start by testing the last one.
* to open a websocket subscribed to a cointegration pair (either for spot, linear, or inverse markets), run:

```
cointbot -n bnbusdt algousdt linear
```

<br>


##### topics for spot market

<br>

* spot market topics are implemented by the `trade_v1_stream()` method, which pushes raw data for each trade (**[API docs here](https://bybit-exchange.github.io/docs/spot/v1/#t-websocket)**).
* after a successful subscription message, the first data message (`f: true`), consists of the last 60 trades.
* after (`f: false`), only new trades are pushed (at a frequency of 300ms, where the message received has a maximum delay of 400ms).
* example of output:

<br>

<img width="470" alt="Screen Shot 2023-01-05 at 8 21 44 PM" src="https://user-images.githubusercontent.com/1130416/210929534-81e4ce6a-72f1-4958-8817-1bf10e2592a8.png">


<br>

##### topics for inverse perpetual/futures market

<br>

* inverse market topics are implemented with orderbook_25_stream(), which fetches the orderbook with a depth of 25 orders per side (**[API docs here](https://bybit-exchange.github.io/docs/futuresV2/inverse/#t-websocketresponse)**).
* after the subscription response, the first response will be the snapshot response, showing the entire orderbook.
* the data is ordered by price (starting with the lowest buys). push frequency is 20ms.
* example of output:

<br>

<img width="474" alt="Screen Shot 2023-01-05 at 8 22 32 PM" src="https://user-images.githubusercontent.com/1130416/210929582-b7cf29dd-218c-40f6-b11d-cb5adb8c3244.png">


<br>


#### topics for USDT linear perpetual

<br>

* finally, USDT linear market topics are implemented with orderbook_25_stream(), which fetches the orderbook with a depth of 25 orders per side (**[API docs here](https://bybit-exchange.github.io/docs/futuresV2/linear/#t-websocketresponse)**).
* the first response is the snapshot response, showing the entire orderbook.
* the data is ordered by price, starting with the lowest buys and ending with the highest sells. push frequency is 20ms.
* example of output:

<br>

<img width="467" alt="Screen Shot 2023-01-05 at 8 23 02 PM" src="https://user-images.githubusercontent.com/1130416/210929620-ea22c837-3bcb-474b-8331-ffa627c2f66f.png">




<br>

---

### 🧎🏻‍♀️✨ deploying a cointegrated trading bots

<br>

* several bots with different strategies are found inside `src/bots/`. 
* each bot has a different number and configuration settings in the `.env` file (*e.g.*, `BOT_COINS`, `BOT_MARKET_TYPE`, `BOT_ORDER_TYPE`, `BOT_STOP_LOSS`, `BOT_TRADEABLE_CAPITAL`, and others). before the next step, you should check them out (and understand their effects).

<br>


#### high-level strategy for Bot1


<br>

* this is how `Bot1` gets set up:


<img width="469" alt="Screen Shot 2023-01-05 at 8 09 14 PM" src="https://user-images.githubusercontent.com/1130416/210928356-78811616-a52a-427a-9888-133eef41b77b.png">


<br>
<br>

* and this is how `Bot1` executes, inside a `while True` loop:


<img width="474" alt="Screen Shot 2023-01-05 at 8 23 52 PM" src="https://user-images.githubusercontent.com/1130416/210929707-6d41898e-c323-4100-84d7-5ad296e58a98.png">



<br>
<br>



* you should check the code (the main class is called `BbBotOne`), and then spin this babe up:

```
cointbot -b 1
```

<br>

###### running on docker

* if you would like to run bot1 on docker, make sure you have **[docker](https://docs.docker.com/compose/install/)** and **[docker compose](https://formulae.brew.sh/formula/docker-compose)** installed, and run:

```
make bot1
```


<br>

⬛️


<br>

----


### resources

<br>


* [pybit documentation](https://openbase.com/python/pybit/documentation)
* [bybit documentation](https://pub.dev/documentation/bybit/latest/bybit/bybit-library.html)
* [bybit postman setup](https://github.com/bybit-exchange/QuickStartWithPostman)
* [cointegration-based pairs trading strategy in the cryptocurrency market](https://arxiv.org/abs/2109.10662)
* [constructing cointegrated cryptocurrency portfolios](https://towardsdatascience.com/constructing-cointegrated-cryptocurrency-portfolios-d0a27922891e)

