from typing import List

import pandas as pd
from haversine import Unit, haversine
from sklearn.base import BaseEstimator, TransformerMixin


class TrimWhitespaces(BaseEstimator, TransformerMixin):
    """Trim Whitespaces"""

    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].apply(lambda x: x.rstrip())

        return X


class DropValues(BaseEstimator, TransformerMixin):
    """DropValues"""

    def __init__(self, variables: List[str], value: str):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for feature in self.variables:
            X[feature]

        return X


class CalculateDistances(BaseEstimator, TransformerMixin):
    """CalculateDistances"""

    def __init__(self, variables: List[str], column_name: str):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.column_name = column_name
        self.latitude1 = variables[0]
        self.longitude1 = variables[1]
        self.latitude2 = variables[2]
        self.longitude2 = variables[3]

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        distance = []

        for i in X.index:
            coord1 = (X[self.latitude1][i], X[self.longitude1][i])
            coord2 = (X[self.latitude2][i], X[self.longitude2][i])

            distance_km = haversine(coord1, coord2, unit=Unit.KILOMETERS)
            distance.append(distance_km)

        X[self.column_name] = distance
        return X


class Mapper(BaseEstimator, TransformerMixin):
    """Categorical variable mapper."""

    def __init__(self, variables: List[str], mappings: dict):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings)

        return X
