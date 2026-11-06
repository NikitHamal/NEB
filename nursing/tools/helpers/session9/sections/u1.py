# ---- Unit 1: foundations
_life, _cur, _teen = round(9200 * 0.10), round(9200 * 0.043), round(5888 * 0.052)
chk("nmhs", (_life, _cur, _teen, round(1000 * 0.23), round(1000 * 0.77), round(2_000_000 / 100_000 * 1.5)), (920, 396, 306, 230, 770, 30))
_exp = [100 - 7 * i for i in range(1, 6)]
_said = [93, 86, 78, 71, 64]; _p = 100; _sc = 0
for _s in _said:
    _sc += (_s == _p - 7); _p = _s
chk("s7", (_exp, _sc, 24 * 60 // 30, 24 * 60 // 15), ([93, 86, 79, 72, 65], 4, 48, 96))
chk("case1", (f"{48 / 1.68 ** 2:.1f}", f"{30 * 48:,}", 3 * 7), ("17.0", "1,440", 21))
T.update(u1_life=920, u1_cur=396, u1_teen=306, u1_treated=230, u1_untreated=770, u1_gap=77, u1_beds=30, u1_s7=4, u1_exp="93, 86, 79, 72, 65",
         u1_obs30=48, u1_obs15=96, c_bmi="17.0", c_fluid="1,440", c_meals=21)
