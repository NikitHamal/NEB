# ---- Unit 1: health, illness, stress, crisis
_ev = [65, 38, 63, 29, 16]
chk("hr", (sum(_ev), round(65 / sum(_ev) * 100)), (211, 31))
chk("hr2", (100 + 38 + 29, 100 + 38 + 29 + 20 + 16, 6 * 7, round(13 / 42 * 100)), (167, 203, 42, 31))
T.update(u1_lcu=211, c1_lcu=203, c1_days=42, c1_visits=7)
