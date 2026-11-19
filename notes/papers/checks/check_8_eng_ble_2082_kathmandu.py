# Sanity checks for 8-eng-ble-2082-kathmandu (marks, pie chart percentages, word counts)
from fractions import Fraction as F
marks = [F(5), F(5), F(5), F(10), F(5), F(5), F(10), F(5, 2), F(5, 2)]
assert len(marks) == 9 and sum(marks) == 50
# Q6: Dang 2071 crop production pie chart percentages
crops = {"Wheat": 20, "Mustard": 30, "Maize": 15, "Barley": 10, "Paddy": 25}
assert sum(crops.values()) == 100
assert crops["Mustard"] + crops["Paddy"] + crops["Wheat"] == 75
assert max(crops, key=crops.get) == "Mustard" and min(crops, key=crops.get) == "Barley"
assert 10 * F(1, 2) == 5 and 5 * F(1, 2) == F(5, 2)
print("8-eng-ble-2082-kathmandu: all checks pass")
