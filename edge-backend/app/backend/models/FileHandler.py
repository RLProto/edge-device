import os
import shutil
import zipfile

from app.utils import model_handler

from .ModelType import ModelType


class InvalidFileTypeError(Exception):
    """Exception raised for invalid file types."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ModelTypeNotSupportedError(Exception):
    """Exception raised when the model type is not supported."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileHandler:
    def __init__(self):
        """
        Initializes the FileHandler with paths for temporary storage and converted models, and
        specifies files to extract based on the model type.
        """
        self.temp_dir = "app/core/data/temp_files"
        self.model_name = None
        self.extract_files = {
            ModelType.TENSORJS: [
                "model.json",
                "model.weights.bin",
                "parameters.json",
                # "recipe.json",
            ],
            ModelType.KERAS: [
                "classes.txt",
                "models/inference/model_inference.tflite",
                # "recipe.json",
            ],
        }
        self._initialize_temp_dir()
        self._check_model_loaded()

    def _initialize_temp_dir(self) -> None:
        os.makedirs(self.temp_dir, exist_ok=True)

    def _check_model_loaded(self) -> None:
        folder_temp_filenames = os.listdir(self.temp_dir)
        for filename in folder_temp_filenames:
            if ".zip" in filename:
                self._set_model_path(filename)
                model_type = self._identify_model_type()
                self._set_model_type(model_type)

    def setup_environment(self) -> None:
        """
        Prepares the environment by ensuring the temporary directory exists and is empty.
        """
        self._erase_old_files()
        os.makedirs(self.temp_dir, exist_ok=True)

    def _erase_old_files(self) -> None:
        """
        Erase all unused files from temporary directory
        """
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        self.model_name = None

    async def save_uploaded_zip(self, file) -> None:
        """
        Asynchronously saves an uploaded zip file to the temporary file path.

        Args:
            file (UploadFile): The file object to be saved.
        """
        self._set_model_path(file.filename)
        with open(self.temp_file_path, "wb") as temp_file:
            contents = await file.read()
            temp_file.write(contents)

    def _set_model_path(self, filename) -> None:
        """
        Initializes the full path for temporary file storage based on predefined directory and model name.
        """
        self.model_name = filename
        self.temp_file_path = os.path.join(self.temp_dir, self.model_name)

    def extract_model_files(self) -> None:
        """
        Extracts specific model files from an uploaded zip file and determines the model type.

        Returns:
            ModelType: The type of the model deduced from the files.
        """
        model_type = self._identify_model_type()
        self._set_model_type(model_type)
        with zipfile.ZipFile(self.temp_file_path, "r") as zip_ref:
            for filename in self.extract_files[model_handler.loaded_model_type]:
                zip_ref.extract(filename, self.temp_dir)

    def _set_model_type(self, model_type) -> None:
        model_handler.load_model_type(model_type)

    def _identify_model_type(self) -> ModelType:
        """
        Identifies the model type based on the filenames present in the zip file.

        Returns:
            ModelType: The type of model based on the files found.

        Raises:
            ModelTypeNotSupportedError: If the model type is unsupported.
        """
        with zipfile.ZipFile(self.temp_file_path, "r") as zip_ref:
            zip_file_names = zip_ref.namelist()
            for model_type, file_list in self.extract_files.items():
                if any(filename in zip_file_names for filename in file_list):
                    return model_type
            self._erase_old_files()
            raise ModelTypeNotSupportedError(
                "Tipo de modelo não suportado. Não treinado no Soda Vision."
            )

    def validate_zip_file(self, file) -> bool:
        """
        Validates that the provided file is a zip file based on its filename.

        Args:
            file (UploadFile): The file object to be validated.

        Returns:
            bool: True if the file is a valid zip file, False otherwise.

        Raises:
            InvalidFileTypeError: If the file is not a zip file.
        """
        if not file.filename.endswith(".zip"):
            raise InvalidFileTypeError(
                f"Tipo de arquivo invalido. '{file.filename}'. Apenas .zip são aceitos."
            )
        return True
