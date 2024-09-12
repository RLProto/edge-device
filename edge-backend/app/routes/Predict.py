from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.backend.models.Predictor import Predictor
from app.dependencies import get_db

router = APIRouter(tags=["Prediction"])

predictor = Predictor()


# Endpoint para receber o sinal do Node-RED
@router.post("/continuous-inference")
async def start_process(request: Request, db: Session = Depends(get_db)):
    response = await predictor.continuous_inference(request, db)
    return response


@router.get("/inference-now")
async def predict_now(db: Session = Depends(get_db)):
    response = await predictor.infere_now(db)
    return response


@router.websocket("/predict")
async def predict(websocket: WebSocket):
    """
    WebSocket endpoint to handle continuous prediction requests, sending frame data, receiving predictions,
    and communicating results back to the client.

    Args:
        websocket (WebSocket): The WebSocket connection with the client.
        db (Session): Database session dependency injected by FastAPI.

    Handles:
        WebSocketDisconnect: Closes the connection gracefully on client disconnect.
        Exception: Closes the WebSocket with an error if other exceptions occur.
    """
    await websocket.accept()
    predictor.add_clients(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        predictor.remove_clients(websocket)
        print("WebSocket desconectado")
    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        predictor.remove_clients(websocket)
        await websocket.close(code=1006, reason="Erro na conexão WebSocket")
