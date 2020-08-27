import get_tweets
import markov_chain

if __name__ == '__main__':
    tweets = get_tweets.returnTweets("tweet")
    model = markov_chain.MarkovChain(tweets)
    while True:
        command = input("Press enter for a tweet, or quit to stop")
        if command=="quit":
            break
        print(model.generateInput())