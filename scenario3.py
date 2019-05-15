from trie_serializer import load, grow_and_dump
from data_reader import numbers_gen

NUM_ROUTES = '10000000'

def main():
  try:
    trie = load(NUM_ROUTES)
  except OSError:
    print('Trie doesn\'t exist!')

    trie = grow_and_dump(NUM_ROUTES)

  def get_price(number):
    return trie.find_closest(number) or 0

  print('Getting prices and writing to scenario3.out...')

  with open('scenario3.out', 'w') as f:
    for number in numbers_gen('10000'):
      f.write(number.decode())
      f.write(', ')
      f.write(str(get_price(number)))
      f.write('\n')

  print('Done!')

if __name__ == '__main__':
  main()
