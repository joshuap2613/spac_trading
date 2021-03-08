import requests
from datetime import datetime, timedelta
import time
from psaw import PushshiftAPI

api = PushshiftAPI()

# start and end are both datetime.datetime objects
# topic and subreddit are both strings
def get_reddit_data(start, end, topic, subreddit):
    start = int(start.timestamp())
    end = int(end.timestamp())

    gen = api.search_comments(after=start, before=end, subreddit=subreddit, q=topic)

    max_response_cache = 1000
    cache = {}

    for c in gen:
        cache[c.body] = c.created

        # Omit this test to actually return all results. Wouldn't recommend it though: could take a while, but you do you.
        if len(cache) >= max_response_cache:
            break


    return cache


# Example Usage:
# print(get_reddit_data(datetime.now()-timedelta(hours=1000), datetime.now()+timedelta(hours=1), "ipoe", "wallstreetbets"))