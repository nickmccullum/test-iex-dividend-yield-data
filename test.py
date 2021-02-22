import pandas as pd 
import numpy as np
from secrets import IEX_CLOUD_API_KEY

stocks = pd.read_csv('wilshire_5000_stocks.csv', header=None)

n = 100
lists_of_stocks = np.array([stocks[0][q:q + n] for q in range(0, len(stocks[0]), n)])
output_dataframe = pd.DataFrame()

for stock_list in lists_of_stocks:
    tickerString = ''
    for a in stock_list:
        tickerString = tickerString + a.strip() + ','
    tickerString = tickerString[:-1]

    batchAPICall = pd.read_json("https://cloud.iexapis.com/stable/stock/market/batch?symbols="+tickerString+"&types=stats,price,dividends&range=5y&cache=true&token="+IEX_CLOUD_API_KEY)
    for stock in stock_list:
        try:
            dividend_yield = batchAPICall[stock]["stats"]["dividendYield"]
            output_dataframe = output_dataframe.append(pd.Series([stock, dividend_yield]), ignore_index=True)
        except KeyError:
            pass
        except TypeError:
            pass

output_dataframe.to_csv('iex_dividend_yield.csv')