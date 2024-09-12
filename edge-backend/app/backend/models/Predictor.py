import asyncio
import json
from typing import Dict
import time
import websockets
from app.backend.models.OPC import OPCUA
from app.backend.models.StatusHandler import StatusHandler
from app.routes.Model import model_handler
from app.utils import filter, inference_log, stream


class Predictor:
    def __init__(self):
        self.opcua = OPCUA()
        self.status_handler = StatusHandler()
        self.connected_clients = []
        self.task = None

    async def infere_now(self, db):
        if self.status_handler.able_to_infere:
            inference = await self._infere_and_save(db)
            return inference
        return {"Error": "Process already running continuouslly"}

    async def continuous_inference(self, request, db):
        data = await request.json()
        self.status_handler.set_status(data)
        if self.status_handler.continuous_status:
            if self.status_handler.check_process_running_status():
                return {"message": "Process already running"}
            self.task = asyncio.create_task(self._process_data(db))
            self.status_handler.set_last_status()
            return {"message": "Process started"}
        self.status_handler.set_last_status()
        try:
            self.task.cancel()
        finally:
            return {"message": "Process stoped"}

    async def _process_data(self, db):
        while self.status_handler.continuous_status:
            inference = await self._infere_and_save(db)
            for client in self.connected_clients:
                await client.send_json(inference)
            await asyncio.sleep(0.57) 

    async def _infere_and_save(self, db):
        inference = await self._execute_inferece()
        await self._save_result(inference, db)
        return inference

    async def _execute_inferece(self):
        async with websockets.connect(
            model_handler.get_classification_route()
        ) as API_inference:
            return await self._get_predictions(API_inference)

    async def _save_result(self, result, db):
        inference_log(result, db)
        await self.opcua.send_values_OPC(result)

    async def _get_predictions(self, API_inference) -> Dict[str, float]:
        """
        Retrieves predictions for the current video frame from the model inference API.

        Args:
            API_inference (websockets.WebSocketClientProtocol): The WebSocket client connected to the model API.

        Returns:
            dict: The filtered prediction results.
        """
        
        await API_inference.send(stream.get_frame())
        response = await API_inference.recv()
        predictions = json.loads(response)
        
        try:
            async with websockets.connect("ws://saveimage:8000/ws/image") as send_image:
                await send_image.send(stream.get_frame())
        except Exception as e:
            # Optionally, handle or log the exception silently here if needed
            print("erro ao conectar no websocket")        
            pass
        finally:
            # Perform any necessary cleanup here silently
            pass
        return filter.compare_results(predictions)
        
    def add_clients(self, websocket):
        self.connected_clients.append(websocket)

    def remove_clients(self, websocket):
        self.connected_clients.remove(websocket)
