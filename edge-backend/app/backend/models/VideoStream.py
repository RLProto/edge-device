import base64

import cv2
import numpy as np

from app.backend.models.FilterProcessor import FilterProcessor


class Stream:
    def __init__(self, filter_processor: FilterProcessor):
        """
        Initializes the video stream and sets up the camera for streaming.
        """
        self.status = False
        self.frame = None
        self.buffer = None
        self.predict_image = None
        self.setup_cam()
        self.filter_processor = filter_processor

    def run_camera_stream(self) -> None:
        """
        Runs the camera stream and handles frame generation and any runtime errors.
        """
        try:
            for frame in self.generate_frames():
                pass
        except RuntimeError:
            print("Erro na câmera, finalizando o stream.")
            self.shutdown_camera()

    def setup_cam(self) -> None:
        """
        Sets up the camera by initializing the video capture device.
        """
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def check_camera(self) -> None:
        """
        Checks if the camera is open and raises an error if it is not.
        Raises:
            RuntimeError: If the camera cannot be started.
        """
        if not self.camera.isOpened():
            raise RuntimeError("Could not start camera.")

    def generate_frames(self) -> bytes:
        self.check_camera()
        self.set_status(True)
        consecutive_errors = 0

        while True:
            try:
                success, self.frame = self.camera.read()
                if not success or self.frame is None:
                    print("Failed to capture frame or frame is None.")
                    consecutive_errors += 1
                    if consecutive_errors > 10:
                        break
                    continue
                consecutive_errors = 0
                #self.frame = self.filter_processor.apply_black_edges(self.frame)
                #self.frame = self.filter_processor.apply_filters(self.frame)

                if not isinstance(self.frame, np.ndarray) or self.frame.size == 0:
                    print(
                        f"Invalid frame after processing: {type(self.frame)}, size: {self.frame.size}"
                    )
                    consecutive_errors += 1
                    if consecutive_errors > 5:
                        break
                    continue

                ret, self.buffer = cv2.imencode(".jpg", self.frame)
                if not ret or self.buffer is None:
                    print("Failed to encode frame to JPEG.")
                    consecutive_errors += 1
                    if consecutive_errors > 5:
                        break
                    continue

                consecutive_errors = 0
            except Exception as e:
                print(f"Error processing frame: {e}")
                consecutive_errors += 1
                if consecutive_errors > 5:
                    break
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + self.buffer.tobytes()
                + b"\r\n\r\n"
            )

    def shutdown_camera(self) -> None:
        """
        Shuts down the camera by releasing the video capture device.
        """
        self.camera.release()

    def set_status(self, status) -> None:
        """
        Sets the status of the stream.

        Args:
            status (bool): The new status of the stream.
        """
        self.status = status

    def while_status(self) -> bool:
        """
        Returns the current status of the stream.

        Returns:
            bool: The current streaming status.
        """
        return self.status

    def get_frame(self) -> str:
        """
        Returns the current frame encoded in base64 format.

        Returns:
            str: The current frame as a base64 encoded string.
        """
        array_frame = self.filter_processor.apply_crop_predict_image(self.frame)
        ret, self.predict_image = cv2.imencode(".jpg", self.frame)
        return self._convert_frame()

    def _convert_frame(self) -> str:
        """
        Converts the current frame to base64 format.

        Returns:
            str: The base64 encoded string of the current frame.
        """
        return base64.b64encode(self.predict_image).decode("utf-8")