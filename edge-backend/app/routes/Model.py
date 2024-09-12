from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.backend.models.FileHandler import (
    FileHandler,
    InvalidFileTypeError,
    ModelTypeNotSupportedError,
)
from app.dependencies import get_db
from app.utils import filter, interface_log, model_handler

router = APIRouter(tags=["Upload Model"])
file_handler = FileHandler()


@router.get("/check-model-loaded/")
async def check_model_loaded() -> JSONResponse:
    model_name = file_handler.model_name if file_handler.model_name else ""
    print(model_name)
    return JSONResponse(content={"Arquivo": model_name})


@router.post("/upload-model/")
async def upload_model(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> JSONResponse:
    """
    Handles POST requests to upload a model file, validates it, and updates the system model settings.

    Args:
        file (UploadFile): The model file to be uploaded.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        JSONResponse: A response confirming the successful upload of the file.

    Raises:
        HTTPException: If the file is not a valid zip file or the model type is not supported.
    """
    try:
        file_handler.validate_zip_file(file)
    except InvalidFileTypeError as e:
        error_message = str(e)
        interface_log(error_message, db)
        raise HTTPException(status_code=400, detail=error_message)

    try:
        file_handler.setup_environment()
        await file_handler.save_uploaded_zip(file)
        file_handler.extract_model_files()
        if not model_handler.loaded_model_type:
            raise HTTPException(status_code=415, detail="Tipo de modelo não suportado")
        filter.reset_filter_result()
    except ModelTypeNotSupportedError as e:
        error_message = str(e)
        interface_log(f"Arquivo: '{file.filename}'. {error_message}", db)
        raise HTTPException(status_code=415, detail=error_message)

    success_message = f"Arquivo '{file.filename}' carregado corretamente"
    interface_log(success_message, db)
    return JSONResponse(content={"Arquivo": file.filename})
