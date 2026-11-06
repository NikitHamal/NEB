# ---- Unit 4: social psychology and health behaviour
_raw = [4, 5, 2, 4, 5, 1, 4, 2, 5, 4]
_sc = [6 - x if i in (2, 5, 7) else x for i, x in enumerate(_raw)]
chk("lik", (sum(_raw), _sc, sum(_sc), f"{sum(_sc) / 50 * 100:.0f}"), (36, [4, 5, 4, 4, 5, 5, 4, 4, 5, 4], 44, "88"))
chk("soc", (f"{12 * 0.37:.1f}", f"{26 / 40 * 100:.0f}", f"{(85 - 31) / 85 * 100:.1f}", f"{10 / 20 * 30:.0f}"), ("4.4", "65", "63.5", "15"))
chk("c4", (20 / 20 * 25, f"{20 * 15 * 365:,}", f"{20 * 15 * 365 * 10:,}", (6 + 2 + 2) * 7, (6 + 2 + 2)), (25, "109,500", "1,095,000", 70, 10))
T.update(u4_raw=36, u4_score=44, u4_pct=88, u4_cat="good", u4_asch="4.4", u4_mil="65", u4_m3="63.5", u4_m2="15", c4_py=25, c4_cost="109,500", c4_cost10="1,095,000", c4_patches=70, c4_weeks=10)
