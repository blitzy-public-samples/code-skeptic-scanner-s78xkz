import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test cases for tweet endpoints
def test_get_tweets():
    response = client.get("/api/tweets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_tweet():
    tweet_data = {"content": "Test tweet", "user_id": 1}
    response = client.post("/api/tweets", json=tweet_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_tweet():
    response = client.get("/api/tweets/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_tweet():
    tweet_data = {"content": "Updated test tweet"}
    response = client.put("/api/tweets/1", json=tweet_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated test tweet"

def test_delete_tweet():
    response = client.delete("/api/tweets/1")
    assert response.status_code == 204

# Test cases for response endpoints
def test_get_responses():
    response = client.get("/api/responses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_response():
    response_data = {"content": "Test response", "tweet_id": 1, "user_id": 1}
    response = client.post("/api/responses", json=response_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_response():
    response = client.get("/api/responses/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_response():
    response_data = {"content": "Updated test response"}
    response = client.put("/api/responses/1", json=response_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated test response"

def test_delete_response():
    response = client.delete("/api/responses/1")
    assert response.status_code == 204

# Test cases for context endpoints
def test_get_contexts():
    response = client.get("/api/contexts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_context():
    context_data = {"content": "Test context", "tweet_id": 1}
    response = client.post("/api/contexts", json=context_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_context():
    response = client.get("/api/contexts/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_context():
    context_data = {"content": "Updated test context"}
    response = client.put("/api/contexts/1", json=context_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated test context"

def test_delete_context():
    response = client.delete("/api/contexts/1")
    assert response.status_code == 204

# Test cases for prompt endpoints
def test_get_prompts():
    response = client.get("/api/prompts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_prompt():
    prompt_data = {"content": "Test prompt", "user_id": 1}
    response = client.post("/api/prompts", json=prompt_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_prompt():
    response = client.get("/api/prompts/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_prompt():
    prompt_data = {"content": "Updated test prompt"}
    response = client.put("/api/prompts/1", json=prompt_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated test prompt"

def test_delete_prompt():
    response = client.delete("/api/prompts/1")
    assert response.status_code == 204

# Test cases for user endpoints
def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_user():
    user_data = {"username": "updateduser"}
    response = client.put("/api/users/1", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_user():
    response = client.delete("/api/users/1")
    assert response.status_code == 204

# Test cases for analytics endpoints
def test_get_tweet_analytics():
    response = client.get("/api/analytics/tweets/1")
    assert response.status_code == 200
    assert "views" in response.json()
    assert "likes" in response.json()
    assert "responses" in response.json()

def test_get_user_analytics():
    response = client.get("/api/analytics/users/1")
    assert response.status_code == 200
    assert "total_tweets" in response.json()
    assert "total_responses" in response.json()
    assert "total_likes" in response.json()

# HUMAN ASSISTANCE NEEDED
# The following test cases might need to be adjusted based on the actual implementation of the analytics endpoints
# and the specific metrics being tracked. Please review and modify as necessary.

def test_get_overall_analytics():
    response = client.get("/api/analytics/overall")
    assert response.status_code == 200
    assert "total_users" in response.json()
    assert "total_tweets" in response.json()
    assert "total_responses" in response.json()

def test_get_trending_topics():
    response = client.get("/api/analytics/trending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "topic" in response.json()[0]
    assert "count" in response.json()[0]