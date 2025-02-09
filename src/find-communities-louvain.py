import math
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import seaborn as sns
import community as community_louvain
from fa2_modified import ForceAtlas2


def load_data(nodes_file: str, edges_file: str):
    """
    Load nodes and edges data from CSV files.
    """
    nodes_df = pd.read_csv(nodes_file)
    edges_df = pd.read_csv(edges_file)
    return nodes_df, edges_df


def filter_edges_by_threshold(edges_df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Filter edges by weight threshold.
    """
    filtered_edges = edges_df[edges_df['Weight'] >= threshold]
    return filtered_edges


def build_graph(nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> nx.Graph:
    """
    Build a graph from nodes and edges data.
    Adds edges with weight attribute and assigns node attributes.
    """
    G = nx.Graph()
    
    # Add edges with weights
    for _, edge in edges_df.iterrows():
        G.add_edge(edge['Source'], edge['Target'], weight=edge['Weight'])
    print("Number of edges:", len(G.edges()))
    
    # Add node attributes
    for _, node in nodes_df.iterrows():
        node_id = node['Id']
        G.add_node(node_id)
        for col in nodes_df.columns:
            G.nodes[node_id][col] = node[col]
    print("Number of nodes:", len(G.nodes()))
    
    return G


def compute_node_sizes(G: nx.Graph, scale: float = 80) -> list:
    """
    Compute node sizes based on the 'Theta/Alpha' attribute.
    """
    sizes = [G.nodes[node]['Theta/Alpha'] * scale for node in G.nodes()]
    return sizes


def compute_communities(G: nx.Graph):
    """
    Compute communities using the Louvain method.
    Returns the partition dictionary, communities dictionary, and modularity.
    """
    partition = community_louvain.best_partition(G, resolution=1, randomize=False)
    num_communities = len(set(partition.values()))
    print("Number of communities:", num_communities)
    modularity = community_louvain.modularity(partition, G)
    print("Modularity:", modularity)
    
    communities = {}
    for node, community_id in partition.items():
        communities.setdefault(community_id, []).append(node)
    
    for community_id, nodes in communities.items():
        print(f"Community {community_id}: {len(nodes)} nodes")
    
    return partition, communities, modularity


def compute_global_layout(G: nx.Graph, communities: dict, iterations: int = 5000, R: float = 15.0) -> dict:
    """
    Compute the global layout of the graph.
    For each community, compute a local layout using ForceAtlas2, then adjust positions to a global layout.
    """
    # Create a ForceAtlas2 instance with specific parameters
    fa2 = ForceAtlas2(
        outboundAttractionDistribution=False,
        edgeWeightInfluence=0.5,
        jitterTolerance=0.7,
        scalingRatio=0.2,
        strongGravityMode=True,
        gravity=1.0
    )
    
    community_local_positions = {}
    community_centroids = {}
    
    # Compute local layout and centroid for each community
    for comm_id, nodes in communities.items():
        subG = G.subgraph(nodes)
        pos_local = fa2.forceatlas2_networkx_layout(subG, pos=None, iterations=iterations)
        community_local_positions[comm_id] = pos_local
        xs = [p[0] for p in pos_local.values()]
        ys = [p[1] for p in pos_local.values()]
        centroid = (sum(xs) / len(xs), sum(ys) / len(ys))
        community_centroids[comm_id] = centroid
    
    # Determine global offsets for communities arranged evenly on a circle
    n_comms = len(communities)
    global_offsets = {}
    for idx, comm_id in enumerate(sorted(communities.keys())):
        angle = 2 * math.pi * idx / n_comms
        global_offsets[comm_id] = (R * math.cos(angle), R * math.sin(angle))
    
    # Build final global layout by adjusting local positions using community centroids and offsets
    pos = {}
    for comm_id, pos_local in community_local_positions.items():
        centroid = community_centroids[comm_id]
        offset = global_offsets[comm_id]
        for node, p in pos_local.items():
            # Recentering the community layout so that its centroid is at (0,0)
            # then adding the global offset.
            pos[node] = (p[0] - centroid[0] + offset[0], p[1] - centroid[1] + offset[1])
    
    return pos


def draw_network_graph(G: nx.Graph, pos: dict, sizes: list, partition: dict, output_file: str):
    """
    Draw the network graph with two subplots:
    one with node labels as IDs and the other with node labels as the 'Group' attribute.
    Save the resulting figure.
    """
    # Create a color map based on community partition
    unique_communities = sorted(set(partition.values()))
    cmap = cm.get_cmap("tab10", len(unique_communities))
    color_map = [cmap(partition[node]) for node in G.nodes()]
    
    # First subplot: labels as IDs
    labels_id = {node: int(node) for node in G.nodes()}
    
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    nx.draw_networkx_nodes(G, pos=pos, node_size=sizes, node_color=color_map)
    nx.draw_networkx_edges(G, pos=pos, alpha=0.08, edge_color='blue', width=0.3)
    nx.draw_networkx_labels(G, pos=pos, labels=labels_id, font_size=8)
    plt.title("Communities (ID)")
    
    # Second subplot: labels as 'Group' attribute
    labels_group = {node: G.nodes[node]['Group'] for node in G.nodes()}
    plt.subplot(122)
    nx.draw_networkx_nodes(G, pos=pos, node_size=sizes, node_color=color_map)
    nx.draw_networkx_edges(G, pos=pos, alpha=0.08, edge_color='blue', width=0.3)
    nx.draw_networkx_labels(G, pos=pos, labels=labels_group, font_size=8)
    plt.title("Communities (Group)")
    
    plt.savefig(output_file)
    plt.close()
    print(f"Network graph saved to: {output_file}")


def compute_average_mmse(G: nx.Graph, communities: dict) -> list:
    """
    Compute the average MMSE value for each community.
    Returns a list of average MMSE values for communities in sorted order of community IDs.
    """
    average_mmse = []
    for comm_id in sorted(communities.keys()):
        mmse_values = [G.nodes[node]['MMSE'] for node in communities[comm_id]]
        avg_mmse = sum(mmse_values) / len(mmse_values)
        average_mmse.append(avg_mmse)
    return average_mmse


def plot_community_bar_chart(G: nx.Graph, communities: dict, average_mmse: list, output_file: str):
    """
    Plot a bar chart showing the ratio of Group A and Group C in each community.
    Annotate each bar with the average MMSE value.
    Save the figure.
    """
    community_sizes = [len(communities[comm_id]) for comm_id in sorted(communities.keys())]
    groupA_ratios = []
    groupC_ratios = []
    
    for comm_id in sorted(communities.keys()):
        nodes = communities[comm_id]
        groupA_count = sum(G.nodes[node]['Group'] == 'A' for node in nodes)
        groupC_count = sum(G.nodes[node]['Group'] == 'C' for node in nodes)
        groupA_ratios.append(groupA_count / len(nodes))
        groupC_ratios.append(groupC_count / len(nodes))
    
    plt.figure(figsize=(12, 6))
    # Bar chart for Group A ratios
    plt.subplot(121)
    plt.bar(range(len(community_sizes)), groupA_ratios)
    for i, avg in enumerate(average_mmse):
        plt.text(i, groupA_ratios[i], f"{avg:.2f}", ha='center', va='bottom')
    plt.title("Group A Ratios")
    plt.xlabel("Community ID")
    plt.ylabel("Ratio of Group A")
    plt.ylim(0, 1)
    
    # Bar chart for Group C ratios
    plt.subplot(122)
    plt.bar(range(len(community_sizes)), groupC_ratios)
    for i, avg in enumerate(average_mmse):
        plt.text(i, groupC_ratios[i], f"{avg:.2f}", ha='center', va='bottom')
    plt.title("Group C Ratios")
    plt.xlabel("Community ID")
    plt.ylabel("Ratio of Group C")
    plt.ylim(0, 1)
    
    plt.savefig(output_file)
    plt.close()
    print("Percentage of Group A and Group C in each community:")
    for i, (groupA, groupC) in enumerate(zip(groupA_ratios, groupC_ratios)):
        print(f"Community {i}: Group A = {groupA:.2f}, Group C = {groupC:.2f}")
    print(f"Bar chart saved to: {output_file}")


def plot_theta_alpha_scatter(nodes_df: pd.DataFrame, output_file: str):
    """
    Plot a scatter plot of Theta vs. Alpha power using seaborn.
    Nodes are colored by the 'Group' attribute.
    Save the figure.
    """
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette('viridis', n_colors=2)
    sns.scatterplot(x='Theta', y='Alpha', hue='Group', data=nodes_df, palette=colors, s=100)
    plt.xlabel('Theta RBP', fontsize=14)
    plt.ylabel('Alpha RBP', fontsize=14)
    # Create legend patches
    groupA_patch = mpatches.Patch(color=colors[0], label='Group A')
    groupC_patch = mpatches.Patch(color=colors[1], label='Group C')
    plt.legend(handles=[groupA_patch, groupC_patch], loc='upper right', fontsize='x-large')
    plt.savefig(output_file)
    plt.close()
    print(f"Scatter plot saved to: {output_file}")


def print_median_values(nodes_df: pd.DataFrame, G: nx.Graph, communities: dict, average_mmse: list):
    """
    Print median values of age in general and for each community.
    Also print the average MMSE for each community.
    """
    overall_median_age = nodes_df['Age'].median()
    print("Median value of age in general:", overall_median_age)
    
    average_age_per_community = []
    for comm_id in sorted(communities.keys()):
        ages = [G.nodes[node]['Age'] for node in communities[comm_id]]
        avg_age = sum(ages) / len(ages)
        average_age_per_community.append(avg_age)
    
    print("Average age per community:", average_age_per_community)
    print("Average MMSE per community:", average_mmse)


def main():
    # File paths
    nodes_file = 'datasets/output/nodes.csv'
    edges_file = 'datasets/output/edges.csv'
    network_graph_output = 'datasets/output/louvain/graph-EEG_euclidean.png'
    bar_chart_output = 'datasets/output/louvain/bar-chart-EEG_euclidean.png'
    scatter_plot_output = 'datasets/output/charts/theta-alpha-scatter-EEG_euclidean.png'
    
    # Threshold for filtering edges by weight
    threshold = 0.15
    
    # Load data
    nodes_df, edges_df = load_data(nodes_file, edges_file)
    
    # Filter edges by weight threshold
    filtered_edges = filter_edges_by_threshold(edges_df, threshold)
    
    # Build the graph
    G = build_graph(nodes_df, filtered_edges)
    
    # Compute node sizes based on 'Theta/Alpha'
    sizes = compute_node_sizes(G, scale=80)
    
    # Compute communities using the Louvain method
    partition, communities, modularity = compute_communities(G)
    
    # Compute the global layout using ForceAtlas2 for each community
    pos = compute_global_layout(G, communities, iterations=5000, R=15.0)
    
    # Draw the network graph with two subplots (ID and Group labels)
    draw_network_graph(G, pos, sizes, partition, network_graph_output)
    
    # Compute average MMSE for each community
    average_mmse = compute_average_mmse(G, communities)
    
    # Plot a bar chart for community group ratios with average MMSE annotation
    plot_community_bar_chart(G, communities, average_mmse, bar_chart_output)
    
    # Plot a scatter plot of Theta vs. Alpha power
    plot_theta_alpha_scatter(nodes_df, scatter_plot_output)
    
    # Print median (average) values for age and MMSE in each community
    print_median_values(nodes_df, G, communities, average_mmse)

    print("Modularity:", modularity)


if __name__ == '__main__':
    main()