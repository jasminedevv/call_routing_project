import pickle
from trie import Trie
from data_reader import routes_gen
from sys import argv

def pickler(number):
  trie = Trie(routes_gen(number))
  pickle.dump(trie, open(f'{number}.trie', 'wb'))

if __name__ == "__main__":
  print('Pickling')
  pickler(argv[1])
  print('Pickled!')
