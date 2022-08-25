import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from src.graphs.undirected_graph import UndirectedGraph
from src.graphs.vertex import Vertex
from src.graphs.edge import Edge
from graphs import search_algorithms
from src.minimum_heap.min_heap import MinHeap
from example_program.calculate_weight import calc_edge_weight


class AnimeSearch(UndirectedGraph):
    """This class inherits UndirectedGraph. 
    
    Attributes:
        media_names: A dict of str, Vertex to map a name to a Vertex.
        media_tags: A dict of str, set to map tags to each Vertex.
    """
    def __init__(self) -> None:
        """Constructs an AnimeSearch object."""
        super().__init__()
        self.media_names: dict[str, Vertex] = {}
        self.media_tags: dict[str, set] = {}
        
    async def search(self, query: str) -> MinHeap:
        """Returns a MinHeap of media search results.
        
        This function is async/awaitable.
        
        Args:
            query: A str query.
            
        Returns:
            A MinHeap of Vertices containing media information.
        """
        return search_algorithms.dijkstra(self, self.media_names[query])
    
    def add_media(self, src: Vertex) -> None:
        """Adds a media to the database.
        """
        v_id = src.get_id().lower()
        # ignore if Vertex already exists
        if v_id in self.media_names.keys():
            return
        # add Vertex to database
        self._update_tags(src)
        for dest in self.media_names.values():
            weight = calc_edge_weight(src, dest)
            self.add(Edge(src, dest, weight))
        self.media_names[v_id] = src
        
    def update_media(self, src: Vertex) -> None:
        """Updates the connections from/to a source Vertex.
        
        Args:
            src: The Vertex to update.
            
        Returns:
            None.
        """
        self.media_names[src.get_id().lower()] = src
        if src not in self._graph:
            return
        # remove vertex connections
        self.remove_media(src)
        self.add_media(src)
        
    def remove_media(self, src: Vertex) -> None:
        """Removes a media from the database.
        """
        self.media_names.pop(src.get_id().lower())
        # update tags dict
        for tag in src.get_tags():
            tag = tag.lower()
            if tag not in self.media_tags:
                continue
            self.media_tags[tag].remove(src)
        # remove from graph
        self.remove(src)
        
    def _update_tags(self, src: Vertex) -> None:
        """Updates internally-stored tags data.
        """
        for tag in src.tags:
            tag = tag.lower()
            if tag not in self.media_tags:
                self.media_tags[tag] = set()
            self.media_tags[tag].add(src)
    