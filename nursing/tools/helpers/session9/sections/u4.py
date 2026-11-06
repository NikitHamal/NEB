# ---- Unit 4: anxiety, OCD, trauma, dissociative
_gad = sum([2, 2, 3, 2, 1, 1, 2]); _yb = sum([3, 2, 3, 2, 3, 3, 2, 3, 2, 3]); _pcl = sum([3] * 8 + [2] * 8 + [1] * 4)
chk("u4a", (round(9200 * 0.03), round(5888 * 0.028), _gad, 2.0 * 10, 2 * 10, _yb, 25 * 4, f"{25 * 4 * 7 / 60:.1f}", f"{25 * 4 / 960 * 100:.1f}", _pcl), (276, 165, 13, 20.0, 20, 26, 100, "11.7", "10.4", 44))
_bpm = 60 // (4 + 6)
chk("case4", (sum([3, 2, 3, 2, 1, 2, 2]), 4 + 6, _bpm, _bpm * 5, round((28 - _bpm) / 28 * 100), 7 * 1 + 21 * 2, 3 * 8, 3 * 8 // 2), (15, 10, 6, 30, 79, 49, 24, 12))
T.update(u4_adult=276, u4_teen=165, u4_gad=13, u4_dz=20, u4_tabs=20, u4_ybocs=26, u4_wash=100, u4_week="11.7", u4_share="10.4", u4_pcl=44,
         c4_gad=15, c4_cyc=10, c4_bpm=6, c4_in5=30, c4_fall=79, c4_sert=49, c4_att=24, c4_goal=12)
