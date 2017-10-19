import urllib2
import json
import time
import random
import os
from urllib import urlencode
from multiprocessing.dummy import Pool as ThreadPool 

API_ROUTE = "https://api.rsbuddy.com/grandExchange"
INCREMENT = 30 # minutes
START_TIME = 1507328958159 # Wed Sep 20 2017 13:30:00 GMT-0400 (EDT)

MAX_RETRY = 10000
MAX_SLEEP = 2

def relative_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)

def load_item(item_summary):
    print "Loading {} ({})".format(item_summary['name'], item_summary['id'])
    query_params = {
        'a': 'graph',
        'g': INCREMENT,
        'start': START_TIME,
        'i': item_summary['id']
    }
    url = API_ROUTE + '?' + urlencode(query_params)
    retry_count = 1
    while retry_count <= MAX_RETRY:
        try:
            return json.load(urllib2.urlopen(url))
        except urllib2.HTTPError:
            print "Couldn't load item: {} ({}), try {}".format(item_summary['name'], item_summary['id'], retry_count)
            time.sleep(random.random()*MAX_SLEEP)
        except urllib2.URLError:
            pass
        retry_count += 1
    raise Exception("Couldn't load item {} ({}) after {} tries".format(item_summary['name'], item_summary['id'], MAX_RETRY))

def filter_criteria(item_summary):
    return item_summary['overall_average'] > 4 and not os.path.isfile(relative_path('data', '{}.json'.format(item_summary['id'])))

def download_items(items):
    p = ThreadPool(32)
    def single_download(item):
        with open(relative_path('data', '{}.json'.format(item['id'])), 'w') as f:
            json.dump(load_item(item), f, sort_keys=True, indent=4, separators=(',', ': '))
    p.map(single_download, items)

def main():
    summary_file = relative_path('static', 'summary.json')
    with open(summary_file, 'r') as f:
        summary = json.load(f)
    print "Loaded {} runescape items".format(len(summary))

    downloadable = [item_summary for item_summary in summary.values() if filter_criteria(item_summary)]
    print "Downloading {} runescape item histories".format(len(downloadable))

    download_items(downloadable)


if __name__ == "__main__":
    main()
