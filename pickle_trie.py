import pickle
from trie import Trie
from data_reader import routes_gen
from sys import argv

def pickler(number):
  print('Growing Trie...')
  trie = Trie(routes_gen(number))
  print('Trie grown!')

  print('Dumping Trie...')
  with open(f'{number}.trie', 'wb') as file:
    pickle.dump(trie, file)
  print('Trie dumped!')

if __name__ == "__main__":
  print('Pickling...')
  pickler(argv[1])
  print('Pickled!')
