import functions_framework
from reddit_sentiment_modules.scraping_python_functions import *
from datetime import date

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    cred = Credentials()    
    reddit = init_reddit()

    subreddits = ["wallstreetbets", "worldnews", "askreddit"]
    #print(reddit)
    df_l = get_comments_from_hot(reddit, subreddit=subreddits[0], num = 10)
    print(f"{subreddits[0]} done")
    df_l["subreddit"]=subreddits[0]
    for subreddit in subreddits[1:]:
        df_r = get_comments_from_hot(reddit, subreddit=subreddit, num = 10)
        df_r["subreddit"]=subreddit
        df_l = pd.concat([df_l, df_r])
        print(f"{subreddit} done")
    df=df_l
    df["date"] = str(date.today())
    df.to_gbq(destination_table=f"reddit_comment_data.raw_daily_hot_comments",
          project_id='ml-deployments-practice',
          if_exists="append")

    success_message = f'Moving data to GBQ successful on the {date.today()}'

    
    return success_message
