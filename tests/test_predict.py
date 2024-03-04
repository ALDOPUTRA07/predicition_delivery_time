import pytest

from prediction_delivery_time.predict import make_prediction


def test_predict(dummy_df):
    # arrange
    data_dummy = dummy_df

    # act
    result = make_prediction(input_data=data_dummy)

    # assert
    assert result['errors'] is None
    assert result['predictions'][0][0] == pytest.approx(23.9, 0.1)
