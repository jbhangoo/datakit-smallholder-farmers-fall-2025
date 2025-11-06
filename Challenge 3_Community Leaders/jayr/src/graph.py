from typing import Any, Dict, List, Tuple
from collections import defaultdict

class MultiDiGraph:
    """
    A directed graph data structure that supports multiple edges between nodes.
    Each edge can have associated attributes (e.g., weight, label, timestamp).
    """

    def __init__(self):
        # Structure: {from_node: {to_node: [edge1_attrs, edge2_attrs, ...]}}
        self.adj_list: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.nodes = set()
        self.edge_count = 0

    def add_edge(self, from_node: str, to_node: str, qid:str):
        """

        :param from_node:
        :param to_node:
        :param qid:
        :return:
        """
        """Add a directed edge with optional attributes."""
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        self.adj_list[from_node][to_node].append(qid)
        self.edge_count += 1

    def get_edges(self, from_node: str, to_node: str) -> List[str]:
        """Get all edges between two nodes."""
        return self.adj_list.get(from_node, {}).get(to_node, [])

    def get_all_edges(self) -> List[Tuple[str, str, str]]:
        """Get all edges as a list of (from_node, to_node, attributes) tuples."""
        edges = []
        for from_node, neighbors in self.adj_list.items():
            for to_node, edge_list in neighbors.items():
                for qids in edge_list:
                    edges.append((from_node, to_node, qids))
        return edges

    def get_neighbors(self, node: str) -> List[str]:
        """Get all nodes that this node has edges to."""
        return list(self.adj_list.get(node, {}).keys())

    def out_degree(self, node: str) -> int:
        """Get the out-degree of a node (number of outgoing edges)."""
        return sum(len(edges) for edges in self.adj_list.get(node, {}).values())

    def in_degree(self, node: str) -> int:
        """Get the in-degree of a node (number of incoming edges)."""
        count = 0
        for from_node, neighbors in self.adj_list.items():
            if node in neighbors:
                count += len(neighbors[node])
        return count

    def __str__(self):
        return f"MultiDiGraph(nodes={len(self.nodes)}, edges={self.edge_count})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> Dict:
        """Convert to a dictionary representation."""
        return {
            'nodes': list(self.nodes),
            'edges': self.get_all_edges(),
            'adjacency_list': {
                str(k): {str(k2): v2 for k2, v2 in v.items()}
                for k, v in self.adj_list.items()
            }
        }