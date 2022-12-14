"""This file contains functions for running graph algorithms
compatible with the UndirectedGraph class.
"""
from src.graphs.undirected_graph import UndirectedGraph # graph data structure
from src.graphs.vertex import Vertex # graph vertex
from src.minimum_heap.min_heap import MinHeap # minimum heap for dijkstra

def dijkstra(graph: UndirectedGraph, src: Vertex) -> MinHeap:
    """Finds the shortest paths from a given graph and source Vertex
    using Dijkstra's Shortest Path algorithm.
    
    Returns None if given Vertex is invalid or not in graph.
    
    Args:
        graph: An UndirectedGraph object.
        src: A source Vertex to start from.
        
    Returns:
        A MinHeap with Vertices sorted by shortest path to longest.
    """
    # checks if src is a valid vertex or if src exists in graph
    if not src or not src in graph:
        return None
    # instantiate data strucutres for algorithm
    known = set()
    edge_to: dict[Vertex, Vertex] = {} # stores which Vertex a Vertex came from
    dist_to: dict[Vertex, int] = {} # stores distance to source Vertex
    # set starting distance
    dist_to[src] = 0
    # instantiate max heap
    result = MinHeap()
    min_heap = MinHeap()
    min_heap.add(src, dist_to[src])
    # find shortest paths
    while min_heap.size() > 0:
        u = min_heap.pop() # longest dist in queue
        known.add(u) # add to known
        if u in result:
            result.change_priority(u, dist_to[u])
        else:
            result.add(u, dist_to[u]) # add to results
        # traverse through edges
        for edge in graph.get_edges(u):
            v = edge.other(u)
            old_dist = dist_to.get(v, float('inf'))
            new_dist = dist_to.get(u) + edge.get_weight()
            # ignore if new distance is longer than old
            if new_dist > old_dist:
                continue
            # update shortest path
            dist_to[v] = new_dist
            edge_to[v] = u
            # update min heap
            if v in min_heap:
                min_heap.change_priority(v, new_dist)
            else:
                min_heap.add(v, new_dist)
    return result
