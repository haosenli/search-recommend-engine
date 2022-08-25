"""This file contains the Edge class, a simple edge that
contains data on 2 vertices.

Example Usage:
    # create Vertices
    v1 = Vertex('a')
    v2 = Vertex('b')
    
    # create Edge
    edge = Edge(v1, v2, 3.0)
"""
from typing import Any # typing
from src.graphs.vertex import Vertex # graph vertex

class Edge:
    """This class connects two Vertex objects and gives them a weight.
    
    Attributes:
        v1: The first Vertex object.
        v2: The second Vertex object.
        weight: The weight relationship between two Vertices
    """
    def __init__(self, v1: Vertex, v2: Vertex, weight: float) -> None:
        """Constructs an Edge object.
        
        Args:
            v1: The first Vertex object.
            v2: The second Vertex object.
            weight: The weight relationship between two Vertices
        
        Returns:
            None.
        """
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        
    def __str__(self) -> str:
        """Returns a str representation of this Edge."""
        return '{' + f'{self.get_v1().id} <--> {self.get_v2().id} , weight: {self.get_weight()}' + '}'
    
    def __eq__(self, other: Any) -> bool:
        """Checks to see if the other object is equivalent to itself."""
        if isinstance(other, self.__class__):
            return self.v1 == other.v1 and \
                self.v2 == other.v2 and \
                self.weight == other.weight
        return False
    
    def __hash__(self) -> int:
        """Returns an int hash code for this edge."""
        return hash((self.v1, self.v2))
        
    def get_v1(self) -> Vertex:
        """Returns the first Vertex in the Edge."""
        return self.v1
    
    def get_v2(self) -> Vertex:
        """Returns the second Vertex in the Edge."""
        return self.v2
    
    def other(self, v: Vertex) -> Vertex:
        """Returns the other Vertex from a given Vertex.
        
        Returns None if given Vertex is not in this Edge.
        
        Args:
            v: The source Vertex.
            
        Returns:
            The destination Vertex.
        """
        if v != self.get_v1() and v != self.get_v2():
            return None
        if v == self.v1:
            return self.get_v2()
        return self.get_v1()
        
    def get_weight(self) -> float:
        """Returns the float weight of the Edge."""
        return self.weight
        
    def set_weight(self, weight: float) -> None:
        """Sets a float weight for the Edge."""
        self.weight = weight