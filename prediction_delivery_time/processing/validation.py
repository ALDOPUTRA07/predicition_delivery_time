from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from prediction_delivery_time.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.config_model.features
        if validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names
    input_data.rename(columns=config.config_model.variables_to_rename, inplace=True)
    relevant_data = input_data[config.config_model.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        DataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    ID: Optional[str]
    Delivery_person_ID: Optional[str]
    Delivery_person_Age: Optional[int]
    Delivery_person_Ratings: Optional[float]
    Restaurant_latitude: Optional[float]
    Restaurant_longitude: Optional[float]
    Delivery_location_latitude: Optional[float]
    Delivery_location_longitude: Optional[float]
    Type_of_order: Optional[str]
    Type_of_vehicle: Optional[str]
    Time_taken: Optional[int]


class DataInputs(BaseModel):
    inputs: List[DataInputSchema]
