"""Core graph algorithms for food delivery route optimization."""

from __future__ import annotations

import heapq
import itertools
import math
import re
from dataclasses import dataclass
from typing import Iterable

from data import BASE_GRAPH, LOCATIONS


Graph = dict[str, dict[str, float]]


@dataclass(frozen=True)
class RouteResult:
    """Final optimized route and supporting details."""

    route: list[str]
    expanded_path: list[str]
    total_distance: float
    strategy: str
    traffic_multiplier: float


def build_weighted_graph(multiplier: float) -> Graph:
    """Return a graph with edge weights adjusted by the traffic multiplier."""

    return {
        node: {
            neighbor: round(distance * multiplier, 2)
            for neighbor, distance in neighbors.items()
        }
        for node, neighbors in BASE_GRAPH.items()
    }


def parse_locations(raw_value: str, depot: str) -> tuple[list[str], list[str]]:
    """Parse user-entered locations and return valid stops plus warnings."""

    tokens = [
        token.upper()
        for token in re.split(r"[\s,;>\-]+", raw_value.strip())
        if token.strip()
    ]

    stops: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    valid_locations = set(LOCATIONS)

    for token in tokens:
        if token not in valid_locations:
            warnings.append(f"Ignored invalid location '{token}'. Use only A-F.")
            continue
        if token == depot:
            warnings.append(f"Ignored depot '{depot}' in delivery stops.")
            continue
        if token in seen:
            warnings.append(f"Ignored duplicate location '{token}'.")
            continue

        seen.add(token)
        stops.append(token)

    return stops, warnings


def dijkstra(graph: Graph, start: str, end: str) -> tuple[float, list[str]]:
    """Find the shortest path between two locations using Dijkstra's algorithm."""

    queue: list[tuple[float, str, list[str]]] = [(0.0, start, [start])]
    visited: set[str] = set()

    while queue:
        distance, node, path = heapq.heappop(queue)
        if node == end:
            return distance, path
        if node in visited:
            continue

        visited.add(node)

        for neighbor, edge_weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(
                    queue,
                    (distance + edge_weight, neighbor, [*path, neighbor]),
                )

    return math.inf, []


def route_distance(graph: Graph, route: Iterable[str]) -> tuple[float, list[str]]:
    """Calculate total shortest-path distance for a route sequence."""

    route_list = list(route)
    total = 0.0
    expanded_path: list[str] = []

    for start, end in zip(route_list, route_list[1:]):
        distance, path = dijkstra(graph, start, end)
        if math.isinf(distance):
            return math.inf, []

        total += distance
        if not expanded_path:
            expanded_path.extend(path)
        else:
            expanded_path.extend(path[1:])

    return round(total, 2), expanded_path


def exact_route(
    graph: Graph,
    depot: str,
    stops: list[str],
    return_to_depot: bool,
) -> tuple[list[str], float, list[str]]:
    """Find the shortest route by checking all possible stop permutations."""

    best_route: list[str] = []
    best_path: list[str] = []
    best_distance = math.inf

    for order in itertools.permutations(stops):
        route = [depot, *order]
        if return_to_depot:
            route.append(depot)

        distance, expanded_path = route_distance(graph, route)
        if distance < best_distance:
            best_distance = distance
            best_route = route
            best_path = expanded_path

    return best_route, best_distance, best_path


def greedy_route(
    graph: Graph,
    depot: str,
    stops: list[str],
    return_to_depot: bool,
) -> tuple[list[str], float, list[str]]:
    """Build a route by repeatedly choosing the nearest unvisited stop."""

    unvisited = set(stops)
    route = [depot]
    current = depot

    while unvisited:
        next_stop = min(
            unvisited,
            key=lambda stop: dijkstra(graph, current, stop)[0],
        )
        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    if return_to_depot:
        route.append(depot)

    distance, expanded_path = route_distance(graph, route)
    return route, distance, expanded_path


def advanced_route(
    graph: Graph,
    depot: str,
    stops: list[str],
    return_to_depot: bool,
) -> tuple[list[str], float, list[str]]:
    """Improve a greedy route using local 2-opt swaps."""

    route, best_distance, best_path = greedy_route(
        graph,
        depot,
        stops,
        return_to_depot,
    )

    improved = True
    while improved and len(route) > 4:
        improved = False
        stop_slice_end = len(route) - 1 if return_to_depot else len(route)

        for left in range(1, stop_slice_end - 1):
            for right in range(left + 1, stop_slice_end):
                candidate = [
                    *route[:left],
                    *reversed(route[left : right + 1]),
                    *route[right + 1 :],
                ]
                distance, expanded_path = route_distance(graph, candidate)

                if distance < best_distance:
                    route = candidate
                    best_distance = distance
                    best_path = expanded_path
                    improved = True
                    break
            if improved:
                break

    return route, best_distance, best_path


def optimize_route(
    graph: Graph,
    depot: str,
    stops: list[str],
    strategy: str,
    return_to_depot: bool,
    traffic_multiplier: float,
) -> RouteResult:
    """Optimize delivery order with the selected strategy."""

    if strategy == "Exact":
        route, total_distance, expanded_path = exact_route(
            graph,
            depot,
            stops,
            return_to_depot,
        )
    elif strategy == "Greedy":
        route, total_distance, expanded_path = greedy_route(
            graph,
            depot,
            stops,
            return_to_depot,
        )
    elif strategy == "Advanced":
        route, total_distance, expanded_path = advanced_route(
            graph,
            depot,
            stops,
            return_to_depot,
        )
    else:
        raise ValueError(f"Unsupported strategy: {strategy}")

    return RouteResult(
        route=route,
        expanded_path=expanded_path,
        total_distance=total_distance,
        strategy=strategy,
        traffic_multiplier=traffic_multiplier,
    )

