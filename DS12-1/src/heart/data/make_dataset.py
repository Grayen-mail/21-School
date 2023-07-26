# -*- coding: utf-8 -*-
"""Модуль создания датасета"""
# from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def read_data(dataset_path: str) -> pd.DataFrame:
    """Reading dataset from path"""
    data = pd.read_csv(dataset_path)
    return data


def split_train_test_data(dataset: pd.DataFrame,
                          test_size: float,
                          random_state: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataset into random train and test subsets"""
    data_train, data_test = train_test_split(dataset, test_size=test_size,
                                             random_state=random_state)
    return data_train, data_test
