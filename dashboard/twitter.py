import re
import tweepy
from datetime import date

class TwitterClient(object):
    # Class constructor
    def __init__(self):
        # Keys and Token information from Twitter Developer Console
        consumer_key = 'KgqihosLaNjHMvmJDw1xooShS'
        consumer_secret = 'oqtdzvdnqy3REcOWJSDYCySniONnJJeyLiHvavAI3CmjJe1gR8'
        access_token = '838098308618944512-Fgi0emj65zKW2QpkInDNFGsg1mizLXS'
        access_token_secret = 'PbVat9e8o0AcXMs7zTSaQJif6XcVPYANt43wOgSVkLkFm'

        # Attempt authentication
        try: 
            # Create OAuthHandler authentication object 
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
            # Set access and secret token
            self.auth.set_access_token(access_token, access_token_secret) 
            # Create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 
        except: 
            print("Error: Authentication Failed")
  
    # Removes links, mentions
    def clean_tweet(self, tweet): 
        tweet = re.sub('@[A-Za-z0–9]+', '', tweet) #Removing @mentions
        #tweet = re.sub('RT[\s]+', '', text) # Removing RT
        tweet = re.sub('https?:\/\/\S+', '', tweet) # Removing hyperlink
        return tweet
    
    def get_tweets(self, query): 
        # empty list to store parsed tweets 
        tweets = {}
        try: 
            # call twitter api to fetch tweets 
            for tweet in tweepy.Cursor(self.api.search, 
            q = query, lang = 'en', results_type = 'mixed').items():
                date = tweet.created_at
                tweet = self.clean_tweet(tweet.text)
                tweets[date] = tweet
    
            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    search = input("Enter stock ticker: ")
    # calling function to get tweets 
    tweets = api.get_tweets(search)
    print(tweets)

if __name__ == "__main__": 
    # calling main function 
    main() 

