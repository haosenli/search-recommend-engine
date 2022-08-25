import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from time import time
import asyncio
import pickle


from src.graphs.vertex import Vertex
from src.trie.word_trie import WordTrie
from src.minimum_heap.min_heap import MinHeap
from old.example_program.anime_search import AnimeSearch


def load_vertices():
    """Generator for vertices"""
    v_path = r'C:\Users\haose\OneDrive\Desktop\Projects\individualized-search-engine\dataset\vertices.pkl'
    with open(v_path, 'rb') as f:
        vertices = pickle.load(f)
    for v in vertices:
        yield v
        
def load_word_trie():
    """Returns a Word Trie"""
    wt_path = r'C:\Users\haose\OneDrive\Desktop\Projects\individualized-search-engine\dataset\word_trie_test.pkl'
    with open(wt_path, 'rb') as f:
        wt = pickle.load(f)
    return wt

async def main():
    anime_search = AnimeSearch()
    word_trie = load_word_trie()
    print('building anime search')
    for vertex in load_vertices():
        anime_search.add_media(vertex)
    print('finished building anime search')
    
    query = await word_trie.word_suggestions('A')
    results: MinHeap = await anime_search.search(query[0])
    print(results.peek().get_id())
    
if __name__ == '__main__':
    asyncio.run(main())