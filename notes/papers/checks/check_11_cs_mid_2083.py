import itertools
assert int("11001", 2) == 25 and hex(0b10101111) == "0xaf" and 2 ** 10 == 1024
assert int("110101", 2) + 0.5 + 0.125 == 53.625 and bin(156) == "0b10011100" and 128 + 16 + 8 + 4 == 156
assert (0b1011 + (0b1111 - 0b0110 + 1)) & 0b1111 == 0b0101 == 11 - 6
assert (~0b0110 & 0b1111) == 0b1001 and 0b1001 + 1 == 0b1010 and 0b1011 + 0b1010 == 0b10101
for a, b in itertools.product([0, 1], repeat=2):
    assert (1 - (a | b)) == ((1 - a) & (1 - b))                          # De Morgan
    f = ((1 - a) & b) | (a & (1 - b)) | (a & b)
    assert f == (a | b)                                                  # Q17a
    assert (a ^ b, a & b) == ((a + b) % 2, (a + b) // 2)                 # half adder
    assert (a | (a & b)) == a                                            # absorption
assert 10 + 6 * 4 + 2 * 8 == 50
print("11-cs-mid-2083: all checks pass")
