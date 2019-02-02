from itertools import islice


def get_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())
