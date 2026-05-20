# Smart Food Delivery Route Optimizer

An intelligent route optimization system built using Python and Streamlit to simulate real-world food delivery planning using graph algorithms and traffic-aware routing.

## Overview

This project focuses on optimizing multi-stop food delivery routes by minimizing travel distance and improving delivery efficiency under different traffic conditions.

The system applies graph-based algorithms such as Dijkstra’s shortest path algorithm along with heuristic optimization strategies to simulate practical logistics and route-planning scenarios.

---

## Features

- Interactive Streamlit web interface
- Traffic-aware weighted graph simulation
- Multi-stop route optimization
- Exact permutation-based route planning
- Greedy nearest-neighbor optimization
- Advanced heuristic optimization (Greedy + 2-Opt)
- Dijkstra shortest-path computation
- Real-time route visualization using NetworkX and Matplotlib
- Input validation and error handling

---

## Tech Stack

- Python
- Streamlit
- NetworkX
- Matplotlib
- Graph Algorithms
- Dijkstra’s Algorithm

---

## Project Structure

```text
.
├── app.py
├── data.py
├── route_optimizer.py
├── visualization.py
├── requirements.txt
└── README.md
```

RUN LOCALLY
```bash
pip install -r requirements.txt
streamlit run app.py
```

