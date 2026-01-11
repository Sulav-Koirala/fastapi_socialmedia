from app import schemas
import pytest

def test_get_posts(auth_client,test_post):
    res = auth_client.get ("/posts")
    print(res.json())
    assert len(res.json())==len(test_post)
    assert res.status_code == 200

def test_unauth_user_get_posts(client,test_post):
    res = client.get("/posts")
    assert res.status_code == 401

def test_get_one_post(auth_client,test_post):
    post_id = test_post[0].id
    res = auth_client.get(f"posts/{post_id}")
    post = schemas.Response(**res.json())
    assert post.id == test_post[0].id

def test_unauth_user_get_one_post(client,test_post):
    post_id = test_post[0].id 
    res = client.get(f"/posts/{post_id}")
    assert res.status_code == 401

def test_no_post_exist_get(auth_client):
    res= auth_client.get("/posts/123")
    assert res.status_code == 404

@pytest.mark.parametrize("title,content,published",[
        ("post1","this is first post",True),
        ("post2","this is second post",False),
        ("post3","this is third post",True)
])
def test_post_posts(auth_client,test_user,title,content,published):
    res = auth_client.post("/posts",json={"title": title,"content": content,"post": published})
    new_post = schemas.Response(**res.json())
    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.owner.id == test_user['id']
    

def test_unauth_user_post_posts(client):
    res = client.post("/posts", json={"title":"hello","content":"im saying hello", "post": False})
    assert res.status_code == 401

def test_delete_post_auth(auth_client,test_post):
    res = auth_client.delete (f"/posts/{test_post[0].id}")
    assert res.status_code == 204

def test_delete_post_unauth(client,test_post):
    res = client.delete (f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_delete_nonexistent_post(auth_client):
    res = auth_client.delete("/posts/100")
    assert res.status_code == 404

def test_delete_otheruser_post(auth_client,test_post):
    res = auth_client.delete(f"/posts/{test_post[1].id}")
    assert res.status_code == 403

def test_update_post_auth(auth_client,test_post):
    res = auth_client.put (f"/posts/{test_post[0].id}", json = {"title": "hello again","content": "i am saying hello again", "post": True})
    updated_post = schemas.Response(**res.json())
    assert res.status_code == 200
    assert updated_post.title == test_post[0].title

def test_update_post_unauth(client,test_post):
    res = client.put (f"/posts/{test_post[0].id}", json={"title": "hello again","content": "i am saying hello again", "post": True})
    assert res.status_code == 401

def test_update_nonexistent_post(auth_client):
    res = auth_client.put("/posts/100", json={"title": "hello again","content": "i am saying hello again", "post": True})
    assert res.status_code == 404

def test_update_otheruser_post(auth_client,test_post):
    res = auth_client.put(f"/posts/{test_post[1].id}",json= {"title": "hello again","content": "i am saying hello again", "post": True})
    assert res.status_code == 403
