import logging
from time import time

import matplotlib.pyplot as plt
from faker import Faker

if __name__ == '__main__':
    start_time = time()

    formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.INFO)
    logger.info('started')

    settings = {
        'collision_limit': 100
    }
    factory = Faker()
    collision_limits = range(settings['collision_limit'])
    found = set()
    for collision_limit in collision_limits:
        done = False
        name = None
        collisions = list()
        while not done:
            name = factory.name()
            done = len(collisions) == collision_limit
            if name in found:
                collisions.append(name)
                logger.info('%d %d %.4f' % (len(found) + len(collisions), len(collisions),
                                            float(len(collisions)) / float(len(found) + len(collisions))))
            else:
                found.add(name)
    output_folder = '../output/'
    output_file = output_folder + 'collision_scatter.png'
    plt.savefig(output_file)

    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
