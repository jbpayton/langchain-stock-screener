# Alpaca Stock Screener

The Alpaca Stock Screener is a Python tool designed to be used with LangChain agents, enabling stock analysis using various technical indicators. The tool takes a natural language query as input and returns a list of stocks whose technical indicators match the query.

This tool uses an internal dataframe for this data and handles operations internally. Note that this tool does not handle queries involving fundamental indicators like earnings growth or debt-to-equity ratio. Data is all acquired using the Alpaca Markets Bars API.

From an architecture standpoint, this tool encapsulates a langchain DataFrame agent making use of the python-repl.

For more information on LangChain, refer to the [LangChain documentation](https://python.langchain.com/)

For more information on the Alpaca algorithmic trading platform, please refer to the [Alpaca Markets website](https://alpaca.markets/)

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

The following is an example of the output of `agenttest.py`:

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
...

Here are 20 stocks where the current price is less than 80% of the 52-week high, but greater than the 5-day moving average:

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




## Disclaimer and Safety Warnings

### Financial Disclaimer
This tool is for educational and informational purposes only. It should not be considered financial advice. You should consult with a financial advisor before making any investment decisions.

### Autonomous Agents Disclaimer

This tool involves the use of autonomous agents, which operate independently based on the code and instructions they're given. While autonomous agents can streamline many tasks, they also carry certain risks. These agents can perform actions rapidly and at scale, which can lead to unexpected outcomes.

Please keep in mind that it is essential to monitor and control the scope of actions available to these agents. Autonomous agents can produce undesired results if they're given ill-defined or overly broad tasks, or if they encounter unforeseen situations.

Be sure to thoroughly understand the behavior of these autonomous agents and to use them responsibly. OpenAI and the creators of this tool accept no responsibility for any damages or losses that may occur due to the use of autonomous agents.

### Python Code Writing Agents Disclaimer

Please be aware that this tool involves AI agents that are capable of writing Python code (it does this to execute the pandas data frame queries). This could potentially have security implications if the agent writes malicious code or accesses sensitive data. Always review and understand the code that the agent generates before executing it. 

Do not provide the agent with access to any sensitive data or systems unless you fully understand the potential risks and have implemented appropriate safeguards. OpenAI and the creators of this tool accept no responsibility for any damages or losses that may occur due to the use of AI agents that can write Python code.


## License

MIT

## Contact

If you have any questions or need further clarification, feel free to create an issue in this repository.

## Contributions

Contributions are always welcome! Please feel free to fork this repository and submit pull requests. If you want to enhance or propose changes, kindly create an issue so we can discuss it.
