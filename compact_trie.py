from typing import Dict, Optional, Any, Tuple, Iterable
from utils import find_unshared
from trie import Trie, TrieNode

class CompactTrie(Trie):
  def find_closest(self, key: str) -> Any:
    node = self.root
    cur_value = None

    while node is not None:
      # Node with key exists -> return value
      if key in node.children:
        return node.children[key]

      for prefix in node.children:
        # Skip non-prefixes
        if len(prefix) > len(key):
          continue

        # Find the first unmatching index
        split_index = find_unshared(key, prefix)

        # No match -> continue searching
        if split_index == 0:
          continue
        # Equivalent to key.startswith(prefix) -> continue searching within this prefix
        elif split_index == len(prefix):
          node = node.children[prefix]
          if node.value is not None:
            cur_value = node.value

          # Strip key of match
          key = key[split_index:]
          break
        # No matches found -> return last match
        else:
          return cur_value
      # Exhausted all nodes -> return last match
      else:
        return cur_value

    return cur_value

  def insert(self, key: str, value: Any) -> None:
    node = self.root

    while 0 < len(key):
      # Node with key already exists, set value
      if key in node.children:
        node.children[key].value = value
        return

      for prefix in node.children:
        # Skip non-prefixes
        if len(prefix) > len(key):
          continue

        # Find the first unmatching index
        split_index = find_unshared(key, prefix)

        # No match -> continue searching for matching prefixes
        if split_index == 0:
          continue
        # Equivalent to key.startswith(prefix) -> continue searching within this prefix
        elif split_index == len(prefix):
          node = node.children[prefix]

          # Strip key of match
          key = key[split_index:]
          break
        # Partial match -> split
        else:
          new_parent = TrieNode()

          # Add prev values keyed with non-matching old prefix substring
          new_parent.children[prefix[split_index:]] = node.children.pop(prefix)
          # Add new value keyed with non-matching key substring
          new_parent.children[key[split_index:]] = TrieNode(value)

          # Add parent keyed with matching string
          node.children[prefix[:split_index]] = new_parent

          return
      # No full or partial matches -> create new node with key
      else:
        node.children[key] = TrieNode(value)
        return


if __name__ == "__main__":
  trie = CompactTrie()

  trie.insert('152', 1)
  trie.insert('1526', 2)
  trie.insert('1527', 3)

  assert trie.find_closest('15267') == 2
