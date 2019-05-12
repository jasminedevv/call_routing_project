import pickle

# from compact_trie import CompactTrie as Trie
from trie import Trie
from data_reader import routes_gen

def dump(trie: Trie, name: str) -> None:
  print('Dumping Trie...')

  with open(f'{name}.pkl', 'wb') as f:
    pickle.dump(trie, f, pickle.HIGHEST_PROTOCOL)

  print('Trie dumped!')

def load(name: str) -> Trie:
  print('Loading Trie...')

  with open(f'{name}.pkl', 'rb') as f:
    trie: Trie = pickle.load(f)

  print('Trie loaded!')

  return trie

def _grow_trie(number):
  print('Growing Trie...')

  trie = Trie(routes_gen(number))

  print('Trie grown!')

  return trie

def main():
  from sys import argv

  _, action, number, *_ = argv

  if action == 'dump':
    dump(_grow_trie(number), number)
  elif action == 'load':
    load(number)

if __name__ == '__main__':
  main()
