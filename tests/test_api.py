from .conftest import client


def test_upload_media():
    file_content = b"Hello, World!"
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/api/medias", files=files, headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True, "media_id": 1}


def test_create_tweet():
    data = {"tweet_data": "1", "tweet_media_ids": []}
    response = client.post("/api/tweets", json=data, headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True, "tweet_id": 1}


def test_add_like_to_tweet():
    response = client.post("/api/tweets/1/likes", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True}


def test_delete_like_to_tweet():
    response = client.delete("/api/tweets/1/likes", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True}


def test_follow_user():
    response = client.post("/api/users/2/follow", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True}


def test_delete_follow_user():
    response = client.delete("/api/users/2/follow", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {"result": True}


def test_get_all_tweets():
    response = client.get("/api/tweets", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "tweets": [
            {
                "id": 1,
                "content": "1",
                "attachments": [],
                "author": {"id": 1, "name": "Дмитрий"},
                "likes": [],
            }
        ],
    }


def test_get_this_user():
    response = client.get("/api/users/me", headers={"Api-Key": "test"})

    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {"id": 1, "name": "Дмитрий", "followers": [], "following": []},
    }


def test_get_user_by_id():
    response = client.get("/api/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {"id": 1, "name": "Дмитрий", "followers": [], "following": []},
    }
