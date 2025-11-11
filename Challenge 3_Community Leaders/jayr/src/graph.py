from typing import Set, Dict, List, Tuple
from collections import defaultdict
from .edge import DiGraphEdge

class MultiDiGraph(object):
    """
    A directed graph data structure that also supports multiple edges between nodes.
    Each edge can have associated attributes (e.g. qid, timestamp, weight).
    """

    def __init__(self):
        # Structure: {from_node: {to_node: [edge1_attrs, edge2_attrs, ...]}}
        self.next_nodes: Dict[str, Dict[str, List[DiGraphEdge]]] = defaultdict(lambda: defaultdict(list))
        self.prev_nodes: Dict[str, Dict[str, List[DiGraphEdge]]] = defaultdict(lambda: defaultdict(list))
        self.nodes: Set[str] = set()
        self.edge_count = 0

    def add_edge(self, from_node: str, to_node: str, edge: DiGraphEdge):
        """
        Add existing edge to the graph
        :param from_node:
        :param to_node:
        :param qid:
        :return:
        """
        self.nodes.add(from_node)
        self.nodes.add(to_node)

        self.next_nodes[from_node][to_node].append(edge)
        self.prev_nodes[to_node][from_node].append(edge)
        self.edge_count += 1

    def add_new_edge(self, from_node: str, to_node: str, qid:str, **kwargs):
        """
        Create edge attributes then add it to the graph
        :param from_node:
        :param to_node:
        :param qid:
        :return:
        """
        """Create a directed edge with attributes."""
        edge = DiGraphEdge(qid, **kwargs)
        self.add_edge(from_node, to_node, edge)

    def remove_node(self, node:str) -> bool:
        """Remove a node from the graph."""
        if node in self.nodes:
            # Remove all edges into the node
            edge_set = self.next_nodes.items()
            for from_node, neighbors in edge_set:
                if node in neighbors:
                    del self.next_nodes[from_node][node]

            # Remove all edges from the node
            if node in self.next_nodes:
                del self.next_nodes[node]

            # Remove the node
            if node in self.nodes:
                self.nodes.remove(node)
            return True
        return False

    def get_edges(self, from_node: str, to_node: str) -> List[DiGraphEdge]:
        """Get all edges between two nodes."""
        return self.next_nodes.get(from_node, {}).get(to_node, [])

    def get_all_edges(self) -> List[Tuple[str, str, DiGraphEdge]]:
        """Get all edge ids as a list of (from_node, to_node, attributes) tuples."""
        edges = []
        for from_node, neighbors in self.next_nodes.items():
            for to_node, edge_list in neighbors.items():
                for edge in edge_list:
                    edges.append((from_node, to_node, edge))
        return edges

    def get_neighbors(self, node: str) -> List[str]:
        """Get all nodes that this node has edges to."""
        return list(self.next_nodes.get(node, {}).keys())

    def out_degree(self, node: str) -> int:
        """Get the out-degree of a node (number of outgoing edges)."""
        return len(self.next_nodes.get(node, {}))

    def in_degree(self, node: str) -> int:
        """Get the in-degree of a node (number of incoming edges)."""
        count = 0
        for from_node, neighbors in self.next_nodes.items():
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
                for k, v in self.next_nodes.items()
            }
        }
        
    def subgraph(self, node_set: Set[str]) -> 'MultiDiGraph':
        """
        Create a subgraph containing only the specified nodes and edges between them.
        :param nodes: valid node IDs in current graph
        :return: new graph with only the given nodes and edges between them
        """
        # Convert to set for faster lookups
        #node_set = set(nodes)
        
        # Create a new graph
        subgraph = MultiDiGraph()
        
        # Add nodes to the subgraph
        for node in node_set:
            if node in self.nodes:
                subgraph.nodes.add(node)
        
        # Add edges between nodes in the subgraph
        for from_node in node_set:
            if from_node in self.next_nodes:
                for to_node, edges in self.next_nodes[from_node].items():
                    if to_node in node_set:
                        for edge in edges:
                            # Create a new edge with the same attributes
                            subgraph.add_edge(from_node, to_node, edge)
        
        return subgraph