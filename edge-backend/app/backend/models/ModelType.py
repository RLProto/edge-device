from enum import Enum


class ModelType(Enum):
    """
    Enumerates types of models supported in the system, providing a way to handle different model types consistently.
    """

    TENSORJS = "TensorFlow.js"
    KERAS = "Tflite"
