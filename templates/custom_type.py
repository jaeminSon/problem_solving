from typing import TypeVar, List

###############
# ALL NAMES ARE UPPERCASE.
#
# NAMING RULE: <catetory>_<subcategory>_<subsubcategory>_...
###############

NAT = TypeVar("NAT")
INT = TypeVar("INT")
REAL = TypeVar("REAL")

LIST1D = TypeVar("LIST1D")
LIST2D = TypeVar("LIST2D")

STRING = TypeVar("STRING")

NODE = TypeVar("NODE")
TREE = TypeVar("TREE")
TREE_HLD = TypeVar("TREE_HLD")
BIPARTITE = TypeVar("BIPARTITE")
GRAPH = TypeVar("GRAPH")
GRAPH_NONNEGEDGE = TypeVar("GRAPH_NONNEGEDGE")

POINT2D = TypeVar("POINT2D")
POLYGON2D = List[POINT2D]
SEGMENT1D = TypeVar("SEGMENT1D")
SEGMENTS1D = List[SEGMENT1D]
SEGMENTS2D = List[POLYGON2D]
HALFPLANE = TypeVar("HALFPLANE")
HALFPLANES = List[HALFPLANE]

