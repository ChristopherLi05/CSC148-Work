import datetime
from datetime import date


class Tweet:
    """A tweet, like in Twitter.
    Instance attributes:
    - content: the contents of the tweet.
    - userid: the id of the user who wrote the tweet.
    - created_at: the date the tweet was written.
    - likes: the number of likes this tweet has received.
    """
    content: str
    userid: str
    created_at: date
    likes: int

    def __init__(self, who: str, when: date, what: str) -> None:
        """Initialize a new Tweet.
        """

    def like(self, n: int) -> None:
        """Record the fact that this tweet received <n> likes.
        These likes are in addition to the ones <self> already has.
        """

    def edit(self, new_content: str) -> None:
        """Replace the contents of this tweet with the new message.
        """


class User:
    """A Twitter user.
    Instance attributes:
    - userid: the userid of this Twitter user.
    - bio: the bio of this Twitter user.
    - tweets: the tweets that this user has made.
    - follows: the people that this user follows
    """
    userid: str
    bio: str
    tweets: list[Tweet]
    follows: list[str]

    def __init__(self, userid: str, bio: str) -> None:
        """Initialize a new user with the given id and bio.
        The new user initially has no tweets.
        """

        self.userid = userid
        self.bio = bio
        self.tweets = []
        self.follows = []

    def tweet(self, message: str) -> None:
        """Record that this User made a tweet with the given content.
        Use date.today() to get the current date for the newly-created tweet.
        """

        self.tweets.append(Tweet(self.userid, datetime.datetime.today(), message))

    def follow(self, userid: str) -> None:
        """
        Follows someone based off their userid
        """
        self.follows.append(userid)
