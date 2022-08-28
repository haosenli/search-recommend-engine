"""This file contains benchmarking functions for measuring memory efficiency
"""
import asyncio
from random import random
from statistics import mean # for benchmarking
from time import time, sleep # for benchmarking
import sys # for import from parent directory
import os # for import from parent directory
from typing import Callable, Iterable 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from src.graphs.search_graph import SearchGraph as sg0
from src.search_engine.search_engine import SearchEngine as se
from old.graphs.search_graph import SearchGraph as sg1
from src.graphs.search_item import SearchItem
from src.graphs import search_algorithms


def weight_func(item1, item2) -> Callable:
    return random() * 100

def generate_items(size: int=10000) -> Iterable[SearchItem]:
    """Generates a given size of SearchItems."""
    for i in range(size):
        yield SearchItem(str(i), tags={f'tag{i}'}) 

def build_sg():
    g = se()
    for item in generate_items():
        g.add_item(item, weight_func, weight_thres=0)
    return g


def build_nx():
    g = sg1()
    for item in generate_items():
        g.add_item(item, weight_func)
    return g

async def main():
    g = build_sg()
    print('finished building graph.')
    g.recommend('1')
    
    

if __name__ == '__main__':
    asyncio.run(main())