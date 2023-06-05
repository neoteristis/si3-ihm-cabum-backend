from pydantic import BaseModel

class FCM(BaseModel):
    token:str
    
class FCMTest(BaseModel):
    title:str
    body:str
    token:str