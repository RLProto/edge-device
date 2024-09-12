from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.backend.models.Crop import CropDataModel, GlobalCropData
from app.dependencies import get_db
from app.utils import interface_log

router = APIRouter(tags=["Crop"])


@router.post("/crop/")
async def video_crop_definitions(
    crop_data: CropDataModel, db: Session = Depends(get_db)
) -> str:
    """
    Handles POST requests to set video cropping coordinates and logs the interaction.

    Args:
        crop_data (CropDataModel): The cropping data model containing the coordinates.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        str: A response string confirming the coordinates.
    """
    try:
        GlobalCropData.set_coordinates(crop_data.model_dump())
    finally:
        response = f"Coordinates: {GlobalCropData.get_coordinates()}"
        interface_log(response, db)
    return response
