import firebase_admin
from firebase_admin import firestore, credentials
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDZ609tpVpSrWfOKVHVoyo9DK8dbYqAtRE",
    "authDomain": "likutil.firebaseapp.com",
    "projectId": "likutil",
    "storageBucket": "likutil.firebasestorage.app",
    "messagingSenderId": "314662541049",
    "appId": "1:314662541049:web:9e6efa3430e1be4f47f428",
    "measurementId": "G-VYRKS8Z4EX",
}

# Initialize Firebase Admin SDK using programmatic credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": firebaseConfig["projectId"]})
db = firestore.client()

# Prepare the user data
user_data = {
    "createdAt": datetime.utcnow().isoformat(),
    "lastLogin": datetime.utcnow().isoformat(),
    "storeUrl": "example.com",  # Replace with actual store URL if available
    "consumerKey": 'data.consumer_key',
    "consumerSecret": 'data.consumer_secret',
    "userId": 'data.user_id',
    "key_permissions": 'data.key_permissions',
    "key_id": 'data.key_id',
}

# Save to Firestore in 'users' collection
db.collection("users").document('data.key_id').set(user_data)


# if __name__ == "__main__":
#     uvicorn.run(
#         "api.index:app",
#         host="0.0.0.0",
#         port=8001 if debug_mode else 8000,
#         reload=debug_mode,
#     )

