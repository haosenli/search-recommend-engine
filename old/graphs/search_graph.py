from typing import Callable, Iterator
import random
import re
import networkx as nx


from src.minimum_heap.min_heap import MinHeap
from src.graphs.search_item import SearchItem
from src.trie.word_trie import WordTrie
from src.graphs import search_algorithms
from src.utils.formatting import wordtrie_format


class SearchGraph:
    """This class is a wrapper for an undirected NetworkX graph,
    tailored for building a search engine network.
    
    Attributes:
        graph: A NetworkX Graph.
        items: A dict of names mapped to SearchItems.
        tags: A dict of tags with set of SearchItem names.
        words: A WordTrie containing all the SearchItem names.
    """
    def __init__(self) -> None:
        """Constructs a SearchGraph. No args are taken."""
        self.graph = nx.Graph()
        self.items: dict[str, SearchItem] = {}
        self.tags: dict[str, set[str]] = {}
        self.words = WordTrie()
        
    def __iter__(self) -> Iterator[SearchItem]:
        """Returns an iterator over all SearchItems."""
        return iter(self.items.values())
    
    def __contains__(self, item_name: str) -> bool:
        """Returns True if item_name is in SearchGraph, False otherwise."""
        return wordtrie_format(item_name) in self.items
        
    async def search(self, query: str) -> MinHeap:
        """An awaitable function to search from a name, returns
        a MinHeap of SearchItem.
        """
        query = wordtrie_format(query)
        query = self.words.word_suggestions(query)[0]
        return search_algorithms.dijkstra(self, query)
    
    def add_item(self, item: SearchItem, 
                 weight_calc: Callable) -> None:
        """Adds a SearchItem to the SearchGraph.
        
        Item name cannot be added if already exists.
        
        Args:
            item: A SearchItem to add into the graph.
            weight_calc: A callable function to calculate the weight between 
                two SearchItems. The callable must take two SearchItems 
                as arguments and return a float weight.
                
        Returns:
            None.
        """
        wt_name = wordtrie_format(item.get_name())
        # do nothing if name already exists
        if wt_name in self.items:
            # TODO: Add SearchGraph Exceptions
            print('[ABORTED] add_item(): '
                  f'item name "{wt_name}" already exists.')
            return
        # self._update_tags(item) # for search by tag
        self.words.add_words(wt_name) # add to WordTrie
        self.graph.add_node(wt_name) # add node to Graph
        # add edge weights to Graph
        other_item: SearchItem
        for other_item in self.items.values():
            score = weight_calc(item, other_item)
            other_wt_name = wordtrie_format(other_item.get_name())
            self.graph.add_edge(wt_name, other_wt_name, weight=score)
        # add to items
        self.items[wt_name] = item
    
    def get_edges(self, item_name: str) -> Iterator[str]:
        """A generator function to iterate over edges from a given
        source name. 
        
        Given name must be formatted using wordtrie_format
        in src.utils.formatting.py
        
        Args:
            item_name: A str formatted item name.
        
        Returns:
            An iterator containing str item name of an edge.
        """
        if item_name not in self.items:
            # TODO: Add SearchGraph Exceptions
            print('[ABORTED] get_edges(): '
                f'item name "{item_name}" does not exist.')
            return
        
        for src, dest, data in self.graph.edges(item_name, data=True):
            yield dest, data['weight']

    def remove(self, item_name: str) -> None:
        """Removes a given item from the SearchGraph."""
        if item_name in self.items:
            self.graph.remove_node(item_name)
            self.items.pop(item_name)
            self.words.remove_words(item_name)
    
    def random_item(self) -> SearchItem:
        """Returns a random item from the graph."""
        return random.choice(tuple(self.items.values()))

    def _update_tags(self, item: SearchItem) -> None:
        """Updates internally-stored tags data.
        """
        for tag in item.get_tags():
            tag = wordtrie_format(tag)
            # add tag into word trie some day
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(item.get_name())
            