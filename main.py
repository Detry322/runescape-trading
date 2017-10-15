import json

from helpers import relative_path, normalized
from orderbook import Orderbook
from metrics import orderbook_stddev, orderbook_spread, orderbook_unbounded, orderbook_regression_error, orderbook_regression_r2

INCREMENT = 30*60*1000 # minutes
START_TIME = 1507828958159 # Wed Sep 20 2017 13:30:00 GMT-0400 (EDT)
END_TIME = 1508085531453

RANGE = range(START_TIME, END_TIME, INCREMENT)

METRIC = orderbook_regression_r2
FILTER = lambda item: 1500000 > item['overall_average'] > 100000

def load_orderbooks():
    summary_file = relative_path('data', 'summary.json')
    with open(summary_file, 'r') as f:
        summaries = json.load(f)
        downloadable = [item_summary for item_summary in summaries.values() if FILTER(item_summary)]
        orderbooks = [Orderbook(summaries, item['id']) for item in downloadable]
        return orderbooks

def main():
    orderbooks = load_orderbooks()
    results = [(METRIC(orderbook, RANGE), orderbook) for orderbook in orderbooks]
    for r, orderbook in sorted(results, reverse=True):
        print "{:< 10.02f} {:< 10.0f} {:< 10.0f} {}".format(r, orderbook.volume_at(END_TIME), orderbook.price_at(END_TIME), orderbook)
    

if __name__ == '__main__':
    main()
