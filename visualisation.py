import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Define the adjacency matrix for a directed graph (2D numpy array)
adjacency_matrix = np.array([
    [0, 1, 2, 0, 0, 0],
    [1, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 6],
    [7, 0, 0, 0, 0, 0]
])

# Convert the adjacency matrix to a NetworkX directed graph
G = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)

# Define edge labels including weights for both directions
edge_labels = {}
for u, v in G.edges():
    edge_labels[(u, v)] = f'{u}->{v}'
    edge_labels[(v, u)] = f'{v}->{u}'  # Reverse direction label

# Define node colors (optional)
node_colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']

# Draw the graph with node labels and edge labels
pos = nx.spring_layout(G)  # Position nodes using spring layout
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

# Show the plot
plt.show()

# Wait for user input
x = input("hi")

plt.clf()

# Redraw the graph with updated edge labels and colors
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

# Show the plot again
plt.show()

# Wait for another user input
y = input("hi")
