# Authors: payam.kavousi@gmail.com
"""
This module provides a two step SKlearn pipeline for preprocessing
"""

from feature_engine.encoding import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from user_similarity_model.config.core import config

pipe = Pipeline(
    [
        # ==== Categorical encoding
        # latest_interest_tag and latest_assessment_tag
        (
            "Targetencoder",
            OrdinalEncoder(
                encoding_method="ordered",
                variables=config.model_config.categorical_vars,
            ),
        ),
        ("scaler", MinMaxScaler()),
    ]
)
