from typing import Generator

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URL = (
    "postgresql+psycopg2://postgres:admin@postgres:5432/twitter"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("following_id", Integer, ForeignKey("users.id")),
)

likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
)

tweet_media_association = Table(
    "tweet_media_association",
    Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
    Column("media_id", Integer, ForeignKey("medias.id")),
)


class Medias(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True)
    file_src = Column(String)
    file_name = Column(String)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    followers = relationship(
        "Users",
        secondary=followers,
        primaryjoin=(followers.c.following_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref="following",
    )

    api_key = Column(String(), nullable=None)
    authored_tweets = relationship(
        "Tweets", backref="author", foreign_keys="Tweets.author_id"
    )


class Tweets(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    media = relationship("Medias", secondary=tweet_media_association, backref="tweets")
    author_id = Column(Integer, ForeignKey("users.id"))
    liked_by_users = relationship("Users", secondary=likes, backref="liked_tweets")


def create_database_tables():
    connection = engine.connect()
    if not engine.dialect.has_table(
        connection, Users.__tablename__
    ) and not engine.dialect.has_table(connection, Tweets.__tablename__):
        Base.metadata.create_all(engine)
    connection.close()


def get_session():
    with Session() as session:
        yield session
