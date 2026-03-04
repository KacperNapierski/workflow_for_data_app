from pydantic import BaseModel
from typing import Optional

class LungCancer(BaseModel):
    id: Optional[int] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    smoking: Optional[bool] = None
    yellow_fingers: Optional[bool] = None
    anxiety: Optional[bool] = None
    peer_pressure: Optional[bool] = None
    chronic_disease: Optional[bool] = None
    fatigue: Optional[bool] = None
    allergy: Optional[bool] = None
    wheezing: Optional[bool] = None
    alcohol_consuming: Optional[bool] = None
    coughing: Optional[bool] = None
    shortness_of_breath: Optional[bool] = None
    swallowing_difficulty: Optional[bool] = None
    chest_pain: Optional[bool] = None
    lung_cancer: Optional[bool] = None

    #class Config:
    #    orm_mode = True