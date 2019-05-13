from typing import Tuple

from data_reader import routes_gen, numbers_gen

def main(number: str) -> Tuple[str, float]:
  routes = list(routes_gen('35000'))
  routes.sort(key=lambda r: len(r[0]), reverse=True)

  for route in routes:
    if number.startswith(route[0].decode()):
      return (number, route[1])

  return (number, 0)

if __name__ == '__main__':
  number = next(numbers_gen('10'))
  result = main(number.decode())

  print(*result, sep=', ')
