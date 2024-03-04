from pathlib import Path
from typing import Dict

from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset.regression_performance import RegressionPreset
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report

from utils.load_data import load_current_data, load_reference_data

REPORT_PATH = Path("monitoring/report")
model_performance = "model_performance.html"
data_drift = "data_drift.html"


def data_columns() -> Dict:
    DATA_COLUMNS: Dict = {
        'target': 'Time_taken',
        'prediction_col': 'prediction',
        'num_features': [
            'Delivery_person_Age',
            'Delivery_person_Ratings',
            'Restaurant_latitude',
            'Restaurant_longitude',
            'Delivery_location_latitude',
            'Delivery_location_longitude',
        ],
        'cat_features': ['Type_of_order', 'Type_of_vehicle'],
    }

    DATA_COLUMNS['columns'] = (
        DATA_COLUMNS['num_features']
        + DATA_COLUMNS['cat_features']
        + [DATA_COLUMNS['target'], DATA_COLUMNS['prediction_col']]
    )

    return DATA_COLUMNS


def column_mapping():
    target = 'Time_taken'
    prediction = 'prediction'
    numerical_features = [
        'Delivery_person_Age',
        'Restaurant_latitude',
        'Restaurant_longitude',
        'Delivery_location_latitude',
        'Delivery_location_longitude',
    ]
    categorical_features = ['Type_of_order', 'Type_of_vehicle']

    column_mapping = ColumnMapping()

    column_mapping.target = target
    column_mapping.prediction = prediction
    column_mapping.numerical_features = numerical_features
    column_mapping.categorical_features = categorical_features

    return column_mapping


def report_performance_model():
    # Load data
    data_column = data_columns()
    data_column = data_column['columns']

    current_data = load_current_data(columns=data_column)
    reference_data = load_reference_data(columns=data_column)

    # Column mapping
    col_mapping = column_mapping()

    # Performance model report
    regression_performance_report = Report(metrics=[RegressionPreset()])
    regression_performance_report.run(
        current_data=current_data,
        reference_data=reference_data,
        column_mapping=col_mapping,
    )

    # Remove old report
    for model_file in REPORT_PATH.iterdir():
        if model_file.name == model_performance:
            model_file.unlink()

    # Save new report
    model_performance_report_path = f"{REPORT_PATH}/{model_performance}"
    regression_performance_report.save_html(model_performance_report_path)


def report_data_drift():
    # Load data
    data_column = data_columns()
    data_column = data_column['columns']

    current_data = load_current_data(columns=data_column)
    reference_data = load_reference_data(columns=data_column)

    # Column mapping
    col_mapping = column_mapping()

    # Performance model report
    data_drift_report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    data_drift_report.run(
        current_data=current_data,
        reference_data=reference_data,
        column_mapping=col_mapping,
    )

    # Remove old report
    for model_file in REPORT_PATH.iterdir():
        if model_file.name == data_drift:
            model_file.unlink()

    # Save new report
    data_drift_report_path = f"{REPORT_PATH}/{data_drift}"
    data_drift_report.save_html(data_drift_report_path)
