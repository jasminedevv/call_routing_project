from typing import Dict

from data_reader import routes_gen, numbers_gen

routes: Dict[str, float] = dict((route.decode(), cost) for route, cost in routes_gen('106000'))

def get_price(number: str) -> float:
  while number:
    try:
      return routes[number]
    except KeyError:
      number = number[:-1]

  return 0

def main():
  print('Getting prices and writing to scenario2.out...')

  with open('scenario2.out', 'w') as f:
    for number in map(bytes.decode, numbers_gen('1000')):
      f.write(number)
      f.write(', ')
      f.write(str(get_price(number)))
      f.write('\n')

  print('Done!')

if __name__ == '__main__':
  main()
