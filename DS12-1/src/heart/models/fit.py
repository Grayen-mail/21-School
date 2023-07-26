"""Модуль тренировки и записи модели"""
import pickle
from typing import Union

import pandas as pd
from hydra.utils import instantiate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


SklearnRegressionModel = Union[RandomForestClassifier, LogisticRegression]


def train_model(
    model_params, train_features: pd.DataFrame, target: pd.Series
) -> SklearnRegressionModel:
    """Функция тренировки модели"""
    model = instantiate(model_params).fit(train_features, target.ravel())
    return model


def serialize_model(model: SklearnRegressionModel, output: str) -> str:
    """Функция записи модели"""
    with open(output, "wb") as file:
        pickle.dump(model, file)
    return output
