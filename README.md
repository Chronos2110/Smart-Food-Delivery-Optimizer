# Smart Food Delivery Route Optimizer

A professional Streamlit web app for optimizing food delivery routes with graph algorithms.

## Features

- Streamlit-only Python UI
- Delivery location input for locations A-F
- Traffic-aware weighted graph
- Exact permutation-based routing
- Greedy nearest-stop routing
- Advanced greedy + 2-opt improvement
- Dijkstra shortest paths between route stops
- Matplotlib and NetworkX route visualization
- Input validation and clear error messages

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

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

This project is ready for GitHub and can be deployed on Streamlit Community Cloud.

