from typing import Dict

from pydantic import BaseModel


class CropDataModel(BaseModel):
    x: float
    y: float
    width: float
    height: float


class GlobalCropData:
    x: float = 0.0
    y: float = 0.0
    width: float = 1920.0
    height: float = 1920.0

    @classmethod
    def set_coordinates(cls, new_data: Dict[str, float]) -> None:
        """Sets the global coordinates for cropping based on provided data."""
        cls.x = new_data.get("x", cls.x)
        cls.y = new_data.get("y", cls.y)
        cls.width = new_data.get("width", cls.width)
        cls.height = new_data.get("height", cls.height)

    @classmethod
    def get_coordinates(cls) -> Dict[str, float]:
        """Returns the current global coordinates for cropping."""
        return {"x": cls.x, "y": cls.y, "width": cls.width, "height": cls.height}

    @classmethod
    def set_base_coordinates(cls):
        cls.x = 0.0
        cls.y = 0.0
        cls.width = 1920.0
        cls.height = 1920.0

    @classmethod
    def recalculate_real_coordinates(cls) -> tuple[int]:
        return (int(position) for position in cls.get_coordinates().values())
