import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.backend.models.Crop import CropDataModel, GlobalCropData
from app.dependencies import get_db
from app.main import app  # assuming 'main' is the entry point for the FastAPI app
from app.routes.Crop import router


class TestCrop(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db_mock = MagicMock()
        app.dependency_overrides[get_db] = lambda: self.db_mock

    def tearDown(self):
        app.dependency_overrides = {}

    @patch("app.backend.models.Crop.GlobalCropData.set_coordinates")
    @patch(
        "app.backend.models.Crop.GlobalCropData.get_coordinates",
        return_value={"x": 0, "y": 0, "width": 100, "height": 100},
    )
    @patch("app.utils.interface_log")
    def test_video_crop_definitions(
        self, mock_interface_log, mock_get_coordinates, mock_set_coordinates
    ):
        crop_data = {"x": 0, "y": 0, "width": 100, "height": 100}
        response = self.client.post("/crop/", json=crop_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Coordinates", response.text)
        mock_set_coordinates.assert_called_once_with(crop_data)
        mock_get_coordinates.assert_called_once()
        # mock_interface_log.assert_called_once()


if __name__ == "__main__":
    unittest.main()
