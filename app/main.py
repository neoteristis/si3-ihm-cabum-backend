from typing import Union

from fastapi import FastAPI,HTTPException,Body
from google.cloud.firestore_v1.field_path import FieldPath
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from .models.version import Version
from .models.accident import Accident

from .utils import haversine

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
def read_accident(id:str):
    doc_ref = db.collection('accidents').document(id)
    doc = doc_ref.get()
    if doc.exists:
        return {"accident" : doc.to_dict()}
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

# Endpoint /accidents : Get all accidents
# - query parameter accidentType allow us to filter wich type of accident we want
# - query parameter latitude allow us to filter the distance of accident we want, only if latitude, longitude AND maxDistance are not null
# - query parameter longitude allow us to filter the distance of accident we want, only if latitude, longitude AND maxDistance are not null
# - query parameter distance allow us to filter the distance of accident we want, only if latitude, longitude AND maxDistance are not null
@app.get("/accident")
def read_accidents(accidentType: str = None, latitude: float = None, longitude: float = None, maxDistance: float = None):
    accidents_ref = db.collection('accidents')
    
    if accidentType :
        accidents_ref = accidents_ref.where("accidentType",'==',accidentType)
    
    results = []
    for doc in accidents_ref.stream():
        accident=doc.to_dict()
        accident["id"]=doc.id
        results.append(accident)
    
    if latitude and longitude and maxDistance :
        results = [result for result in results if haversine(latitude, longitude, result.get('latitude'), result.get('longitude')) <= maxDistance]
    
    return {'arrays': results}


# Endpoint /accident : Create an accident (return ID)
@app.post('/accident')
def create_accident(accident:Accident):
    accident_item = {
        'accidentType': accident.accidentType,
        'description': accident.description,
        'image': accident.image,
        'latitude': accident.latitude,
        'longitude': accident.longitude
    }
    if accident.accidentType and accident.description and accident.image and accident.latitude and accident.longitude :
        update_time, id = db.collection('accidents').add(accident_item)
        return {"id":id.id}
    else :
        raise HTTPException(status_code=422, detail="Accident not complete, we miss some parameter.")

# Endpoint /accident : update an accident (all fields) by ID
@app.put('/accident/{id}')
def update_accident(id:str,accidentType:str = Body(...),description:str = Body(...),image:str = Body(...),latitude:float = Body(...),longitude:float = Body(...)):
    if not accidentType or not description or not image or not latitude or not longitude :
        raise HTTPException(status_code=422, detail="We miss parameter here")
    else :
        doc_ref = db.collection('accidents').document(id)
        doc = doc_ref.get()
        if doc.exists:
            accident = {
                'accidentType': accidentType,
                'description': description,
                'image': image,
                'latitude': latitude,
                'longitude': longitude
            }
            doc_ref.update(accident)
            doc = doc_ref.get()
            return {"status" : "Success",
                "accident" : doc.to_dict()}
        else :
            raise HTTPException(status_code=404, detail="Accident not found")

# Endpoint /accident : delete an accident by ID
@app.delete('/accident/{id}')
def delete_accident(id:str):
    doc_ref = db.collection('accidents').document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return {
            "status" : "Deleted Succesfully"
        }
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

# Endpoint /accident : update an accident one or multiple fields by ID
@app.patch('/accident/{id}')
def patch_accident(id:str, accidentType:str = Body(None), description:str = Body(None), image: str= Body(None), latitude:float=Body(None),longitude:float=Body(None)):
    doc_ref = db.collection('accidents').document(id)
    doc = doc_ref.get()
    if doc.exists:
        if accidentType :
            doc_ref.update({
                u'accidentType' : accidentType
            })
        if description :
            doc_ref.update({
                u'description' : description
            })
        if image :
            doc_ref.update({
                u'image' : image
            })
        if latitude :
            doc_ref.update({
                u'latitude' : latitude
            })
        if longitude :
            doc_ref.update({
                u'longitude' : longitude
            })
        doc = doc_ref.get()
        return {"status" : "Success",
                "accident" : doc.to_dict()}
    else :
        raise HTTPException(status_code=404, detail="Accident not found")

@app.get("/about")
def read_all_about():
    doc_ref = db.collection(u'about')
    results = []
    for doc in doc_ref.stream():
        version = doc.to_dict()
        results.append({
            "id" : doc.id,
            "name" : version["name"],
            "version" : version["version"],
            "last" : version["last"]
        })
    return {"arrays" : results}
    
@app.get('/about/{id}')
def read_about(id:str):
    doc_ref = db.collection(u'about').document(id)
    doc = doc_ref.get()
    if doc.exists:
        version = doc.to_dict()
        return {
            "id" : doc.id,
            "name" : version["name"],
            "version" : version["version"],
            "last" : version["last"]
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.delete('/about/{id}')
def delete_accident(id:str):
    doc_ref = db.collection('about').document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return {
            "status" : "Deleted Succesfully"
        }
    else :
        raise HTTPException(status_code=404, detail="About not found")
    
@app.post('/about')
def create_accident(version:Version):
    version_item = {
        "name" : version.name,
        "version" : version.version,
        "last" : version.last
    }
    if version.name and version.version and version.last :
        update_time, id = db.collection('about').add(version_item)
        return {"id":id.id}
    else :
        raise HTTPException(status_code=422, detail="Version not complete, we miss some parameter.")
    
@app.put('/about/{id}')
def update_accident(id:str,name:str = Body(...),version:str = Body(...),last:bool = Body(...)):
    if not name or not version or not last:
        raise HTTPException(status_code=422, detail="We miss parameter here")
    else :
        doc_ref = db.collection('about').document(id)
        doc = doc_ref.get()
        if doc.exists:
            version = {
                "name" : name,
                "version" : version,
                "last" : last
            }
            doc_ref.update(version)
            doc = doc_ref.get()
            return {"status" : "Success",
                "accident" : doc.to_dict()}
        else :
            raise HTTPException(status_code=404, detail="Version not found")