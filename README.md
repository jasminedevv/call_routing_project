# Scenario 1
If our time constraint is 5 minutes, we decided to use our favorite tool: our text editors.

To find a number: open it in VS Code, ctrl+C, add a comma to the end, then delete numbers off the end until you find a match.

# Scenario 2
Load the carrier list into a dictionary. For a number we want to find, search the whole number and remove characters off the end (+ the trailing comma) until you find a match.

# Scenario 3

Search for the prefix in a radix trie and look up the end value in the carrier dictionary.

## Requirements

- Python 3
- [These files](https://www.dropbox.com/sh/tj6ppp6uwf12cce/AADje96PJhfsIXJEtP1OjwjFa) a folder called "data"
- 2 GB spare RAM (the 10M file is taxing)

## Running

1. Run `python trie_serializer.py dump 10000000`
2. Run `python scenario3.py`

Results will be in a file called "out.txt"

# Scenario 4
Exactly like scenario 2 except with a database. It's a lot slower than our scenario 3 solution but it was much quicker to make. It also wasn't able to handle the 10000000 file without exceeding Heroku's limits so it uses the 106000 file.
You can try it yourself here: [call-api-jasmine-dacio-django.herokuapp.com](https://call-api-jasmine-dacio-django.herokuapp.com) and view the repo [here](https://github.com/lacunahag/call_routing_django_api)
