# Authors: payam.kavousi@gmail.com
"""
This module provides runs the training
"""

from pipeline import pipe
from processing.modeling_data_manager import load_abt_raw, save_pipeline

import user_similarity_model.model as pred


def run_training():
    """Train the model and save the model"""
    # read training data from Azure Postgresql
    data = load_abt_raw()
    columns = [col for col in data.columns if col != "user_handle"]
    data["latest_interest_tag"] = data["latest_interest_tag"].astype("O")
    data["latest_assessment_tag"] = data["latest_assessment_tag"].astype("O")
    # fit model
    pipe.fit(data.loc[:, columns], data["total_courses_time_spent"])
    data.loc[:, columns] = pipe.transform(data.loc[:, columns])
    sim = pred.SimilarityModel()
    sim.fit(data)
    model = {"pipeline": pipe, "similarity_model": sim}

    # persist trained model
    save_pipeline(pipeline_to_persist=model)


if __name__ == "__main__":
    run_training()
