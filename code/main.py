import logging
from time import time

import matplotlib.pyplot as plt
import numpy as np
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
        'seeds' : 200,
        'collision_limit' : 100
    }
    factory = Faker()
    seeds = range(settings['seeds'])
    collision_limits = range(settings['collision_limit'])
    counts = [[0 for x in seeds] for y in collision_limits]
    for collision_limit in collision_limits:
        for random_seed in seeds:
            found = set()
            done = False
            name = None
            collisions = list()
            while not done:
                name = factory.name()
                done = len(collisions) == collision_limit
                if name in found:
                    collisions.append(name)
                else:
                    found.add(name)
            count = len(found)
            counts[collision_limit][random_seed] = count
            logger.info('seed %d found repeats  %s after %d trials' % (random_seed, collisions, count))
        plt.scatter(seeds, counts[collision_limit], s=1)
        fitline = np.polyfit(seeds, counts[collision_limit], 1)
        p = np.poly1d(fitline)
        plt.plot(seeds, p(seeds), '--')
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
