import os
import pandas as pd
from scipy.spatial.distance import euclidean

def create_output_directory(output_dir: str):
    """
    Create the output directory if it does not exist.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory ensured: {output_dir}")

def load_data(input_file: str) -> pd.DataFrame:
    """
    Load data from the CSV file.
    """
    data = pd.read_csv(input_file)
    print(f"Data loaded from: {input_file}")
    return data

def calculate_euclidean_distance(row1: pd.Series, row2: pd.Series) -> float:
    """
    Calculate the Euclidean distance between two points using the 'Theta' and 'Alpha' columns.
    """
    return euclidean([row1['Theta'], row1['Alpha']], [row2['Theta'], row2['Alpha']])

def calculate_edges(data: pd.DataFrame, scaling_factor: float = 100.0) -> list:
    """
    Calculate edges between nodes, generating a dictionary for each edge with the following keys:
    'Source', 'Target', 'Distance', and 'Weight' (similarity).

    The scaling_factor multiplies the distance for better visualization.
    """
    edges = []
    for i, row1 in data.iterrows():
        for j, row2 in data.iterrows():
            if i < j:  # Avoid duplicate edges and self-loops
                distance = calculate_euclidean_distance(row1, row2) * scaling_factor
                weight = 1 / (1 + distance)  # Convert distance to similarity
                edge = {
                    'Source': row1['Id'],
                    'Target': row2['Id'],
                    'Distance': distance,
                    'Weight': weight
                }
                edges.append(edge)
    print(f"Calculated edges: {len(edges)}")
    return edges

def save_edges(edges: list, output_file: str):
    """
    Save the calculated edges to a CSV file.
    """
    edges_df = pd.DataFrame(edges)
    edges_df.to_csv(output_file, index=False)
    print(f"Edges saved to: {output_file}")

def main():
    # Parameters and file paths
    input_file = 'datasets/output/nodes.csv'  # File with EEG signals (Theta and Alpha)
    output_dir = 'datasets/output/'
    output_file = os.path.join(output_dir, 'edges.csv')

    # Create the output directory
    create_output_directory(output_dir)

    # Load the data
    data = load_data(input_file)

    # Calculate edges
    edges = calculate_edges(data)

    # Save the edges to a CSV file
    save_edges(edges, output_file)

if __name__ == '__main__':
    main()