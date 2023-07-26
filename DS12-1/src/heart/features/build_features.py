"""Модуль признаков"""
from typing import List

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


def process_categorical_features(categorical_df: pd.DataFrame) -> pd.DataFrame:
    """Функция предобработки категориальных признаков"""
    categorical_pipeline = build_categorical_pipeline()
    return pd.DataFrame(categorical_pipeline.fit_transform(categorical_df).toarray())


def build_categorical_pipeline() -> Pipeline:
    """Цепочка предобработки категориальных признаков"""
    categorical_pipeline = Pipeline(
        [
            ("simple", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder())
        ]
    )
    return categorical_pipeline


def process_numerical_features(numerical_df: pd.DataFrame) -> pd.DataFrame:
    """Функция обработки числовых признаков"""
    num_pipeline = build_numerical_pipeline()
    return pd.DataFrame(num_pipeline.fit_transform(numerical_df))


def build_numerical_pipeline() -> Pipeline:
    """Пайплайн обработки числовых признаков"""
    num_pipeline = Pipeline(
        [
            ("OutlierRemover", OutlierRemover()),
            ("impute", SimpleImputer(missing_values=np.nan, strategy="most_frequent"))
        ]
    )
    return num_pipeline


def make_features(transformer: ColumnTransformer, df_futures: pd.DataFrame) -> pd.DataFrame:
    """Функция выбора признаков"""
    return pd.DataFrame(transformer.transform(df_futures))


def extract_target(data: pd.DataFrame, target_col: List[str]) -> pd.Series:
    """Функция выбора цели"""
    target = data[target_col].values
    return target


class OutlierRemover(BaseEstimator, TransformerMixin):
    """ Класс обработки числовых признаков"""

    def __init__(self, factor=1.5):
        """Функция инициализации"""
        self.factor = factor

    def outlier_removal(self, data: pd.DataFrame):
        """Функция подготовки данных"""
        data = pd.Series(data).copy()
        quant1 = data.quantile(0.25)
        quant3 = data.quantile(0.75)
        iqr = quant3 - quant1
        lower_bound = quant1 - (self.factor * iqr)
        upper_bound = quant3 + (self.factor * iqr)
        data.loc[((data < lower_bound) | (data > upper_bound))] = np.nan
        return pd.Series(data)

    def fit(self, data, futures=None):
        """Функция обучения модели (не используется)"""
        _, _ = data, futures
        return self

    def transform(self, data: np.array):
        """Функция обработки (не используется)"""
        return pd.DataFrame(data).apply(self.outlier_removal)


def build_transformer(categorical_features: List[str],
                      numerical_features: List[str]) -> ColumnTransformer:
    """Функция создания обработок"""
    transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                build_categorical_pipeline(),
                list(categorical_features),
            ),
            (
                "numerical_pipeline",
                build_numerical_pipeline(),
                list(numerical_features),
            )
        ]
    )
    return transformer
