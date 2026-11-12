"""Numerical check for Accounting 2082 1041'K' (every figure in the solutions is asserted here)."""
# Q10
assert 80000 + 1200000 - 120000 == 1160000
# Q11
assert 18000 // 3000 == 6
# Q12
app = 9000*30; allot_app = 6000*30; refund = 2000*30
excess = 4000*30 - 3000*30            # 4000 applicants paid 1,20,000, 3000 shares accepted at 30
assert (app, allot_app, refund, excess) == (270000, 180000, 60000, 30000)
assert app == allot_app + refund + excess
allot_due = 6000*45; allot_cash = allot_due - excess
call_due = 6000*25; call_cash = 5500*25; arrear = 500*25
assert (allot_due, allot_cash, call_due, call_cash, arrear) == (270000, 240000, 150000, 137500, 12500)
# Q13
pc = 600000+200000+100000; sh = pc/90
assert (pc, sh, sh*100, sh*10) == (900000, 10000, 1000000, 100000)
assert 500*1000*1.05 == 525000 and 500*1000*0.90 == 450000
# Q14
gp = 900000+50000 - (40000+550000+60000); assert gp == 300000
exp = 80000+12000+35000+25000+(15000+3000)+30000; assert exp == 200000
npbt = gp+10000-exp; tax = npbt*0.25; assert (npbt, tax, npbt-tax) == (110000, 27500, 82500)
# Q15
gp15 = 450000-(200000+50000); dep = 350000*0.10
np15 = gp15 - (35000+12000+dep); assert (gp15, dep, np15) == (200000, 35000, 118000)
assets = 350000-dep+160000+40000+15000+(20000-12000); liab = 350000+70000+np15
assert assets == liab == 538000
# Q17 FIFO
units = 500+600+800; val = 500*20+600*22+800*23; assert (units, val) == (1900, 41600)
close = (units-1500)*23; assert (units-1500, close, val-close) == (400, 9200, 32400)
# Q18
assert 400*(50/10) == 2000
assert 25000+10000+5000-3000 == 37000
# Q20
ns = 780000-15000; npur = 330000+20000-28000
cogs = 40000+npur+60000-90000; gp20 = ns-cogs
assert (ns, npur, cogs, gp20) == (765000, 322000, 332000, 433000)
oi = 80000 + 7000 + 3000          # discount received + interest income (3,000 accrued)
opx = (20000+4000)+10000+20000+4000   # salary, carriage on sales, depreciation, bad-debt provision
fin = 12000+4000                  # 8% of 2,00,000 = 16,000
np20 = gp20+oi-opx-fin; assert (oi, opx, fin, np20) == (90000, 58000, 16000, 449000)
ta = 180000+100000+100000+90000+76000+3000+388000
tl = 200000+449000+200000+80000+4000+4000
assert ta == tl == 937000
# TB totals
assert sum([40000,330000,200000,100000,80000,20000,10000,15000,100000,12000,60000,20000,388000]) == 1375000
assert sum([28000,200000,7000,80000,780000,200000,80000]) == 1375000
# Q21
assert 40000+70000-20000 == 90000
cfo = 70000+80000+30000+2000+48000-20000; assert cfo == 210000
assert 300000-40000+320000-80000 == 500000
cfi = -100000-320000+40000; assert cfi == -380000
cff = 200000-50000-30000-20000+30000; assert cff == 130000
assert cfo+cfi+cff == 110000-150000 == -40000
# Q22
mat = 40000+400000+20000+10000-60000; prime = mat+200000+80000
fo = 20000+40000+20000; fac = prime+fo; works = fac+80000-20000
oo = 30000+25000+18000; cop = works+oo; cogs22 = cop+100000-70000
sd = 15000+10000; cos_ = cogs22+sd; profit = cos_*0.2; sales = cos_+profit
assert (mat, prime, fo, fac, works, oo, cop, cogs22, sd, cos_, profit, sales) == (410000, 690000, 80000, 770000, 830000, 73000, 903000, 933000, 25000, 958000, 191600, 1149600)
print("ALL CHECKS PASS")
