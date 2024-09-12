from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .db_manager import Base


class Inferencia(Base):
    """
    Represents an inference log in the database.

    Attributes:
        id (Integer): The primary key.
        accuracy_predicted (String): The predicted accuracy as a string.
        class_predicted (String): The predicted class.
        created_at (DateTime): Timestamp of when the record was created, set automatically.
    """

    __tablename__ = "logsinferencia"

    id = Column(Integer, primary_key=True)
    accuracy_predicted = Column(String)
    class_predicted = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Interface(Base):
    """
    Represents a user interface interaction log in the database.

    Attributes:
        id (Integer): The primary key.
        command (String): The command or action taken by the user.
        created_at (DateTime): Timestamp of when the record was created, set automatically.
    """

    __tablename__ = "logsinterface"

    id = Column(Integer, primary_key=True)
    command = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
