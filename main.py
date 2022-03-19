import innova_factory_store as ifs
import json
import praw
import util as u


def main(subr):
    posts = ifs.get_posts()
    subreddit = u.get_subreddit(subr)
    for post in posts:
        if subr == 'DiscReleases':
            subreddit.submit(post['title'], selftext=post['content'], flair_id=post['flair_id'])
        else:
            subreddit.submit(post['title'], selftext=post['content'])
    print(f'Submitted {len(posts)} posts to r/{subr}')


if __name__ == '__main__':
    main('BotsPlayHere')
