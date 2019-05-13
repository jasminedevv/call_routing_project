from typing import Generator, Tuple

def routes_gen(num) -> Generator[Tuple[bytes, float], None, None]:
  """Takes the carrier list file and returns a list of tuples: (prefix, cost)"""
  with open(f'data/route-costs-{num}.txt', 'rb') as routes:
    for route in routes:
        prefix, cost = route[:-1].split(b',')
        yield (prefix, float(cost)) # returns a bunch of values without loading the whole thing into memory

def numbers_gen(num) -> Generator[bytes, None, None]:
  with open(f'data/phone-numbers-{num}.txt', 'rb') as numbers:
    for number in numbers:
      yield number[:-1]
