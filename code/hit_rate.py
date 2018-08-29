import logging
from time import time

import matplotlib.pyplot as plt
from faker import Faker
from json import load

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

    with open('hit-rate-settings.json') as settings_fp:
        settings = load(settings_fp)


    for random_state in range(0, settings['test_count']):
        factory = Faker()
        factory.seed(random_state)
        found = set()
        done = False
        name = None
        collisions = list()
        collision_limit = settings['collision_limit']
        xs = list()
        ys = list()
        collision_rate = -1
        while not done:
            name = factory.name()
            done = collision_rate > collision_limit
            if name in found:
                collisions.append(name)
                collision_count = len(collisions)
                found_count = len(found)
                total_samples = found_count + collision_count
                collision_rate = float(collision_count) / float(total_samples)
                xs.append(total_samples)
                ys.append(collision_rate)
                logger.info('%d %d %.4f' % (total_samples, collision_count, collision_rate))
            else:
                found.add(name)

        plt.plot(xs, ys)
    plt.savefig('../output/hit_rates.png')
    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
