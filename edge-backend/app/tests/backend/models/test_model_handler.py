import os
import unittest
from unittest.mock import MagicMock

from app.backend.models.ModelHandler import ModelHandler
from app.backend.models.ModelType import ModelType

filter_mock = MagicMock()
filter_mock.return_value = True
filter_mock.recipe_path = ""


class TestModelHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ModelHandler(filter_mock)

    def test_get_classification_route_tensorjs(self):
        self.handler.loaded_model_type = ModelType.TENSORJS
        expected_route = f"ws://{os.getenv('HOST_JS', 'sv-inferencia-js')}:7987"
        self.assertEqual(self.handler.get_classification_route(), expected_route)

    def test_get_classification_route_keras(self):
        self.handler.loaded_model_type = ModelType.KERAS
        expected_route = (
            f"ws://{os.getenv('HOST_PYTHON', 'sv-inferencia-python')}:9999/inference"
        )
        self.assertEqual(self.handler.get_classification_route(), expected_route)

    def test_check_is_local_model_true(self):
        self.handler.loaded_model_type = ModelType.TENSORJS
        self.assertTrue(self.handler.check_is_local_model())

    def test_check_is_local_model_false(self):
        self.handler.loaded_model_type = ModelType.KERAS
        self.assertFalse(self.handler.check_is_local_model())


if __name__ == "__main__":
    unittest.main()
