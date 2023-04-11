from typing import Union

from fastapi import FastAPI,HTTPException

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from .models.version import Version

app = FastAPI()

cred = credentials.Certificate('./ihmpolytech-15b17-firebase-adminsdk-xhoym-6f6672a5ab.json')

firebase_admin.initialize_app(cred)
db = firestore.client()


@app.get("/")
def read_root():
    return {"Hello": "World"}

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