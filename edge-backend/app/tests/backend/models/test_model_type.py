import unittest

from app.backend.models.ModelType import ModelType


class TestModelType(unittest.TestCase):
    def test_model_type(self):
        self.assertEqual(ModelType.TENSORJS.value, "TensorFlow.js")
        self.assertEqual(ModelType.KERAS.value, "Tflite")


if __name__ == "__main__":
    unittest.main()
