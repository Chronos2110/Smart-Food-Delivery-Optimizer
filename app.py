"""Streamlit app for a Smart Food Delivery Route Optimizer."""

from __future__ import annotations

import math

import streamlit as st

from data import LOCATION_NAMES, LOCATIONS, STRATEGIES, TRAFFIC_PROFILES
from route_optimizer import build_weighted_graph, optimize_route, parse_locations
from visualization import create_route_figure


def format_route(route: list[str]) -> str:
    """Return a readable route string."""

    return " -> ".join(route)


def location_reference() -> list[dict[str, str]]:
    """Return location rows for the dashboard reference table."""

    return [
        {"Code": code, "Location": LOCATION_NAMES[code]}
        for code in LOCATIONS
    ]


def main() -> None:
    """Render the Streamlit application."""

    st.set_page_config(
        page_title="Smart Food Delivery Route Optimizer",
        page_icon=":truck:",
        layout="wide",
    )

    st.title("Smart Food Delivery Route Optimizer")
    st.caption("Graph-based route planning with Dijkstra, greedy, exact, and 2-opt routing.")

    with st.sidebar:
        st.header("Route Inputs")

        depot = st.selectbox(
            "Starting depot",
            LOCATIONS,
            index=0,
            format_func=lambda code: f"{code} - {LOCATION_NAMES[code]}",
        )
        raw_locations = st.text_input(
            "Delivery locations (A-F)",
            value="B, C, D, E, F",
            help="Enter location codes separated by commas, spaces, arrows, or hyphens.",
        )
        traffic_label = st.selectbox(
            "Traffic condition",
            list(TRAFFIC_PROFILES.keys()),
            index=1,
        )
        strategy = st.selectbox(
            "Optimization strategy",
            list(STRATEGIES.keys()),
            index=0,
        )
        return_to_depot = st.checkbox("Return to starting depot", value=True)

        st.divider()
        st.subheader("Location Codes")
        st.dataframe(
            location_reference(),
            hide_index=True,
            use_container_width=True,
        )

    stops, warnings = parse_locations(raw_locations, depot)
    graph = build_weighted_graph(TRAFFIC_PROFILES[traffic_label])

    top_left, top_mid, top_right = st.columns(3)
    with top_left:
        st.metric("Deliveries", len(stops))
    with top_mid:
        st.metric("Traffic multiplier", f"{TRAFFIC_PROFILES[traffic_label]:.2f}x")
    with top_right:
        st.metric("Strategy", strategy)

    for warning in warnings:
        st.warning(warning)

    if not raw_locations.strip():
        st.error("Please enter at least one delivery location from A-F.")
        st.stop()

    if not stops:
        st.error("No valid delivery stops found. Enter one or more locations from A-F.")
        st.stop()

    try:
        result = optimize_route(
            graph=graph,
            depot=depot,
            stops=stops,
            strategy=strategy,
            return_to_depot=return_to_depot,
            traffic_multiplier=TRAFFIC_PROFILES[traffic_label],
        )
    except ValueError as error:
        st.error(str(error))
        st.stop()

    if math.isinf(result.total_distance):
        st.error("No connected route could be found for the selected locations.")
        st.stop()

    route_section, detail_section = st.columns([1.45, 1])

    with route_section:
        with st.container(border=True):
            st.subheader("Optimized Route")
            st.markdown(f"### {format_route(result.route)}")
            st.caption("Shortest paths between route stops may pass through intermediate locations.")

            step_rows = [
                {
                    "Step": index,
                    "From": start,
                    "To": end,
                }
                for index, (start, end) in enumerate(
                    zip(result.route, result.route[1:]),
                    start=1,
                )
            ]
            st.dataframe(step_rows, hide_index=True, use_container_width=True)

    with detail_section:
        with st.container(border=True):
            st.subheader("Route Summary")
            st.metric("Total distance", f"{result.total_distance:.2f} km")
            st.write(f"Traffic: **{traffic_label}**")
            st.write(f"Method: **{result.strategy}**")
            st.write(f"Expanded graph path: **{format_route(result.expanded_path)}**")

        with st.container(border=True):
            st.subheader("Strategy Notes")
            st.write(STRATEGIES[strategy])

    with st.container(border=True):
        st.subheader("Route Visualization")
        figure = create_route_figure(graph, result.expanded_path)
        st.pyplot(figure, clear_figure=True, use_container_width=True)


if __name__ == "__main__":
    main()
