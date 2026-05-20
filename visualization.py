"""Matplotlib and NetworkX graph rendering for Streamlit."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from route_optimizer import Graph


NODE_POSITIONS = {
    "A": (0.0, 1.0),
    "B": (1.4, 2.0),
    "C": (1.7, 0.8),
    "D": (3.2, 1.0),
    "E": (2.8, 2.2),
    "F": (4.2, 1.7),
}


def create_route_figure(graph: Graph, route_path: list[str]):
    """Create a route visualization figure for display inside Streamlit."""

    network = nx.Graph()

    for node, neighbors in graph.items():
        network.add_node(node)
        for neighbor, distance in neighbors.items():
            network.add_edge(node, neighbor, weight=distance)

    route_edges = {
        tuple(sorted((start, end)))
        for start, end in zip(route_path, route_path[1:])
    }
    edge_colors = [
        "#f97316" if tuple(sorted(edge)) in route_edges else "#cbd5e1"
        for edge in network.edges()
    ]
    edge_widths = [
        4.0 if tuple(sorted(edge)) in route_edges else 1.7
        for edge in network.edges()
    ]
    node_colors = [
        "#16a34a" if node in route_path else "#2563eb"
        for node in network.nodes()
    ]

    figure, axis = plt.subplots(figsize=(9, 5.6))
    figure.patch.set_facecolor("#ffffff")
    axis.set_facecolor("#ffffff")

    nx.draw_networkx_edges(
        network,
        NODE_POSITIONS,
        ax=axis,
        edge_color=edge_colors,
        width=edge_widths,
    )
    nx.draw_networkx_nodes(
        network,
        NODE_POSITIONS,
        ax=axis,
        node_color=node_colors,
        node_size=1400,
        linewidths=2,
        edgecolors="#0f172a",
    )
    nx.draw_networkx_labels(
        network,
        NODE_POSITIONS,
        ax=axis,
        labels={node: node for node in network.nodes()},
        font_size=12,
        font_weight="bold",
        font_color="#ffffff",
    )
    nx.draw_networkx_edge_labels(
        network,
        NODE_POSITIONS,
        ax=axis,
        edge_labels=nx.get_edge_attributes(network, "weight"),
        font_size=8,
        font_color="#334155",
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "#ffffff", "edgecolor": "none"},
    )

    axis.set_title("Optimized Delivery Network", fontsize=15, fontweight="bold", pad=16)
    axis.margins(0.16)
    axis.axis("off")
    figure.tight_layout()
    return figure
