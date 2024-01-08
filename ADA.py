import time

start_time = time.time()
import networkx as nx
import folium
from geopy.distance import geodesic



# example road network (synthetic data for illustration)
road_network = nx.Graph()

# adding nodes (intersections) and edges (roads) with weights (distances)
road_network.add_edge("B", "A", weight=5)
road_network.add_edge("A", "D", weight=7)
road_network.add_edge("C", "G", weight=3)
road_network.add_edge("H", "C", weight=0)
road_network.add_edge("B", "H", weight=0)
road_network.add_edge("D", "E", weight=0)
road_network.add_edge("F", "G", weight =9)
road_network.add_edge("F", "I", weight =7)
road_network.add_edge("I", "J", weight =4)
road_network.add_edge("J", "K", weight =5)
road_network.add_edge("K", "E", weight =0)

# coordinates of some hypothetical points in Jakarta (synthetic data for illustration)
node_coordinates = {
    "A": (-6.225222, 106.804288),  # Jakarta coordinates
    "B": (-6.229062, 106.799127),
    "C": (-6.221361, 106.798301),
    "D": (-6.224934, 106.804770),
    "E": (-6.222684, 106.803107),
    "F": (-6.222342, 106.799599),
    "G": (-6.221521, 106.800329),
    "H": (-6.228742, 106.798301),
    "I": (-6.223356, 106.802464),
    "J": (-6.223974, 106.802947),
    "K": (-6.223483, 106.803655)
}

# function to interpolate points along the geodesic line between two coordinates
def interpolate_points(start_coords, end_coords, num_points=100):
    line = []
    for i in range(num_points + 1):
        fraction = i / num_points
        intermediate_point = (
            start_coords[0] + fraction * (end_coords[0] - start_coords[0]),
            start_coords[1] + fraction * (end_coords[1] - start_coords[1])
        )
        line.append(intermediate_point)
    return line

# function to find the shortest path
def find_shortest_path(graph, start, end):
    shortest_path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    return shortest_path

# example of finding the shortest path between two points
start_point = "A"
end_point = "E"
shortest_path = find_shortest_path(road_network, start_point, end_point)
print(f"Shortest path from {start_point} to {end_point}: {shortest_path}")

# create a Folium map centered around Jakarta
jakarta_map = folium.Map(location=[-6.2088, 106.8456], zoom_start=14)

# plot road network on the map
for edge in road_network.edges():
    start, end = edge
    start_coords = node_coordinates[start]
    end_coords = node_coordinates[end]
    
    # interpolate points along the road segment
    line_points = interpolate_points(start_coords, end_coords)
    
    # plot the road segment
    folium.PolyLine(locations=line_points, color='blue', weight=2.5).add_to(jakarta_map)

# mark nodes on the map
for node, coords in node_coordinates.items():
    folium.Marker(location=coords, popup=node).add_to(jakarta_map)

# highlight shortest path on the map
path_coords = [node_coordinates[node] for node in shortest_path]
folium.PolyLine(locations=path_coords, color='red', weight=5).add_to(jakarta_map)

# display the map
jakarta_map.save("jakarta_road_network.html")  # save the map to an HTML file
jakarta_map
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)