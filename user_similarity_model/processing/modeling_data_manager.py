import os

import joblib
import pandas as pd
import psycopg2

from user_similarity_model import __version__ as _version
from user_similarity_model.config.core import (
    DATASET_DIR,
    SQL_DIR,
    TRAINED_MODEL_DIR,
    config,
)


def load_abt_raw():
    conn = psycopg2.connect(**config.app_config.database_specs)
    cur = conn.cursor()
    with open(os.path.join(SQL_DIR, "base-table-features.sql")) as file:
        query = file.read()
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    abt_raw = pd.DataFrame(rows, columns=column_names, dtype=float)
    abt_raw.head(10).to_csv(os.path.join(DATASET_DIR, "sample_query_raw_data.csv"))
    return abt_raw


def save_pipeline(pipeline_to_persist):
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def remove_old_pipelines(files_to_keep):
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()


def load_pipeline(file_name):
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model
