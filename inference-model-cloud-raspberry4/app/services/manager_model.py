import os

import tflite_runtime.interpreter as tflite

MODEL_PATH = os.getenv("MODEL_PATH", "")


class ManagerModel:
    def __init__(self):
        self.model_tflite_file_name = "model_inference.tflite"
        self.classes_file_name = "classes.txt"
        self.path_model_in_zip = "models/inference/"
        self.classes_path = os.path.join(MODEL_PATH, self.classes_file_name)
        self.model_path = os.path.join(
            MODEL_PATH, self.path_model_in_zip, self.model_tflite_file_name
        )

    def get_model(self):
        if os.path.exists(self.model_path) and os.path.getsize(self.model_path) > 0:
            self.model = self.get_format_tflite_model(self.model_path)
            return self.model
        else:
            print(f"Erro: Arquivo do modelo não existe ou está vazio.")
            return None

    def get_classes(self):
        with open(self.classes_path, "r") as file:
            linhas = file.readlines()
        classes = [linha.strip() for linha in linhas]
        return classes

    def get_format_tflite_model(self, model_path):
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        return interpreter, input_details, output_details
