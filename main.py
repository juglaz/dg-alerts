import innova_factory_store as ifs
import json
import praw


def main(subr):
    posts = ifs.get_posts()
    subreddit = get_subreddit(subr)
    for post in posts:
        subreddit.submit(post['title'], selftext=post['content'], flair_id=post['flair_id'])
    print(f'Submitted {len(posts)} posts to r/{subr}')


if __name__ == '__main__':
    main('BotsPlayHere')
