from data_reader import routes_gen, numbers_gen
from utils import decode_route_prefix

# Generate the routes sorted
routes = list(decode_route_prefix(routes_gen('106000')))
routes.sort(key=lambda r: len(r[0]), reverse=True)

def get_cost(number: str) -> float:
  """Finds the price of a number by searching for the longest corresponding route."""
  for prefix, cost in routes:
    if number.startswith(prefix):
      return cost

  return 0

if __name__ == '__main__':
  from random import choice

  number = choice(list(numbers_gen('1000'))).decode()
  cost = get_cost(number)

  print(number, cost, sep=', ')
