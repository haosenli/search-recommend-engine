from math import sqrt
from statistics import mean, median, stdev
import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import asyncio
import pickle
import time


from src.minimum_heap.min_heap import MinHeap
from src.graphs.search_item import SearchItem
from src.search_engine.search_engine import SearchEngine
from example_program.calculate_weight import calc_edge_weight
from data_collection_tools.utils.status_report import print_progress_bar
  
    
def build_database():
    """Builds Vertices and WordTrie"""
    print('Building AnimeSearch and WordTrie.')
    se = SearchEngine()
    data: dict
    mal:dict
    for data in get_anime_info():
        title = data['title']
        tags = data.get('tags', set())
        mal = data['mal_stats']
        mal['mean'] = mal.get('mean', 0.0)
        # build SearchItem
        item = SearchItem(name=title, tags=tags, info=data)
        # build SearchGraph
        se.add_item(item, calc_edge_weight)
    
    searchengine_path = os.path.join(os.getcwd(), 'dataset/searchengine.pkl')
    with open(searchengine_path, 'wb') as f:
        pickle.dump(se, f)
        
def get_anime_info():
    """Generator for anime info."""
    # load in database
    file_path = os.path.join(os.getcwd(), 'dataset/anime_search_database.pkl')
    with open(file_path, 'rb') as f:
        anime_database = pickle.load(f)
    total_len = len(anime_database)
    
    for cnt, data in enumerate(anime_database.values()):
        print_progress_bar(cnt, total_len)
        # convert lists to sets
        for key, value in data.items():
            if type(value) is not list:
                continue
            data[key] = set(value)
        # convert VAs to sets
        try:
            for lang, vas in data.get('voice_actors').items():
                if type(vas) is not list:
                    continue
                data['voice_actors'][lang] = set(vas)
        except:
            data['voice_actors'] = {'japanese': set()}
        # convert studios
        studios = set()
        for studio in data['mal_stats'].get('studios', []):
            studios.add(studio['name'])
        data['mal_stats']['studios'] = studios
        # yield
        yield data
        
def test():
    se = SearchEngine()
    for i in range(18000):
        print_progress_bar(i, 18000)
        item = SearchItem(name=str(i))
        # build SearchGraph
        def calc(s1, s2):
            pass
        se.add_item(item, calc)
        
async def animesearch_test():
    print('Building SearchEngine.')
    # testing parameters
    samples = 17000
    weight_thres = 32
    trials = 10
    #    
    cwd = os.getcwd()
    # filepath = os.path.join(cwd, 'dataset/searchengine.pkl')
    # with open(filepath, 'rb') as f:
    #     se = pickle.load(f)
    
    se = SearchEngine()
    data: dict
    mal: dict
    for i, data in enumerate(get_anime_info()):
        if i > samples:
            break
        title = data['title']
        tags = data.get('tags', set())
        mal = data['mal_stats']
        mal['mean'] = mal.get('mean', 0.0)
        # build SearchItem
        item = SearchItem(name=title, tags=tags, info=data)
        print(item)
        # build SearchGraph
        se.add_item(item, calc_edge_weight, weight_thres)
    print('Finished building SearchEngine.')
    # runtime benchmark
    se: SearchEngine
    nums = []
    # for row in se.graph:
    #     nums.extend(row)
    
    # matrix = se.graph
    # size = len(se.graph)
    # for i in range(size):
    #     for j in range(size):
    #         weight = matrix[i][j]
    #         if weight < 69:
    #             nums.append(weight)
    
    # filepath = os.path.join(cwd, 'dataset/nums.pkl')
    # with open(filepath, 'wb') as f:
    #     pickle.dump(nums, f)
        
    # filepath = os.path.join(cwd, 'dataset/nums.pkl')
    # with open(filepath, 'rb') as f:
    #     nums = pickle.load(f)
        
    # new_nums = [num for num in nums if num < 32]

    # print(f'Num edge weights: {len(new_nums)}')
    # print(f'Num vertices: {sqrt(len(new_nums))}')
    # print(f'Mean: {mean(new_nums)}')
    # print(f'Median: {median(new_nums)}')
    # print(f'Std deviation: {stdev(new_nums)}')
    
    t0 = time.time()
    for _ in range(trials):
        results = await se.search('a', limit=5)
    print(f'Average runtime for {samples} samples in {trials} trials: '
          f'{(time.time()-t0)/trials} s.')
        
if __name__ == '__main__':
    # build_database()
    asyncio.run(animesearch_test())