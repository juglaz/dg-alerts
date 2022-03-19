import innova_factory_store as ifs
import json
import praw


def main(subr):
    posts = ifs.get_posts()
    subreddit = get_subreddit(subr)
    for post in posts:
        subreddit.submit(post['title'], selftext=post['content'])
    print(f'Submitted {len(posts)} posts to r/{subr}')


def get_subreddit(subr):
    with open('client_secrets.json', 'r') as f:
        creds = json.loads(f.read())

    reddit = praw.Reddit(client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent'],
        redirect_uri=creds['redirect_uri'],
        refresh_token=creds['refresh_token'],
        validate_on_submit=True)

    subreddit = reddit.subreddit(subr)
    return subreddit


if __name__ == '__main__':
    main('BotsPlayHere')
