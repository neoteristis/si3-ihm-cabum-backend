from typing import Union

from fastapi import FastAPI,HTTPException

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel

from .models.version import Version

class Accident(BaseModel):
    accidentType:str
    description:str
    image:str
    latitude:float
    longitude:float


description = """
IHMWebService API helps you do store details about incident. 🚀
"""

app = FastAPI(title="IHMWebServiceApp",
    description=description,
    version="0.0.1")

cred = credentials.Certificate('./ihmpolytech-15b17-firebase-adminsdk-xhoym-6f6672a5ab.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

# Endpoint / : Contains only a hello world
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Endpoint /accident : Get an accident by this ID
@app.get("/accident/{id}")
def read_accident(id:int):
    return {
        
    }

# Endpoint /accidents : Get all accidents
# - query parameter accidentType allow us to filter wich type of accident we want
@app.get("/accidents")
def read_accidents(accidentType:str = None):
    return {
        
    }

# Endpoint /accident : Create an accident (return ID)
@app.post('/accident')
def create_accident(accident:Accident):
    accident_item = {
        u'accidentType': accident.accidentType,
        u'description': accident.description,
        u'image': accident.image,
        u'latitude': accident.latitude,
        u'longitude': accident.longitude
    }
    update_time, id = db.collection(u'accidents').add(accident_item)
    return {"accident_id":id}

# Endpoint /accident : update an accident (all fields) by ID
@app.put('/accident/{id}')
def update_accident(id:str,accidentType:str,description:str,image:str,latitude:float,longitude:float):
    doc = db.collection(u'accidents').document(id)
    if doc.exists:
        accident = {
            u'accidentType': accidentType,
            u'description': description,
            u'image': image,
            u'latitude': latitude,
            u'longitude': longitude
        }
        doc.set(accident)
        return {}
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

# Endpoint /accident : delete an accident by ID
@app.delete('/accident/{id}')
def delete_accident(id:str):
    doc = db.collection(u'accidents').document(id)
    if doc.exists:
        doc.delete()
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

# Endpoint /accident : update an accident one or multiple fields by ID
@app.patch('/accident/{id}')
def patch_accident(id:str,accidentType:str=None,description:str=None,image:str=None,latitude:float=None,longitude:float=None):
    doc = db.collection(u'accidents').document(id)
    if doc.exists:
        if accidentType != None :
            doc.set({
                u'accidentType' : accidentType
            })
        if description != None :
            doc.set({
                u'description' : description
            })
        if image != None :
            doc.set({
                u'image' : image
            })
        if latitude != None :
            doc.set({
                u'latitude' : latitude
            })
        if longitude != None :
            doc.set({
                u'longitude' : longitude
            })
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

@app.get("/about")
def read_about():
    doc_ref = db.collection(u'about').document(u'MW1ID0klidAoWN7tVJK4')
    doc = doc_ref.get()
    if doc.exists:
        version = Version.from_dict(doc.to_dict())
        return {
            "name" : version.name,
            "version" : version.version
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")