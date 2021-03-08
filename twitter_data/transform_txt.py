import pandas as pd
import numpy as np
import sys

filename = sys.argv[1]
with open(filename) as f:
    content = f.read()

dic = []
entries = content.split("name::")
for entry in entries[1:]:
    #print("ayayaya", entry)
    name, entry = entry.split("timestamp::")[0].strip(),entry.split("timestamp::")[1].strip()
    timestamp, entry = entry.split("likes::")[0].strip(),entry.split("likes::")[1].strip()
    likes, entry = entry.split("IsReply::")[0].strip(),entry.split("IsReply::")[1].strip()
    isreply, entry = entry.split("IsRetweet::")[0].strip(),entry.split("IsRetweet::")[1].strip()
    isretweet, entry = entry.split("text::")[0].strip(),entry.split("text::")[1].strip()
    text, entry = entry.split("retweets::")[0].strip(),entry.split("retweets::")[1].strip()
    retweets, replies = entry.split("replies::")[0].strip(),entry.split("replies::")[1].strip()
    #print("name", name)
    #print("timestamp", timestamp)
    #print("likes", likes)
    #print("isretweet", isretweet)
    #print("retweets", retweets)
    #print("replies", replies)
    dic.append({"name": name, "timestamp": timestamp, "likes": likes, "isretweet": isretweet, "isreply" : isreply, "likes": likes, "text" : text, "retweets" : retweets, "replies" : replies})


df = pd.DataFrame(dic)
df.to_csv(filename.split(".txt")[0]+".csv", index=False)

    

