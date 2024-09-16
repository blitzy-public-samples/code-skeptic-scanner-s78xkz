from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.tweets import router as tweets_router
from app.api.responses import router as responses_router
from app.api.contexts import router as contexts_router
from app.api.prompts import router as prompts_router
from app.api.users import router as users_router
from app.api.analytics import router as analytics_router
from app.core.config import settings
from app.db.firestore import get_db
from app.services.tweet_ingestion import start_tweet_stream

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tweets_router, prefix="/api/tweets", tags=["tweets"])
app.include_router(responses_router, prefix="/api/responses", tags=["responses"])
app.include_router(contexts_router, prefix="/api/contexts", tags=["contexts"])
app.include_router(prompts_router, prefix="/api/prompts", tags=["prompts"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])

@app.on_event("startup")
async def startup_event():
    # HUMAN ASSISTANCE NEEDED
    # The confidence level for this function is below 0.8. Please review and adjust as necessary.
    # Initialize database connection
    db = get_db()
    
    # Start the tweet streaming process
    # Note: This might need to be adjusted based on the actual implementation of start_tweet_stream
    await start_tweet_stream()

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections
    db = get_db()
    # Assuming there's a method to close the database connection
    await db.close()
    
    # Perform any necessary cleanup
    # Add any additional cleanup operations here if needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)