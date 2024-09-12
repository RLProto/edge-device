import base64
from io import BytesIO

import numpy as np
from PIL import Image

from app.model.inference_model import InferenceModel
from app.services.validator.model_validator import ModelValidator


class InferenceModelCloud:

    def __init__(self, model_tflite, classes):
        self.classes = classes
        self.model_tflite = model_tflite

    async def predict(self, data) -> InferenceModel:
        image_data = base64.b64decode(data)
        image_file = BytesIO(image_data)

        ModelValidator.validate_image_data(image_file)
        ModelValidator.validate_model_loaded(image_file)
        interpreter, input_details, output_details = self.model_tflite
        input_shape = input_details[0]["shape"]

        image = Image.open(image_file).resize((input_shape[1], input_shape[2]))
        image_array = np.array(image, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=0)

        interpreter.set_tensor(input_details[0]["index"], image_array)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])

        class_index = np.argmax(output_data)
        accuracy = round(output_data[0][class_index] * 100, 2)
        prediction = self.classes[class_index]

        response = InferenceModel(
            prediction=prediction,
            accuracy=accuracy,
        )
        return response
