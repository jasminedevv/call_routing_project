def find_unshared(s1: str, s2: str) -> int:
  for i, (c1, c2) in enumerate(zip(s1, s2)):
    if c1 != c2:
      return i

  return min(len(s1), len(s2))
