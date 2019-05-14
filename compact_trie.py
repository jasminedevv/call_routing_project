from typing import Dict, Optional, Any, Tuple, Iterable,Sequence, List, Hashable

from utils import PickleMixin

def _find_uncommon_index(s1: Sequence, s2: Sequence) -> int:
  i = -1

  for i, (c1, c2) in enumerate(zip(s1, s2)):
    if c1 != c2:
      return i

  return i + 1

Key = Sequence[Hashable]
Value = Any
Key_Value = Tuple[Key, Value]
Mapper = Dict[Hashable, int]

class CompactTrie(PickleMixin):
  __slots__ = '_key', '_value', '_buckets', '_mapper'

  def __init__(
    self,
    key: Optional[Key] = None,
    value: Optional[Value] = None,
    keys: Optional[Key] = None,
    mapper: Optional[Mapper] = None,
    items: Optional[Iterable[Key_Value]] = None,
  ):
    self._mapper: Mapper

    if mapper:
      self._mapper = mapper
    elif keys:
      self._mapper = {key: index for index, key in enumerate(keys)}
    else:
      raise ValueError('mapper or keys must be provided')

    self._key = key
    self._value = value
    self._buckets: Optional[List[Optional['CompactTrie']]] = None

    if items:
      for key, value in items:
        self[key] = value

  def __setitem__(self, key: Key, value: Value) -> None:
    # Falsy keys (empty sequences or None)
    if not key:
      self._value = value
      return

    mapper = self._mapper
    buckets = self._buckets
    index = mapper[key[0]]

    # Trie has no subries
    if not self._buckets:
      # Create bucket with new subtrie at key
      buckets = self._buckets = [None] * len(mapper)
      buckets[index] = CompactTrie(key, value, mapper=mapper)
      return
    # Check existing
    else:
      subtrie = buckets[index]

      if subtrie:
        if not subtrie._key:
          raise KeyError(f'Subtrie at {index} has no key')

        prefix: Key = subtrie._key
        len_key = len(key)
        len_prefix = len(prefix)

        # [0, min(len(key), len(prefix))]
        uncommon_index = _find_uncommon_index(key, prefix)

        # Not a prefix
        if uncommon_index == 0:
          raise KeyError(f'Subtrie with key={key} misplaced at bucket {index}')
        # Prefix fully prefixes key
        elif uncommon_index == len_prefix:
          # Recursively set value in subtrie with rest of key
          subtrie[key[len_prefix:]] = value
          return
        # Key fully prefixes prefix
        elif uncommon_index == len_key:
          parent_prefix = prefix[:uncommon_index]
          old_prefix = prefix[uncommon_index:]

          old_index = mapper[old_prefix[0]]

          parent = CompactTrie(parent_prefix, value, mapper=mapper)
          parent._buckets = [None] * len(mapper)
          subtrie._key = old_prefix

          # Move old subtrie to parent and parent where it was
          parent._buckets[old_index], buckets[index] = subtrie, parent
          return
        # Key and prefix partially prefix each other
        else:
          parent_prefix = prefix[:uncommon_index]
          old_prefix = prefix[uncommon_index:]
          new_prefix = key[uncommon_index:]

          old_index = mapper[old_prefix[0]]
          new_index = mapper[new_prefix[0]]

          # Create new node to split previous values and new
          parent = CompactTrie(parent_prefix, mapper=mapper)
          parent._buckets = [None] * len(mapper)
          subtrie._key = old_prefix

          # Add parent keyed with matching string
          parent._buckets[old_index] = subtrie
          parent._buckets[new_index] = CompactTrie(new_prefix, value, mapper=mapper)

          buckets[index] = parent
          return
      # No existing subtrie
      else:
        # Create new subtrie
        buckets[index] = CompactTrie(key, value, mapper=mapper)
        return

  def find_closest(self, key: Key, current: Value = None) -> Value:
    current = self._value if self._value is not None else current

    if not key:
      return current

    if self._buckets is None:
      return current
    else:
      mapper = self._mapper
      buckets = self._buckets
      index = mapper[key[0]]
      subtrie = buckets[index]

      if subtrie:
        if not subtrie._key:
          raise KeyError(f'Subtrie at {index} has no key')

        prefix: Key = subtrie._key

        len_prefix = len(prefix)

        # [0, min(len(key), len(prefix))]
        uncommon_index = _find_uncommon_index(key, prefix)

        # Not a prefix
        if uncommon_index == 0:
          raise KeyError(f'Subtrie with key={key} misplaced at bucket {index}')
        # Prefix fully prefixes key
        elif uncommon_index == len_prefix:
          # Recursively get value in subtrie with rest of key
          return subtrie.find_closest(key[len_prefix:], current)
        else:
          return current
      # No matches
      else:
        return current

if __name__ == '__main__':
  from string import digits

  PHONE_KEYS = bytes('+' + digits, 'utf-8')
  trie = CompactTrie(keys=PHONE_KEYS)

  trie[b'152'] = 1
  trie[b'1526'] = 2
  trie[b'1527'] = 3

  assert trie.find_closest(b'15267') == 2
