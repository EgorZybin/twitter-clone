from typing import List, Union

from pydantic import BaseModel


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Union[int, List[int]]
