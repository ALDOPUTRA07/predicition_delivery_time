from prediction_delivery_time.config.core import create_and_validate_config


def test_config_core():
    # arrange
    _config = create_and_validate_config()

    # assert
    assert _config.config_model.test_size == 0.1
