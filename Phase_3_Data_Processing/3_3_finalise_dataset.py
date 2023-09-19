import pandas as pd

# Load the datasets.
dataset = pd.read_csv('processed_data.txt')
identified_features = pd.read_csv('identified_features.csv')

# Merge the datasets.
merged_dataset = pd.merge(dataset, identified_features, on='customer_id')

# Drop any unnecessary columns.
merged_dataset.drop(columns=['customer_id'], inplace=True)

# Scale the data.
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_dataset = scaler.fit_transform(merged_dataset)

# Split the data into training and test sets.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(scaled_dataset, merged_dataset['target'], test_size=0.25, random_state=42)

# Save the training and test sets.
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)
