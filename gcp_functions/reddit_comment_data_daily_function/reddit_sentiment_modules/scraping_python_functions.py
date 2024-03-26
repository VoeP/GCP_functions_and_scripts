import praw
from reddit_sentiment_modules.credentials import Credentials
import pandas as pd
import numpy as np


def init_reddit():
    """Initializes a connection to reddit with praw using the credentials defined in the reddit_credentials.py file.
    If you don't have these you can ask VoeP for them or define them for yourself, creating them is definitiely not difficult
    whatsoever."""
    # Create the credentials object
    cred = Credentials()
    reddit = praw.Reddit(
    client_id=cred.client_id,
    client_secret=cred.client_secret,
    password=cred.password,
    user_agent=cred.agent,
    redirect_uri=cred.redirect_uri,
    username=cred.username,
    )
    print(cred.agent)
    return reddit


def get_comments_from_hot(reddit, num=20, subreddit="wallstreetbets"):
    """Gets the comment dataset from num first posts in the hot category from subreddit. reddit is the
    connection specified with praw, which can be initialized using the init_reddit function."""
    subreddit = reddit.subreddit(subreddit)
    text=[]
    score=[]
    level=[]
    posts=[]
    urls = []
    authors=[]
    for i in subreddit.hot(limit=num):
        submission=reddit.submission(i)
        url = submission.url
        for top_level_comment in submission.comments:
            try:
                text.append(top_level_comment.body)
                score.append(top_level_comment.score)
                level.append("top")
                posts.append(submission.title)
                urls.append(url)
              #  redditor = "username : " + str(top_level_comment.author.id)
              #  authors.append(redditor)

                for second_level_comment in top_level_comment.replies:
                    text.append(second_level_comment.body)
                    score.append(second_level_comment.score)
               #     redditor="username : " + str(second_level_comment.author.id)
               #     authors.append(redditor)
                    level.append("second")
                    posts.append(submission.title)
                    urls.append(url)
            except AttributeError:
                pass
    df_comments = pd.DataFrame.from_dict({"text":text, "score":score, "level":level,"post": posts})
    return df_comments