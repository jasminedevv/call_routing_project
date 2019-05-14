from typing import (
  Sequence,
  Hashable,
  Any,
  Dict,
  Optional,
  Iterable,
  Tuple,
  List,
)

from utils import PickleMixin

def _find_uncommon_index(s1: Sequence, s2: Sequence) -> int:
  """Finds the index of the first uncommon value between two sequences."""
  i = -1

  for i, (c1, c2) in enumerate(zip(s1, s2)):
    if c1 != c2:
      return i

  return i + 1

Key = Sequence[Hashable]
Value = Any
Mapper = Dict[Hashable, int]

class CompactTrie(PickleMixin):
  __slots__ = '_key', '_value', '_buckets', '_mapper'

  def __init__(
    self,
    keys: Optional[Key] = None,
    items: Optional[Iterable[Tuple[Key, Value]]] = None,
    _mapper: Optional[Mapper] = None,
    _key: Optional[Key] = None,
    _value: Optional[Value] = None,
  ) -> None:
    """Initializes the Trie

    Args:
        keys: All potential items in keys that are added. Defaults to None.
        items: Key value pairs to automatically add. Defaults to None.
        _mapper: A premade mapper passed down from the parent. Defaults to None.
        _key: The key of in relation to its parent. Defaults to None.
        _value: The value in relation to its parent. Defaults to None.

    Raises:
        ValueError: Neither keys nor _mapper were provided.
    """
    self._mapper: Mapper

    if _mapper:
      self._mapper = _mapper
    elif keys:
      self._mapper = {key: index for index, key in enumerate(keys)}
    else:
      raise ValueError('mapper or keys must be provided')

    self._key = _key
    self._value = _value
    self._buckets: Optional[List[Optional['CompactTrie']]] = None

    if items:
      for key, value in items:
        self[key] = value

  def __setitem__(self, key: Key, value: Value) -> None:
    """Recursively sets the value of a key within the trie.

    Raises:
        KeyError: A subtrie is misplaced or has no key, this is a bug.
    """
    # Falsy keys (empty sequences or None)
    if not key:
      self._value = value
      return

    mapper = self._mapper
    buckets = self._buckets
    index = mapper[key[0]]

    # Trie has no subtries
    if not self._buckets:
      # Create bucket with new subtrie at key
      buckets = self._buckets = [None] * len(mapper)
      buckets[index] = CompactTrie(_key=key, _value=value, _mapper=mapper)
      return
    # Check existing
    else:
      subtrie = buckets[index]

      if subtrie:
        prefix: Optional[Key] = subtrie._key

        if not prefix:
          raise KeyError(f'Subtrie at {index} has no key')

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

          parent = CompactTrie(_key=parent_prefix, _value=value, _mapper=mapper)
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
          parent = CompactTrie(_key=parent_prefix, _mapper=mapper)
          parent._buckets = [None] * len(mapper)
          subtrie._key = old_prefix

          # Add parent keyed with matching string
          parent._buckets[old_index] = subtrie
          parent._buckets[new_index] = CompactTrie(_key=new_prefix, _value=value, _mapper=mapper)

          buckets[index] = parent
          return
      # No existing subtrie
      else:
        # Create new subtrie
        buckets[index] = CompactTrie(_key=key, _value=value, _mapper=mapper)
        return

  def find_closest(self, key: Key, _current: Value = None) -> Value:
    """Finds the value of the longest matching prefix.

    Args:
        key: The key to match the longest prefix of.
        _current: The longest value in the parent. Defaults to None.

    Raises:
        KeyError: A subtrie is misplaced or has no key.

    Returns:
        The value of the longest match in this subtrie or its subtries.
    """
    _current = self._value if self._value is not None else _current

    if not key:
      return _current

    if self._buckets is None:
      return _current
    else:
      mapper = self._mapper
      buckets = self._buckets
      index = mapper[key[0]]
      subtrie = buckets[index]

      if subtrie:
        prefix: Optional[Key] = subtrie._key

        if not prefix:
          raise KeyError(f'Subtrie at {index} has no key')

        len_prefix = len(prefix)

        # [0, min(len(key), len(prefix))]
        uncommon_index = _find_uncommon_index(key, prefix)

        # Not a prefix
        if uncommon_index == 0:
          raise KeyError(f'Subtrie with key={key} misplaced at bucket {index}')
        # Prefix fully prefixes key
        elif uncommon_index == len_prefix:
          # Recursively get value in subtrie with rest of key
          return subtrie.find_closest(key[len_prefix:], _current)
        else:
          return _current
      # No matches
      else:
        return _current

if __name__ == '__main__':
  from string import digits

  PHONE_KEYS = bytes('+' + digits, 'utf-8')
  trie = CompactTrie(keys=PHONE_KEYS)

  trie[b'152'] = 1
  trie[b'1526'] = 2
  trie[b'1527'] = 3

  assert trie.find_closest(b'15267') == 2
