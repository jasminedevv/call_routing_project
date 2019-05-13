class PickleMixin:
  def __getstate__(self):
    return tuple(getattr(self, attr) for attr in self.__slots__)

  def __setstate__(self, state):
    for attr, value in zip(self.__slots__, state):
      setattr(self, attr, value)
