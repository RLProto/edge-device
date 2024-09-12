import os

from app.backend.models.FilterHandler import FilterHandler
from app.backend.models.ModelHandlerInterface import ModelHandlerInterface

from .ModelType import ModelType


class ModelHandler(ModelHandlerInterface):
    def __init__(self, filter_handler: FilterHandler):
        """
        Initializes the ModelHandler with environment-specific settings for hosting addresses
        and predefined classification routes based on model types.
        """
        self.host_js = os.getenv("HOST_JS", "sv-inferencia-js")
        self.host_python = os.getenv("HOST_PYTHON", "sv-inferencia-python")
        self.classification_routes = {
            ModelType.TENSORJS: f"ws://{self.host_js}:7987",
            ModelType.KERAS: f"ws://{self.host_python}:9999/inference",
        }
        self.loaded_model_type = None
        self.filter_handler = filter_handler

    def load_model_type(self, model_type) -> None:
        """
        Loads the specified model type into the handler.

        Args:
            model_type (ModelType): The type of model to be loaded.
        """
        self.loaded_model_type = model_type
        self.filter_handler.load_filters()

    def get_classification_route(self) -> str:
        """
        Retrieves the WebSocket classification route for the loaded model type.

        Returns:
            str: The classification route URL.

        Raises:
            ValueError: If no model type is loaded.
        """
        if self.loaded_model_type is None:
            raise ValueError("Modelo não carregado.")
        return self.classification_routes[self.loaded_model_type]

    def check_is_local_model(self) -> bool:
        """
        Checks if the loaded model type is a local (TensorJS) model.

        Returns:
            bool: True if the model is local, False otherwise.
        """
        return self.loaded_model_type == ModelType.TENSORJS
