# Authors: payam.kavousi@gmail.com
"""
This module provide a test for deployed API
"""

from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, test_data):
    "Given a payload test the response"
    payload = {
        # ensure pydantic plays well with np.nan
        "inputs": [test_data]
    }
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["predictions"]
