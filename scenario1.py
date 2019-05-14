from data_reader import routes_gen, numbers_gen

# Generate the routes sorted
routes = list(((route.decode(), cost) for route, cost in routes_gen('106000')))
routes.sort(key=lambda r: len(r[0]), reverse=True)

def get_cost(number: str) -> float:
  """Finds the price of a number by searching for the longest corresponding route."""
  for route in routes:
    if number.startswith(route[0]):
      return route[1]

  return 0

if __name__ == '__main__':
  from random import choice

  number = choice(list(numbers_gen('1000'))).decode()
  cost = get_cost(number)

  print(number, cost, sep=', ')
