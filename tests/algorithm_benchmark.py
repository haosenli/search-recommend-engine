"""This file contains benchmarking functions for graph_algorithms.py
"""
from random import randint
from statistics import mean # for benchmarking
from time import time # for benchmarking
import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from src.graphs.undirected_graph import UndirectedGraph
from src.graphs.vertex import Vertex
from src.graphs.edge import Edge
from graphs import search_algorithms


def dijkstra_bench():
    # runtime scaling
    # print('Dijkstra benchmark for runtime scaling:\n')
    # for i in range(2, 6):
    #     num_verts = 10 ** i // 2
    #     num_edges = 10 ** i
    #     graph, creation_runtimes = create_graph(num_verts, num_edges)
    #     data, algo_runtime = run_dijkstra(graph, graph.get_random_source())
    #     print_info(data, num_verts, num_edges, creation_runtimes, algo_runtime, show_print=False)
    # average runtime
    print('Dijkstra benchmark for runtime consistency:\n')
    timings = []
    runs = 50
    for _ in range(runs):
        num_verts = 250000
        num_edges = 500000
        graph, creation_runtimes = create_graph(num_verts, num_edges)
        data, algo_runtime = run_dijkstra(graph, graph.get_random_source())
        timings.append(float(algo_runtime))
    mean_time = '{:.5f}'.format(mean(timings))
    print(f'The average mean algorithm runtime for {num_verts} '
          f'vertices and {num_edges} edges over {runs} runs is: {mean_time}')
        
def create_graph(
        num_verts: int, 
        num_edges: int,
    ) -> tuple[UndirectedGraph, tuple[float, float, float]]:
    """Creates a graph with data based on the given arguments.
    
    Args:
        num_verts: An int number of vertices to generate.
        num_edges: An int number of edges to generate.
    
    Returns:
        A tuple containing a UndirectedGraph with randomzied data, 
        and a tuple of 3 floats for vertices creation runtime, 
        edges creation runtime, and graph creation runtime.
    """
    v = []
    e = []
    t0 = time()
    # create vertices
    for i in range(num_verts):
        v.append(Vertex(f'v {str(i)}'))
    t1 = time()
    # create edges
    for _ in range(num_edges):
        e.append(Edge(v[randint(0, num_verts-1)], 
                      v[randint(0, num_verts-1)], 
                      randint(10, 100)))
    t2 = time()
    # create graph
    g = UndirectedGraph(e)
    # run shortest path
    t3 = time()
    vert_runtime = '{:.5f}'.format(t1-t0)
    edge_runtime = '{:.5f}'.format(t2-t1)
    graph_runtime = '{:.5f}'.format(t3-t2)
    return g, (vert_runtime, edge_runtime, graph_runtime)
    
def run_dijkstra(
        graph: UndirectedGraph, 
        src: Vertex,
    ) -> tuple[list[tuple[str, int]], float]:
    """Runs dijkstra's algorithm on the given graph and list of vertices.
    
    Args:
        graph: An UndirectedGraph.
        src: A source Vertex.
    
    Returns:
        A tuple containing a list of (str, int) tuples representing an item 
        and its priority, and a float algorithm runtime.
    """
    t0 = time()
    q = search_algorithms.dijkstra(graph, src)
    t1 = time()
    algo_runtime = '{:.5f}'.format(t1-t0)
    return q._sorted(), algo_runtime

def print_info(
        data: list[tuple[str, int]],
        num_verts: int,
        num_edges: int,
        creation_runtime: tuple[float, float, float],
        algo_runtime: float,
        show_print: bool=True,
        ) -> None:
    """Prints out information about a graph algorithm benchmark.
    
    Args:
        data: A list of sorted (vertex name, priority) tuple information.
        num_verts: An int number of vertices.
        num_edges: An int number of edges.
        creation_runtime: A tuple of floats for vertex, edge, and graph
            creation runtime.
        algo_runtime: A float for algorithm runtime.
        show_print: A (optional) bool to enable printing for vertex
            and priority information. Defaults to True.
            
    Returns:
        None.
    """
    v_rt, e_rt, g_rt = creation_runtime
    print(
        f'Benchmark with {num_verts} Vertices and {num_edges} Edges.\n'
        'Runtimes:\n'
        f'Vertices: {v_rt} s, Edges: {e_rt} s, Graph: {g_rt}, '
        f'Algorithm: {algo_runtime} s.\n'
        )
    if show_print:
        width = 8
        template = '{:>6}   ' + 2 * ('{:<' + str(width) + '}   ')
        print(template.format('Index', 'Vertex', 'Priority'))
        print(template.format('_' * 6, '_' * width, '_' * width))
        # print first 50 lines
        for count, info in enumerate(data):
            item, priority = info
            print(template.format(f'{count}.)', str(item.id), str(priority)))
            if count > 30:
                print('...')
                break

def main():
    dijkstra_bench()

if __name__ == '__main__':
    main()