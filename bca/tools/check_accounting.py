#!/usr/bin/env python3
"""BCA 403 Financial Accounting: independent verification of every figure in the book.
Keys out_* are exact lines the executed python blocks must print; other keys are numbers quoted in prose.
Independent methods: per-account balances (not delta tracking), closed forms with Fraction, column sums.
    python3 bca/tools/check_accounting.py --print | --fill unit-*.md | --verify unit-*.md"""
import sys
from fractions import Fraction as F
from decimal import Decimal as D, ROUND_HALF_UP
from tokcommon import run
T = {}
m = lambda x: f"{int(x):,}"
m2 = lambda x: f"{(D(F(x).numerator) / D(F(x).denominator)).quantize(D('0.01'), ROUND_HALF_UP):,}"
# ---- unit 1: account balances after six transactions
cash, furn, stock, credit = 500000, 0, 0, 0
furn = 120000; cash -= 120000                      # furniture for cash
stock = 80000; credit = 80000                      # goods on credit
cash += 60000; stock -= 40000                      # cash sale, cost 40000
cash -= 10000                                      # rent
cash -= 50000; credit -= 50000                     # pay creditor
A = cash + furn + stock; L = credit; E = 500000 + (60000 - 40000) - 10000
assert (A, L, E) == (540000, 30000, 510000) and A == L + E
T["out_eq"] = "step 6: A=540000 L=30000 E=510000"
T["u1_A"], T["u1_L"], T["u1_E"] = m(A), m(L), m(E)
T["u1_ex"] = m(900000 - 350000); assert T["u1_ex"] == "550,000"
# ---- unit 2: journal, VAT 13%, TDS 10% on rent
purch, vat_in = 100000, 100000 * 13 // 100
sales, vat_out = 200000, 200000 * 13 // 100
tds = 50000 // 10
bal = {"Cash": 500000 - (50000 - tds) + 150000 - (purch + vat_in), "Debtors": (sales + vat_out) - 150000, "Purchases": purch,
       "VAT Input": vat_in, "Rent": 50000}
