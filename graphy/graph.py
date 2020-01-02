import json
import os
import random


class GraphNode:
    def __init__(self, node_id, location, size=1, label=None):
        self.node_id = node_id
        self.x = location[0]
        self.y = location[1]
        self.size = size
        self.label = label

    def as_dict(self):
        return dict(id=self.node_id,
                    label=self.label,
                    x=self.x,
                    y=self.y,
                    size=self.size)


class GraphEdge:
    def __init__(self, edge_id, source, target):
        self.edge_id = edge_id
        self.source = source
        self.target = target

    def as_dict(self):
        return dict(id=self.edge_id,
                    source=self.source,
                    target=self.target)


class Graph:
    def __init__(self):
        self.graph = {"nodes": [], "edges": []}
        self.node_ids = set()
        self.edge_ids = set()
        self.edge_counter = 0

    def add_node(self, node):
        if node.node_id in self.node_ids:
            # need a hashmap to all nodes if graph gets large
            for graph_node in self.graph["nodes"]:
                if node.node_id in graph_node.keys():
                    graph_node.label = node.label
                    graph_node.x = node.x
                    graph_node.y = node.y
                    graph_node.size = node.size
        else:
            self.graph["nodes"].append(node.as_dict())
            self.node_ids.add(node.node_id)

    def add_edge(self, edge):
        if edge.edge_id in self.edge_ids:
            # need a hashmap to all nodes if graph gets large
            for edge_node in self.graph["edges"]:
                if edge.edge_id in edge_node.keys():
                    edge_node.source = edge.source
                    edge_node.target = edge.target
        else:
            self.graph["edges"].append(edge.as_dict())
            self.edge_ids.add(edge.edge_id)
            self.edge_counter += 1

    def get_neighbors(self, node_id):
        if node_id not in self.node_ids:
            return None
        neighbors = set()
        edges = self.graph["edges"]
        for edge in edges:
            if edge["source"] == node_id:
                neighbors.add(edge["target"])
        return neighbors

    def write_json(self, path=os.path.join(os.getcwd(), 'static', 'data')):
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, 'graph.json'), 'w') as f:
            print(self.graph)
            json.dump(self.graph, f, indent=2)


def build_graph(node_count=10, edge_count=20):
    graph = Graph()

    for i in range(node_count):
        node = GraphNode('n{}'.format(i), location=(i, random.randint(0, node_count)), label='Node {}'.format(i))
        graph.add_node(node)

    for i in range(node_count):
        # add 2 new edges at random from each node

        source_node_id = 'n{}'.format(i)
        neighbors = graph.get_neighbors(source_node_id)
        neighbors.add(source_node_id)
        disconnected_nodes = graph.node_ids.difference(neighbors)

        if len(disconnected_nodes) < 2:
            continue

        new_neighbors = random.sample(disconnected_nodes, 2)
        for node in new_neighbors:
            edge = GraphEdge('e{}'.format(graph.edge_counter), source='n{}'.format(i), target=node)
            graph.add_edge(edge)

    return graph


if __name__ == "__main__":
    test_graph = build_graph()
    # print(test_graph.graph)
    # print(test_graph.get_neighbors('n0'))
    test_graph_dir = os.path.join(os.getcwd(), 'static', 'data')
    test_graph.write_json(test_graph_dir)
    with open(os.path.join(test_graph_dir, 'graph.json'), 'r') as test_json:
        test_graph_json = json.load(test_json)
    print(test_graph_json)
