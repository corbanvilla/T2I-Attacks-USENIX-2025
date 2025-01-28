"""
Helper functions for statistical analysis.
"""

from collections import Counter

import numpy as np


def remove_outliers_iqr(df, column):
    """
    Remove outliers from a specified column in a Pandas DataFrame using the IQR method.
    """
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter the DataFrame to remove outliers
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    print(f"Removed {len(df) - len(df_filtered)} outliers from column '{column}'")

    return df_filtered


def entropy(y):
    """
    Calculate the entropy of a label distribution.
    """
    distribution = Counter(y)
    total_count = len(y)
    probabilities = [count / total_count for count in distribution.values()]
    return -sum(p * np.log2(p) for p in probabilities)


def information_gain(X, y, feature_index, split_value):
    """
    Calculate the information gain for a specific split on a feature.

    Parameters:
    - X: Feature dataset, numpy array of shape (num_samples, num_features)
    - y: Labels, numpy array of shape (num_samples,)
    - feature_index: Index of the feature to split on
    - split_value: Value of the feature to split on

    Returns:
    - Information gain of the split
    """
    # Calculate the entropy before the split
    entropy_before = entropy(y)

    # Split the data based on the feature value
    left_indices = X[:, feature_index] <= split_value
    right_indices = X[:, feature_index] > split_value

    left_y = y[left_indices]
    right_y = y[right_indices]

    # Calculate the entropy after the split
    total_count = len(y)
    left_entropy = entropy(left_y) if len(left_y) > 0 else 0
    right_entropy = entropy(right_y) if len(right_y) > 0 else 0

    entropy_after = (len(left_y) / total_count) * left_entropy + (
        len(right_y) / total_count
    ) * right_entropy

    # Calculate information gain
    info_gain = entropy_before - entropy_after
    return info_gain


def find_best_split(X, y):
    """
    Find the best feature and value to split the dataset on.

    Parameters:
    - X: Feature dataset, numpy array of shape (num_samples, num_features)
    - y: Labels, numpy array of shape (num_samples,)

    Returns:
    - Best feature index to split on
    - Best feature value to split on
    - Information gain of the best split
    """
    best_feature = None
    best_value = None
    best_gain = -1

    num_features = X.shape[1]

    for feature_index in range(num_features):
        unique_values = np.unique(sorted(X[:, feature_index]))

        for value in unique_values:
            gain = information_gain(X, y, feature_index, value)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature_index
                best_value = value

    sorted_best_features = sorted(set(X[:, best_feature]))
    value_after_best = sorted_best_features[sorted_best_features.index(best_value) + 1]
    best_value_median_split = (best_value + value_after_best) / 2

    return best_feature, best_value_median_split, best_gain
