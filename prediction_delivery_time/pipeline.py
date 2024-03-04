from feature_engine.selection import DropFeatures
from sklearn.pipeline import Pipeline
from xgboost.sklearn import XGBRegressor

from prediction_delivery_time.config.core import config
from prediction_delivery_time.processing import features as f

params = config.config_model.xgboost_parameter
for key, val in params.items():
    vars()[key] = val

price_pipe = Pipeline(
    [
        ("drop_features", DropFeatures(features_to_drop=config.config_model.drop_vars)),
        (
            "trim_whitespace",
            f.TrimWhitespaces(variables=config.config_model.trim_whitespace_vars),
        ),
        (
            "distance_column",
            f.CalculateDistances(
                variables=config.config_model.distance_column, column_name='distance'
            ),
        ),
        (
            "type_vehicle_map",
            f.Mapper(
                variables=config.config_model.type_vehicle_vars,
                mappings=config.config_model.map_type_vehicle,
            ),
        ),
        (
            "type_order_map",
            f.Mapper(
                variables=config.config_model.type_order_vars,
                mappings=config.config_model.map_type_order,
            ),
        ),
        (
            'model',
            XGBRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                reg_alpha=reg_alpha,
                min_child_weight=min_child_weight,
                gamma=gamma,
                colsample_bytree=colsample_bytree,
                subsample=subsample,
                nthread=nthread,
                scale_pos_weight=scale_pos_weight,
                seed=seed,
            ),
        ),
    ]
)
