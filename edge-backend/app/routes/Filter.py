from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.backend.models.PredictFilter import FilterDataModel
from app.dependencies import get_db
from app.utils import filter, interface_log

router = APIRouter(tags=["Filter"])


@router.post("/filter/")
async def change_filter(
    filter_value: FilterDataModel, db: Session = Depends(get_db)
) -> str:
    """
    Handles POST requests to change filter settings and logs the interaction.

    Args:
        filter_value (FilterDataModel): The filter settings model containing new settings.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        str: A response string confirming the new filter settings.
    """
    try:
        filter.set_filter(filter_value.model_dump())
    finally:
        response = f"Filtro definido como: {filter.get_filter()}"
        interface_log(response, db)
    return response
