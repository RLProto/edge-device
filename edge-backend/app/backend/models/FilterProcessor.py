from fastapi import HTTPException

from app.backend.models.Crop import GlobalCropData
from app.backend.models.FilterHandler import FilterHandler
from app.backend.services.image_processing import apply_crop, process_image_with_filters


class FilterProcessor:
    def __init__(self, filter_handler: FilterHandler):
        self.filter_handler = filter_handler

    def apply_filters(self, image):
        """Aplica os filtros do FilterHandler ao frame."""
        try:
            processed_image = process_image_with_filters(
                image, self.filter_handler.filter_specs
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro no processamento: {str(e)}"
            )
        return processed_image

    def apply_black_edges(self, image):
        return apply_crop(image, (0, -420, 1920, 1920))

    def apply_crop_predict_image(self, image):
        coordinates = GlobalCropData.recalculate_real_coordinates()
        return apply_crop(image, coordinates)
