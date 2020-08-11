import praw
from secret import CLIENT_ID, CLIENT_SECRET, USER_AGENT


def rddit(subreddit):
    # reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)

    # subreddit
    subreddit = reddit.subreddit(subreddit)

    for submission in subreddit.hot(limit=1):
        title = submission.title
        desc = submission.selftext
        url = submission.url

    if len(desc) > 1001:
        desc = desc[:1001] + '...'
    data = {'name': 'r/'+subreddit.display_name,
            'title': title, 'desc': desc, 'url': url}
    return data
