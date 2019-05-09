def routes_gen(num):
  with open(f'data/route-costs-{num}.txt') as routes:
    for route in routes:
        prefix, cost = route[:-1].split(',')
        yield (prefix, float(cost))

def numbers_gen(num):
  with open(f'data/phone-numbers-{num}.txt') as numbers:
    for number in numbers:
      yield number[:-1]
