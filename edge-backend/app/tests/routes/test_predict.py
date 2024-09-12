# import json
# from unittest.mock import AsyncMock, MagicMock, patch

# import pytest
# from fastapi import WebSocket
# from fastapi.testclient import TestClient

# from app.backend.models.OPC import OPCUA
# from app.routes.Model import model_handler
# from app.routes.Predict import get_predictions, router
# from app.sql_app import crud
# from app.utils import filter, stream


# @pytest.mark.asyncio
# async def test_get_predictions():
#     # Setup mocks and test data
#     mock_ws = AsyncMock()
#     mock_ws.recv = AsyncMock(
#         return_value=json.dumps({"label": "cat", "confidence": 0.95})
#     )
#     with patch(
#         "websockets.connect", new_callable=AsyncMock
#     ) as mock_websockets_connect, patch(
#         "app.utils.stream.get_frame", return_value=b"frame_data"
#     ) as mock_get_frame, patch(
#         "app.backend.models.PredictFilter.PredictFilter.compare_results",
#         return_value={"label": "cat", "confidence": 0.95},
#     ) as mock_compare_results:
#         mock_websockets_connect.return_value.__aenter__.return_value = mock_ws

#         result = await get_predictions(mock_ws)
#         assert result == {"label": "cat", "confidence": 0.95}
#         mock_get_frame.assert_called_once()
#         mock_ws.send.assert_called_once_with(b"frame_data")
#         mock_ws.recv.assert_called_once()
#         mock_compare_results.assert_called_once_with(
#             {"label": "cat", "confidence": 0.95}
#         )


# @pytest.mark.asyncio
# async def test_predict_websocket():
#     # Setup client and mocks
#     client = TestClient(router)
#     with patch(
#         "app.routes.Predict.get_predictions", new_callable=AsyncMock
#     ) as mock_get_predictions, patch(
#         "app.sql_app.crud.create_inference_log"
#     ) as mock_create_inference_log, patch(
#         "app.backend.models.OPC.OPCUA.send_values_OPC"
#     ) as mock_send_values_OPC, patch(
#         "app.routes.Model.model_handler.get_classification_route",
#         return_value="ws://localhost",
#     ) as mock_get_classification_route:
#         mock_get_predictions.return_value = {"label": "cat", "confidence": 0.95}
#         try:
#             with client.websocket_connect("/predict") as websocket:
#                 websocket.send_json({"frame": "data"})
#                 response = websocket.receive_json()
#                 assert response == {"label": "cat", "confidence": 0.95}
#                 mock_get_predictions.assert_called_once()
#                 mock_create_inference_log.assert_called_once()
#                 mock_send_values_OPC.assert_called_once()
#         except Exception as e:
#             print(f"An error occurred: {e}")
