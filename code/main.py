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

    factory = Faker()
    random_seed = 1
    factory.random.seed(random_seed)
    for _ in range(10):
        logger.info(factory.name())

    seeds = range(1, 200)
    counts = list()
    collision_limit = 10
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
        counts.append(count)
        logger.info('seed %d found repeats  %s after %d trials' % (random_seed, collisions, count))
    plt.scatter(seeds, counts)
    fitline = np.polyfit(seeds, counts, 1)
    p = np.poly1d(fitline)
    plt.plot(seeds, p(seeds), 'r--')
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
