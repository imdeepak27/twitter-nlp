import json
import time

import requests

import helper_functions

r = helper_functions.connect_redis_db()

def gen_tweet_stats():
    time_interval = 1
    while True:
        time_start = time.time()
        url = 'http://compute-tweet-stats.cfapps.pez.pivotal.io/tweet_rate'
        tr = requests.get(url, {'time_interval': time_interval}).content

        url = 'http://compute-tweet-stats.cfapps.pez.pivotal.io/avg_sentiment'
        avg_polarity = requests.get(url, {'time_interval': time_interval}).content
        while not helper_functions.been_n_second(.98, time.time(), time_start, wait_time=.01):
            pass
        stats = {'tweet_rate': tr, 'avg_polarity': avg_polarity}
        r.publish('tweet_stats', json.dumps(stats))

if __name__ == '__main__':
    gen_tweet_stats()