from IPython.display import display, Markdown
import json


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
