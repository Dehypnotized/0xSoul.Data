# For me this one looks preferable

import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def identify_features_using_ml(dataset, ml_algorithm):
    """Identify features in a dataset using a machine learning algorithm.

    Args:
        dataset: A Pandas DataFrame containing the dataset.
        ml_algorithm: A machine learning algorithm, such as a decision tree or random forest.

    Returns:
        A Pandas DataFrame containing the identified features.
    """

    # Create a new DataFrame to store the identified features.
    identified_features = pd.DataFrame()

    # Create a selector object to select the features that are important for the machine learning algorithm.
    selector = SelectFromModel(ml_algorithm, threshold='auto')

    # Fit the selector to the dataset.
    selector.fit(dataset.drop(columns=['target']), dataset['target'])

    # Get the list of selected features.
    selected_features = selector.get_support()

    # Add the selected features to the new DataFrame.
    for i in range(len(dataset.columns)):
        if selected_features[i]:
            identified_features[dataset.columns[i]] = dataset[dataset.columns[i]]

    return identified_features

# Example usage:

# Load the dataset from the previous script.
dataset = pd.read_csv('processed_data.txt')

# Create a decision tree classifier.
decision_tree_classifier = DecisionTreeClassifier()

# Identify the features in the dataset using the decision tree classifier.
identified_features_using_decision_tree = identify_features_using_ml(dataset, decision_tree_classifier)

# Create a random forest classifier.
random_forest_classifier = RandomForestClassifier()

# Identify the features in the dataset using the random forest classifier.
identified_features_using_random_forest = identify_features_using_ml(dataset, random_forest_classifier)

# Save the identified features to new files.
identified_features_using_decision_tree.to_csv('identified_features_using_decision_tree.csv', index=False)
identified_features_using_random_forest.to_csv('identified_features_using_random_forest.csv', index=False)
