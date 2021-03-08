import nltk
import pandas as pd
import yfinance as yf
import numpy as np
import pandas
from datetime import datetime, timedelta
from pandas_datareader import data as web
yf.pdr_override()
nltk.download('vader_lexicon')

def correlation(ticker, start, end, scores_df): # ticker, start datetime, end datetime, dataframe returned by sentiment function
    dfEOD = pd.DataFrame()
    startDate = (start - timedelta(days=1)).strftime('%Y-%m-%d')
    endDate = end.strftime('%Y-%m-%d')
    dfEOD = web.DataReader(ticker,data_source='yahoo',start=startDate , end=endDate)

    dfEOD.index = dfEOD.index.astype('datetime64[ns]') 
    dfEOD2 = dfEOD.drop(['Open', 'High','Low','Close','Volume'], axis=1) # drop unwanted rows  

    # calculate daily returns
    dfEOD2['Returns'] = dfEOD2['Adj Close']/dfEOD2['Adj Close'].shift(1) - 1 

    scores_df['Score(1)'] = scores_df.shift(1)

    dfEOD3 = pd.merge(dfEOD2[['Returns']], scores_df[['Score(1)']], left_index=True, right_index=True, how='left')
    dfEOD3.fillna(0, inplace=True) 

    print(scores_df)

    dfReturnsScore = dfEOD3[(dfEOD3['Score(1)'] > 0.5) | (dfEOD3['Score(1)'] < -0.5)]

    return dfReturnsScore

    #use this function to return the dataframe
    # Using the returned dataframe you can return a correlation score using the code below
    # dfReturnsScore['Returns'].corr(dfReturnsScore['Score(1)'])
    #You can also plot the relationship between scores and returns using the code below
    # dfReturnsScore.plot(x="Score(1)", y="Returns", style="o")