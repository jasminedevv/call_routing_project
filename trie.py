from typing import Dict, Optional, Any

class TrieNode:
  children: Dict[str, 'TrieNode']

  def __init__(self, value: Optional[str] = None) -> None:
    self.children = {}
    self.value = value

  def is_empty(self) -> bool:
    return len(self.children) == 0

  def has_child(self, character: str) -> bool:
    return character in self.children

  def __str__(self, depth=0):
    ret = str(self.value)

    for child in self.children:
      ret += '\n' + ' ' * depth + f'{child}: {self.children[child].__str__(depth + 1)}'

    return ret

class Trie:
  root: Optional[TrieNode] = None

  def is_empty(self) -> bool:
    return self.root is None

  def get_closest(self, string: str) -> Any:
    node = self.root
    current_closest = None

    for character in string:
      if node.value is not None:
        current_closest = node.value

      if character not in node.children:
        return current_closest

      node = node.children[character]

    return current_closest

  def insert(self, string: str, value: Any) -> None:
    if self.is_empty():
      self.root = TrieNode()

    node = self.root

    for character in string:
      if character not in node.children:
        node.children[character] = TrieNode()

      node = node.children[character]

    node.value = value

if __name__ == "__main__":
  trie = Trie()

  trie.insert('152', 1)
  trie.insert('1526', 2)
  trie.insert('1527', 3)
  print(trie.get_closest('15267'))
