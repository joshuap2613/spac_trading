import nltk
import pandas as pd
import yfinance as yf
import numpy as np
import pandas
from datetime import datetime
from pandas_datareader import data as web
yf.pdr_override()
nltk.download('vader_lexicon')

def get_scores(word_inputs):
    words = word_inputs
    df = pd.DataFrame(list(words.items()),columns = ['String', 'Date'])
    from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
    results = []
    for string in words:
        pol_score = SIA().polarity_scores(string) # run analysis
        pol_score['string'] = string # add strings for viewing
        results.append(pol_score)

    df['Score'] = pd.DataFrame(results)['compound']
    df1 = df.groupby(['Date']).sum() # creates a daily score by summing the scores of the individual articles in each day
    return df1