# date util fns
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

YEARS = 10
MARKET_SYM = '^DJI'

def get_date_before_years(year: int):
  return date.today() - relativedelta(years=year)

def get_date_format(d: date):
  return d.strftime("%m/%d/%Y")

def get_date_str_before_years(year: int):
  return get_date_format(get_date_before_years(year))

from yahoo_fin.stock_info import get_data

# get_data(ticker, start_date = None, end_date = None, index_as_date = True, interval = “1d”)

def get_stock_history_data(symbol: str, start_date: str, end_date: str):
  interval = "1d"
  return get_data(symbol, start_date=start_date, end_date=end_date, index_as_date = True, interval=interval)

def get_stock_history_data_before_today(symbol: str, year: int):
  today_str = get_date_format(date.today())
  history_date_str = get_date_str_before_years(year)
  return get_stock_history_data(symbol, history_date_str, today_str)

def read_stock_prices(symbols: list[str]):
   historical_datas = {}
   for ticker in symbols:
       historical_datas[ticker] = get_stock_history_data_before_today(ticker, YEARS)

   # join df columms
   out_df = pd.DataFrame()
   for ticker in symbols:
      out_df[ticker] = historical_datas[ticker]['close']

   out_df.dropna(inplace=True)
   # skip the date column
   # out_df = out_df.iloc[0:, 1:]
   return out_df

def read_market_prices():
   # uses market indicator
   symbol = MARKET_SYM
   df = get_stock_history_data_before_today(symbol, YEARS)
   # use the close market price column
   df = df.iloc[0:, [4]]
   return df

# # dump to csv file
# def dump_to_file(df: pd.DataFrame, file_path="file.csv"):
#   df.to_csv(path_or_buf=file_path)

# ticker_list = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'DIS', 'GS', 'HD', 'IBM', 'JPM', 'KO', 'MCD', 'MRK', 'UNH', 'WBA']

# historical_datas = {}
# for ticker in ticker_list:
#     historical_datas[ticker] = get_stock_history_data_before_today(ticker, 15)

# # join df columms
# out_df = pd.DataFrame()
# for ticker in ticker_list:
#   out_df[ticker] = historical_datas[ticker]['close']

# dump_to_file(out_df, "stocks_history.csv")

# ticker_list = ["^DJT"]

# history = {}
# for ticker in ticker_list:
#     history[ticker] = get_stock_history_data_before_today(ticker, 15)
#     history[ticker].drop('ticker', axis=1, inplace=True)

# dump_to_file(history["^DJT"], "dji_history.csv")

# # save files
# history["^DJT"]