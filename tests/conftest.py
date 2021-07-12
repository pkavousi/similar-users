import os

import pandas as pd
import pytest

from user_similarity_model.config.core import DATASET_DIR, config


@pytest.fixture()
def sample_local_data():
    """AI is creating summary for sample_local_data

    Returns:
        [Dict]: This function returns a dictionary with CSV files which
        in dataset folder. The data will be compared in tests against data
        that are pulled from Azure PostgreSQL server.
    """
    sample_data = {}
    for file in config.app_config.csv_files:
        sample_data[file[0:-4]] = pd.read_csv(os.path.join(DATASET_DIR, file))
    return sample_data
