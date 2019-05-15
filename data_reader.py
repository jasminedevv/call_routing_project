from typing import Generator, Tuple

Route = Tuple[bytes, float]
Number = bytes

def routes_gen(num) -> Generator[Route, None, None]:
  """Produces routes and their costs from the file data/route-costs-{num}.txt.

  Args:
      num ([type]): [description]

  Yields:
      Tuples of routes and their costs
  """
  with open(f'data/route-costs-{num}.txt', 'rb') as routes:
    for route in routes:
        prefix, cost = route[:-1].split(b',')
        yield (prefix, float(cost))

def numbers_gen(num) -> Generator[Number, None, None]:
  """Produces phone numbers from the file data/phone-numbers-{num}.txt.

  Args:
      num: The number in the file.

  Yields:
      A phone number in bytes.
  """
  with open(f'data/phone-numbers-{num}.txt', 'rb') as numbers:
    for number in numbers:
      yield number[:-1]
