import pandas as pd
import yfinance as yf
from datetime import datetime
from pandas_datareader import data as web

def get_pricing(start, end, ticker):
    try:
        startDate = start.strftime('%Y-%m-%d')
        endDate = end.strftime('%Y-%m-%d')
        dfEOD = web.DataReader(ticker,data_source='yahoo',start=startDate , end=endDate)

        dfEOD.index = dfEOD.index.astype('datetime64[ns]') 
        
        dfEOD.reset_index(inplace=True)
        dfEOD = dfEOD.rename(columns = {'index':'Date'})
        
        return dfEOD
    except:
        return pd.DataFrame({'Date' : [], 'Score': []})