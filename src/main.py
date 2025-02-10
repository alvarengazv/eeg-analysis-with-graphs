import os
import mne
import pandas as pd
import numpy as np
from scipy.signal import welch

def extract_participant_id(file_name):
    """
    Extract the participant ID from the EEG file name.
    """
    participant_id = file_name.split('_')[0]
    # get only id number from participant_id
    participant_id = participant_id.split('-')[1]
    # string to int
    return int(participant_id)

def compute_epoch_rbp(epoch, sfreq, freq_bands):
    """
    Compute the relative band power (RBP) for a single epoch.
    """
    psd_all_channels = []
    # type of epoch: iterate over channels in the epoch
    for channel_data in epoch:
        # Compute PSD using Welch's method
        freqs, psd = welch(channel_data, sfreq, nperseg=int(sfreq * 2))
        
        # Calculate total power in the range of interest (0.5–45 Hz)
        total_power = np.sum(psd[(freqs >= 0.5) & (freqs <= 45)])
        
        # Calculate relative power for each frequency band
        band_powers = []
        for band, (fmin, fmax) in freq_bands.items():
            band_power = np.sum(psd[(freqs >= fmin) & (freqs <= fmax)])
            relative_power = band_power / total_power
            band_powers.append(relative_power)
        
        psd_all_channels.append(band_powers)
    
    # Average across channels
    mean_band_powers = np.mean(psd_all_channels, axis=0)
    return mean_band_powers

def compute_features_from_raw(raw, epoch_length, overlap, freq_bands):
    """
    Compute RBP features from the raw EEG data by creating epochs and processing each epoch.
    """
    sfreq = raw.info['sfreq']
    print(f"Sampling frequency: {sfreq}")
    
    # Create epochs
    events = mne.make_fixed_length_events(raw, duration=epoch_length, overlap=overlap)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=epoch_length, baseline=None, preload=True)
    
    # Prepare feature matrix
    feature_matrix = []
    
    for epoch in epochs.get_data():
        mean_band_powers = compute_epoch_rbp(epoch, sfreq, freq_bands)
        feature_matrix.append(mean_band_powers)
    
    # Convert to DataFrame
    columns = list(freq_bands.keys())
    df = pd.DataFrame(feature_matrix, columns=columns)
    return df

def process_file(file_path, epoch_length, overlap, freq_bands):
    """
    Process a single EEG file: load the data, compute the features, and return the RBP metrics.
    """
    # Load the .set file
    raw = mne.io.read_raw_eeglab(file_path, preload=True)
    
    # Compute features from raw data
    df = compute_features_from_raw(raw, epoch_length, overlap, freq_bands)
    
    # make column with ratio of theta / alpha
    alpha = df["Alpha"].mean()
    theta = df["Theta"].mean()
    
    # Compute RBP mean for the participant
    features = {
        "Theta/Alpha": theta / alpha,
        "Delta": df["Delta"].mean(),
        "Theta": theta,
        "Alpha": alpha,
        "Beta": df["Beta"].mean(),
        "Gamma": df["Gamma"].mean()
    }

    return features

def load_participant_info(participant_info_path):
    """
    Load and filter participant information.
    """
    # Load participant info
    participant_info = pd.read_csv(participant_info_path, sep='\t')
    
    # Exclude participants in group "F"
    filtered_participants = participant_info[participant_info['Group'] != "F"]
    
    filtered_participants['participant_id'] = filtered_participants['participant_id'].str[-3:]
    
    # string to int
    filtered_participants['participant_id'] = filtered_participants['participant_id'].astype(int)
    return filtered_participants

def main():
    # Define frequency bands
    freq_bands = {
        "Delta": (0.5, 4),
        "Theta": (4, 8),
        "Alpha": (8, 13),
        "Beta": (13, 25),
        "Gamma": (25, 45),
    }
    
    # Parameters
    epoch_length = 4  # seconds
    overlap = 0.5  # 50% overlap
    input_directory = 'datasets/derivatives'
    output_directory = 'datasets/output'
    os.makedirs(output_directory, exist_ok=True)
    
    # Load participant info
    participant_info_path = 'datasets/participants.tsv'  # Replace with actual path
    filtered_participants = load_participant_info(participant_info_path)
    
    # List to store RBP features
    all_rbp_features = []
    
    # Iterate over EEG files in all subdirectories
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith("_task-eyesclosed_eeg.set"):
                file_path = os.path.join(root, file_name)
                participant_id = extract_participant_id(file_name)
                # Skip participants not in the filtered metadata
                if participant_id not in filtered_participants['participant_id'].values:
                    continue
                
                print("Processing:", file_name)
                
                try:
                    features = process_file(file_path, epoch_length, overlap, freq_bands)
                    features["participant_id"] = participant_id
                    all_rbp_features.append(features)
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
    
    # Convert all RBP features to a DataFrame
    rbp_df = pd.DataFrame(all_rbp_features)
    
    # Merge RBP features with participant metadata
    rbp_with_info = pd.merge(
        rbp_df,
        filtered_participants[['participant_id', 'Age', 'MMSE', 'Group']],
        on='participant_id',
        how='inner'
    )
    
    # Save the RBP features to a CSV file
    nodes_output_path = os.path.join(output_directory, 'nodes.csv')
    rbp_with_info.rename(columns={'participant_id': 'Id'}, inplace=True)
    # Order rows according to the column "Id"
    rbp_with_info.sort_values(by='Id', inplace=True)
    rbp_with_info[['Id', 'Theta/Alpha', 'Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'MMSE', 'Age', 'Group']].to_csv(nodes_output_path, index=False)
    
    print(f"Nodes file saved: {nodes_output_path}")

if __name__ == '__main__':
    main()