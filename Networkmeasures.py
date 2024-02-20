import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
user_data = pd.read_csv("user_data.csv")
G = nx.from_pandas_edgelist(user_data, "Source", "Target", create_using=nx.DiGraph())
largest_component = max(nx.weakly_connected_components(G), key=len)
largest_component_subgraph = G.subgraph(largest_component)
degree_sequence = [d for n, d in largest_component_subgraph.degree()]
sorted_degrees = sorted(degree_sequence, reverse=True)
clustering_coefficient = nx.clustering(largest_component_subgraph)
closeness_centrality = nx.closeness_centrality(largest_component_subgraph)
betweenness_centrality = nx.betweenness_centrality(largest_component_subgraph)
# Plot all measures in a single figure
plt.figure(figsize=(12, 10))
# Degree Distribution Histogram
plt.subplot(3, 2, 1)
plt.hist(sorted_degrees, bins=20, color='skyblue', edgecolor='black')
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
# Degree Rank Plot
plt.subplot(3, 2, 2)
plt.plot(sorted_degrees, marker='o', linestyle='-')
plt.title("Degree Rank Plot")
plt.xlabel("Node Rank")
plt.ylabel("Degree")
# Clustering Coefficient Distribution
plt.subplot(3, 2, 3)
plt.hist(list(clustering_coefficient.values()), bins=20, color='skyblue', edgecolor='black')
plt.title("Clustering Coefficient Distribution")
plt.xlabel("Clustering Coefficient")
plt.ylabel("Frequency")
# Closeness Centrality Distribution
plt.subplot(3, 2, 4)
plt.hist(list(closeness_centrality.values()), bins=20, color='skyblue', edgecolor='black')
plt.title("Closeness Centrality Distribution")
plt.xlabel("Closeness Centrality")
plt.ylabel("Frequency")
# Betweenness Centrality Distribution
plt.subplot(3, 2, 5)
plt.hist(list(betweenness_centrality.values()), bins=20, color='skyblue', edgecolor='black')
plt.title("Betweenness Centrality Distribution")
plt.xlabel("Betweenness Centrality")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
