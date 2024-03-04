from typing import Any, List, Optional

from pydantic import BaseModel

from prediction_delivery_time.processing.validation import DataInputSchema


class DataInput(BaseModel):
    inputs: List[DataInputSchema]

    model_config = {
        "json_schema_extra": {
            "example": {
                "inputs": [
                    {
                        "ID": "4607",
                        "Delivery_person_ID": "INDORES13DEL02",
                        "Delivery_person_Age": 37,
                        "Delivery_person_Ratings": 4.9,
                        "Restaurant_latitude": 22.745049,
                        "Restaurant_longitude": 75.892471,
                        "Delivery_location_latitude": 22.765049,
                        "Delivery_location_longitude": 75.912471,
                        "Type_of_order": "Snack",
                        "Type_of_vehicle": "motorcycle",
                        "Time_taken": 24,
                    }
                ]
            }
        }
    }


class PredictionResults(BaseModel):
    predictions: float
    version: Optional[Any]
    errors: Optional[Any]
