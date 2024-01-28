# Import necessary libraries, packages, and modules
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error


def make_prediction(dataset, user_values):
    # Drop unnecessary columns
    dataset = dataset.drop(["Unnamed: 0", "county", "city"], axis=1)
    # Drop rows with zero values
    dataset = dataset[(dataset != 0).all(1)]

    # Separate features
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Encode the independent categorical variables
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse_output=False), [0,1,6])], remainder='passthrough')
    X = np.array(ct.fit_transform(X))

    # Split the dataset into the Training and Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    # Standardize the features
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Create and train the K-Nearest Neighbors Regressor
    regressor = KNeighborsRegressor(n_neighbors=5, weights='distance')
    regressor.fit(X_train, y_train)

    # Make predictions
    y_pred = regressor.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')

    # New set of features for prediction (original values)
    new_features_original = pd.DataFrame(user_values)
    # Transform the original features using the same ColumnTransformer
    new_features_transformed = ct.transform(new_features_original)
    # Standardize the transformed features using the same StandardScaler
    new_features_standardized = sc.transform(new_features_transformed)
    # Make predictions for the new features
    predicted_value = regressor.predict(new_features_standardized)

    return predicted_value

if __name__ == "__main__":
    # Import dataset
    dataset = pd.read_csv(f"app/data/ProcessedDataDB-23-12-11.csv")

    # Define new input data
    new_data = {'manufacturer': ["Dacia"],
                'model': ["Logan"], 
                'mileage': [100000], 
                'capacity': [1461], 
                'power': [115], 
                'year': [2020], 
                'fuel': ['Diesel']
                }
    
    print(f'For the car with follow speicifications:\n'\
        f'manufacturer: {new_data["manufacturer"][0]}.\n'\
        f'model: {new_data["model"][0]}.\n'\
        f'mileage: {new_data["mileage"][0]} km.\n'\
        f'capacity: {new_data["capacity"][0]} cm3.\n'\
        f'power: {new_data["power"][0]} HP.\n'\
        f'year: {new_data["year"][0]}.\n'\
        f'fuel: {new_data["fuel"][0]}.\n'\
        f'the estimated price is: {int(make_prediction(dataset, new_data)[0])} EUR.')