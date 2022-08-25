import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import asyncio

from src.minimum_heap.min_heap import MinHeap
from src.graphs.search_item import SearchItem
from src.graphs.search_graph import SearchGraph
from src.search_engine.search_engine import SearchEngine
from example_program.calculate_weight import calc_edge_weight

def calc_similarities(item1: SearchItem, item2: SearchItem) -> int:
    """Returns an int similarity from two SearchItems."""
    set1 = item1.get_tags()
    set2 = item2.get_tags()
    similarity = 0
    set1_len = len(set1)
    # iterate thru the smaller set
    if set1_len == min(set1_len, len(set2)):
        for tag in set1:
            if tag not in set2:
                continue
            similarity += 1
    else:
        for tag in set2:
            if tag not in set1:
                continue
            similarity += 1
    return 10 - similarity

### globals
items = [
    SearchItem('Nate', {'tag1', 'tag2', 'tag3', 'tag4'}),
    SearchItem('Nathan', {'tag1', 'tag2', 'tag3', 'tag4'}),
    SearchItem('nathank', {'tag1', 'tag7', 'tag2', 'tag4'}),
    SearchItem('Haosen', {'tag6', 'tag5', 'tag3', 'tag4'}),
    SearchItem('haoli', {'tag1', 'tag5', 'tag6', 'tag4'}),
    # SearchItem('Test', {'tag8', 'tag5', 'tag9', 'tag10'}),
]

se = SearchEngine()
for item in items:
    se.add_item(item, calc_similarities)
###

async def search_results(query: str) -> MinHeap:
    return await se.search(query)
    
async def main():
    results = await search_results('nat')
    for result in results:
        print(f'{result}')
    print()
    print('Graph:')
    for row in se.graph:
        print(row)
    print()
    print('Items:')
    print(se.items)
    print()
    print('Items Dict:')
    print(se.item_dict)

if __name__ == '__main__':
    asyncio.run(main())