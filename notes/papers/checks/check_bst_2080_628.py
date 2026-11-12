import re, os
assert 8 * 8 == 64 and 2 * 18 == 36 and 64 + 36 == 100
assert 2 + 6 == 8 and 4 + 5 + 9 == 18 and 6 + 12 == 18 and 4 + 7 + 7 == 18
src = open(os.path.join(os.path.dirname(__file__), '..', 'content', '12-bst-2080-628.md')).read()
assert len(re.findall(r'^@q \d+', src, re.M)) == 10 + 3
assert sorted(map(int, re.findall(r'^@s (\d+)', src, re.M))) == list(range(1, 14))
assert 'TODO' not in src and 'FIXME' not in src
print('12-bst-2080-628: all checks pass')
