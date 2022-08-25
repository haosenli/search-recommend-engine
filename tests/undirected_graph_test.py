"""TODO: Document.
"""
import unittest # for unit testing
import sys # for import from parent directory
import os # for import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# import custom classes
from src.graphs.undirected_graph import UndirectedGraph
from src.graphs.vertex import Vertex
from src.graphs.edge import Edge


class UndirectedGraphTest(unittest.TestCase):
    """TODO: Document.
    """
    pass
        

if __name__ == '__main__':
    unittest.main()