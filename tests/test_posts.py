def test_get_posts(auth_client,test_post):
    res = auth_client.get ("/posts")
    print(res.json())
    assert len(res.json())==len(test_post)
    assert res.status_code == 200
