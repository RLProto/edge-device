from threading import Thread

from fastapi import Depends
from sqlalchemy.orm import Session

from app.backend.models.FilterHandler import FilterHandler
from app.backend.models.FilterProcessor import FilterProcessor
from app.backend.models.ModelHandler import ModelHandler
from app.backend.models.PredictFilter import PredictFilter
from app.backend.models.VideoStream import Stream
from app.dependencies import get_db
from app.sql_app import crud

filter_handler = FilterHandler(recipe_path="app/core/data/recipe.json")
filter_processor = FilterProcessor(filter_handler=filter_handler)
stream = Stream(filter_processor=filter_processor)
filter = PredictFilter()
model_handler = ModelHandler(filter_handler)


def start_system():
    camera = Thread(target=stream.run_camera_stream)
    camera.start()


def stop_stream():
    stream.shutdown_camera()


def interface_log(command: str, db: Session = Depends(get_db)):
    log = {"command": command}
    crud.create_interface_log(db, log)


def inference_log(command: str, db: Session = Depends(get_db)):
    crud.create_inference_log(db, command)
