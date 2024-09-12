from sqlalchemy.orm import Session

from . import models, schemas


def create_inference_log(
    db: Session, Inferencia: schemas.Inferencia
) -> models.Inferencia:
    """
    Creates a log entry for an inference in the database.

    Args:
        db (Session): The database session.
        Inferencia (schemas.Inferencia): The inference data.

    Returns:
        models.Inferencia: The created database entry.
    """
    db_inference = models.Inferencia(
        class_predicted=Inferencia["classification"],
        accuracy_predicted=Inferencia["confidence-score"],
    )
    db.add(db_inference)
    db.commit()
    db.refresh(db_inference)
    return db_inference


def create_interface_log(db: Session, Interface: schemas.Interface) -> models.Interface:
    """
    Creates a log entry for a user interface interaction in the database.

    Args:
        db (Session): The database session.
        Interface (schemas.Interface): The interface interaction data.

    Returns:
        models.Interface: The created database entry.
    """
    db_interface_click = models.Interface(**Interface)
    db.add(db_interface_click)
    db.commit()
    db.refresh(db_interface_click)
    return db_interface_click
