from typing import Any


def generate_error_response(error_type: str, error_message: str) -> dict:
    return {"result": False, "error_type": error_type, "error_message": error_message}


def generate_good_response(obj: str, data: Any):
    return {"result": True, obj: data}


def generate_tweet_data(tweet):
    attachments = [media.file_src for media in tweet.media]
    likes = [{"user_id": like.id, "name": like.name} for like in tweet.liked_by_users]

    return {
        "id": tweet.id,
        "content": tweet.content,
        "attachments": attachments,
        "author": {"id": tweet.author.id, "name": tweet.author.name},
        "likes": likes,
    }


def generate_user_data(user):
    return {
        "id": user.id,
        "name": user.name,
        "followers": [
            {"id": follower.id, "name": follower.name} for follower in user.followers
        ],
        "following": [
            {"id": following.id, "name": following.name} for following in user.following
        ],
    }
