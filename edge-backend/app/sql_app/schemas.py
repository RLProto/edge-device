from datetime import datetime

from pydantic import BaseModel


class LogBase(BaseModel):
    """
    Base model for log entries, providing a common attribute for the creation timestamp.

    Attributes:
        created_at (datetime): The timestamp when the log entry was created.
    """

    created_at: datetime


class Inferencia(LogBase):
    """
    Schema for inference log entries, extending the LogBase with specific inference details.

    Attributes:
        id (int): The primary key identifier.
        accuracy_predicted (str): The predicted accuracy as a string.
        class_predicted (str): The predicted class.
    """

    id: int
    accuracy_predicted: str
    class_predicted: str

    class ConfigDict:
        from_attributes = True


class Interface(LogBase):
    """
    Schema for interface interaction log entries, extending the LogBase with command details.

    Attributes:
        id (int): The primary key identifier.
        command (str): The command or action taken by the user.
    """

    id: int
    command: str

    class ConfigDict:
        from_attributes = True
