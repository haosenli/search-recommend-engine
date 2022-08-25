"""Vertex provides a simple data storage structure for the search engine.
"""
from typing import Any, Hashable

class Vertex:
    """TODO: Write summary of class.
    Attributes:
    """
    def __init__(self, id: Hashable, tags: set[str]=None,
                 score: float=None, info: Any=None) -> None:
        """Constructs a new Vertex with the given data.
        TODO: Document.
        """
        self.id = id
        self.tags = tags
        self.score = score
        self.info = info
        
    def __str__(self) -> str:
        """Returns a str representation of the Vertex"""
        return f'Vertex: {str(self.id)}'+ ': {' + f'tags: {self.tags}, ' + \
            f'score: {self.score}, info: {self.info}' + '}'
    
    def __eq__(self, other: Any) -> bool:
        """Returns a bool to check if the other given 
        object is equivalent to the current Vertex.
        """
        if isinstance(other, self.__class__):
            return self.id == other.id and \
                self.tags == other.tags and \
                self.score == other.score and \
                self.info == other.info
        return False
    
    def __hash__(self) -> int:
        """Returns an int hash code for the Vertex object.
        """
        return hash(self.id)
    
    def get_id(self) -> Hashable:
        """Returns a hashable ID."""
        return self.id
    
    def get_tags(self) -> set[str]:
        """Returns a set of associated tags of the Vertex."""
        return self.tags 

    def get_score(self) -> float:
        """Returns a score as a float."""
        return self.score

    def get_info(self) -> Any:
        """Returns a dict of information."""
        return self.info

    def add_tags(self, *tags: str) -> None:
        """Adds tags to the Vertex.
        TODO: Document
        """
        for tag in tags:
            self.tags.append(tag)
