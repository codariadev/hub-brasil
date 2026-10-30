from firebase_admin import get_app, initialize_app
from firebase_admin import firestore as firebase_firestore


def get_firestore_client():
	try:
		app = get_app()
	except ValueError:
		app = initialize_app()
	return firebase_firestore.client(app)
