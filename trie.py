from typing import (Optional,
  Any,
  Tuple,
  Iterable,
  Dict,
  List,
  Hashable,
)

from utils import PickleMixin

Key = Iterable[Hashable]
Value = Optional[Any]
Mapper = Dict[Hashable, int]

class Trie(PickleMixin):
  __slots__ = '_subtries', '_value', '_mapper'

  def __init__(
    self,
    keys: Optional[Key] = None,
    items: Optional[Iterable[Tuple[Key, Value]]] = None,
    _value: Value = None,
    _mapper: Optional[Mapper] = None,
  ) -> None:
    self._mapper: Mapper

    if _mapper:
      self._mapper = _mapper
    elif keys:
      self._mapper = {item: index for index, item in enumerate(keys)}
    else:
      raise ValueError('keys or _mapper must be provided')

    self._subtries: Optional[List[Optional['Trie']]] = None
    self._value = _value

    if items is not None:
      for key, value in items:
        self[key] = value

  def __setitem__(self, key: Key, value: Value) -> None:
    """Recursively sets the value of a key within the trie."""
    iter_key = iter(key)

    try:
      mapper = self._mapper
      index = mapper[next(iter_key)]
      subtries = self._subtries

      if not subtries:
        subtries = self._subtries = [None] * len(mapper)

      child = subtries[index]

      if not child:
        child = subtries[index] = Trie(_mapper=self._mapper)

      child[iter_key] = value
    except StopIteration:
      self._value = value

  def find_closest(self, key: Key, _current: Optional[Value] = None) -> Optional[Value]:
    """Finds the value of the longest matching prefix of a key.

    Args:
      key: The key to match the longest prefix of.
      _current: The longest value in the parent. Defaults to None.

    Returns:
        The value of the longest match in this subtrie or its subtries.
    """
    _current = self._value or _current
    iter_key = iter(key)

    try:
      mapper = self._mapper
      index = mapper[next(iter_key)]
      subtries = self._subtries

      if not subtries:
        return _current

      child = subtries[index]

      if not child:
        return _current

      return child.find_closest(iter_key, _current)
    except StopIteration:
      return _current

if __name__ == "__main__":
  from string import digits
  trie = Trie(keys=bytes(digits, 'utf-8'))

  trie[b'152'] = 1
  trie[b'1526'] = 2
  trie[b'1527'] = 3

  assert trie.find_closest(b'15267') == 2
