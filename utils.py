from typing import Iterable, Generator, Tuple
from data_reader import Route

class PickleMixin:
  def __getstate__(self):
    return tuple(getattr(self, attr) for attr in self.__slots__)

  def __setstate__(self, state):
    for attr, value in zip(self.__slots__, state):
      setattr(self, attr, value)

def decode_route_prefix(routes: Iterable[Route]) -> Generator[Tuple[str, float], None, None]:
  for prefix, cost in routes:
    yield (prefix.decode(), cost)
