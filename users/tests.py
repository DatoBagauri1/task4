from django.test import TestCase

from django.core.cache import cache
import random
import time


def expensive_calculations():
    numbers = [i for i in range(10_000_000)]
    random.shuffle(numbers)
    numbers.sort()
    return numbers


def get_list():
    start = time.time()

    sorted_list = cache.get('numbers')

    if not sorted_list:
        sorted_list = expensive_calculations()
        cache.set('numbers', sorted_list, 60 * 10)

    end = time.time()

    print(end - start)
    return sorted_list


get_list()
get_list()
