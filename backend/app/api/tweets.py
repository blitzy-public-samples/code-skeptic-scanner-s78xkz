from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.schema.models import Tweet, TweetCreate
from app.services.tweet_analysis import analyze_tweet

router = APIRouter()

@router.get('/tweets/', response_model=List[Tweet])
def get_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tweets = db.query(Tweet).offset(skip).limit(limit).all()
    return tweets

# HUMAN ASSISTANCE NEEDED
# This function needs review for production readiness
@router.post('/tweets/', response_model=Tweet)
def create_tweet(tweet: TweetCreate, db: Session = Depends(get_db)):
    new_tweet = Tweet(**tweet.dict())
    analysis_result = analyze_tweet(new_tweet.content)
    new_tweet.sentiment = analysis_result.get('sentiment')
    new_tweet.keywords = analysis_result.get('keywords')
    
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    
    return new_tweet

@router.get('/tweets/{tweet_id}', response_model=Tweet)
def get_tweet(tweet_id: str, db: Session = Depends(get_db)):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet