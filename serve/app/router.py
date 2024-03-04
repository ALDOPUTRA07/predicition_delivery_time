import json
import logging
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from prediction_delivery_time import __version__ as _version
from prediction_delivery_time.config.core import config
from prediction_delivery_time.predict import make_prediction
from serve.app.database import get_db
from serve.app.models import PredictionTable
from serve.app.schemas import schema
from utils.report import (
    REPORT_PATH,
    data_drift,
    model_performance,
    report_data_drift,
    report_performance_model,
)

api_router = APIRouter()

# Logger
logger = logging.getLogger(__name__)


# Defining path operation for root endpoint
@api_router.get('/', status_code=status.HTTP_200_OK)
def model_info():
    return {
        'name': config.app_config.package_name,
        'description': "",
        'version': _version,
    }


# predict
@api_router.post(
    '/predict',
    response_model=schema.PredictionResults,
    status_code=status.HTTP_201_CREATED,
)
def predict(data: schema.DataInput, db: Session = Depends(get_db)) -> Any:
    input_df = jsonable_encoder(data.inputs)
    df = pd.DataFrame(input_df)

    result = make_prediction(input_data=df.replace({np.nan: None}))

    if result["errors"] is not None:
        logger.warning(f"Prediction validation error: {result.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(result["errors"]))

    result['predictions'] = result['predictions'][0][0]
    df['prediction'] = result['predictions']

    db.add_all([PredictionTable(**pred) for pred in df.to_dict('records')])
    db.commit()

    return result


@api_router.get('/monitoring-models', status_code=status.HTTP_200_OK)
def monitoring_model() -> FileResponse:
    # Update data
    report_performance_model()

    # Report model
    report_model = f"{REPORT_PATH}/{model_performance}"

    return FileResponse(report_model)


@api_router.get('/monitoring-data-drift', status_code=status.HTTP_200_OK)
def monitoring_data_drift() -> FileResponse:
    # Update data
    report_data_drift()

    # Report model
    report_datadrift = f"{REPORT_PATH}/{data_drift}"

    return FileResponse(report_datadrift)
