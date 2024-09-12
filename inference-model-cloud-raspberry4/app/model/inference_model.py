from pydantic import BaseModel, Field


class InferenceModel(BaseModel):
    prediction: str = Field(..., alias="classification")
    accuracy: float = Field(..., alias="confidence-score")

    class Config:
        populate_by_name = True
