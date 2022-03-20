import json
import praw
from apscheduler.schedulers.blocking import BlockingScheduler

import util as u
import innova_factory_store as ifs


def main(subr):
    posts = ifs.get_posts()
    subreddit = u.get_subreddit(subr)
    for post in posts:
        if subr == 'DiscReleases':
            subreddit.submit(post['title'], selftext=post['content'], flair_id=post['flair_id'])
        else:
            subreddit.submit(post['title'], selftext=post['content'])
    print(f'Submitted {len(posts)} posts to r/{subr}')


def monitor_releases(subr):
    sched = BlockingScheduler()

    @sched.scheduled_job('interval', minutes=1)
    def check_releases():
        main(subr)

    sched.start()


if __name__ == '__main__':
    import sys
    if sys.argv:
        subr = sys.argv[1]
        if subr not in ('BotsPlayHere', 'DiscReleases'):
            raise NotImplementedError(f'Subreddit "{subr}" not allowed. This bot is only intended to post to "DiscReleases" and "BotsPlayHere" for testing.')
    else:
        subr = 'BotsPlayHere'
    monitor_releases(subr)
