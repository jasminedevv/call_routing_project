# Scenario 1
If our time constraint is 5 minutes, we decided to use our favorite tool: our text editors.

To find a number: open it in VS Code, ctrl+C, add a comma to the end, then delete numbers off the end until you find a match.

# Scenario 2
Load the carrier list into a dictionary. For a number we want to find, search the whole number and remove characters off the end (+ the trailing comma) until you find a match.

# Scenario 3
Search for the prefix in a radix trie and look up the end value in the carrier dictionary.

## Generate a Pickled Trie

You'll likely need 16GB of RAM

1. Download [route-costs-10000000.txt](https://www.dropbox.com/sh/tj6ppp6uwf12cce/AADje96PJhfsIXJEtP1OjwjFa?preview=route-costs-10000000.txt) into a folder called "data"
2. Run `python pick_trie.py 10000000`

Your pickled Trie should be available at 10000000.trie
