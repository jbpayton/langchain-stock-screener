import alpaca_trade_api as tradeapi
import pandas as pd
import pandas_market_calendars as mcal
import pickle
import time
import os
import datetime
import numpy as np
import pytz

from . import FinanceHelper as fh
from .scrape_tickers import dump_all
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

class StockScreener:

    def __init__(self, interval='1Hour', verbose=False):
        if not os.path.exists("./sp500andETFs.pickle"):
            dump_all()

        assetsToDownload = pickle.load(open("./sp500andETFs.pickle", "rb"))

        self.screener_df = None
        self.verbose = verbose

        # if we are supressing updates, then we want to only get the symbols that we don't already have
        # so we need to load the screener_df from disk
        if os.path.exists("./screener_df_" + interval + ".pickle"):
            self.screener_df = pickle.load(open("./screener_df_" + interval + ".pickle", "rb"))
        else:
            # if the screener_df doesn't exist, then we need to get all the symbols
            print("screener_df_" + interval + ".pickle does not exist, so we will get all symbols")

        # get a year ago as an ISO8601 date string without the time part
        self.lastDate = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()[:10]

        if assetsToDownload == []:
            print("No assets to download")
            return

        self.fetch_for_all_symbols(assetsToDownload, interval)

        # save the screener_df to disk
        pickle.dump(self.screener_df, open("screener_df_" + interval + ".pickle", "wb"))

        # initialize the internal agent
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(model_name='gpt-4', temperature=0),
            self.screener_df,
            max_iterations=5,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

    def fetch_for_all_symbols(self, assetList, barTime):
        api = tradeapi.REST(key_id=os.environ.get('ALPACA_KEY'),
                            secret_key=os.environ.get('ALPACA_SECRET'),
                            base_url=os.environ.get('ALPACA_URL'))

        iteratorPos = 0  # Tracks position in list of symbols to download
        assetListLen = len(assetList)

        # first get the SPY data
        print("Syncing Index Data (SPY) from " + self.lastDate + " to present...")
        index_open, index_close, index_high, index_low, index_returns, avg_daily_volume = self.fetch_symbol(api, barTime, "SPY")
        wk_index_close = index_close[-52 * 5 * 8::20]
        index_returns = np.diff(wk_index_close) / wk_index_close[:-1] * 100
        index_volatility = np.std(index_returns)

        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        # Get the previous weekday
        previous_weekday = now - pd.DateOffset(days=1)
        while not mcal.get_calendar('NYSE').valid_days(start_date=previous_weekday.strftime('%Y-%m-%d'),
                                                       end_date=previous_weekday.strftime(
                                                           '%Y-%m-%d')).empty:
            previous_weekday -= pd.DateOffset(days=1)

        # Check if last_updated is later than 4:00 PM on the previous weekday
        previous_weekday_4pm = previous_weekday.replace(hour=16, minute=0, second=0)

        # now get the rest of the symbols
        while iteratorPos < assetListLen:
            symbol = assetList[iteratorPos]

            if self.screener_df is not None:
                if symbol in self.screener_df['symbol'].values:

                    last_updated = self.screener_df.loc[self.screener_df['symbol'] == symbol, 'last_updated'].iloc[0]
                    if (now - last_updated).total_seconds() < 3600:
                        iteratorPos += 1
                        continue


                    if last_updated > previous_weekday_4pm:
                        iteratorPos += 1
                        continue

            print("Syncing Data for " + symbol + " (" + str(iteratorPos + 1) + " of " + str(
                assetListLen) + ") from " + self.lastDate + " to present...")

            open, close, high, low, returns, avg_daily_volume = self.fetch_symbol(api, barTime, symbol)

            if open is None:
                iteratorPos += 1
                continue

            current_price = close[-1]

            start = time.time();
            # Assume all bars are 1 hour long (assume 8 hours of trading per day)
            # get 52 week high and low
            high_52_week = np.max(high[-52 * 5 * 8:])
            low_52_week = np.min(low[-52 * 5 * 8:])
            # get 26 week high and low
            high_26_week = np.max(high[-26 * 5 * 8:])
            low_26_week = np.min(low[-26 * 5 * 8:])
            # get 13 week high and low
            high_13_week = np.max(high[-13 * 5 * 8:])
            low_13_week = np.min(low[-13 * 5 * 8:])
            # get current percent change from 52 week high
            pct_from_52_week_high = (close[-1] - high_52_week) / high_52_week
            # get current percent change from 52 week low
            pct_from_52_week_low = (close[-1] - low_52_week) / low_52_week
            # get current percent change from 26 week high
            pct_from_26_week_high = (close[-1] - high_26_week) / high_26_week
            # get current percent change from 26 week low
            pct_from_26_week_low = (close[-1] - low_26_week) / low_26_week
            # get current percent change from 13 week high
            pct_from_13_week_high = (close[-1] - high_13_week) / high_13_week
            # get current percent change from 13 week low
            pct_from_13_week_low = (close[-1] - low_13_week) / low_13_week

            short_term_volatility = np.std(close[-13 * 5 * 8:])
            medium_term_volatility = np.std(close[-26 * 5 * 8:])
            long_term_volatility = np.std(close[-52 * 5 * 8:])

            # get some moving averages at different time scales
            # 5 day
            ma_5_day = np.mean(close[-5 * 5 * 8:])
            # 10 day
            ma_10_day = np.mean(close[-10 * 5 * 8:])
            # 20 day
            ma_20_day = np.mean(close[-20 * 5 * 8:])
            # 50 day
            ma_50_day = np.mean(close[-50 * 5 * 8:])
            # 100 day
            ma_100_day = np.mean(close[-100 * 5 * 8:])
            # 200 day
            ma_200_day = np.mean(close[-200 * 5 * 8:])
            # get current percent change from 200 day moving average
            pct_from_200_day_ma = (close[-1] - ma_200_day) / ma_200_day
            # get current percent change from 100 day moving average
            pct_from_100_day_ma = (close[-1] - ma_100_day) / ma_100_day
            # get current percent change from 50 day moving average
            pct_from_50_day_ma = (close[-1] - ma_50_day) / ma_50_day
            # get current percent change from 20 day moving average
            pct_from_20_day_ma = (close[-1] - ma_20_day) / ma_20_day
            # get current percent change from 10 day moving average
            pct_from_10_day_ma = (close[-1] - ma_10_day) / ma_10_day
            # get current percent change from 5 day moving average
            pct_from_5_day_ma = (close[-1] - ma_5_day) / ma_5_day

            # get 14 day RSI (last value only)
            rsi = fh.getRSI(close, n=14)[-1]

            # calculate beta vs index
            wk_close = close[-52 * 5 * 8::20]
            wk_returns = np.diff(wk_close) / wk_close[:-1] * 100
            len_returns = len(wk_returns)

            beta = np.cov(wk_returns, index_returns[-1 * len_returns::])[0][1] / index_volatility ** 2

            if self.verbose:
                print("Time to calculate: " + str(time.time() - start) + " seconds")

            new_row = pd.DataFrame([{"symbol": symbol,
                                     "last_updated": datetime.datetime.now(pytz.timezone('US/Eastern')),
                                     "current_price": current_price, "high_52_week": high_52_week,
                                     "low_52_week": low_52_week, "high_26_week": high_26_week,
                                     "low_26_week": low_26_week, "high_13_week": high_13_week,
                                     "low_13_week": low_13_week, "short_term_volatility": short_term_volatility,
                                     "medium_term_volatility": medium_term_volatility,
                                     "long_term_volatility": long_term_volatility, "ma_5_day": ma_5_day,
                                     "ma_10_day": ma_10_day, "ma_20_day": ma_20_day, "ma_50_day": ma_50_day,
                                     "ma_100_day": ma_100_day, "ma_200_day": ma_200_day,
                                     "pct_from_52_week_high": pct_from_52_week_high,
                                     "pct_from_52_week_low": pct_from_52_week_low,
                                     "pct_from_26_week_high": pct_from_26_week_high,
                                     "pct_from_26_week_low": pct_from_26_week_low,
                                     "pct_from_13_week_high": pct_from_13_week_high,
                                     "pct_from_13_week_low": pct_from_13_week_low,
                                     "pct_from_200_day_ma": pct_from_200_day_ma,
                                     "pct_from_100_day_ma": pct_from_100_day_ma,
                                     "pct_from_50_day_ma": pct_from_50_day_ma,
                                     "pct_from_20_day_ma": pct_from_20_day_ma,
                                     "pct_from_10_day_ma": pct_from_10_day_ma,
                                     "pct_from_5_day_ma": pct_from_5_day_ma,
                                     "rsi_14": rsi, "beta": beta, "avg_daily_volume": avg_daily_volume}])
            if self.screener_df is None:
                self.screener_df = new_row
            else:
                self.screener_df = pd.concat([self.screener_df, new_row], ignore_index=True)

            if self.verbose:
                # print out the last row
                print(self.screener_df.tail(1))

            iteratorPos += 1

    def fetch_symbol(self, api, barTime, symbol):
        while True:  # Add this loop
            try:
                returned_data = api.get_bars(symbol, barTime, start=self.lastDate)
                break  # If get_bars succeeds, break the loop
            except:  # If get_bars fails, wait 5 seconds and try again
                print("Exception occurred when getting bars. Retrying in 5 seconds...")
                time.sleep(5)

        if returned_data.df.empty:
            return None, None, None, None, None, None

        open = returned_data.df.open.values
        close = returned_data.df.close.values
        high = returned_data.df.high.values
        low = returned_data.df.low.values
        returns = (close - open) / open

        # Convert the list of Bar objects to a list of dictionaries
        bar_list = [bar.__dict__ for bar in returned_data]

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(bar_list)
        df = pd.json_normalize(df['_raw'])

        # Convert the 't' column to datetime
        df['t'] = pd.to_datetime(df['t'])

        # Convert to Eastern Time
        df['t'] = df['t'].dt.tz_convert('US/Eastern')

        # Add a date column
        df['date'] = df['t'].dt.date

        # Calculate daily volumes
        daily_volumes = df.groupby('date')['v'].sum()

        # Calculate average daily volume
        average_daily_volume = daily_volumes.mean()

        return open, close, high, low, returns, average_daily_volume

    def run(self, query):
        safety = "Ensure that valid json is used with internal tools and functions. Also, outputs should be in well formatted JSON. Also please check to ensure that we stay within th emodel's context limit."
        return self.agent.run("Please use this natural language prompt to select up to 20 results:" + query + safety)
