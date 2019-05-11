from memory_profiler import memory_usage
# from memory_profiler import profile

from trie_serializer import load
from data_reader import numbers_gen

# @profile
def main():
  trie = load('10000000')

  with open('out.txt', 'w') as f:
    for number in numbers_gen('1000'):
      f.write(number)
      f.write(', ')
      f.write(str(trie.find_closest(number)))
      f.write('\n')

if __name__ == '__main__':
  print(max(memory_usage(proc=main)))
