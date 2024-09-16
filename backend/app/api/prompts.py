from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.schema.models import Prompt, PromptCreate

router = APIRouter()

@router.get('/prompts/', response_model=List[Prompt])
def get_prompts(db: Session = Depends(get_db)):
    prompts = db.query(Prompt).all()
    return prompts

@router.post('/prompts/', response_model=Prompt)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    new_prompt = Prompt(**prompt.dict())
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)
    return new_prompt

@router.put('/prompts/{prompt_id}', response_model=Prompt)
def update_prompt(prompt_id: str, prompt: PromptCreate, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    for key, value in prompt.dict().items():
        setattr(db_prompt, key, value)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.delete('/prompts/{prompt_id}')
def delete_prompt(prompt_id: str, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.delete(db_prompt)
    db.commit()
    return {"message": "Prompt deleted successfully"}