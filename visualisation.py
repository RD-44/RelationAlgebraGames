import networkx as nx
import matplotlib.pyplot as plt

# Create a complete graph with 6 nodes
G = nx.complete_graph(6)

# Define edge labels
edge_labels = {(u, v): f'{u}-{v}' for u, v in G.edges()}

print(G.edges())

# Define node colors
node_colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']

# Draw the graph with node labels and edge labels
pos = nx.spring_layout(G)  # Position nodes using spring layout
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

# Show the plot
plt.show(block=False)

x = input("hi")

plt.clf()
# Draw the graph with node labels and edge labels
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')
# Show the plot
plt.show(block=False)


y = input("hi")


