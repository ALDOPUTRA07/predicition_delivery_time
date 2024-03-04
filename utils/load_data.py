from typing import List, Text

import pandas as pd
from sqlalchemy import select

from serve.app.database import SessionLocal, engine
from serve.app.models import PredictionTable


def load_reference_data(columns: List[Text]) -> pd.DataFrame:
    DATA_REF_DIR = "monitoring/data"
    ref_path = f"{DATA_REF_DIR}/deliverytime_train_monitoring.csv"
    ref_data = pd.read_csv(ref_path)
    ref_data.rename(columns={'Time_taken(min)': 'Time_taken'}, inplace=True)
    reference_data = ref_data.loc[:, columns]
    return reference_data


def load_current_data(columns: List[Text]) -> pd.DataFrame:
    # Test monitoring data
    DATA_REF_DIR = "monitoring/data"
    cur_test_path = f"{DATA_REF_DIR}/deliverytime_test_monitoring.csv"
    cur_test_data = pd.read_csv(cur_test_path)
    cur_test_data.rename(columns={'Time_taken(min)': 'Time_taken'}, inplace=True)
    current_test_data = cur_test_data.loc[:, columns]

    # Data current from database
    db = SessionLocal()
    db.query(PredictionTable)
    query = select(PredictionTable)
    current_database = pd.read_sql_query(query, con=engine)
    current_database_data = current_database.loc[:, columns]

    # Union the two table
    current_data = pd.concat([current_test_data, current_database_data])
    current_data = current_data.loc[:, columns]

    return current_data
