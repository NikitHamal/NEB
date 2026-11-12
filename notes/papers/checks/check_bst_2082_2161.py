import re, os
rev_rooms = 12 * 3000 * 365 * 60 // 100
assert rev_rooms == 7884000
assert rev_rooms + 2500000 == 10384000
assert 4000000 + 1500000 + 1200000 + 300000 + 1000000 == 8000000
assert 5000000 + 3000000 == 8000000
assert 3000000 * 12 // 100 == 360000
exp = 4200000 + 1300000 + 900000 + 400000 + 360000 + 700000 + 600000
assert exp == 8460000
assert 10384000 - exp == 1924000
assert 1924000 + 700000 == 2624000
assert abs(8000000 / 2624000 - 3.0) < 0.06
# marks
assert 1 + 2 + 1 + 1 + 1.5 + 1.5 == 8
src = open(os.path.join(os.path.dirname(__file__), '..', 'content', '12-bst-2082-2161.md')).read()
assert len(re.findall(r'^@q \d+', src, re.M)) == 11 + 8 + 3
assert sorted(map(int, re.findall(r'^@s (\d+)', src, re.M))) == list(range(1, 23))
print('12-bst-2082-2161: all checks pass')
