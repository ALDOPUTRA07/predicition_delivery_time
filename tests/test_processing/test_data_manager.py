# from prediction_delivery_time import __version__ as _version
from prediction_delivery_time.config.core import config
from prediction_delivery_time.processing.data_manager import (  # , load_pipeline
    load_dataset,
)


def test_load_dataset():
    # arrange
    file_dataset = config.app_config.data

    # act
    dataset = load_dataset(file_name=file_dataset)

    # assert
    assert dataset.shape == (45593, 11)


# def test_load_pipeline():
#     # arrange
#     pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"

#     # act
#     _price_pipe = load_pipeline(file_name=pipeline_file_name)

#     # assert
#     assert _price_pipe is not None