cr = {"Capital": 500000, "Creditors (Himal)": 0, "Sales": sales, "VAT Output": vat_out, "TDS Payable": tds}
assert sum(bal.values()) == sum(cr.values()) == 731000
T["out_tb"] = "total debits 731000, total credits 731000"
T["out_cash2"] = "Cash: Dr 492000"; T["out_deb2"] = "Debtors: Dr 76000"
T["u2_vatnet"] = m(vat_out - vat_in); T["u2_cash"] = m(bal["Cash"]); T["u2_deb"] = m(bal["Debtors"])
T["u2_tds"] = m(tds); T["u2_net"] = m(50000 - tds); T["u2_tot"] = m(731000); T["u2_inv"] = m(purch + vat_in)
assert (T["u2_vatnet"], T["u2_cash"], T["u2_deb"]) == ("13,000", "492,000", "76,000")
# ---- unit 3: triple column cash book, sales book, suspense
cdr = [20000, 15000, 30000, 5000]; ccr = [10000, 4000]                  # cash column
bdr = [80000, 10000]; bcr = [24000, 5000]                              # bank column
cb, bb = sum(cdr) - sum(ccr), sum(bdr) - sum(bcr); assert (cb, bb) == (56000, 61000)
T["out_cb"] = "closing cash 56000, closing bank 61000"; T["u3_cash"], T["u3_bank"] = m(cb), m(bb)
T["u3_da"], T["u3_dr"] = "500", "1,000"
inv1, inv2 = 50000 * 90 // 100, 30000 * 90 // 100; net = inv1 + inv2; v = net * 13 // 100
assert (net, v) == (72000, 9360); T["u3_sales"], T["u3_vat"], T["u3_gross"] = m(net), m(v), m(net + v)
T["out_sales"] = "sales book: net 72000, VAT 9360, gross 81360"
d_, c_ = 842500, 841600; diff = d_ - c_; assert diff == 900 and diff % 9 == 0 and abs(5400 - 4500) == 900
T["out_susp"] = "difference 900, divisible by 9: True"; T["out_susp0"] = "suspense after rectification: 0"; T["u3_diff"] = "900"
# ---- unit 4: bank reconciliation
cbk = 45200 - 350 + 1200 + 6000 - 3000; pb = cbk + 12000 - 8500
assert (cbk, pb) == (49050, 52550) and pb - 12000 + 8500 == cbk
T["out_brs1"] = "adjusted cash book balance: 49050"; T["out_brs2"] = "reconciled bank balance: 49050"
T["u4_cb"], T["u4_pb"], T["u4_unadj"] = m(cbk), m(pb), "45,200"
# ---- unit 5: depreciation and inventory
slm = F(600000 - 60000, 5); assert slm == 108000
T["out_slm"] = "SLM annual charge: 108000"; T["u5_slm"] = m(slm)
close5 = F(600000) * F(3, 4) ** 5; T["out_wdv"] = f"year 5 closing WDV: {float(close5):.2f}"; T["u5_wdv5"] = m2(close5)
assert T["u5_wdv5"] == "142,382.81"; T["u5_dep1"] = m(600000 // 4); T["u5_dep2"] = "112,500"
bv3 = 600000 - 3 * slm; gain = 300000 - bv3; assert (bv3, gain) == (276000, 24000)
T["out_disp"] = "gain on disposal: 24000"; T["u5_bv3"], T["u5_gain"] = m(bv3), m(gain)
fifo_c = 100 * 50 + 180 * 55; fifo_e = 20 * 55 + 150 * 60; assert (fifo_c, fifo_e) == (14900, 10100) and fifo_c + fifo_e == 25000
T["out_fifo"] = "FIFO: COGS 14900 closing 10100"; T["u5_fc"], T["u5_fe"] = m(fifo_c), m(fifo_e)
avg = F(25000, 450); wc, we = avg * 280, avg * 170
T["out_wa"] = f"Weighted average: COGS {float(wc):.2f} closing {float(we):.2f}"
T["u5_wc"], T["u5_we"], T["u5_avg"] = m2(wc), m2(we), f"{float(avg):.2f}"
T["u5_gpf"], T["u5_gpw"] = m(22400 - fifo_c), m2(22400 - wc); assert T["u5_gpw"] == "6,844.44"
# ---- unit 6: final accounts (hand-built closed form)
cogs = 40000 + 600000 - 10000 + 5000 + 30000 - 70000; netsales = 1000000 - 20000
gp = netsales - cogs; exp = (110000 + 10000) + (60000 - 5000) + 25000 + 8000 + 2 * 200000 // 100
npf = gp + 6000 - exp; assert (cogs, gp, exp, npf) == (595000, 385000, 212000, 179000)
cap = 500000 + npf - 30000; tot_a = 275000 + 70000 + 196000 + 5000 + 223000; tot_l = cap + 110000 + 10000
assert tot_a == tot_l == 769000
T["out_gp"] = "gross profit: 385000"; T["out_np"] = "net profit: 179000"; T["out_bs"] = "balance sheet total: 769000 = 769000"
T["u6_cogs"], T["u6_gp"], T["u6_np"], T["u6_exp"], T["u6_cap"], T["u6_bs"] = m(cogs), m(gp), m(npf), m(exp), m(cap), m(tot_a)
tax = F(npf) * F(25, 100); T["u6_tax"], T["u6_pat"] = m(tax), m(npf - tax); assert (T["u6_tax"], T["u6_pat"]) == ("44,750", "134,250")
T["out_co"] = "company: tax 44750, profit after tax 134250"
# ---- unit 7: ratios
ca, cl, eq = 70000 + 196000 + 5000 + 223000, 120000, cap
q = F(196000 + 223000, cl)
T["out_cr"] = f"current ratio 4.12, quick ratio {float(q):.2f}"; assert f"{float(q):.2f}" == "3.49" and f"{float(F(ca, cl)):.2f}" == "4.12"
T["out_de"] = f"debt to equity {float(F(cl, eq)):.2f}"
gm, nm = F(gp, netsales), F(npf, netsales); at = F(netsales, tot_a); em = F(tot_a, eq); roe = F(npf, eq)
assert nm * at * em == roe
T["out_pm"] = f"gross margin {float(gm*100):.2f}%, net margin {float(nm*100):.2f}%"
T["out_roe"] = f"ROE {float(roe*100):.2f}% = {float(nm):.4f} x {float(at):.4f} x {float(em):.4f}"
T["out_inv"] = f"inventory turnover {float(F(cogs, 55000)):.2f} times, {float(F(365*55000, cogs)):.1f} days"
T["out_dd"] = f"debtor days {float(F(200000*365, netsales)):.1f}"
T["u7_roa"] = f"{float(F(npf, tot_a)*100):.2f}"; T["u7_roe"] = f"{float(roe*100):.2f}"; T["u7_at"] = f"{float(at):.4f}"
T["out_sql"] = "sqlite trial balance: debits=731000 credits=731000 balanced=True"
assert (T["u7_roa"], T["u7_roe"]) == ("23.28", "27.58")
if __name__ == "__main__":
    run(T, sys.argv[1:])
