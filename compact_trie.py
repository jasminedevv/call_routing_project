from typing import Dict, Optional, Any, Tuple, Iterable
from trie import Trie, TrieNode

def find_uncommon_index(s1: str, s2: str) -> int:
  i = 0
  bounds = min(len(s1), len(s2))

  while i < bounds:
    if s1[i] != s2[i]:
      break

    i += 1

  return i

# TODO: Make find_closest and insert reuse more code
class CompactTrie(Trie):
  def find_closest(self, key: str) -> Any:
    node = self.root
    cur_value = None

    while node is not None:
      # Node with key exists
      if key in node.children:
        # Return value of child
        return node.children[key].value

      len_key = len(key)

      for prefix in node.children:
        len_prefix = len(prefix)

        # Non-prefixes
        if len_prefix > len_key or key[0] != prefix[0]:
          continue

        uncommon_index = find_uncommon_index(key, prefix)

        # Equivalent to key.startswith(prefix)
        if uncommon_index == len_prefix:
          # Search child node for matches
          node = node.children[prefix]

          # Store value for returning later
          if node.value is not None:
            cur_value = node.value

          # Strip key of match
          key = key[uncommon_index:]

          # Stop searching old prefixes
          break
        # Partial match
        else:
          # Return last match
          return cur_value
      # No potential prefixes found
      else:
        # Return last match
        return cur_value

    return cur_value

  def insert(self, key: str, value: Any) -> None:
    node = self.root

    while key:
      # Node with key already exists, set value
      if key in node.children:
        node.children[key].value = value
        return

      len_key = len(key)

      for prefix in node.children:
        len_prefix = len(prefix)

        # Non-prefixes
        if len_prefix > len_key or key[0] != prefix[0]:
          continue

        uncommon_index = find_uncommon_index(key, prefix)

        # Equivalent to key.startswith(prefix)
        if uncommon_index == len_prefix:
          # Search child node for matches
          node = node.children[prefix]

          # Strip key of match
          key = key[len_prefix:]

          # Stop searching old prefixes
          break
        # Partial match
        else:
          # Create new node to split previous values and new
          new_parent = TrieNode()

          # Split off new key and prefix for prev values
          split_prefix, split_key = prefix[:uncommon_index], prefix[uncommon_index:]

          # Move prev node to its new key on parent
          new_parent.children[split_key] = node.children.pop(prefix)
          # Create new node with value with substring of non-matching key
          new_parent.children[key[uncommon_index:]] = TrieNode(value)

          # Add parent keyed with matching string
          node.children[split_prefix] = new_parent

          # Node inserted, exit
          return
      # No potential prefixes found
      else:
        # Create new node with value with key
        node.children[key] = TrieNode(value)

        # Node inserted, exit
        return

if __name__ == "__main__":
  trie = CompactTrie()

  trie.insert('152', 1)
  trie.insert('1526', 2)
  trie.insert('1527', 3)

  assert trie.find_closest('15267') == 2
