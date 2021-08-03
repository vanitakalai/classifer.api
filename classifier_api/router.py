from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from classifier_api.model_selection import run_models

router = APIRouter()


class Prediction(BaseModel):
    pattern: str
    product_id: int


@router.get(
    "/predict",
    response_model=Prediction,
)
async def get_prediction(
    name: str,
    description: str,
    product_id: int,
    image_url: Optional[List[str]] = Query(None),
) -> dict:

    pattern = run_models(name, description, image_url)

    return {"pattern": pattern, "product_id": product_id}
