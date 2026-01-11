import pytest
from app import models

@pytest.fixture()
def test_like(test_post,session,test_user):
    new_like = models.Likes(post_id=test_post[1].id,user_id=test_user['id'])
    session.add(new_like)
    session.commit()

def test_successful_like(auth_client,test_post):
    res = auth_client.post ("/like", json = {"post_id": test_post[0].id, "like_dislike": 1})
    assert res.status_code == 201

def test_likes_twice(auth_client,test_post,test_like):
    res = auth_client.post("/like",json={"post_id": test_post[1].id,"like_dislike": 1})
    assert res.status_code == 409

def test_nonexistant_post_like(auth_client):
    res = auth_client.post("/like",json={"post_id": 10,"like_dislike": 1})
    assert res.status_code == 404

def test_successful_unlike(auth_client,test_post,test_like):
    res = auth_client.post ("/like",json={"post_id": test_post[1].id,"like_dislike":0})
    assert res.status_code == 201

def test_unlike_twice(auth_client,test_post):
    res = auth_client.post ("/like",json={"post_id": test_post[0].id,"like_dislike":0})
    assert res.status_code == 404

def test_nonexistant_post_unlike(auth_client):
    res = auth_client.post("/like",json={"post_id": 10,"like_dislike": 1})
    assert res.status_code == 404

def test_unauth_like(client,test_post):
    res = client.post("/like",json={"post_id": test_post[0].id,"like_dislike": 1})
    assert res.status_code == 401

