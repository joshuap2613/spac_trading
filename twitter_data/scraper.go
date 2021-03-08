package main

import (
    "context"
    "fmt"
    "os"
    twitterscraper "github.com/n0madic/twitter-scraper"
)

func main() {
    scraper := twitterscraper.New()
    //fmt.Println("test")
    //fmt.Println(os.Args)
    //last_ID := ""
    //for tweet := range scraper.GetTweets(context.Background(), "AcquisitionCorp", 1000) {
    for _, arg := range os.Args[1:] {
        //fmt.Println(arg)
        for tweet := range scraper.GetTweets(context.Background(), arg, 1000) {
            if tweet.Error != nil {
                panic(tweet.Error)
            }
            //fmt.Println(tweet.Text)
            //fmt.Println(tweet)
            fmt.Println("name::",arg,"timestamp::", tweet.Timestamp, "likes::", tweet.Likes, "IsReply::", tweet.IsReply, "IsRetweet::", tweet.IsRetweet, "text::",tweet.Text, "retweets::", tweet.Retweets, "replies::", tweet.Replies)
            //last_ID =  tweet.ID
    }
    }

    //fmt.Println("bob")
    //fmt.Println(last_ID)

    //tweets, _, err := scraper.FetchTweets("elonmusk",50, last_ID)
	//if err != nil {
		//panic(err)
	//}
	//for _, tweet := range tweets {
	//	fmt.Println(tweet.ID)
    //}
}
