import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.backend.models.PredictFilter import FilterDataModel
from app.dependencies import get_db
from app.main import app  # assuming 'main' is the entry point for the FastAPI app
from app.utils import filter


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db_mock = MagicMock()
        app.dependency_overrides[get_db] = lambda: self.db_mock

    def tearDown(self):
        app.dependency_overrides = {}

    @patch("app.backend.models.PredictFilter.PredictFilter.set_filter")
    @patch("app.backend.models.PredictFilter.PredictFilter.get_filter")
    def test_change_filter(self, mock_get_filter, mock_set_filter):
        filter_data = {"filter_value": 10}
        mock_get_filter.return_value = filter_data
        response = self.client.post("/filter/", json=filter_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Filtro definido como", response.text)
        mock_set_filter.assert_called_once_with(filter_data)
        mock_get_filter.assert_called_once()


if __name__ == "__main__":
    unittest.main()
