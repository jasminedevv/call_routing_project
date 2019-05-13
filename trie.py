from typing import Optional, Any, Tuple, Iterable, Dict, List

from utils import PickleMixin

class _Node(PickleMixin):
  __slots__ = 'children', 'value'

  def __init__(self, children_cap: int, value: Optional[str] = None) -> None:
    self.children: List[Optional['_Node']] = [None] * children_cap
    self.value: Any = value

class Trie(PickleMixin):
  __slots__ = 'root', 'mapper'

  def __init__(self, keys: bytes, items: Optional[Iterable[Tuple[bytes, Any]]] = None):
    self.mapper: Dict[int, int] = {char: index for index, char in enumerate(keys)}
    self.root: _Node = _Node(len(self.mapper))

    if items is not None:
      for key, value in items:
        self.insert(key, value)

  def find_closest(self, key: bytes) -> Any:
    node = self.root
    cur_val = node.value
    mapper = self.mapper

    for character in key:
      children = node.children
      index = mapper[character]

      child = children[index]

      if child is None:
        break

      node = child

      if node.value is not None:
        cur_val = node.value

    return cur_val

  def insert(self, key: bytes, value: Any) -> None:
    node = self.root
    mapper = self.mapper
    len_mapper = len(mapper)

    for character in key:
      children = node.children
      index = mapper[character]

      child = children[index]

      if child is None:
        child = children[index] = _Node(len_mapper)

      node = child

    node.value = value

if __name__ == "__main__":
  from string import digits
  trie = Trie(bytes(digits, 'utf-8'))

  trie.insert(b'152', 1)
  trie.insert(b'1526', 2)
  trie.insert(b'1527', 3)

  assert trie.find_closest(b'15267') == 2
