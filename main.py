import json

from helpers import relative_path, normalized
from orderbook import Orderbook
from metrics import orderbook_stddev, orderbook_spread, orderbook_unbounded, orderbook_regression_error, orderbook_regression_r2

INCREMENT = 30*60*1000 # minutes
START_TIME = 1507828958159 # Wed Sep 20 2017 13:30:00 GMT-0400 (EDT)
END_TIME = 1508085531453

RANGE = range(START_TIME, END_TIME, INCREMENT)

METRIC = normalized(orderbook_regression_error)
ITEM_FILTER = lambda item: 15000 > item['overall_average'] > 2000
ORDERBOOK_FILTER = lambda orderbook: orderbook.volume_at(END_TIME) > 4

def load_orderbooks():
    summary_file = relative_path('data', 'summary.json')
    with open(summary_file, 'r') as f:
        summaries = json.load(f)
        downloadable = [item_summary for item_summary in summaries.values() if ITEM_FILTER(item_summary)]
        orderbooks = [Orderbook(summaries, item['id']) for item in downloadable]
        return [orderbook for orderbook in orderbooks if ORDERBOOK_FILTER(orderbook)]

def main():
    orderbooks = load_orderbooks()
    results = [(METRIC(orderbook, RANGE), orderbook) for orderbook in orderbooks]
    for r, orderbook in sorted(results, reverse=True):
        print "{:< 10.02f} {:< 10.0f} {:< 10.0f} {}".format(r, orderbook.volume_at(END_TIME), orderbook.price_at(END_TIME), orderbook)
    

if __name__ == '__main__':
    main()
