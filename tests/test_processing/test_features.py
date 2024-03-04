from prediction_delivery_time.config.core import config
from prediction_delivery_time.processing.features import TrimWhitespaces


def test_trim_whitespaces(dummy_df):
    # arrange
    data_dummy = dummy_df
    trim_whitespaces = TrimWhitespaces(
        variables=config.config_model.trim_whitespace_vars
    )

    # act
    result_trim_whitespaces = trim_whitespaces.fit_transform(X=data_dummy, y=[0])

    # assert
    assert (result_trim_whitespaces['Type_of_order'].values[0] != '') is True
