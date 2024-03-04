from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from strictyaml import YAML, load

import prediction_delivery_time

# Project Directories
PACKAGE_ROOT = Path(prediction_delivery_time.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    data: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    test_size: float
    random_state: int
    xgboost_parameter: Dict[str, Union[int, float]]
    variables_to_rename: Dict[str, str]
    target: str
    features: List[str]
    drop_vars: List[str]
    trim_whitespace_vars: List[str]
    distance_column: List[str]
    type_vehicle_vars: List[str]
    type_order_vars: List[str]
    map_type_vehicle: Dict[str, int]
    map_type_order: Dict[str, int]


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    config_model: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        config_model=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
