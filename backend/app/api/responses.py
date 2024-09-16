from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.schema.models import Response, ResponseCreate
from app.services.response_generation import generate_response

router = APIRouter()

@router.get('/responses/', response_model=List[Response])
def get_responses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    responses = db.query(Response).offset(skip).limit(limit).all()
    return responses

@router.post('/responses/', response_model=Response)
def create_response(response: ResponseCreate, db: Session = Depends(get_db)):
    # HUMAN ASSISTANCE NEEDED
    # This function needs more implementation details and error handling
    # The confidence level is below 0.8, indicating potential issues
    generated_response = generate_response(response.tweet_content)
    new_response = Response(
        tweet_id=response.tweet_id,
        content=generated_response,
        sentiment=response.sentiment
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response

@router.put('/responses/{response_id}', response_model=Response)
def update_response(response_id: str, response: ResponseCreate, db: Session = Depends(get_db)):
    db_response = db.query(Response).filter(Response.id == response_id).first()
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    
    for key, value in response.dict().items():
        setattr(db_response, key, value)
    
    db.commit()
    db.refresh(db_response)
    return db_response