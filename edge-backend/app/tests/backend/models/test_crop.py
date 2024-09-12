import unittest

from app.backend.models.Crop import CropDataModel, GlobalCropData


class TestCropDataModel(unittest.TestCase):
    def test_create_model(self):
        model = CropDataModel(x=10, y=20, width=30, height=40)
        self.assertEqual(model.x, 10)
        self.assertEqual(model.y, 20)
        self.assertEqual(model.width, 30)
        self.assertEqual(model.height, 40)


class TestGlobalCropData(unittest.TestCase):
    def test_set_coordinates(self):
        new_data = {"x": 50, "y": 60, "width": 70, "height": 80}
        GlobalCropData.set_coordinates(new_data)
        coords = GlobalCropData.get_coordinates()
        self.assertEqual(coords["x"], 50)
        self.assertEqual(coords["y"], 60)
        self.assertEqual(coords["width"], 70)
        self.assertEqual(coords["height"], 80)

    def test_get_coordinates_default(self):
        coords = GlobalCropData.get_coordinates()
        self.assertEqual(coords["x"], 0.0)
        self.assertEqual(coords["y"], 0.0)
        self.assertEqual(coords["width"], 400.0)
        self.assertEqual(coords["height"], 400.0)


if __name__ == "__main__":
    unittest.main()
