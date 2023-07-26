"""Модуль признаков моделей"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass()
class FeatureConfig:
    """Класс признаков моделей"""
    categorical_features: List[str]
    numerical_features: List[str]
    target_col: List[str]
    use_log_trick: bool = field(default=True)
    features_to_drop: Optional[List[str]] = None
