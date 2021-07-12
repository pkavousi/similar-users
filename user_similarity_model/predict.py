from user_similarity_model import __version__ as _version
from user_similarity_model.config.core import config
from user_similarity_model.processing.modeling_data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(user_handle):
    results = {"predictions": None, "version": _version}
    predictions = _pipe["similarity_model"].predict(user_handle)
    results = {
        "predictions": predictions,
        "version": _version,
    }
    return results
