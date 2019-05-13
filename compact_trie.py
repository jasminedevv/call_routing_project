from typing import Dict, Optional, Any, Tuple, Iterable, Sequence

from utils import PickleMixin

def _find_uncommon_index(s1: Sequence, s2: Sequence) -> int:
  i = -1

  for i, (c1, c2) in enumerate(zip(s1, s2)):
    if c1 != c2:
      return i

  return i + 1

Key = Optional[Sequence]
Value = Any
Key_Value = Tuple[Key, Value]

class CompactTrie(PickleMixin):
  __slots__ = '_value', '_subtries'

  def __init__(self, value: Value = None, items: Optional[Iterable[Key_Value]] = None):
    self._value = value
    self._subtries: Optional[Dict[Sequence, 'CompactTrie']] = None

    if items is not None:
      for key, value in items:
        self[key] = value

  def __setitem__(self, key: Key, value: Value) -> None:
    # Falsy keys (empty sequences or None)
    if not key:
      self._value = value
      return

    # Trie has no subries
    if self._subtries is None:
      # Create dictionary with new subtrie at key
      self._subtries = { key: CompactTrie(value) }
      return
    # Trie has existing subrie
    elif key in self._subtries:
      # Set existing subtree at key
      self._subtries[key][None] = value
      return
    # Search for prefixes
    else:
      len_key = len(key)

      for prefix in self._subtries:
        len_prefix = len(prefix)

        # [0, min(len(key), len(prefix))]
        uncommon_index = _find_uncommon_index(key, prefix)

        # Not a prefix
        if uncommon_index == 0:
          continue
        # Prefix fully prefixes key
        elif uncommon_index == len_prefix:
          # Recursively set value in subtrie with rest of key
          self._subtries[prefix][key[len_prefix:]] = value
          return
        # Key fully prefixes prefix
        elif uncommon_index == len_key:
          new_trie = CompactTrie(value)

          new_trie._subtries = {
            # Move old trie
            prefix[uncommon_index:]: self._subtries.pop(prefix)
          }

          # Add a new trie as a subtrie with the old trie as a subtrie of it
          self._subtries[key] = new_trie
          return
        # Key and prefix partially prefix each other
        else:
          # Create new node to split previous values and new
          new_parent = CompactTrie()

          new_prefix = prefix[:uncommon_index]

          rest_old_key = prefix[uncommon_index:]
          rest_new_key = key[uncommon_index:]

          new_parent._subtries = {
            # Move old subtrie
            rest_old_key: self._subtries.pop(prefix),
            rest_new_key: CompactTrie(value)
          }

          # Add parent keyed with matching string
          self._subtries[new_prefix] = new_parent
          return
      # No matches
      else:
        # Create new subtrie
        self._subtries[key] = CompactTrie(value)
        return

  def find_closest(self, key: Key, current: Value = None) -> Value:
    current = self._value if self._value is not None else current

    if not key:
      return current

    if self._subtries is None:
      return current
    elif key in self._subtries:
      return self._subtries[key].find_closest(None, current)
    else:
      for prefix in self._subtries:
        len_prefix = len(prefix)

        # [0, min(len(key), len(prefix))]
        uncommon_index = _find_uncommon_index(key, prefix)

        # Not a prefix
        if uncommon_index == 0:
          continue
        # Prefix fully prefixes key
        elif uncommon_index == len_prefix:
          # Recursively get value in subtrie with rest of key
          return self._subtries[prefix].find_closest(key[len_prefix:], current)
        else:
          return current
      # No matches
      else:
        return current

if __name__ == '__main__':
  trie = CompactTrie()

  trie[b'152'] = 1
  trie[b'1526'] = 2
  trie[b'1527'] = 3

  assert trie.find_closest(b'15267') == 2
