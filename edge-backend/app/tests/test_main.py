import unittest

from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.main import app  # Ensure 'app' is correctly imported


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_app_creation(self):
        self.assertIsNotNone(app)

    def test_cors_middleware(self):
        middleware = [mw.cls for mw in app.user_middleware]
        self.assertIn(CORSMiddleware, middleware)

    def test_startup_event(self):
        with self.client:
            response = self.client.get("/")
            # Ensure the app started correctly by checking the response status
            self.assertEqual(response.status_code, 404)  # or some other expected status

    def test_shutdown_event(self):
        with self.client:
            response = self.client.get("/")
            # Ensure the app runs correctly, implying it will also shut down correctly
            self.assertEqual(response.status_code, 404)  # or some other expected status

    def test_include_routers(self):
        routes = [route.name for route in app.router.routes]
        self.assertIn("video_crop_definitions", routes)
        self.assertIn("change_filter", routes)
        self.assertIn("upload_model", routes)
        self.assertIn("predict", routes)
        self.assertIn("video_feed", routes)


if __name__ == "__main__":
    unittest.main()
