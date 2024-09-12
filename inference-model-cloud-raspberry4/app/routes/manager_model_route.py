from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from app.model.inference_model import InferenceModel
from app.services.inference_model_cloud import InferenceModelCloud
from app.services.manager_model import ManagerModel

router = APIRouter(tags=["Manager Model Cloud"])

manager_model_instance = ManagerModel()
model_inference = None


def get_manager_model() -> ManagerModel:
    return manager_model_instance


@router.websocket("/inference")
async def predict(
    websocket: WebSocket, manager_model: ManagerModel = Depends(get_manager_model)
):
    await websocket.accept()
    try:
        global model_inference
        model_inference = InferenceModelCloud(
            manager_model.get_model(), manager_model.get_classes()
        )
        while True:
            data = await websocket.receive_text()
            response: InferenceModel = await model_inference.predict(data)
            await websocket.send_text(response.model_dump_json(by_alias=True))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
