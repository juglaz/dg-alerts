from IPython.display import display, Markdown
import json
import praw


BOT_NOTE = '''
### BTW, *This is my bot.*
Please let me know if you have any feedback or if it's acting up.    
*Cheers!*
'''


def clean_markdown(markdown):
    ''' remove leading whitespace from each line '''
    cleaned = ''
    for line in markdown.strip().split('\n'):
        cleaned += line.lstrip() + '\n'
    return cleaned


def printmd(string):
    ''' Renders markdown in notebook output of codecell '''
    display(Markdown(string))


def get_prev_featured(site_key):
    with open('prev_featured.json', 'r') as f:
        return json.loads(f.read()).get(site_key)


def update_prev_featured(site_key, featured):
    with open('prev_featured.json', 'r+') as f:
        all_featured = json.loads(f.read())
        all_featured[site_key] = featured
        f.seek(0)
        f.write(json.dumps(all_featured))
        f.truncate()


def get_new_drops(prev_featured, featured, get_disc_info):
    ''' returns details for all new drops '''
    new_drops = [k for k in featured.keys() if k not in prev_featured.keys()]
    new_drops_info = {k: get_disc_info(featured[k]) for k in new_drops}
    return new_drops_info


def get_reddit():
    with open('client_secrets.json', 'r') as f:
        creds = json.loads(f.read())

    reddit = praw.Reddit(client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent'],
        redirect_uri=creds['redirect_uri'],
        refresh_token=creds['refresh_token'],
        validate_on_submit=True)
    return reddit


def get_subreddit(subr):
    reddit = get_reddit()
    subreddit = reddit.subreddit(subr)
    return subreddit


def update_flairs_json():
    with open('flairs.json', 'w') as f:
        reddit = get_reddit()
        flairs_raw = reddit.post("r/DiscReleases/api/flairselector/", data={"is_newlink": True})["choices"]
        flairs = {f['flair_text']: f['flair_template_id'] for f in flairs_raw}
        f.write(json.dumps(flairs))


def get_flair_id(flair):
    with open('flairs.json', 'r') as f:
        flairs = json.loads(f.read())
        return flairs.get(flair)
