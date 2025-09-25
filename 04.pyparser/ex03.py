import json
import networkx as nx
import matplotlib.pyplot as plt

def load_json_graph(file_path: str):
    """Load graph from JSON file"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.DiGraph()

    # 노드 추가
    for node in data["nodes"]:
        G.add_node(node["id"])

    # 엣지 추가 (라벨 포함)
    for edge in data["edges"]:
        G.add_edge(edge["from"], edge["to"], label=edge.get("type", ""))

    return G

def draw_graph(G):
    """Draw graph with edge labels"""
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))

    nx.draw(
        G, pos,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        font_size=9,
        font_weight="bold",
        arrows=True
    )

    # edge labels
    edge_labels = nx.get_edge_attributes(G, "type")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("JSON Graph Viewer")
    plt.show()

if __name__ == "__main__":
    graph_file = "graph.json"
    G = load_json_graph(graph_file)
    draw_graph(G)
