import unittest
from unittest.mock import Mock, patch

import cv2
import numpy as np

from app.backend.models.FilterProcessor import FilterProcessor
from app.backend.models.VideoStream import Stream


class TestStream(unittest.TestCase):
    def setUp(self):
        self.mock_filter_processor = Mock(spec=FilterProcessor)
        self.stream = Stream(self.mock_filter_processor)

    def test_stream_initialization(self):
        self.assertFalse(self.stream.status)
        self.assertIsNone(self.stream.frame)
        self.assertIsNone(self.stream.buffer)
        self.assertIsNone(self.stream.predict_image)
        self.assertIsInstance(self.stream.filter_processor, FilterProcessor)

    @patch("cv2.VideoCapture")
    def test_setup_cam(self, mock_video_capture):
        self.stream.setup_cam()
        mock_video_capture.assert_called_once_with(0)

    def test_check_camera_success(self):
        self.stream.camera = Mock()
        self.stream.camera.isOpened.return_value = True
        self.stream.check_camera()  # Should not raise an exception

    def test_check_camera_failure(self):
        self.stream.camera = Mock()
        self.stream.camera.isOpened.return_value = False
        with self.assertRaises(RuntimeError):
            self.stream.check_camera()

    def test_set_status(self):
        self.stream.set_status(True)
        self.assertTrue(self.stream.status)
        self.stream.set_status(False)
        self.assertFalse(self.stream.status)

    def test_while_status(self):
        self.stream.status = True
        self.assertTrue(self.stream.while_status())
        self.stream.status = False
        self.assertFalse(self.stream.while_status())

    def test_shutdown_camera(self):
        self.stream.camera = Mock()
        self.stream.shutdown_camera()
        self.stream.camera.release.assert_called_once()

    @patch("cv2.imencode")
    def test_get_frame(self, mock_imencode):
        mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.stream.frame = mock_frame
        self.stream.filter_processor.apply_crop_predict_image.return_value = mock_frame
        mock_imencode.return_value = (True, b"mock_encoded_image")

        result = self.stream.get_frame()

        self.stream.filter_processor.apply_crop_predict_image.assert_called_once_with(
            mock_frame
        )
        mock_imencode.assert_called_once_with(".jpg", mock_frame)
        self.assertIsInstance(result, str)

    @patch("cv2.imencode")
    def test_generate_frames(self, mock_imencode):
        mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.stream.camera = Mock()
        self.stream.camera.read.return_value = (True, mock_frame)
        self.stream.filter_processor.apply_black_edges.return_value = mock_frame
        self.stream.filter_processor.apply_filters.return_value = mock_frame

        # Create a mock numpy array that has a tobytes method
        mock_buffer = Mock()
        mock_buffer.tobytes.return_value = b"mock_encoded_image"

        mock_imencode.return_value = (True, mock_buffer)

        generator = self.stream.generate_frames()
        frame = next(generator)

        self.assertTrue(self.stream.status)
        self.assertIsInstance(frame, bytes)
        self.assertTrue(
            frame.startswith(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n")
        )
        self.assertTrue(frame.endswith(b"\r\n\r\n"))
        self.assertIn(b"mock_encoded_image", frame)

        # Verify that the mock methods were called
        self.stream.camera.read.assert_called_once()
        self.stream.filter_processor.apply_black_edges.assert_called_once_with(
            mock_frame
        )
        self.stream.filter_processor.apply_filters.assert_called_once_with(mock_frame)
        mock_imencode.assert_called_once_with(".jpg", mock_frame)
        mock_buffer.tobytes.assert_called_once()

    def test_generate_frames_failure(self):
        self.stream.camera = Mock()
        self.stream.camera.read.return_value = (False, None)

        generator = self.stream.generate_frames()
        with self.assertRaises(StopIteration):
            for _ in range(11):  # More than the consecutive error limit
                next(generator)


if __name__ == "__main__":
    unittest.main()
