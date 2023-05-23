from pydantic import BaseModel

class Accident(BaseModel):
    accidentType:str
    description:str
    image:str
    latitude:float
    longitude:float
    date:str
    numberOfApproval:int