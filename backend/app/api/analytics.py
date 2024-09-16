from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.services.analytics import get_tweet_trends, get_response_performance

router = APIRouter()

@router.get('/analytics/trends')
async def get_trends(db: Session = Depends(get_db)):
    trend_data = get_tweet_trends(db)
    return trend_data

@router.get('/analytics/performance')
async def get_performance(db: Session = Depends(get_db)):
    performance_metrics = get_response_performance(db)
    return performance_metrics