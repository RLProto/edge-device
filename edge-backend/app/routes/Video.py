from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.backend.models.Crop import GlobalCropData
from app.utils import stream

router = APIRouter(tags=["Video"])


@router.get("/video")
def video_feed() -> StreamingResponse:
    """
    Streams video frames to the client using multipart streaming response.

    Returns:
        StreamingResponse: A streaming response that continuously sends video frames to the client.
    """
    GlobalCropData.set_base_coordinates()
    return StreamingResponse(
        stream.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )
