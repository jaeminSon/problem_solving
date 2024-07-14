from typing import TypeVar, List

###############
# ALL NAMES ARE UPPERCASE.
################

NAT = TypeVar("NAT") # subtype of INT, REAL
INT = TypeVar("INT") # subtype of REAL
REAL = TypeVar("REAL")

LIST1D = TypeVar("LIST1D")
LIST2D = TypeVar("LIST2D")

STRING = TypeVar("STRING")

NODE = TypeVar("NODE")
TREE = TypeVar("TREE") # subtype of GRAPH
TREE_HLD = TypeVar("TREE_HLD")
BIPARTITE = TypeVar("BIPARTITE") # subtype of GRAPH
GRAPH = TypeVar("GRAPH")
GRAPH_NONNEGEDGE = TypeVar("GRAPH_NONNEGEDGE") # subtype of GRAPH

POINT2D = TypeVar("POINT2D") # subtype of LIST1D
POLYGON2D = List[POINT2D] # subtype of LIST1D
SEGMENT1D = TypeVar("SEGMENT1D") # subtype of LIST1D
SEGMENTS1D = List[SEGMENT1D] # subtype of LIST2D
SEGMENTS2D = List[POLYGON2D]
HALFPLANE = TypeVar("HALFPLANE")
HALFPLANES = List[HALFPLANE]
