import random


def simulate_new_drop(featured):
    ''' returns prev_featured (random disc removed from featured) '''
    prev_featured = featured.copy()
    new_drop = random.choice(list(featured.keys()))
    del prev_featured[new_drop]
    return prev_featured
