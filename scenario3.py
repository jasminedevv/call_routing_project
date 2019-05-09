from trie import Trie
from data_reader import routes_gen, numbers_gen


def main():
  print('Growing Trie')
  trie = Trie(routes_gen('10000000'))
  print('Trie grown')

  for number in numbers_gen('1000'):
    print(number, trie.find_closest(number), sep=', ')

if __name__ == '__main__':
  main()
