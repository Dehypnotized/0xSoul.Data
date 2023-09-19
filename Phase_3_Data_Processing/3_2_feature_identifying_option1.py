import pandas as pd

def identify_features(dataset, feature_list):
    """Identify features in a dataset from a feature list.

    Args:
        dataset: A Pandas DataFrame containing the dataset.
        feature_list: A list of feature names.

    Returns:
        A Pandas DataFrame containing the identified features.
    """

    # Create a new DataFrame to store the identified features.
    identified_features = pd.DataFrame()

    # Iterate over the feature list and add the features to the new DataFrame if they are present in the dataset.
    for feature in feature_list:
        if feature in dataset.columns:
            identified_features[feature] = dataset[feature]

    return identified_features

# Example usage:

# Load the dataset from the previous script.
dataset = pd.read_csv('processed_data.txt')

# Create a list of feature names.
feature_list = ['customer_tenure', 'customer_spending_history', 'customer_support_tickets']

# Identify the features in the dataset from the feature list.
identified_features = identify_features(dataset, feature_list)

# Save the identified features to a new file.
identified_features.to_csv('identified_features.csv', index=False)
