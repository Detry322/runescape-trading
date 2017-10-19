import os
import json

def stddev(lst):
    """calculates standard deviation"""
    mn = float(sum(lst)) / len(lst)
    return (sum(map(lambda x: (x - mn)**2.0, lst))/(len(lst) + 1))**0.5

def normalized(func):
    def new(orderbook, r):
        return func(orderbook, r)/orderbook.price_at(list(r)[-1])
    return new

def relative_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)

def find_end_time():
    CANNONBALL_ID = '2'
    with open(relative_path('data', '{}.json'.format(CANNONBALL_ID)), 'r') as f:
        data = json.load(f)
        return data[-1]['ts']

