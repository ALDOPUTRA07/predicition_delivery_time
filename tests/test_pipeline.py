import pytest

from prediction_delivery_time import pipeline


def test_drop_features(data_sample):
    # arrange
    data_sample = data_sample

    # act
    result_drop_features = pipeline.price_pipe[:1].fit_transform(data_sample)
    result_drop_features = list(result_drop_features)

    # assert
    ('Delivery_person_ID' not in result_drop_features) is False


def test_trim_whitespaces(data_sample):
    # arrange
    data_sample = data_sample

    # act
    result_trim_whitespaces = pipeline.price_pipe[:2].fit_transform(data_sample)
    result_trim_whitespaces = result_trim_whitespaces['Type_of_order'].values[0]

    # assert
    assert (result_trim_whitespaces[-1] == ' ') is False


def test_distance_column(data_sample):
    # arrange
    data_sample = data_sample

    # act
    result_distance_column = pipeline.price_pipe[:3].fit_transform(data_sample)

    # assert
    assert (result_distance_column['distance'].values[0]) == pytest.approx(6.2, 0.1)


def test_type_vehicle_map(data_sample):
    # arrange
    data_sample = data_sample

    # act
    result_type_vehicle_map = pipeline.price_pipe[:4].fit_transform(data_sample)

    # assert
    assert result_type_vehicle_map['Type_of_vehicle'].dtype == 'int64'
    assert result_type_vehicle_map['Type_of_vehicle'].values[0] == 0


def test_type_order_map(data_sample):
    # arrange
    data_sample = data_sample

    # act
    result_type_order_map = pipeline.price_pipe[:5].fit_transform(data_sample)

    # assert
    assert result_type_order_map['Type_of_order'].dtype == 'int64'
    assert result_type_order_map['Type_of_order'].values[0] == 2
