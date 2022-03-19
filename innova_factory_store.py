import requests
import json
from bs4 import BeautifulSoup
import random

import util as u


SITE_URL = 'https://proshop.innovadiscs.com'
SITE_NAME = 'Innova Factory Store'
SITE_KEY = 'innova-factory-store'
FLAIR = 'Innova'
FLAIR_ID = u.get_flair_id(FLAIR)


def get_options(label_node):
    ''' returns list of options from color/weight dropdowns '''
    select_node = label_node.find_next_sibling()
    attr_id = select_node.attrs['name']
    options = [opt.text for opt in select_node.select('option') if opt.text != 'Choose Options']
    return options


def get_disc_info(url):
    ''' returns dict of detailed disc info '''
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # get color and weight options
    labels = soup.find_all('label')
    try:
        weight_label = [lab for lab in labels if 'Disc Weight' in lab.text][0]
        weights = get_options(weight_label)
    except IndexError:
        weights = None
    try:
        color_label = [lab for lab in labels if 'Color' in lab.text][0]
        colors = get_options(color_label)
    except IndexError:
        colors = None
    
    # get price
    for s in soup.select('.price-section'):
        if s.attrs.get('itemprop') == 'offers':
            price = s.select('.price')[0].text
    
    # get product description
    desc = soup.select('.productView-description')[0].select('#tab-description')[0]
    desc_p = desc.select('p')
    if desc_p:
        description = '\n\n'.join([p.text for p in desc_p]).strip()
    else:
        description = desc.text.strip()

    # get image hyperlink
    images = [t.attrs.get('href') for t in soup.select('.productView-thumbnail a') if 'href' in t.attrs]
    
    return {
        'weights': weights,
        'colors': colors,
        'price': price,
        'description': description,
        'images': images,
        'url': url
    }


def get_featured():
    ''' returns dict of all featured items with url '''
    resp = requests.get(SITE_URL)
    soup = BeautifulSoup(resp.content, 'html.parser')
    featured = {c.text: c.attrs['href'] for c in soup.select('.card-body a')}
    return featured


def get_markdown(name, info):
    markdown = f'''
        ### [{name}]({info['url']})
        **Price:** {info['price']}

        **Description**  
        {info['description']}  

    '''
    if info['colors']:
        markdown += f"**Available Colors:** {', '.join(info['colors'])}\n\n"
    if info['weights']:
        markdown += f"**Available Weights** {', '.join(info['weights'])}\n\n"
    markdown += u.BOT_NOTE
    return u.clean_markdown(markdown)


def get_post(name, info):
    return {
        'title': f'New Drop at {SITE_NAME}: {name}',
        'content': get_markdown(name, info),
        'flair_id': FLAIR_ID
    }


def get_posts():
    prev_featured = u.get_prev_featured(SITE_KEY)
    featured = get_featured()
    new_drops = u.get_new_drops(prev_featured, featured, get_disc_info)
    posts = [get_post(name, info) for name, info in new_drops.items()]

    # write back featured items to prev_featured.json
    u.update_prev_featured(SITE_KEY, featured)
    return posts
