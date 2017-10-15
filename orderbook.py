from helpers import relative_path
import json
import bisect

class DataPoint(object):
    def __init__(self, underlying):
        self.underlying = underlying

    def __getitem__(self, item):
        if item in self.underlying:
            return self.underlying[item]
        if item == 'buyingPrice':
            return float('inf')
        return 0

class Orderbook(object):
    """
        A simple class that can be used to query the price of a asset_name at a given point in time.
    """
    def __init__(self, summary, item_id):
        self.item_id = str(item_id)
        self.asset_name = summary[self.item_id]['name']
        with open(relative_path('data', '{}.json'.format(item_id)), 'r') as f:
            self.orders = sorted([DataPoint(point) for point in json.load(f)], key=lambda x: x['ts'])
            self.timestamps = [x['ts'] for x in self.orders]

    def info_at(self, timestamp):
        index = bisect.bisect(self.timestamps, timestamp)
        return self.orders[index if index != len(self.timestamps) else index - 1]

    def price_at(self, timestamp):
        return self.info_at(timestamp)['overallPrice']

    def volume_at(self, timestamp):
        return self.info_at(timestamp)['overallCompleted']

    def bid_at(self, timestamp):
        return self.info_at(timestamp)['sellingPrice']

    def offer_at(self, timestamp):
        return self.info_at(timestamp)['buyingPrice']

    def __str__(self):
        return 'Orderbook(id={}, asset_name={})'.format(self.item_id, self.asset_name)

    def __repr__(self):
        return self.__str__()
