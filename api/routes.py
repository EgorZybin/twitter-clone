import os
import shutil
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Form, Header, UploadFile, File, Depends
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator
from api.methods import (
    generate_good_response,
    generate_error_response,
    generate_tweet_data,
    generate_user_data,
)
from api.models import create_database_tables, get_session, Users, Tweets, Medias
from api.schemas import TweetIn

app = FastAPI()

GOOD_RESPONSE = {"result": True}
UPLOAD_FOLDER = "uploadfile"

Instrumentator().instrument(app).expose(app)

sentry_sdk.init(
    dsn="https://2f8bdf6f4ab3fffafcfd80495ab758ed@o4507900552478720.ingest.de.sentry.io/4508084034273360",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
create_database_tables()

@app.get("/api/uploadfile/{file_name}")
async def get_file_from_dir(file_name: str):
    file_path = f"uploadfile/{file_name}"
    return FileResponse(file_path)


@app.post("/api/tweets")
def create_new_tweet(
    tweet_data: TweetIn, api_key: str = Header(None), session=Depends(get_session)
):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        media = (
            session.query(Medias)
            .filter(Medias.id.in_(tweet_data.tweet_media_ids))
            .all()
        )
        if not user:
            return generate_error_response("UserNotFound", "User not found")

        tweet_text = tweet_data.tweet_data
        media_ids = [media_obj.id for media_obj in media]
        new_tweet = Tweets(content=tweet_text, author_id=user.id)

        for media_id in media_ids:
            new_tweet.media.append(session.query(Medias).get(media_id))

        session_obj.add(new_tweet)
        session.commit()
        return generate_good_response("tweet_id", new_tweet.id)


@app.post("/api/medias")
async def download_file_from_tweet(
    file: UploadFile = File(...), session=Depends(get_session)
):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with session as session_obj:
        new_media = Medias(file_name=file.filename, file_src=f"api/{file_path}")
        session_obj.add(new_media)
        session_obj.commit()

        return {"result": True, "media_id": new_media.id}


@app.delete("/api/tweets/{id}")
def delete_tweet_by_id(
    id: int, api_key: str = Header(None), session=Depends(get_session)
):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        tweet = (
            session_obj.query(Tweets)
            .filter(Tweets.id == id, Tweets.author_id == user.id)
            .first()
        )
        if not user or not tweet:
            return generate_error_response(
                "TweetNotFound",
                "Твит не найден или пользователь не имеет прав для удаления",
            )

        for media in tweet.media:
            tweet.media.remove(media)
        session_obj.delete(tweet)
        session_obj.commit()
        return GOOD_RESPONSE


@app.post("/api/tweets/{id}/likes")
def like_a_tweet(id: int, api_key: str = Header(None), session=Depends(get_session)):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        tweet = session_obj.query(Tweets).filter(Tweets.id == id).first()

        if not user or not tweet:
            error_response = generate_error_response("TweetNotFound", "Твит не найден")
            return error_response

        tweet.liked_by_users.append(user)
        session_obj.commit()

        return GOOD_RESPONSE


@app.delete("/api/tweets/{id}/likes")
def delete_like_from_tweet(
    id: int, api_key: str = Header(None), session=Depends(get_session)
):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        tweet = session_obj.query(Tweets).filter(Tweets.id == id).first()
        if not user or not tweet:
            return generate_error_response(
                "TweetNotFound",
                "Твит не найден или пользователь не имеет прав для удаления",
            )

        tweet.liked_by_users.remove(user)
        session_obj.commit()
        return GOOD_RESPONSE


@app.post("/api/users/{id}/follow")
def follow_user(id: int, api_key: str = Header(None), session=Depends(get_session)):
    with session as session_obj:
        user_who_is_following = (
            session_obj.query(Users).filter(Users.api_key == api_key).first()
        )
        user_being_followed_by = session_obj.query(Users).filter(Users.id == id).first()
        if not user_who_is_following or not user_being_followed_by:
            return generate_error_response("UserNotFound", "User not found")

        user_who_is_following.following.append(user_being_followed_by)
        session_obj.commit()
        return GOOD_RESPONSE


@app.delete("/api/users/{id}/follow")
def delete_follow_on_user(
    id: int, api_key: str = Header(None), session=Depends(get_session)
):
    with session as session_obj:
        user_who_is_followed = (
            session_obj.query(Users).filter(Users.api_key == api_key).first()
        )
        user_was_followed_by = session_obj.query(Users).filter(Users.id == id).first()
        if not user_who_is_followed or not user_was_followed_by:
            return generate_error_response("UserNotFound", "User not found")

        user_who_is_followed.following.remove(user_was_followed_by)
        session_obj.commit()

        return GOOD_RESPONSE


@app.get("/api/tweets")
def get_tweets_list(api_key: str = Header(None), session=Depends(get_session)):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        tweets = session_obj.query(Tweets).all()
        if not user:
            return generate_error_response("UserNotFound", "User not found")
        tweets_data = [generate_tweet_data(tweet) for tweet in tweets]
        return generate_good_response("tweets", tweets_data)


@app.get("/api/users/me")
def get_this_user_profile(api_key: str = Header(None), session=Depends(get_session)):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.api_key == api_key).first()
        if not user:
            return generate_error_response("UserNotFound", "User not found")

        user_info = generate_user_data(user)

        return generate_good_response("user", user_info)


@app.get("/api/users/{id}")
def get_user_by_id(id: int, session=Depends(get_session)):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.id == id).first()

        if not user:
            return generate_error_response("UserNotFound", "User not found")

        user_info = generate_user_data(user)

        return generate_good_response("user", user_info)


# ТЕСТОВЫЕ


@app.post("/users")
async def create_new_user(
    name: str = Form(...), api_key: str = Form(...), session=Depends(get_session)
):
    new_data = Users(name=name, api_key=api_key)
    session.add(new_data)
    session.commit()
    session.close()


@app.delete("/users/{id}")
def delete_user(id: int, session=Depends(get_session)):
    with session as session_obj:
        user = session_obj.query(Users).filter(Users.id == id).first()
        session_obj.delete(user)
        session.commit()


if __name__ == "__main__":
    uvicorn.run(app)
