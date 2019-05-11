from trie_serializer import load
from data_reader import numbers_gen

def main():
  trie = load('10000000')

  print('Writing results to out.txt...')

  with open('out.txt', 'w') as f:
    for number in numbers_gen('10000'):
      f.write(number)
      f.write(', ')
      f.write(str(trie.find_closest(number) or 0))
      f.write('\n')

  print('Finished!')

if __name__ == '__main__':
  main()
