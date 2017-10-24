import json
import sys

from helpers import relative_path, find_end_time
from orderbook import Orderbook

# filters
arb_filter = lambda s: s.sum_offer_at(END_TIME) < s.etf_bid_at(END_TIME) or s.sum_bid_at(END_TIME) > s.etf_offer_at(END_TIME)
vol_filter = lambda s: s.sum_volume_at(END_TIME) > 100 and s.etf_volume_at(END_TIME) > 10
no_filter = lambda s: True

END_TIME = find_end_time()
ITEMSET_FILTER = arb_filter

class ItemSet(object):
    def __init__(self, summary, set_description):
        self.item_id = set_description['id']
        self.etf_name = set_description['name']
        self.orderbook = Orderbook(summary, self.item_id)
        self.parts = [Orderbook(summary, part['id']) for part in set_description['parts']]

    def sum_price_at(self, timestamp):
        return sum(part.price_at(timestamp) for part in self.parts)

    def etf_price_at(self, timestamp):
        return self.orderbook.price_at(timestamp)

    def sum_volume_at(self, timestamp):
        return sum(part.volume_at(timestamp) for part in self.parts)

    def min_volume_at(self, timestamp):
        return min(part.volume_at(timestamp) for part in self.parts)

    def etf_volume_at(self, timestamp):
        return self.orderbook.volume_at(timestamp)

    def sum_bid_at(self, timestamp):
        return sum(part.bid_at(timestamp) for part in self.parts)

    def etf_bid_at(self, timestamp):
        return self.orderbook.bid_at(timestamp)

    def sum_offer_at(self, timestamp):
        return sum(part.offer_at(timestamp) for part in self.parts)

    def etf_offer_at(self, timestamp):
        return self.orderbook.offer_at(timestamp)

    def __str__(self):
        return 'ItemSet(id={}, parts={}, asset_name={})'.format(self.item_id, ', '.join(p.item_id for p in self.parts), self.etf_name)

    def __repr__(self):
        return self.__str__()

def load_sets(sets_json, summary):
    items = [ItemSet(summary, set_description) for set_description in sets_json.values()]
    return [i for i in items if ITEMSET_FILTER(i)]

def show_overview(sets_json, summary):
    sets = load_sets(sets_json, summary)
    print "{: >11} {: >11} {: >11} {: >11} {: >11}    {}".format("ETF Vol", "Min Vol", "Price Diff", "Sum Price", "ETF Price", "ItemSet")
    for s in sorted(sets, key=lambda s: abs(s.sum_price_at(END_TIME) - s.etf_price_at(END_TIME)), reverse=True):
        sump = s.sum_price_at(END_TIME)
        etfp = s.etf_price_at(END_TIME)
        print "{: >11} {: >11} {: >11} {: >11} {: >11}    {}".format(s.etf_volume_at(END_TIME), s.min_volume_at(END_TIME), sump - etfp, sump, etfp, s)

def show_item(sets_json, summary, item_id):
    item_set = ItemSet(summary, sets_json[item_id])
    print "{}".format(item_set)
    print "{: >10} {: >10} {: >10} {: >10}   {: <10}".format("Price", "Bid", "Ask", "Volume", "Item")
    print "{: >10} {: >10} {: >10} {: >10}   {: <10}".format(
                                                   item_set.etf_price_at(END_TIME), 
                                                   item_set.etf_bid_at(END_TIME), 
                                                   item_set.etf_offer_at(END_TIME),
                                                   item_set.etf_volume_at(END_TIME),
                                                   item_set.orderbook)
    print "{: >10} {: >10} {: >10} {: >10}   {: <10}".format(
                                                   item_set.sum_price_at(END_TIME), 
                                                   item_set.sum_bid_at(END_TIME), 
                                                   item_set.sum_offer_at(END_TIME),
                                                   item_set.sum_volume_at(END_TIME),
                                                   "Total")
    for part in item_set.parts:
        print "{: >10} {: >10} {: >10} {: >10}   {: <10}".format(
                                               part.price_at(END_TIME), 
                                               part.bid_at(END_TIME), 
                                               part.offer_at(END_TIME),
                                               part.volume_at(END_TIME),
                                               part)


def main():
    with open(relative_path('static', 'sets.json')) as f:
        sets_json = json.load(f)
    with open(relative_path('static', 'summary.json')) as f:
        summary = json.load(f)

    if len(sys.argv) > 1:
        show_item(sets_json, summary, sys.argv[1])
    else:
        show_overview(sets_json, summary)

if __name__ == "__main__":
    main()
