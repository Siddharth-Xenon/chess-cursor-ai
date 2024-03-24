import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Path to your Firebase Admin SDK private key file
# Make sure to replace 'path/to/your/firebase-private-key.json' with the actual path to your Firebase private key file
private_key_path = "keys\chess-tutor-520-firebase-adminsdk-byee5-e23511e61b.json"

# Initialize Firebase Admin SDK
# This assumes you have a Firebase project and have downloaded the private key JSON file
# from the Firebase Console -> Project Settings -> Service accounts -> Generate new private key
cred = credentials.Certificate(private_key_path)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
