from google.cloud.firestore import Client
from google.auth import default
from typing import Any, Dict, List, Optional
from app.core.config import settings

db: Client = Client()

def get_db() -> Client:
    global db
    if db is None:
        _, project = default()
        db = Client(project=project)
    return db

def add_document(collection_name: str, data: Dict[str, Any]) -> str:
    client = get_db()
    doc_ref = client.collection(collection_name).add(data)
    return doc_ref[1].id

def get_document(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
    client = get_db()
    doc_ref = client.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def update_document(collection_name: str, document_id: str, data: Dict[str, Any]) -> bool:
    client = get_db()
    doc_ref = client.collection(collection_name).document(document_id)
    doc_ref.update(data)
    return True

def delete_document(collection_name: str, document_id: str) -> bool:
    client = get_db()
    doc_ref = client.collection(collection_name).document(document_id)
    doc_ref.delete()
    return True

# HUMAN ASSISTANCE NEEDED
# This function may need additional error handling and optimization for production use
def query_documents(collection_name: str, filters: Dict[str, Any], limit: Optional[int] = None) -> List[Dict[str, Any]]:
    client = get_db()
    query = client.collection(collection_name)
    
    for field, value in filters.items():
        query = query.where(field, '==', value)
    
    if limit:
        query = query.limit(limit)
    
    docs = query.stream()
    return [doc.to_dict() for doc in docs]