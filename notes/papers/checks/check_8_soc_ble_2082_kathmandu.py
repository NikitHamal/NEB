# Sanity checks for 8-soc-ble-2082-kathmandu (marks per group, Q18 split)
A = [1] * 9
B = [3] * 7
C = [5] * 4
assert sum(A) == 9 and sum(B) == 21 and sum(C) == 20 and sum(A + B + C) == 50
assert 1 + 1 + 1 + 1 + 0.5 + 0.5 == 5      # Q18 split
assert 1 + 4 == 5                            # Q19 split
assert 2 + 2 + 1 == 5                        # Q20 split
print("8-soc-ble-2082-kathmandu: all checks pass")
