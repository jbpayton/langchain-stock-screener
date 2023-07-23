Here's your reformatted markdown document with the Table of Contents updated. I've also incorporated the changes you wanted in the Requirements and Important Information sections.

# Alpaca Stock Screener

The Alpaca Stock Screener is a Python tool designed to be used with LangChain agents, enabling stock analysis using various technical indicators. The tool takes a natural language query as input and returns a list of stocks whose technical indicators match the query.

This tool uses an internal dataframe for this data and handles operations internally. Note that this tool does not handle queries involving fundamental indicators like earnings growth or debt-to-equity ratio.

For more information on LangChain, refer to the [LangChain documentation](https://python.langchain.com/)

## Table of Contents
- [Requirements](#requirements)
- [Files](#files)
- [Technical Indicators](#technical-indicators)
- [Installation](#installation)
- [Usage](#usage)
- [Important Information](#important-information)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contact](#contact)
- [Contributions](#contributions)

## Requirements

This code requires several key-value pairs either in a `secrets.json` file or as environment variables. Make sure to fill in the placeholders with your actual data.

The keys needed are:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ALPACA_URL`: Your Alpaca URL
- `ALPACA_KEY`: Your Alpaca key
- `ALPACA_SECRET`: Your Alpaca secret

### secrets.json

Create a `secrets.json` file in the root directory of this project and populate it as follows:

```json
{
  "OPENAI_API_KEY": "<your-openai-api-key>",
  "ALPACA_URL": "<your-alpaca-url>",
  "ALPACA_KEY": "<your-alpaca-key>",
  "ALPACA_SECRET": "<your-alpaca-secret>"
}
```

### Environment Variables

Alternatively, you can set these as environment variables in your operating system:

```bash
export OPENAI_API_KEY=<your-openai-api-key>
export ALPACA_URL=<your-alpaca-url>
export ALPACA_KEY=<your-alpaca-key>
export ALPACA_SECRET=<your-alpaca-secret>
```

Remember to replace `<your-openai-api-key>`, `<your-alpaca-url>`, `<your-alpaca-key>`, and `<your-alpaca-secret>` with your actual data.

## Files

This repository includes the following Python scripts:

1. `alpaca_stock_screener/tool.py`: Defines the `StockScreenerTool` class that screens stocks based on the given query.
2. `alpaca_stock_screener/StockScreener.py`: Defines the `StockScreener` class that handles data management and stock screening calculations.
3. `agenttest.py`: Initialises a simple agent and runs a query using the `StockScreenerTool`.
4. `BabyAGITest.py`: This is a more complex example that shows the `StockScreenerTool` being integrated within a LangChain's Baby AGI setup, along with other tools.

## Technical Indicators

The technical indicators used in this tool include:

- Current price
- 52-week, 26-week, and 13-week high and low
- Short-term, medium-term, and long-term volatility
- 5-day, 10-day, 20-day, 50-day, 100-day, and 200-day moving averages
- Percent change from 52-week, 26-week, and 13-week high and low
- Percent change from 200-day, 100-day, 50-day, 20-day, 10-day, and 5-day moving averages
- 14-day RSI
- Beta
- Average daily volume

Note: I am certain that there could be better and more efficient calculations for some of these indicators. If you have any suggestions, please feel free to create an issue in this repository.

## Installation

This project has been tested with Python 3.9.

To install the required packages, run the following command:

```
pip install -r requirements.txt
```

`requirements.txt` file:

```
numpy~=1.23.5
langchain~=0.0.219
numba~=0.56.4
pandas~=2.0.2
pytz~=2023.3
beautifulsoup4~=4.12.2
requests~=2.28.1
faiss-cpu
duckduckgo-search
alpaca_trade_api
pandas_market_calendars
tabulate
```

## Usage

For simple usage, refer to `agenttest.py`.

For a more complex example of integrating the `StockScreenerTool` within LangChain's Baby AGI setup, refer to `BabyAGITest.py`.

Please note that the `StockScreenerTool` does not support asynchronous operations.

```> Entering new AgentExecutor chain...
To answer this question, I need to define what makes a stock a "good buy". There are many strategies for this, but a common one is to look for stocks that are undervalued compared to their intrinsic value. However, the Stock Screener tool I have access to only provides technical indicators, not fundamental ones like earnings or book value that could help estimate intrinsic value. Therefore, I'll have to use a technical strategy. One simple strategy is to look for stocks that are currently trading at a low price compared to their 52-week high, but have started to rebound recently. This could indicate that they were oversold and are now starting to recover. I'll use the Stock Screener to find stocks that meet these criteria.
Action: Stock Screener
Action Input: Find stocks where the current price is less than 80% of the 52-week high, but greater than the 5-day moving average.Syncing Index Data (SPY) from 2022-07-23 to present...
Syncing Data for DTN (555 of 588) from 2022-07-23 to present...
Syncing Data for FLGE (558 of 588) from 2022-07-23 to present...
Syncing Data for BGU (564 of 588) from 2022-07-23 to present...
Syncing Data for BGZ (582 of 588) from 2022-07-23 to present...


> Entering new AgentExecutor chain...

Invoking: `python_repl_ast` with `df_filtered = df[(df['current_price'] < 0.8 * df['high_52_week']) & (df['current_price'] > df['ma_5_day'])]
df_filtered.head(20)`


    symbol                     last_updated  current_price  high_52_week  \
10     AAP 2023-07-23 16:25:11.659734-04:00        70.7200       194.350   
11     AES 2023-07-23 16:25:12.355730-04:00        22.0000        30.020   
13       A 2023-07-23 16:25:13.875744-04:00       127.6200       160.265   
18     ARE 2023-07-23 16:25:17.918131-04:00       123.0000       172.650   
22     ALL 2023-07-23 16:25:21.046823-04:00       110.8200       142.150   
27    AMCR 2023-07-23 16:25:26.952213-04:00        10.1499        13.000   
39    AMGN 2023-07-23 16:25:37.217837-04:00       234.7000       298.000   
44     APA 2023-07-23 16:25:41.252774-04:00        38.5800        48.550   
51     AIZ 2023-07-23 16:25:47.878831-04:00       129.5400       176.310   
60    BALL 2023-07-23 16:25:56.249697-04:00        57.5900        74.350   
65     WRB 2023-07-23 16:26:01.953410-04:00        61.5700        76.990   
68     BIO 2023-07-23 16:26:04.419900-04:00       414.1800       572.700   
69    TECH 2023-07-23 16:26:05.383806-04:00        89.4200       397.340   
76     BXP 2023-07-23 16:26:13.199084-04:00        63.5100        87.790   
78     BMY 2023-07-23 16:26:14.716104-04:00        64.8000        81.435   
87     CPT 2023-07-23 16:26:23.526006-04:00       112.9000       147.715   
94    CTLT 2023-07-23 16:26:31.017094-04:00        47.5900       102.900   
100    CNC 2023-07-23 16:26:37.016699-04:00        70.6300        97.730   
103     CF 2023-07-23 16:26:39.416922-04:00        79.3000       112.440   
105   SCHW 2023-07-23 16:26:41.579051-04:00        66.3500        86.630   

     low_52_week  high_26_week  low_26_week  high_13_week  low_13_week  \
10       63.5000      149.1700      63.5000      122.8200      63.5000   
11       19.2500       26.7700      19.2500       23.0700      19.2500   
13      113.2801      158.4900     113.2801      137.1600     113.2801   
18      108.8100      172.6500     108.8100      124.7900     108.8100   
22      100.5730      139.0200     100.5730      119.9878     100.5730   
27        9.1100       11.9000       9.1100       11.0900       9.1100   
39      211.7100      257.1500     211.7100      238.4800     211.7100   
44       30.5000       41.1100      30.6700       38.7750      30.6700   
51      104.4900      136.5500     104.4900      134.8200     115.4300   
60       46.0000       62.1400      49.7000       61.1300      50.8200   
65       55.5000       75.5300      55.5000       64.7500      55.5000   
68      344.6300      516.9700     356.5100      489.3550     356.5100   
69       69.8050       89.9100      69.8050       89.9100      74.1300   
76       46.1803       73.2000      46.1803       64.5750      46.8000   
78       61.4050       71.0650      61.4050       67.1600      61.4050   
87       97.7400      127.6000      97.7400      114.0400     101.7400   
94       28.0000       74.4900      28.0000       51.1500      28.0000   
100      61.3400       74.4450      61.3400       71.6600      61.3400   
103      60.0800       87.4838      60.0800       79.8000      60.0800   
105      44.0100       68.8000      45.6500       68.8000      52.3700   

     short_term_volatility  medium_term_volatility  long_term_volatility  \
10               17.460334               27.785736             36.305644   
11                0.792908                1.880968              2.644787   
13                6.051612               11.709306             12.102727   
18                3.640561               16.340390             17.349684   
22                4.276962                9.222223              9.832002   
27                0.273247                0.562959              0.796649   
39                5.322027                9.270320             20.650454   
44                1.786247                2.351703              4.840158   
51                4.204438                6.233355             15.793710   
60                1.994191                2.291369              3.943812   
65                1.248402                4.170954              5.710504   
68               31.446923               47.241173             51.834077   
69                2.887317                4.050795            120.262126   
76                4.819824                5.970069             10.574154   
78                1.253073                2.433182              4.997040   
87                2.712509                6.200083             10.531232   
94                4.823296               13.093079             16.130495   
100               1.815543                2.740636              8.694137   
103               4.146498                6.055143             14.095942   
105               3.900035                4.140204             12.715836   

       ma_5_day   ma_10_day   ma_20_day   ma_50_day  ma_100_day  ma_200_day  \
10    69.859518   68.630134   92.880202  127.805005  136.756979  136.756979   
11    21.178893   20.810333   21.985269   24.559806   24.512786   24.512786   
13   119.450854  119.877686  127.371148  136.369851  136.024766  136.024766   
18   116.212900  116.662665  119.297225  137.605456  138.832328  138.832328   
22   107.692005  110.531553  112.233553  122.969400  122.652462  122.652462   
27     9.920024    9.985839   10.407589   11.127562   11.308988   11.308988   
39   225.927354  223.798168  231.243878  247.084997  245.720238  245.720238   
44    35.873538   34.749051   34.618352   38.568774   39.138312   39.138312   
51   126.944182  126.865074  123.130099  133.932959  134.121173  134.121173   
60    56.586105   55.335960   54.344138   54.411996   55.028293   55.028293   
65    59.466433   58.427313   59.800494   65.737725   65.604621   65.604621   
68   381.579061  378.029199  421.579827  436.658185  437.681872  437.681872   
69    80.605394   80.995477   79.222227  165.361964  167.752761  167.752761   
76    59.054994   55.473176   53.395451   63.495455   66.100374   66.100374   
78    63.134473   64.107900   65.821292   70.152439   70.623458   70.623458   
87   110.140390  109.078860  107.644142  115.464328  116.076205  116.076205   
94    44.834884   42.005137   45.056923   54.303173   60.458762   60.458762   
100   66.763522   66.272590   66.208811   73.777932   76.001797   76.001797   
103   72.596455   69.719207   70.572256   83.773876   87.812387   87.812387   
105   60.228023   57.442718   54.418334   62.227013   66.219032   66.219032   

     pct_from_52_week_high  pct_from_52_week_low  pct_from_26_week_high  \
10               -0.636120              0.113701              -0.525910   
11               -0.267155              0.142857              -0.178185   
13               -0.203694              0.126588              -0.194776   
18               -0.287576              0.130411              -0.287576   
22               -0.220401              0.101886              -0.202849   
27               -0.219238              0.114149              -0.147067   
39               -0.212416              0.108592              -0.087303   
44               -0.205355              0.264918              -0.061542   
51               -0.265271              0.239736              -0.051337   
60               -0.225420              0.251957              -0.073222   
65               -0.200286              0.109369              -0.184827   
68               -0.276794              0.201811              -0.198832   
69               -0.774953              0.280997              -0.005450   
76               -0.276569              0.375262              -0.132377   
78               -0.204273              0.055289              -0.088159   
87               -0.235690              0.155105              -0.115204   
94               -0.537512              0.699643              -0.361122   
100              -0.277295              0.151451              -0.051246   
103              -0.294735              0.319907              -0.093546   
105              -0.234099              0.507612              -0.035610   

     pct_from_26_week_low  pct_from_13_week_high  pct_from_13_week_low  \
10               0.113701              -0.424198              0.113701   
11               0.142857              -0.046381              0.142857   
13               0.126588              -0.069554              0.126588   
18               0.130411              -0.014344              0.130411   
22               0.101886              -0.076406              0.101886   
27               0.114149              -0.084770              0.114149   
39               0.108592              -0.015850              0.108592   
44               0.257907              -0.005029              0.257907   
51               0.239736              -0.039163              0.122239   
60               0.158753              -0.057909              0.133215   
65               0.109369              -0.049112              0.109369   
68               0.161763              -0.153621              0.161763   
69               0.280997              -0.005450              0.206259   
76               0.375262              -0.016492              0.357051   
78               0.055289              -0.035140              0.055289   
87               0.155105              -0.009996              0.109691   
94               0.699643              -0.069599              0.699643   
100              0.151451              -0.014373              0.151451   
103              0.319907              -0.006266              0.319907   
105              0.453450              -0.035610              0.266947   

     pct_from_200_day_ma  pct_from_100_day_ma  pct_from_50_day_ma  \
10             -0.482878            -0.482878           -0.446657   
11             -0.102509            -0.102509           -0.104227   
13             -0.061788            -0.061788           -0.064163   
18             -0.114039            -0.114039           -0.106140   
22             -0.096471            -0.096471           -0.098800   
27             -0.102493            -0.102493           -0.087860   
39             -0.044849            -0.044849           -0.050124   
44             -0.014265            -0.014265            0.000291   
51             -0.034157            -0.034157           -0.032800   
60              0.046553             0.046553            0.058406   
65             -0.061499            -0.061499           -0.063399   
68             -0.053696            -0.053696           -0.051478   
69             -0.466954            -0.466954           -0.459247   
76             -0.039188            -0.039188            0.000229   
78             -0.082458            -0.082458           -0.076297   
87             -0.027363            -0.027363           -0.022209   
94             -0.212852            -0.212852           -0.123624   
100            -0.070680            -0.070680           -0.042668   
103            -0.096938            -0.096938           -0.053404   
105             0.001978             0.001978            0.066257   

     pct_from_20_day_ma  pct_from_10_day_ma  pct_from_5_day_ma     rsi_14  \
10            -0.238589            0.030451           0.012317  51.305506   
11             0.000670            0.057167           0.038770  47.022792   
13             0.001954            0.064585           0.068389  75.544955   
18             0.031038            0.054322           0.058402  66.398141   
22            -0.012595            0.002610           0.029046  67.484156   
27            -0.024760            0.016429           0.023173  72.918848   
39             0.014946            0.048713           0.038830  54.272091   
44             0.114438            0.110246           0.075445  59.987476   
51             0.052058            0.021085           0.020449  60.072683   
60             0.059728            0.040734           0.017741  63.535577   
65             0.029590            0.053788           0.035374  54.093287   
68            -0.017553            0.095630           0.085437  73.127779   
69             0.128724            0.104012           0.109355  75.485087   
76             0.189427            0.144878           0.075438  51.657934   
78            -0.015516            0.010796           0.026381  77.746647   
87             0.048826            0.035031           0.025055  66.542001   
94             0.056219            0.132957           0.061450  51.909263   
100            0.066776            0.065750           0.057913  65.833070   
103            0.123671            0.137420           0.092340  57.525779   
105            0.219258            0.155064           0.101647  42.737164   

         beta  avg_daily_volume  
10  -0.257217      1.406117e+06  
11   0.004778      4.743421e+06  
13  -0.237622      1.514166e+06  
18  -0.012863      9.197799e+05  
22   0.173188      1.819785e+06  
27   0.284975      7.759569e+06  
39   0.196122      2.475214e+06  
44   0.131061      6.466619e+06  
51   0.629989      4.325123e+05  
60  -0.170069      1.973117e+06  
65  -0.071807      1.371369e+06  
68   0.095331      1.725372e+05  
69   1.035072      6.955522e+05  
76   0.155984      1.600158e+06  
78   0.185509      8.406558e+06  
87  -0.234790      7.934303e+05  
94   0.533325      3.022792e+06  
100 -0.521041      3.510779e+06  
103  0.030519      2.602837e+06  
105 -0.146676      1.363110e+07  Here are 20 stocks where the current price is less than 80% of the 52-week high, but greater than the 5-day moving average:

1. AAP: Current Price = 70.72, 52-week High = 194.35, 5-day MA = 69.86
2. AES: Current Price = 22.00, 52-week High = 30.02, 5-day MA = 21.18
3. A: Current Price = 127.62, 52-week High = 160.27, 5-day MA = 119.45
4. ARE: Current Price = 123.00, 52-week High = 172.65, 5-day MA = 116.21
5. ALL: Current Price = 110.82, 52-week High = 142.15, 5-day MA = 107.69
6. AMCR: Current Price = 10.15, 52-week High = 13.00, 5-day MA = 9.92
7. AMGN: Current Price = 234.70, 52-week High = 298.00, 5-day MA = 225.93
8. APA: Current Price = 38.58, 52-week High = 48.55, 5-day MA = 35.87
9. AIZ: Current Price = 129.54, 52-week High = 176.31, 5-day MA = 126.94
10. BALL: Current Price = 57.59, 52-week High = 74.35, 5-day MA = 56.59
11. WRB: Current Price = 61.57, 52-week High = 76.99, 5-day MA = 59.47
12. BIO: Current Price = 414.18, 52-week High = 572.70, 5-day MA = 381.58
13. TECH: Current Price = 89.42, 52-week High = 397.34, 5-day MA = 80.61
14. BXP: Current Price = 63.51, 52-week High = 87.79, 5-day MA = 59.05
15. BMY: Current Price = 64.80, 52-week High = 81.44, 5-day MA = 63.13
16. CPT: Current Price = 112.90, 52-week High = 147.72, 5-day MA = 110.14
17. CTLT: Current Price = 47.59, 52-week High = 102.90, 5-day MA = 44.83
18. CNC: Current Price = 70.63, 52-week High = 97.73, 5-day MA = 66.76
19. CF: Current Price = 79.30, 52-week High = 112.44, 5-day MA = 72.60
20. SCHW: Current Price = 66.35, 52-week High = 86.63, 5-day MA = 60.23

Please note that the current price, 52-week high, and 5-day moving average are all in USD.

> Finished chain.

Observation: Here are 20 stocks where the current price is less than 80% of the 52-week high, but greater than the 5-day moving average:

1. AAP: Current Price = 70.72, 52-week High = 194.35, 5-day MA = 69.86
2. AES: Current Price = 22.00, 52-week High = 30.02, 5-day MA = 21.18
3. A: Current Price = 127.62, 52-week High = 160.27, 5-day MA = 119.45
4. ARE: Current Price = 123.00, 52-week High = 172.65, 5-day MA = 116.21
5. ALL: Current Price = 110.82, 52-week High = 142.15, 5-day MA = 107.69
6. AMCR: Current Price = 10.15, 52-week High = 13.00, 5-day MA = 9.92
7. AMGN: Current Price = 234.70, 52-week High = 298.00, 5-day MA = 225.93
8. APA: Current Price = 38.58, 52-week High = 48.55, 5-day MA = 35.87
9. AIZ: Current Price = 129.54, 52-week High = 176.31, 5-day MA = 126.94
10. BALL: Current Price = 57.59, 52-week High = 74.35, 5-day MA = 56.59
11. WRB: Current Price = 61.57, 52-week High = 76.99, 5-day MA = 59.47
12. BIO: Current Price = 414.18, 52-week High = 572.70, 5-day MA = 381.58
13. TECH: Current Price = 89.42, 52-week High = 397.34, 5-day MA = 80.61
14. BXP: Current Price = 63.51, 52-week High = 87.79, 5-day MA = 59.05
15. BMY: Current Price = 64.80, 52-week High = 81.44, 5-day MA = 63.13
16. CPT: Current Price = 112.90, 52-week High = 147.72, 5-day MA = 110.14
17. CTLT: Current Price = 47.59, 52-week High = 102.90, 5-day MA = 44.83
18. CNC: Current Price = 70.63, 52-week High = 97.73, 5-day MA = 66.76
19. CF: Current Price = 79.30, 52-week High = 112.44, 5-day MA = 72.60
20. SCHW: Current Price = 66.35, 52-week High = 86.63, 5-day MA = 60.23

Please note that the current price, 52-week high, and 5-day moving average are all in USD.
Thought:Now that I have a list of 20 stocks that meet the criteria, I need to narrow it down to the top 5. I'll do this by selecting the stocks with the highest percent change from their 5-day moving average. This indicates that they have been increasing in price recently, which could be a sign of a positive trend.
Action: Stock Screener
Action Input: From the list of 20 stocks, find the top 5 stocks with the highest percent change from their 5-day moving average.Syncing Index Data (SPY) from 2022-07-23 to present...
Syncing Data for DTN (555 of 588) from 2022-07-23 to present...
Syncing Data for FLGE (558 of 588) from 2022-07-23 to present...
Syncing Data for BGU (564 of 588) from 2022-07-23 to present...
Syncing Data for BGZ (582 of 588) from 2022-07-23 to present...


> Entering new AgentExecutor chain...

Invoking: `python_repl_ast` with `df['pct_change_from_ma_5_day'] = ((df['current_price'] - df['ma_5_day']) / df['ma_5_day']) * 100
df_top_5 = df.nlargest(5, 'pct_change_from_ma_5_day')[['symbol', 'pct_change_from_ma_5_day']]
df_top_5.to_json(orient='records')`


[{"symbol":"FBGX","pct_change_from_ma_5_day":38.7670212401},{"symbol":"ZION","pct_change_from_ma_5_day":17.3154292338},{"symbol":"CFG","pct_change_from_ma_5_day":11.9911326144},{"symbol":"CZR","pct_change_from_ma_5_day":11.5861421867},{"symbol":"KEY","pct_change_from_ma_5_day":11.224211224}]The top 5 stocks with the highest percent change from their 5-day moving average are:

1. FBGX with a percent change of 38.77%
2. ZION with a percent change of 17.32%
3. CFG with a percent change of 11.99%
4. CZR with a percent change of 11.59%
5. KEY with a percent change of 11.22%

> Finished chain.

Observation: The top 5 stocks with the highest percent change from their 5-day moving average are:

1. FBGX with a percent change of 38.77%
2. ZION with a percent change of 17.32%
3. CFG with a percent change of 11.99%
4. CZR with a percent change of 11.59%
5. KEY with a percent change of 11.22%
Thought:I now know the final answer.
Final Answer: The top 5 stocks that are currently a good buy, based on the criteria of trading at a low price compared to their 52-week high but having started to rebound recently, are FBGX, ZION, CFG, CZR, and KEY.

> Finished chain.
```

## Important Information

### How the Code Updates Its Store of Indicators

The `StockScreener.py` script initializes its store of indicators by first checking for an existing data file (`screener_df_{interval}.pickle`), where `{interval}` is the data time frame (e.g., `1Hour`). If the file doesn't exist, the script prints a message and then proceeds to gather all symbols from a predefined list stored in `sp500andETFs.pickle`.

The script then fetches data for all these symbols by calling the `fetch_for_all_symbols` method. This method iterates over the entire list of symbols and fetches relevant data for each symbol using the `fetch_symbol` method. The data fetched includes open, close, high, low, returns, and average daily volume.

Various stock metrics are calculated for each symbol such as 52-week high and low, 26-week high and low, 13-week high and low, percent change from different week highs and lows, volatility, moving averages, relative strength index (RSI), and beta.

The script then constructs a new dataframe row for each symbol, which includes all these metrics, and appends it to `screener_df`. If `screener_df` does not exist, it gets created with the new row.

At the end of each iteration, the method checks whether the data of the symbol is already in `screener_df`. If it exists, the method checks the time of the last update. If the last update was within an hour or later than 4:00 PM on the previous weekday, the method skips the current symbol and moves on to the next. If not, it goes ahead and fetches the data, calculates the metrics, and updates the row in `screener_df`.

Once all symbols have been processed, the updated `screener_df` is then saved to disk for future use.

### Token Usage Warning

Please be aware that this tool often generates large data frames and consequently makes many requests to the OpenAI API. This can use up a lot of tokens and can often exceed token lengths for queries. This makes using the tool quite expensive. Consider this aspect before using the tool extensively. Improvements to manage this more efficiently are planned for future versions.

## Disclaimer

This tool is for educational and informational purposes only. It should not be considered financial advice. You should consult with a financial advisor before making any investment decisions.

## License

MIT

## Contact

If you have any questions or need further clarification, feel free to create an issue in this repository.

## Contributions

Contributions are always welcome! Please feel free to fork this repository and submit pull requests. If you want to enhance or propose changes, kindly create an issue so we can discuss it.