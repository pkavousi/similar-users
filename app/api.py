from typing import Any

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from loguru import logger

from app import __version__, schemas
from app.config import settings
from user_similarity_model import __version__ as model_version
from user_similarity_model.predict import make_prediction

api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleUserDataInputs) -> Any:
    """
    Output the similar users
    """
    print(input_data.inputs)
    input_df = jsonable_encoder(input_data.inputs)[0]["user_handle"]
    print(input_df)
    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = make_prediction(input_df)

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results
