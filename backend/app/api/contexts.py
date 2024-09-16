from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.schema.models import Context, ContextCreate

router = APIRouter()

@router.get('/contexts/', response_model=List[Context])
def get_contexts(db: Session = Depends(get_db)):
    contexts = db.query(Context).all()
    return contexts

@router.post('/contexts/', response_model=Context)
def create_context(context: ContextCreate, db: Session = Depends(get_db)):
    new_context = Context(**context.dict())
    db.add(new_context)
    db.commit()
    db.refresh(new_context)
    return new_context

@router.put('/contexts/{context_id}', response_model=Context)
def update_context(context_id: str, context: ContextCreate, db: Session = Depends(get_db)):
    db_context = db.query(Context).filter(Context.id == context_id).first()
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    
    for key, value in context.dict().items():
        setattr(db_context, key, value)
    
    db.commit()
    db.refresh(db_context)
    return db_context

@router.delete('/contexts/{context_id}')
def delete_context(context_id: str, db: Session = Depends(get_db)):
    db_context = db.query(Context).filter(Context.id == context_id).first()
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    
    db.delete(db_context)
    db.commit()
    return {"message": "Context deleted successfully"}