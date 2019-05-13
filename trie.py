from typing import Optional, Any, Tuple, Iterable, Dict, List, Sequence, Hashable

from utils import PickleMixin

Key = Iterable[Hashable]
Value = Optional[Any]
Mapper = Dict[Hashable, int]

class Trie(PickleMixin):
  __slots__ = '_children', '_value', '_mapper'

  def __init__(
    self,
    value: Value = None,
    items: Optional[Iterable[Tuple[Key, Value]]] = None,
    keys: Optional[Key] = None,
    mapper: Optional[Mapper] = None,
  ) -> None:
    self._mapper: Mapper

    if mapper:
      self._mapper = mapper
    elif keys:
      self._mapper = {item: index for index, item in enumerate(keys)}
    else:
      raise ValueError('keys or mapper must be provided')

    self._children: Optional[List[Optional['Trie']]] = None
    self._value = value

    if items is not None:
      for key, value in items:
        self[key] = value

  def __setitem__(self, key: Key, value: Value) -> None:
    iter_key = iter(key)

    try:
      mapper = self._mapper
      index = mapper[next(iter_key)]
      children = self._children

      if not children:
        children = self._children = [None] * len(mapper)

      child = children[index]

      if not child:
        child = children[index] = Trie(mapper=self._mapper)

      child[iter_key] = value
    except StopIteration:
      self._value = value

  def find_closest(self, key: Key, current: Optional[Value] = None) -> Optional[Value]:
    current = self._value or current
    iter_key = iter(key)

    try:
      mapper = self._mapper
      index = mapper[next(iter_key)]
      children = self._children

      if not children:
        return current

      child = children[index]

      if not child:
        return current

      return child.find_closest(iter_key, current)
    except StopIteration:
      return current

if __name__ == "__main__":
  from string import digits
  trie = Trie(keys=bytes(digits, 'utf-8'))

  trie[b'152'] = 1
  trie[b'1526'] = 2
  trie[b'1527'] = 3

  assert trie.find_closest(b'15267') == 2
