"""Numeric checks for Accounting 2080 (1041 'Q'). Run: python3 check_acc_2080_Q.py"""
# Q10 indirect CFO
assert 140000 + 40000 - 80000 == 100000
# Q11
assert 600000 // 30000 == 20
# Q12 shares
apps, allot_sh, face = 16000, 10000, 100
app_rec = apps * 30; assert app_rec == 480000
refund = 4000 * 30; assert refund == 120000
adj = 12000 * 30 - allot_sh * 30; assert adj == 60000
allot_due = allot_sh * 40; assert allot_due == 400000
adv = 400 * 40; assert adv == 16000
assert allot_due - adj + adv == 356000
assert allot_sh * 40 - adv == 384000
assert 30 + 30 + 40 == 100 and 30 + 40 + 40 == 110
assert allot_sh * 30 + allot_sh * 30 + allot_sh * 40 == 1000000
assert allot_sh * 10 == 100000
# Q13
assert 650000 + 340000 == 9000 * 110 == 990000
assert 9000 * 100 == 900000 and 9000 * 10 == 90000
assert 5000 * 100 * 0.07 == 35000 and 500000 * 0.95 == 475000
# Q14
dep = 0.15 * 400000; assert dep == 60000
pl_dr = 52000 + 96000 + 12000 + 22000 + 14000 + dep; assert pl_dr == 256000
np_ = 560000 + 12000 - pl_dr; assert np_ == 316000
div = 0.10 * 600000; assert div == 60000
assert 168000 + np_ == 484000 and 484000 - 55000 - div == 369000
# Q15
gp = 320000 - (20000 + 160000); assert gp == 140000
npf = gp - (96000 + 8000 + 12000); assert npf == 24000
assert 150000 + npf + 30000 == 204000 == (150000 - 12000) + 40000 + 22000 + (12000 - 8000)
# Q17(II) LIFO periodic
avail = 300 * 5 + 500 * 6 + 400 * 7; assert avail == 7300
close = 300 * 5; assert close == 1500 and avail - close == 5800 == 400 * 7 + 500 * 6
# Q18
assert 500 * 3 / 30 == 50 and 50 * 600 == 30000
assert 80000 + 15000 + 6000 - 5000 == 96000
# Q20
cogs = 20000 + 150000 + 25000 - 30000; assert cogs == 165000
gp = 400000 - cogs; assert gp == 235000
dep = 0.15 * 250000; assert dep == 37500
exp = 50000 + 15000 + 15000 + 12000 + 30000 + dep; assert exp == 159500
pbt = gp + 15000 - exp - 5000; assert pbt == 85500
tax = 0.10 * pbt; assert tax == 8550 and pbt - tax == 76950
assets = (250000 - dep) + 40000 + 30000 + 11000 + (25000 - 15000) + 100000
assert assets == 403500 == 250000 + 76950 + 50000 + 18000 + tax
assert 235000 - exp + 15000 == 90500 and 90500 - 5000 == pbt and 235000 - exp == 75500
wc = (30000 + 11000 + 10000 + 100000) - (18000 + tax); assert wc == 124450
assert 212500 + 40000 + wc == 376950 == 250000 + 76950 + 50000
# Q21 direct method
assert 29+2+89+50+80 == 250 and 32+3+62+68+90 == 255 and 15+30+25+180 == 250 and 10+20+30+195 == 255
dep21 = 180000 + 29000 - 195000; assert dep21 == 14000
assert 89000 + (100000 - 80000 - 26000 - dep21) - 7000 == 62000   # reconciles retained earnings
rec = 100000 + (15000 - 10000); assert rec == 105000
purch = 80000 + 20000 - 30000; assert purch == 70000
paid_sup = purch - (32000 - 29000); assert paid_sup == 67000
paid_exp = (26000 - 4000) - (3000 - 2000); assert paid_exp == 21000
cfo = rec - paid_sup - paid_exp; assert cfo == 17000
cfi = -29000
cff = (90000 - 80000) + (68000 - 50000) - 4000 - 7000; assert cff == 17000
assert cfo + cfi + cff == 5000 and 25000 + 5000 == 30000
# Q22
assert 100000 + 80000 == 180000 and 180000 + 60000 == 240000 and 240000 + 50000 == 290000 and 290000 + 30000 == 320000
fo = 40000 * 60000 / 80000; assert fo == 30000
works = 60000 + 40000 + fo; assert works == 130000
oh = works * 80000 / 240000; assert abs(oh - 43333.3333) < 0.01
cost = works + oh; assert abs(cost - 173333.3333) < 0.01
price = cost / 0.75; assert abs(price - 231111.11) < 0.01
assert abs(price * 0.25 - 57777.78) < 0.01
print("all Accounting 2080 checks pass")
