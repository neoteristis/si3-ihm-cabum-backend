from typing import Union

from fastapi import FastAPI,HTTPException

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from .models.version import Version

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
@app.get("/accident")
def read_accident():
    return {}

# Endpoint /accident : Get all accidents
@app.get("/accidents")
def read_accidents():
    return {}

# Endpoint /accident : Create an accident (return ID)
@app.post('/accident')
def create_accident():
    return {}

# Endpoint /accident : update an accident (all fields) by ID
@app.put('/accident')
def update_accident():
    return {}

# Endpoint /accident : delete an accident by ID
@app.delete('/accident')
def delete_accident():
    return {}

# Endpoint /accident : update an accident one or multiple fields by ID
@app.patch('/accident')
def patch_accident():
    return {}

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