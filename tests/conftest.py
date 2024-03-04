import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

from prediction_delivery_time.config.core import config
from prediction_delivery_time.processing.data_manager import load_dataset


@pytest.fixture
def dataset():
    data = load_dataset(file_name=config.app_config.data)

    return data


@pytest.fixture
def data_train_test():
    data = load_dataset(file_name=config.app_config.data)

    X_train, X_test, y_train, y_test = train_test_split(
        data[config.config_model.features],  # predictors
        data[config.config_model.target],
        test_size=config.config_model.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.config_model.random_state,
    )

    return X_train, X_test, y_train, y_test


@pytest.fixture
def data_sample():
    data = load_dataset(file_name=config.app_config.data)

    X_train, _, _, _ = train_test_split(
        data[config.config_model.features],  # predictors
        data[config.config_model.target],
        test_size=config.config_model.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.config_model.random_state,
    )

    data_sample = X_train.iloc[:1]

    return data_sample


@pytest.fixture
def dummy_df():
    dummy_data = {
        "ID": ["4607"],
        "Delivery_person_ID": ["INDORES13DEL02"],
        "Delivery_person_Age": [37],
        "Delivery_person_Ratings": [4.9],
        "Restaurant_latitude": [22.745049],
        "Restaurant_longitude": [75.892471],
        "Delivery_location_latitude": [22.765049],
        "Delivery_location_longitude": [75.912471],
        "Type_of_order": ["Snack "],
        "Type_of_vehicle": ["motorcycle "],
        "Time_taken": [24],
    }
    df_dummy_data = pd.DataFrame(dummy_data)
    return df_dummy_data
