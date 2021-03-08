from correlation import correlation
from pricing import get_pricing
from reddit import get_reddit_data
from sentiment_analysis import get_scores
from twitter import TwitterClient
from datetime import datetime, timedelta, date

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


app = dash.Dash()

def get_reddit_sentiment(start, end, ticker):
    reddit_data = get_reddit_data(start, end, ticker, "wallstreetbets")
    
    for k in reddit_data:
        reddit_data[k] = datetime.fromtimestamp(reddit_data[k])
        reddit_data[k] = reddit_data[k].replace(minute=0, second=0)

    df = get_scores(reddit_data)
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'Date'})

    return df

app.layout = html.Div([
    dcc.Graph(id='sentiment-v-time'),
    dcc.Input(id='ticker', value='AAPL', type='text'),
    dcc.Input(id='person1', value='', type='text'),
    dcc.Input(id='person2', value='', type='text'),
    dcc.Input(id='person3', value='', type='text'),
    dcc.Input(id='person4', value='', type='text'),

    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=datetime.now().date(),
        start_date= (datetime.now() - timedelta(days=7)).date(),
        end_date=datetime.now().date()
    ),
    html.Button('Go', id='button'),
    html.H1('Correlation: ', id='correlation'),  
])

@app.callback(
    Output('sentiment-v-time', 'figure'),
    [Input('button', 'n_clicks')],
    state=[State(component_id='ticker', component_property='value'),
        State(component_id='person1', component_property='value'),
        State(component_id='person2', component_property='value'),
        State(component_id='person3', component_property='value'),
        State(component_id='person4', component_property='value'),
        State(component_id='date-picker', component_property='start_date'),
        State(component_id='date-picker', component_property='end_date')])
def get_plot(n_clicks, ticker, p1, p2, p3, p4, start_date, end_date,):
    print(ticker, start_date, end_date)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    df = get_reddit_sentiment(start, end, ticker)
    yf = get_pricing(start, end, ticker)


    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Score']),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=yf['Date'], y=yf['Close']),
        secondary_y=True
    )

    fig.update_yaxes(title_text="<b>Sentiment</b> axis", secondary_y=False)
    fig.update_yaxes(title_text="<b>Close</b> axis", secondary_y=True)

    return fig

@app.callback(
    Output('correlation', component_property='children'),
    [Input('button', 'n_clicks')],
    state=[State(component_id='ticker', component_property='value'),
        State(component_id='person1', component_property='value'),
        State(component_id='person2', component_property='value'),
        State(component_id='person3', component_property='value'),
        State(component_id='person4', component_property='value'),
        State(component_id='date-picker', component_property='start_date'),
        State(component_id='date-picker', component_property='end_date')])
def get_correlation(n_clicks, ticker, p1, p2, p3, p4, start_date, end_date):
    import time 

    time.sleep(1)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    data = get_reddit_data(start, end, ticker, 'wallstreetbets')
    for k in data:
        data[k] = datetime.fromtimestamp(data[k])
        data[k] = data[k].replace(hour=0, minute=0, second=0)
    
    # print(data)
    score = get_scores(data)

    df = correlation(ticker, start, end, score)

    return 'Correlation: ' + str(df['Returns'].corr(df['Score(1)']))

if __name__ == '__main__':
    # TODO: add time ranges
    # TODO: track vol vs # comments
    #twitter = TwitterClient()
    #tweets = twitter.get_tweets()

    app.run_server(debug=True)
