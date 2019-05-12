from trie import Trie
from data_reader import routes_gen, numbers_gen
import pickle

def main():
  # print('Growing Trie')
  # trie = Trie(routes_gen('1000000'))
  # print('Trie grown')
  trie = pickle.load(open('10000000.trie', 'rb'))

  for number in numbers_gen('100'):
    print(number, trie.find_closest(number), sep=', ')

if __name__ == '__main__':
  main()
