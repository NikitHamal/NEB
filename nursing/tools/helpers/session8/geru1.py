# ---- Unit 1: ageing, Nepal demography, CGA
_share = 2.97 / 29.16 * 100; _rise = (2.97 - 2.154) / 2.154 * 100
_t14 = math.log(14 / _share) / math.log(1.0329 / 1.0092)
chk("dem", (round(_share, 1), round(_rise, 1), round(70 / 3.29, 1), round(_t14, 1)), (10.2, 37.9, 21.3, 13.7))
_b = [10, 0, 5, 5, 10, 5, 10, 10, 10, 5]
chk("cga", (sum([0, 1, 1, 1, 0, 1]), sum(_b), round(4 / 6, 2), sum([0, 1, 1, 1, 1])), (4, 70, 0.67, 4))
chk("m", (round(2.97 / 29.16 * 100, 1), 4 / 8, round(60 * 60 / (72 * 1.2), 1)), (10.2, 0.5, 41.7))
_cg = (140 - 78) * 46 / (72 * 1.1) * 0.85
chk("c", (round(6 / 52 * 100, 1), round(46 / 1.5 ** 2, 1), round(_cg, 1), round(4 / 7, 2), 30 * 46, round(1.2 * 46)), (11.5, 20.4, 30.6, 0.57, 1380, 55))
T.update(u1_old="2.97", u1_share="10.2", u1_rise="37.9", u1_dbl="21.3", u1_t14="13.7", u1_katz=4, u1_barthel=70, u1_gait="0.67", u1_tug=14, u1_fried=4,
         u1_m1="10.2", u1_m2="0.50", u1_m3="41.7", c_loss="11.5", c_bmi="20.4", c_crcl="30.6", c_gait="0.57", c_kcal="1,380", c_prot=55)
