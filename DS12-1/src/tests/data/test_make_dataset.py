import pandas as pd

from heart.data.make_dataset import read_data, split_train_test_data
from heart.entities import SplittingConfig


def test_load_dataset(dataset_path: str, target_col: str):
    data = read_data(dataset_path)
    assert len(data) == 100
    assert target_col in data.keys(), (
        "target_col not in dataset"
    )


def test_split_dataset(dataset: pd.DataFrame):
    train_data, test_data = split_train_test_data(dataset, SplittingConfig.test_size,
                                                  SplittingConfig.random_state)
    assert len(test_data) == int(100*SplittingConfig.test_size)
    assert len(train_data) == 100 - len(test_data)

    pass
