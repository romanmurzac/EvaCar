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

    # Identify categorical columns
    categorical_columns = [0, 1, 6]
    
    # Create transformers for numerical and categorical features
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

    # Create ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, ~np.isin(range(X.shape[1]), categorical_columns)),
            ('categorical', categorical_transformer, categorical_columns)
        ])

    # Fit-transform and set column names explicitly
    X = preprocessor.fit_transform(X)
    
    # Split the dataset into the Training and Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    # Create and train the K-Nearest Neighbors Regressor
    regressor = KNeighborsRegressor(n_neighbors=5, weights='distance')
    regressor.fit(X_train, y_train)

    # New set of features for prediction (original values)
    new_features_original = pd.DataFrame(user_values)
    # Transform the original features using the same ColumnTransformer
    new_features_transformed = preprocessor.transform(new_features_original)
    # Make predictions for the new features
    predicted_value = regressor.predict(new_features_transformed)

    return predicted_value
