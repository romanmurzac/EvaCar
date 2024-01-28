# Import necessary libraries, packages, and modules
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor


def make_prediction(dataset, user_values):
    # Drop unnecessary columns
    dataset = dataset.drop(["Unnamed: 0", "county", "city"], axis=1)
    # Drop rows with zero values
    dataset = dataset[(dataset != 0).all(1)]

    # Separate features
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Encode the independent categorical variables
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse_output=False, handle_unknown="ignore"), [0,1,6])], remainder='passthrough')
    X = ct.fit_transform(X)
    column_names = ct.get_feature_names_out(['manufacturer', 'model', 'mileage', 'capacity', 'power', 'year', 'fuel'])
    X = pd.DataFrame(X, columns=column_names)

    # Split the dataset into the Training and Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    # Standardize the features
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Create and train the K-Nearest Neighbors Regressor
    regressor = KNeighborsRegressor(n_neighbors=5, weights='distance')
    regressor.fit(X_train, y_train)

    # New set of features for prediction (original values)
    new_features_original = pd.DataFrame(user_values)
    # Transform the original features using the same ColumnTransformer
    new_features_transformed = ct.transform(new_features_original)
    # Standardize the transformed features using the same StandardScaler
    new_features_standardized = sc.transform(new_features_transformed)
    # Make predictions for the new features
    predicted_value = regressor.predict(new_features_standardized)

    return predicted_value
