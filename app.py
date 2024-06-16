from flask import Flask, render_template, request, jsonify
import folium
import networkx as nx
import osmnx as ox
from geopy.distance import geodesic

app = Flask(__name__)

# Load and process OSM data
place_name = "Piedmont, California, USA"
graph = ox.graph_from_place(place_name, network_type='drive')
graph = ox.project_graph(graph)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    start = data['start']
    end = data['end']

    # Find the nearest nodes in the graph to the start and end points
    start_node = ox.distance.nearest_nodes(graph, start[1], start[0])
    end_node = ox.distance.nearest_nodes(graph, end[1], end[0])

    # Find the shortest path
    shortest_path = nx.shortest_path(graph, start_node, end_node, weight='length')
    shortest_path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

    return jsonify(shortest_path_coords)

if __name__ == '__main__':
    app.run(debug=True)
