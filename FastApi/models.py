from pydantic import BaseModel
from typing import Literal

class PredictInput(BaseModel):
    category: str
    day_of_week: str

class LocationPredictionOutput(BaseModel):
    latitude: float
    longitude: float
    unit: Literal["degrees"] = "degrees"

class TemperaturePredictionOutput(BaseModel):
    prediction: float
    unit: Literal["degrees Celsius"] = "degrees Celsius"