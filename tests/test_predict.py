from user_similarity_model.config.core import config
from user_similarity_model.predict import make_prediction


def test_make_prediction():
    """This function tests if the predicted values of user
    similarity model are valid"""
    # Given
    user_handle = 78
    # Then
    result = make_prediction(user_handle)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    assert predictions[0] > 0
    assert predictions[0] != 78
    assert len(predictions) == config.model_config.number_of_similar_users_to_show
