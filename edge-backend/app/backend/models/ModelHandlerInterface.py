from abc import ABC, abstractmethod


class ModelHandlerInterface(ABC):
    """
    An interface to handle different model operations.
    This might include methods to load, process, and use various machine learning models.
    """

    @abstractmethod
    def load_model_type(self, model_type):
        """
        Abstract method to define actions to be taken once a model type is identified and loaded.
        :param model_type: Enum or identifier for the type of model loaded.
        """
        pass

    @abstractmethod
    def get_classification_route(self):
        """Get the network route for model classification based on the loaded model type."""
        pass

    @abstractmethod
    def check_is_local_model(self):
        """Check if the current model is local, influencing data processing strategies."""
        pass
