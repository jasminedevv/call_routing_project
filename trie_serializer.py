import pickle
from string import digits

from compact_trie import CompactTrie as Trie
# from trie import Trie
from data_reader import routes_gen

PHONE_KEYS = bytes('+' + digits, 'utf-8')

def dump(trie: Trie, name: str) -> None:
  print(f'Dumping {name} Trie...')

  with open(f'{name}.pkl', 'wb') as f:
    pickle.dump(trie, f, pickle.HIGHEST_PROTOCOL)

  print(f'{name} Trie dumped!')

def load(name: str) -> Trie:
  print(f'Loading {name} Trie...')

  with open(f'{name}.pkl', 'rb') as f:
    trie: Trie = pickle.load(f)

  print(f'{name} Trie loaded!')

  return trie

def _grow_trie(number):
  print(f'Growing {number} Trie...')

  # trie = Trie(PHONE_KEYS, routes_gen(number))
  trie = Trie(items=routes_gen(number))

  print(f'{number} Trie grown!')

  return trie

def _grow_dump(number):
  trie = _grow_trie(number)
  dump(trie, number)

def main():
  from sys import argv
  from glob import glob
  from multiprocessing import Pool

  _, action, *numbers = argv

  pool = Pool(5)

  if action == 'dump':
    pool.map(_grow_dump, numbers)
  elif action == 'load':
    pool.map(load, numbers)

  pool.close()
  pool.join()

if __name__ == '__main__':
  main()
