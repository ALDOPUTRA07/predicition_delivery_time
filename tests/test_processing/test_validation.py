from prediction_delivery_time.processing.validation import validate_inputs


def test_validate_inputs(dataset):
    # arrange
    data = dataset

    # act
    validated_data, errors = validate_inputs(input_data=data)

    # assert
    assert errors is None
    assert validated_data.shape == (45593, 11)


def test_validate_inputs_errors(dataset):
    # arrange
    data = dataset
    data.loc[0, "Type_of_order"] = 1

    # act
    validated_data, errors = validate_inputs(input_data=data)

    # assert
    assert errors is None
