from sklearn.model_selection import train_test_split

from prediction_delivery_time.config.core import config
from prediction_delivery_time.pipeline import price_pipe
from prediction_delivery_time.processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.data)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.config_model.features],  # predictors
        data[config.config_model.target],
        test_size=config.config_model.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.config_model.random_state,
    )

    # fit model
    try:
        price_pipe.fit(X_train, y_train)
    except ValueError:
        raise ValueError("Training model has been failed")

    # persist trained model
    save_pipeline(pipeline_to_persist=price_pipe)


if __name__ == "__main__":
    run_training()
