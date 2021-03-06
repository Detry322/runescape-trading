from helpers import stddev

import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

def orderbook_stddev(orderbook, r):
    samples = [orderbook.price_at(timestamp) for timestamp in r]
    return stddev(samples)

def orderbook_better_stddev(orderbook, r):
    samples = [
        orderbook.price_at(timestamp)
        for timestamp in r
        if orderbook.offer_at(timestamp) != float('inf') and orderbook.bid_at(timestamp) != 0
    ]
    if len(samples) == 0:
        return 0
    return stddev(samples)

def orderbook_spread(orderbook, r):
    spreads = [
        orderbook.offer_at(timestamp) - orderbook.bid_at(timestamp)
        for timestamp in r
        if orderbook.offer_at(timestamp) != float('inf') and orderbook.bid_at(timestamp) != 0
    ]
    if len(spreads) == 0:
        return 0
    return sum(spreads)/float(len(spreads))

def orderbook_unbounded_offer(orderbook, r):
    return sum(1 if orderbook.offer_at(timestamp) == float('inf') else 0 for timestamp in r)

def orderbook_unbounded_bid(orderbook, r):
    return sum(1 if orderbook.bid_at(timestamp) == 0 else 0 for timestamp in r)

def orderbook_unbounded(orderbook, r):
    return orderbook_unbounded_offer(orderbook, r) + orderbook_unbounded_bid(orderbook, r)

def orderbook_regression_error(orderbook, r):
    samples = [orderbook.price_at(timestamp) for timestamp in r]
    r = np.array(r).reshape(-1, 1)
    regr = linear_model.LinearRegression()
    regr.fit(r, samples)
    predicted = regr.predict(r)
    return mean_squared_error(samples, predicted)**0.5

def orderbook_regression_r2(orderbook, r):
    samples = [orderbook.price_at(timestamp) for timestamp in r]
    r = np.array(r).reshape(-1, 1)
    regr = linear_model.LinearRegression()
    regr.fit(r, samples)
    return -regr.score(r, samples)
