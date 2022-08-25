"""This file contains the UndirectedGraph class,
an interface representing an undirected graph.

Example usage:
    # vertices
    v1 = Vertex('A', ['AA', 'AB', 'AC'], 1.0)
    v2 = Vertex('B', ['BA', 'BB', 'BC'], 2.0)
    v3 = Vertex('C', ['CA', 'CB', 'CC'], 1.5)
    v4 = Vertex('D', ['DA', 'DB', 'DC'], 3.0)
    
    # graph object
    ug = UndirectedGraph([Edge(v1, v2, v1.score + v2.score)])
    
    # adding to graph
    ug.add(Edge(v1, v3, v1.score + v4.score))
    ug.add(Edge(v2, v4, v2.score + v4.score))
    ug.add(Edge(v4, v1, v4.score + v1.score))
    
    print(ug)
    ug.remove(v1)
    print(ug)
"""
from __future__ import annotations # typing
from typing import Any, Hashable, Iterable # typing
from io import BytesIO # typing
import copy # for creating deepcopy of graph
import random # to select a random vertex
import pickle # for file IO

from src.graphs.vertex import Vertex # graph vertex
from src.graphs.edge import Edge # graph edges


class UndirectedGraph:
    """This class provides an interface representing an undirected graph.
    It is meant to be used with the accompanied Vertex and Edge classes.
    
    Attributes:
        _graph: A dict with Vertex as keys and A set of Edges as its values.
    """
    def __init__(self, edges: Iterable[Edge]=[]) -> None:
        """Constructs an UndirectedGraph object.
        
        Args:
            edges: An (optional) iterable of edges to create the graph with.
                This graph will be empty by default.
        
        Returns:
            None.
        """
        # graph represented as a dict of set 
        # stores Vertex: {Edge, Edge, ...}
        self._graph: dict[Vertex, set[Edge]] = {}
        self.add_connections(edges)
    
    def __str__(self) -> str:
        """Returns a str representation of the UndirectedGraph."""
        result = ['{']
        for src, edges in self._graph.items():
            # str formatting
            s = []
            for edge in edges:
                s.append(str(edge))
            s = ', '.join(s)
            result.append(f'   {str(src.id)}: {s}')
        result.append('}')
        return '\n'.join(result)
    
    def __eq__(self, other: Any) -> bool:
        """Compares the given object to see if it is equivalent.
        
        Args:
            other: Any object.
        
        Returns:
            A bool.
        """
        if isinstance(other, self.__class__):
            return self._graph == other._graph
        return False
    
    def __contains__(self, key: Hashable) -> bool:
        """Checks if the given key exists in the graph.
        
        Args:
            key: A hashable key.
            
        Returns:
            None.
        """
        return key in self._graph
        
    def add(self, edge: Edge) -> None:
        """Adds the given Edge to the graph."""
        self._add_vertex(edge.v1, edge.v2)
        # connect vertices bi-directionally
        self._graph[edge.v1].add(edge)
        self._graph[edge.v2].add(edge)
    
    def add_connections(self, edges: Iterable[Edge]) -> None:
        """Adds the given Edges to the graph.
        
        Args:
            edges: An iterable of Edges.
            
        Returns:
            None.
        """
        for edge in edges:
            self.add(edge)
            
    def get_edges(self, src: Vertex) -> set[Edge]:
        """Returns a set of edges from a source Vertex.
        Returns an empty set if given Vertex does not exist.
        
        Args:
            src: A source Vertex.
        
        Returns:
            A set of Vertices.
        """
        if src not in self._graph:
            return set()
        return self._graph[src]
    
    def get_sources(self) -> set:
        """Returns a set of vertices to graph."""
        return self._graph.keys()

    def get_random_source(self) -> Vertex:
        """Returns a random Vertex from the graph. Returns
        None if graph is empty."""
        if len(self._graph) > 0:
            return random.choice(tuple(self._graph.keys()))
        return None
    
    def size(self) -> int:
        """Returns an int number of source Vertices in the graph."""
        return len(self._graph)
            
    def copy(self) -> UndirectedGraph:
        """Returns a deepcopy of the Undirected Graph object."""
        c = UndirectedGraph()
        c._graph = copy.deepcopy(self._graph)
        return c
            
    def remove(self, *vertices: Vertex) -> None:
        """Completely removes the given Vertex/Vertices from the graph.
        
        Vertex is ignored if it does not exist in the graph.
        
        Args:
            *vertices: Vertex object(s) to be removed.
        
        Returns:
            None.
        """
        for src in vertices:
            if src not in self._graph:
                continue
            # remove all connections to vertex
            for edge in self._graph.pop(src):
                self._graph[edge.other(src)].remove(edge)
                    
    def remove_all(self) -> None:
        """Removes all data stored in the graph."""
        self._graph.clear()
        
    def _add_vertex(self, *vertices: Vertex) -> None:
        """Adds the given Vertices to the graph. Will not create
        any connections with the rest of the graph.
        
        Ignores if Vertex already exists in graph.
        
        Args:
            *vertices: Vertex object(s) to be added.
            
        Returns:
            None.
        """
        # create new set if vertex not in graph
        for src in vertices:
            if src not in self._graph:
                self._graph[src] = set()
                
    def save_pickle(self, file_path: str) -> BytesIO:
        """Saves the UndirectedGraph into a pickle file.
        
        Args:
            file_path: A str file path for the output file.
            
        Returns:
            None.
        """
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
            
    def read_pickle(self, file_path: str) -> UndirectedGraph:
        """Returns an UndirectedGraph from a pickle file.
        
        Args:
            file_path: A str file path for the input file.
            
        Returns:
            An UndirectedGraph stored in the file.
        """
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
        return graph
    