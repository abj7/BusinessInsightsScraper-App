from twython import Twython
import json
import pandas as pd

df = pd.DataFrame(['<a href="http://example.com">example.com</a>'])

def search_tweets(company_name):
    with open("Parser/twitter_credentials.json", "r") as file:
        creds = json.load(file)
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    query = {'q': company_name,
            'count': 100,
            'lang': 'en',
            }

    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'twitter_url': []}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])
        dict_['twitter_url'].append("https://twitter.com/" + status['user']['screen_name'] + "/status/" + status['id_str'])

    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    df = df.head(20)
    return df