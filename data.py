"""Graph data and traffic configuration for the route optimizer."""

from __future__ import annotations


LOCATIONS = ("A", "B", "C", "D", "E", "F")

LOCATION_NAMES = {
    "A": "Central Kitchen",
    "B": "North Market",
    "C": "City Mall",
    "D": "Tech Park",
    "E": "University Gate",
    "F": "Lake View",
}

BASE_GRAPH = {
    "A": {"B": 3.0, "C": 2.0, "D": 5.0},
    "B": {"A": 3.0, "C": 1.5, "E": 5.0},
    "C": {"A": 2.0, "B": 1.5, "D": 3.0, "E": 6.0, "F": 6.0},
    "D": {"A": 5.0, "C": 3.0, "F": 4.0},
    "E": {"B": 5.0, "C": 6.0, "F": 2.5},
    "F": {"C": 8.0, "D": 4.0, "E": 2.5},
}

TRAFFIC_PROFILES = {
    "Light traffic": 0.9,
    "Normal traffic": 1.0,
    "Moderate traffic": 1.25,
    "Heavy traffic": 1.6,
    "Severe traffic": 2.0,
}

STRATEGIES = {
    "Exact": "Try every delivery order and select the shortest route.",
    "Greedy": "Always visit the nearest unvisited delivery next.",
    "Advanced": "Build a greedy route, then improve it with 2-opt swaps.",
}
