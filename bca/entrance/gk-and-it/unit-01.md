---
subject: General Knowledge and IT
grade: BCA
unit: 1
title: Nepal: First Persons, Geography, Government and Culture
hours: 3
area: General Knowledge
---

About five of the ten GK-and-IT questions are general knowledge, and Nepal gets the larger share. The Dean's Office model asked the date of the constitution (3 Ashwin 2072), the deepest river of Nepal, the first prime minister and the author of *Basain*. General knowledge cannot be derived, so this chapter is a compact, *dated* fact base. **Facts marked "as of" are current affairs: check the news in the weeks before the exam.**

::: key What the paper asks from this chapter
- **Firsts**: first people, first constitution, first prime ministers and presidents.
- **Geography records**: highest, longest, deepest, largest.
- **Government**: provinces, districts, local levels, parliament.
- **Culture**: writers and works, national symbols, heritage sites.
:::

## 1.1 First persons and firsts in Nepal

| Item | Answer |
|---|---|
| First to climb Everest (29 May 1953) | Tenzing Norgay Sherpa with Edmund Hillary |
| First Nepali woman on Everest (1993) | Pasang Lhamu Sherpa |
| Most Everest summits (as of 17 May 2026) | Kami Rita Sherpa, 32 |
| First constitution | Nepal Sarkar Vaidhanik Kanoon, 1948 (2004 BS) |
| First president (2008) | Ram Baran Yadav |
| Second president | Bidya Devi Bhandari (2015–2023) |
| Third president (since March 2023) | Ram Chandra Paudel |
| First national park | Chitwan (1973) |
| Joined the UN | 14 December 1955 |
| First woman prime minister (interim, Sept 2025) | Sushila Karki |

::: caution Who was Nepal's "first prime minister"?
Sources differ, so read the options carefully. **Bhimsen Thapa** (Mukhtiyar from 1806) is widely counted as the first. **Jung Bahadur Rana** founded the hereditary Rana prime ministership in 1846. **Matrika Prasad Koirala** was the first prime minister after the end of Rana rule in 1951. The Dean's Office model offers all three names, so a "first PM" question depends on the key the paper sets.
:::

```photogrid label="1.1" cols="2" ratio="1.25" caption="Two famous firsts. (a) Tenzing Norgay Sherpa and Edmund Hillary, the first climbers confirmed on the summit of Everest on 29 May 1953. (b) Prithvi Narayan Shah of Gorkha, who began the unification of Nepal and took Kathmandu in 1768, in a portrait by Amar Chitrakar."
@ photo id="bcagk/tenzing" cap="Tenzing Norgay (left) and Edmund Hillary, 1953"
focus 0.5 0.5
@ photo id="bcagk/pns" cap="Prithvi Narayan Shah, founder of modern Nepal"
focus 0.5 0.3
```

```svgfig label="1.1" caption="Nepal's political history to scale (one tick = 10 years). The hereditary Rana prime ministership lasted 105 years, from the Kot massacre of 1846 to the revolution of 1951. Only the dates that the entrance paper has asked are shown."
ev = [(1768, "Unification: Kathmandu\ntaken by Prithvi Narayan", "up", 1), (1846, "Jung Bahadur Rana\nstarts Rana rule", "dn", 1),
      (1948, "First constitution\n(Vaidhanik Kanoon)", "up", 3), (1951, "Rana rule ends\n(7 Falgun 2007)", "dn", 2),
      (1955, "Nepal joins\nthe UN", "up", 2), (1973, "Chitwan, first\nnational park", "dn", 1),
      (1990, "People's movement,\nmulti-party system", "up", 1), (2008, "Republic declared\n(15 Jestha 2065)", "dn", 2),
      (2015, "Present constitution\n(3 Ashwin 2072)", "up", 3), (2025, "September protests,\ninterim government", "up", 2),
      (2026, "Election 5 March;\nBalendra Shah PM", "dn", 1)]
yrs = [e[0] for e in ev]; assert yrs == sorted(yrs)
assert 1951 - 1846 == 105
f = Fig(780, 330); X0, X1, A0, A1 = 50, 730, 1760, 2030; ax = lambda y: X0 + (y - A0) * (X1 - X0) / (A1 - A0)
Y = 170
f.line(X0, Y, X1, Y, color=NAVY, sw=3)
for y in range(1760, 2031, 10):
    f.line(ax(y), Y - (7 if y % 50 == 0 else 4), ax(y), Y + (7 if y % 50 == 0 else 4), color=SLATE, sw=1)
    if y % 50 == 0 and y not in (2050,): f.text(ax(y), Y + 20, str(y), size=10, color=SLATE)
f.box(ax(1846), Y - 5, ax(1951) - ax(1846), 10, "", fill="#fecaca", stroke=RED, r=2)
f.text((ax(1846) + ax(1951)) / 2, Y + 36, "Rana era: 105 years", size=9.5, color=RED, bold=True)
for yr, lab, d, lv in ev:
    x = ax(yr); sgn = -1 if d == "up" else 1
    yy = Y + sgn * (28 + lv * 34)
    f.line(x, Y, x, yy, color=TEAL, sw=1.1)
    f.circle(x, Y, 4.5, fill=TEAL, stroke=TEAL)
    an = "end" if x > 690 else ("start" if x < 90 else "middle")
    f.text(x, yy + (-18 if d == "up" else 14) - (0 if d == "up" else 0), lab, size=10, color=NAVY, bold=True, anchor=an)
    f.text(x, yy + (-4 if d == "up" else 0), "", size=1)
```

## 1.2 Geography of Nepal: largest, longest, highest, deepest

| Record | Answer |
|---|---|
| Highest peak | Everest (Sagarmatha), 8,848.86 m (Nepal–China survey, 2020) |
| Third highest in the world | Kanchenjunga, 8,586 m |
| Peaks above 8,000 m wholly or partly in Nepal | 8 of the world's 14 |
| Longest river in Nepal | Karnali |
| Largest river by volume | Koshi (Sapta Koshi) |
| Largest lake | Rara (Mugu) |
| Deepest lake | Shey Phoksundo (Dolpa), about 145 m |
| Highest-altitude lake | Tilicho, 4,919 m |
| Lowest point | Kechana Kawal, Jhapa (about 60 m) |
| Area / population (2021 census) | 147,516 km² / 29.16 million |
| UNESCO World Heritage Sites | 4: Kathmandu Valley, Sagarmatha NP, Chitwan NP, Lumbini |
| Birthplace of Buddha | Lumbini |

Question banks often quote Karnali as both the longest and the deepest river of Nepal; Koshi carries the most water.

```photogrid label="1.2" cols="4" ratio="1.1" caption="Four of the eight Nepali peaks above 8,000 m: (a) Everest, 8,848.86 m, the highest point on Earth; (b) Kanchenjunga, 8,586 m, third highest in the world and on the Nepal-India border; (c) Dhaulagiri I, 8,167 m, seventh highest; (d) Annapurna I, 8,091 m, the first 8,000 m peak ever climbed (France, 1950)."
@ photo id="bcagk/everest" cap="Everest (Sagarmatha), 8,848.86 m"
focus 0.4 0.4
@ photo id="bcagk/kanchen" cap="Kanchenjunga, 8,586 m"
focus 0.5 0.7
@ photo id="bcagk/dhaula" cap="Dhaulagiri I, 8,167 m"
focus 0.4 0.5
@ photo id="bcagk/annap" cap="Annapurna I, 8,091 m"
focus 0.5 0.5
```

```svgfig label="1.2" caption="The eight Nepali eight-thousanders ranked by height (the bar axis starts at 8,000 m, so the bars exaggerate the gaps). Everest exceeds the eighth, Annapurna I, by 757.86 m. K2 (second) and Nanga Parbat (ninth) are not in Nepal, which is why Kanchenjunga is 3rd in the world but 2nd in Nepal."
pk = [("Everest", 8848.86, 1), ("Kanchenjunga", 8586, 3), ("Lhotse", 8516, 4), ("Makalu", 8485, 5),
      ("Cho Oyu", 8188, 6), ("Dhaulagiri I", 8167, 7), ("Manaslu", 8163, 8), ("Annapurna I", 8091, 10)]
assert len(pk) == 8 and [p[1] for p in pk] == sorted([p[1] for p in pk], reverse=True)
assert [p[2] for p in pk] == sorted(p[2] for p in pk)
gap = round(pk[0][1] - pk[-1][1], 2); assert gap == 757.86
f = Fig(760, 330); L, R = 170, 540; sc = lambda h: L + (h - 8000) * (R - L) / 900
f.text(380, 20, "Height above sea level (m), axis starts at 8,000 m", size=10, color=NAVY, bold=True)
for h in range(8000, 8901, 100):
    f.line(sc(h), 34, sc(h), 300, color="#e2e8f0", sw=1); f.text(sc(h), 314, f"{h:,}", size=9.5, color=SLATE)
for i, (n, h, r) in enumerate(pk):
    y = 40 + i * 32
    f.box(L, y, sc(h) - L, 22, "", fill=("#fecaca" if i == 0 else "#dbeafe"), stroke=(RED if i == 0 else NAVY), r=3)
    f.text(L - 8, y + 11, n, size=10.5, color=NAVY, bold=True, anchor="end", vmid=True)
    f.text(sc(h) + 6, y + 11, f"{h:,} m   (world #{r})", size=9.5, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="1.3" caption="Nepal's three ecological belts, computed from the area of 147,516 km2 using the commonly quoted shares (about 23 percent Terai, 42 percent Hill, 35 percent Mountain; textbooks differ by a point or two). The belt is narrow from south to north, so altitude climbs from about 60 m to 8,848.86 m in under 200 km."
share = {"Terai": 23, "Hill": 42, "Mountain": 35}; assert sum(share.values()) == 100
A = 147516; km = {k: round(A * v / 100) for k, v in share.items()}
f = Fig(780, 330)
f.text(390, 18, "Share of Nepal's area", size=10.5, color=NAVY, bold=True)
x = 60; cols = {"Terai": "#bbf7d0", "Hill": "#fde68a", "Mountain": "#bfdbfe"}
for k in ("Terai", "Hill", "Mountain"):
    w = share[k] / 100 * 660
    f.box(x, 30, w, 40, f"{k} {share[k]}%\n{km[k]:,} km2", fill=cols[k], stroke=SLATE, size=10, bold=True, r=3); x += w
f.text(60, 92, "south", size=9, color=SLATE, anchor="start"); f.text(720, 92, "north", size=9, color=SLATE, anchor="end")
pts = [(60, 300), (170, 285), (215, 250), (260, 250), (330, 215), (400, 190), (470, 200), (520, 150), (580, 110), (640, 128), (700, 130), (720, 300)]
f.poly(pts, fill="#e2e8f0", stroke=SLATE, sw=1.6)
f.poly([(60, 300), (170, 285), (172, 300)], fill="#86efac", stroke=TEAL, sw=1)
f.text(115, 322, "Terai\n60-300 m flat plains", size=9, color=TEAL, bold=True)
f.text(240, 237, "Churia (Siwalik)", size=9, color=SLATE, bold=True)
f.text(345, 176, "Mahabharat range\nand mid-hills", size=9, color=SLATE, bold=True)
f.text(500, 128, "High Himal\nEverest 8,848.86 m", size=9, color=NAVY, bold=True)
f.line(60, 300, 720, 300, color=SLATE, sw=1.2)
f.text(60, 118, "Schematic cross-section, not to scale", size=9, color=SLATE, italic=True, anchor="start")
```

```photogrid label="1.3" cols="3" ratio="1.35" caption="Three lakes that GK papers love: (a) Rara in Mugu, the largest lake of Nepal; (b) Shey Phoksundo in Dolpa, the deepest; (c) Tilicho in Manang, one of the highest lakes in the world at 4,919 m."
@ photo id="bcagk/rara" cap="Rara Lake, Mugu: largest"
focus 0.5 0.6
@ photo id="bcagk/phoksundo" cap="Shey Phoksundo, Dolpa: deepest, about 145 m"
focus 0.5 0.55
@ photo id="bcagk/tilicho" cap="Tilicho Lake, Manang: 4,919 m"
fit 1.35
focus 0.4 0.5
```

```svgfig label="1.4" caption="Altitude of four lakes drawn to scale against Everest's 8,848.86 m. Tilicho sits at more than half of Everest's height; Phewa, the lake of Pokhara, is lower than the top of many hills in Kathmandu Valley."
lk = [("Phewa (Pokhara)", 742), ("Rara (Mugu)", 2990), ("Shey Phoksundo (Dolpa)", 3611), ("Tilicho (Manang)", 4919)]
assert [l[1] for l in lk] == sorted(l[1] for l in lk)
ratio = round(4919 / 8848.86 * 100, 1); assert ratio == 55.6
f = Fig(760, 300); base = 262; top = 30; sc = lambda h: base - h / 8848.86 * (base - top)
f.line(70, base, 740, base, color=SLATE, sw=1.4)
f.box(90, sc(8848.86), 60, base - sc(8848.86), "", fill="#fecaca", stroke=RED, r=3)
f.text(120, sc(8848.86) - 8, "Everest 8,848.86 m", size=9.5, color=RED, bold=True)
x = 230
for n, h in lk:
    f.box(x, sc(h), 70, base - sc(h), "", fill="#bfdbfe", stroke=NAVY, r=3)
    f.text(x + 35, sc(h) - 8, f"{h:,} m", size=10, color=NAVY, bold=True)
    f.text(x + 35, base + 16, n.replace(" (", "\n("), size=9, color=SLATE, bold=True)
    x += 125
f.text(380, 20, f"Tilicho is {ratio}% of Everest's height", size=10.5, color=NAVY, bold=True)
```

## 1.3 Constitution, federal structure and prime ministers

- Monarchy abolished and Nepal declared a republic on **15 Jestha 2065 (28 May 2008)**. The present constitution was promulgated on **3 Ashwin 2072 (20 September 2015)**. Democracy Day is **7 Falgun**.
- **7 provinces, 77 districts, 753 local levels** (6 metropolitan, 11 sub-metropolitan, 276 municipalities, 460 rural municipalities).
- Federal parliament: **House of Representatives 275** (165 first-past-the-post + 110 proportional) and **National Assembly 59**.
- Provincial capitals: Koshi — Biratnagar; Madhesh — Janakpur; Bagmati — Hetauda; Gandaki — Pokhara; Lumbini — Deukhuri; Karnali — Birendranagar (Surkhet); Sudurpashchim — Godawari.
- **Current affairs (as of 27 March 2026).** After the September 2025 protests, Sushila Karki led an interim government. In the general election of 5 March 2026 the Rastriya Swatantra Party (RSP) won 182 of 275 seats, and **Balendra Shah** (aged 35) was sworn in as Prime Minister on 27 March 2026 by President Ram Chandra Paudel.

```svgfig label="1.5" caption="Nepal's federal structure with every sum checked in the code: 6 + 11 + 276 + 460 = 753 local levels; 165 + 110 = 275 House seats; 8 members from each of 7 provinces plus 3 nominated = 59 National Assembly seats."
loc = [("Metropolitan cities", 6), ("Sub-metropolitan cities", 11), ("Municipalities", 276), ("Rural municipalities", 460)]
assert sum(n for _, n in loc) == 753 and 165 + 110 == 275 and 8 * 7 + 3 == 59
f = Fig(780, 340)
f.box(300, 10, 180, 44, "Federation of Nepal\n(1 centre)", fill="#dbeafe", stroke=NAVY, size=11, bold=True)
f.box(40, 90, 330, 54, "Federal Parliament\nHouse of Representatives 275 + National Assembly 59", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(410, 90, 330, 54, "7 provinces\nProvincial assemblies and governments", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(340, 54), (205, 90)], color=NAVY); f.arrow([(440, 54), (575, 90)], color=NAVY)
f.box(40, 175, 150, 56, "House 275\n165 FPTP + 110 PR", fill="#f0fdfa", stroke=TEAL, size=10, bold=True)
f.box(210, 175, 160, 56, "National Assembly 59\n56 elected + 3 nominated", fill="#f0fdfa", stroke=TEAL, size=9, bold=True)
f.arrow([(115, 144), (115, 175)], color=TEAL); f.arrow([(290, 144), (290, 175)], color=TEAL)
f.box(410, 175, 330, 40, "77 districts (14 + 8 + 13 + 11 + 12 + 10 + 9)", fill="#fffbeb", stroke=AMBER, size=10, bold=True)
f.arrow([(575, 144), (575, 175)], color=AMBER)
f.box(410, 238, 330, 30, "753 local levels", fill="#fef3c7", stroke=AMBER, size=11, bold=True)
f.arrow([(575, 215), (575, 238)], color=AMBER)
tot = 753; x = 410
cols = ["#fecaca", "#fed7aa", "#bfdbfe", "#bbf7d0"]
for (n, c), col in zip(loc, cols):
    w = max(c / tot * 330, 14)
    f.box(x, 280, w, 22, "", fill=col, stroke=SLATE, r=2, sw=1); x += w
f.text(410, 318, "Bar width = share of 753:  rural 460 (61%)  municipal 276 (37%)  sub-metro 11  metro 6", size=8.5, color=SLATE, anchor="start")
f.text(40, 270, "Local levels in order:", size=10, color=NAVY, bold=True, anchor="start")
for i, ((n, c), col) in enumerate(zip(loc, cols)):
    f.box(40, 280 + i * 14, 10, 10, "", fill=col, stroke=SLATE, r=1, sw=0.8); f.text(56, 286 + i * 14, f"{n}: {c}", size=9, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="1.6" caption="Schematic map of the seven provinces from west to east. Box widths are proportional to the number of districts (77 in all); Madhesh is the southern Terai strip below Bagmati and Koshi. Capitals are as named in the 2015 constitution notices."
pv = [("Sudurpashchim", "Godawari", 9), ("Karnali", "Birendranagar", 10), ("Lumbini", "Deukhuri", 12),
      ("Gandaki", "Pokhara", 11), ("Bagmati", "Hetauda", 13), ("Koshi", "Biratnagar", 14)]
mad = ("Madhesh", "Janakpur", 8)
assert sum(p[2] for p in pv) + mad[2] == 77
f = Fig(780, 270); x = 30; unit = 720 / 69; pos = {}
cols = ["#fecaca", "#fed7aa", "#fef08a", "#bbf7d0", "#bfdbfe", "#e9d5ff"]
f.text(390, 18, "WEST", size=9, color=SLATE, bold=True, anchor="middle"); 
for (n, c, d), col in zip(pv, cols):
    w = d * unit; pos[n] = (x, w)
    f.box(x, 40, w, 110, f"{n}\n\n{c}\n{d} districts", fill=col, stroke=SLATE, size=9.5, bold=True, r=4)
    x += w
f.text(30, 32, "West", size=10, color=NAVY, bold=True, anchor="start"); f.text(750, 32, "East", size=10, color=NAVY, bold=True, anchor="end")
bx = pos["Bagmati"][0] + 20; bw = mad[2] * unit + 60
f.box(bx, 175, bw, 70, f"{mad[0]}\n{mad[1]}\n{mad[2]} districts", fill="#fbcfe8", stroke=SLATE, size=10, bold=True, r=4)
f.text(bx - 12, 210, "Terai strip:", size=9.5, color=NAVY, bold=True, anchor="end")
f.text(bx + bw + 12, 210, "= 77 - 69 = 8 districts", size=9, color=SLATE, anchor="start")
```

```photogrid label="1.4" cols="3" ratio="1.3" caption="Heritage and government buildings behind the GK questions: (a) the Pashupatinath temple area, Kathmandu Valley World Heritage Site; (b) the Maya Devi Temple at Lumbini, birthplace of Gautam Buddha; (c) Singha Durbar seen from the air in 1915, now the seat of the federal government secretariat."
@ photo id="bcagk/pashu" cap="Pashupatinath temple area, Kathmandu"
focus 0.6 0.5
@ photo id="bcagk/lumbini" cap="Maya Devi Temple, Lumbini (UNESCO 1997)"
call 0.45 0.90 0.36 0.55 "Maya Devi Temple"
call 0.60 0.12 0.45 0.25 "Sacred pond"
@ photo id="bcagk/singha" cap="Singha Durbar, 1915 (public domain)"
focus 0.5 0.5
```

## 1.4 Literature, art, national symbols and Miss Nepal

| Writer | Work / title |
|---|---|
| Bhanubhakta Acharya | *Aadikavi*, first poet; Nepali *Ramayana* |
| Laxmi Prasad Devkota | *Mahakavi*; *Muna Madan* |
| Lil Bahadur Chhetri | novel *Basain* |
| Parijat | novel *Shirishko Phool* |
| Lekhnath Paudyal | *Kavishiromani* |

National symbols: bird — **Danphe** (Himalayan monal); flower — **rhododendron (lali guras)**; animal — **cow**; colour — **crimson**. Miss Nepal winners change every year: learn the latest from the news; the books do not carry a fixed list.

```photogrid label="1.5" cols="3" ratio="1.25" caption="National symbols and the first national park: (a) the Danphe (Himalayan monal), national bird; (b) the lali guras (Rhododendron arboreum), national flower, in bloom; (c) a one-horned rhinoceros in Chitwan National Park, Nepal's first national park (1973)."
@ photo id="bcagk/monal" cap="Danphe: national bird"
focus 0.5 0.5
@ photo id="bcagk/rhodo" cap="Lali guras: national flower"
focus 0.5 0.5
@ photo id="bcagk/chitwan" cap="Rhino, Chitwan NP (1973)"
focus 0.5 0.5
```

## 1.5 Eight traps in Nepal GK questions

Most marks are lost by mixing two similar facts, not by never having seen the fact. These eight traps appear again and again in TU entrance papers and in the Dean's Office model.

1. **Two dates, two events.** *3 Ashwin 2072 (20 September 2015)* is the date of the present constitution, while *15 Jestha 2065 (28 May 2008)* is the date Nepal became a republic. A question that says "republic" wants Jestha; a question that says "constitution" wants Ashwin. Write both beside each other once and you will never swap them.
2. **Three possible "first prime ministers".** Bhimsen Thapa (Mukhtiyar from 1806), Jung Bahadur Rana (the first Rana, 1846) and Matrika Prasad Koirala (first after Rana rule, 1951) can each be called "first". Read the other options: if only one of the three names is present, choose it. If two are present, look for words such as "Rana" or "after 1951" in the stem.
3. **Longest is not largest.** Karnali is the longest river inside Nepal, but Koshi (Sapta Koshi) carries the largest volume of water. The same pair of words appears for lakes: Rara is the *largest* by area, Phoksundo is the *deepest*, and Tilicho is the *highest*. Match the adjective to the record before you read the options.
4. **Everest has two numbers.** The old figure was 8,848 m (Indian survey, 1954), and the figure agreed by Nepal and China in December 2020 is 8,848.86 m. If both appear as options, the current answer is 8,848.86 m. If only 8,848 appears, it is still the intended answer.
5. **"Eight of the 14" is wholly or partly.** Nepal has eight peaks above 8,000 m wholly or partly inside its border: Everest, Kanchenjunga, Lhotse, Makalu, Cho Oyu, Dhaulagiri, Manaslu and Annapurna I. Several are shared with China (Tibet) or India (Sikkim), so a question about peaks "fully in Nepal" has a smaller answer: Dhaulagiri I, Manaslu and Annapurna I.
6. **Count the levels correctly.** Nepal has 7 provinces, 77 districts and 753 local levels, and the House of Representatives has 275 seats, not 334 (the old Constituent Assembly had 601). Remember the sums 6 + 11 + 276 + 460 = 753 and 165 + 110 = 275. A wrong option such as 744 or 334 is a number from an older system.
7. **Bikram Sambat to AD.** For dates from mid-April to December add 57 years to the AD year to get the BS year (2015 AD gives 2072 BS), and for January to mid-April add 56 years. Use this to check that a date is possible, for example that 2072 BS cannot be 2008 AD.
8. **"As of" facts expire.** The record number of Everest summits, the name of the Prime Minister and the winner of an election change every few months. Check the news in the last four weeks before the exam and read the dated lines in this chapter first.

### 1.5.1 Worked checks: do the sum before you choose

**Q. How many members of the National Assembly are elected by the provincial assemblies and local representatives?** (a) 59 (b) 56 (c) 8 (d) 3

**Answer: (b).** The National Assembly has 8 members from each of the 7 provinces, so 8 x 7 = 56 are elected. The President nominates 3 more on the Government's recommendation, giving 56 + 3 = 59. Option (a) is the total, option (c) is the number per province and option (d) is the nominated number: the paper often hides the right answer among its own sub-totals.

**Q. Which lake is the highest in altitude?** (a) Rara (b) Phewa (c) Shey Phoksundo (d) Tilicho

**Answer: (d).** Phewa is 742 m, Rara is 2,990 m, Phoksundo is about 3,611 m and Tilicho is 4,919 m (Fig 1.4). The adjective "highest" asks for altitude, so the answer is Tilicho. If the stem said "largest" the answer would be Rara and if it said "deepest" it would be Shey Phoksundo.

## Formula and fact sheet

| Quick facts | |
|---|---|
| Constitution | 3 Ashwin 2072 |
| Provinces / districts / local levels | 7 / 77 / 753 |
| House / National Assembly | 275 / 59 |
| Everest | 8,848.86 m |
| UN membership | 1955 |
| Longest / deepest lake / largest lake | Karnali / Phoksundo / Rara |

## Chapter summary

- Constitution: 3 Ashwin 2072; republic: 15 Jestha 2065; Democracy Day: 7 Falgun.
- 7, 77, 753; 275 + 59.
- Everest 8,848.86 m; Kanchenjunga is third highest.
- Karnali is longest, Koshi largest by volume, Rara largest lake, Phoksundo deepest.
- Balendra Shah became Prime Minister on 27 March 2026.

## Practice questions

**Set A — Recall (20 questions)**

1. The present constitution of Nepal was promulgated on
   (a) 2 Ashwin 2072 (b) 3 Ashwin 2072 (c) 4 Ashwin 2072 (d) 15 Jestha 2065
2. The height of Mount Everest recognised by Nepal and China is
   (a) 8,848 m (b) 8,611 m (c) 8,848.86 m (d) 8,586 m
3. The number of provinces in Nepal is
   (a) 7 (b) 5 (c) 6 (d) 9
4. The number of districts in Nepal is
   (a) 75 (b) 70 (c) 80 (d) 77
5. The number of local levels in Nepal is
   (a) 744 (b) 750 (c) 753 (d) 760
6. The House of Representatives has how many members?
   (a) 165 (b) 275 (c) 334 (d) 110
7. The first President of Nepal was
   (a) Bidya Devi Bhandari (b) Ram Chandra Paudel (c) Girija Prasad Koirala (d) Ram Baran Yadav
8. Democracy Day in Nepal is observed on
   (a) 7 Falgun (b) 15 Jestha (c) 3 Ashwin (d) 1 Baisakh
9. Nepal became a member of the United Nations in
   (a) 1945 (b) 1955 (c) 1965 (d) 1975
10. The national bird of Nepal is
    (a) peacock (b) eagle (c) Danphe (d) crow
11. The national flower of Nepal is
    (a) lotus (b) rose (c) marigold (d) rhododendron
12. The author of *Muna Madan* is
    (a) Laxmi Prasad Devkota (b) Bhanubhakta Acharya (c) Lil Bahadur Chhetri (d) Parijat
13. The *Aadikavi* of Nepali literature is
    (a) Laxmi Prasad Devkota (b) Lekhnath Paudyal (c) Bhanubhakta Acharya (d) Siddhicharan Shrestha
14. The author of the novel *Basain* is
    (a) Gopal Prasad Rimal (b) Ramlal Joshi (c) Lokendra Bahadur Chand (d) Lil Bahadur Chhetri
15. Along with Edmund Hillary, the first to climb Everest (1953) was
    (a) Pasang Lhamu Sherpa (b) Tenzing Norgay Sherpa (c) Kami Rita Sherpa (d) Appa Sherpa
16. The largest lake of Nepal is
    (a) Rara (b) Phewa (c) Begnas (d) Tilicho
17. The first national park of Nepal is
    (a) Sagarmatha (b) Langtang (c) Bardiya (d) Chitwan
18. The birthplace of Gautam Buddha is
    (a) Janakpur (b) Pokhara (c) Lumbini (d) Bhaktapur
19. The number of UNESCO World Heritage Sites in Nepal is
    (a) 4 (b) 2 (c) 6 (d) 10
20. Nepal Rastra Bank is Nepal's
    (a) largest commercial bank (b) central bank (c) stock exchange (d) insurance board

::: note Answers and explanations — Set A
**1.** (b) — 3 Ashwin 2072 (20 September 2015).
**2.** (c) — announced in December 2020 after a joint survey.
**3.** (a) — seven provinces.
**4.** (d) — 77 districts.
**5.** (c) — 753 local levels.
**6.** (b) — 275 (165 FPTP + 110 PR).
**7.** (d) — Ram Baran Yadav, 2008.
**8.** (a) — 7 Falgun marks the end of Rana rule (1951).
**9.** (b) — 14 December 1955.
**10.** (c) — Danphe, the Himalayan monal.
**11.** (d) — rhododendron (lali guras).
**12.** (a) — Laxmi Prasad Devkota.
**13.** (c) — Bhanubhakta Acharya.
**14.** (d) — Lil Bahadur Chhetri.
**15.** (b) — Tenzing Norgay, 29 May 1953.
**16.** (a) — Rara Lake in Mugu.
**17.** (d) — Chitwan, established in 1973.
**18.** (c) — Lumbini, a UNESCO World Heritage Site.
**19.** (a) — Kathmandu Valley, Sagarmatha, Chitwan and Lumbini.
**20.** (b) — Nepal Rastra Bank is the central bank (1956).
:::

**Set B — Understanding (12 questions)**

1. The National Assembly of Nepal has
   (a) 275 members (b) 110 members (c) 165 members (d) 59 members
2. How many members of the House of Representatives are elected by first-past-the-post?
   (a) 110 (b) 165 (c) 100 (d) 175
3. Who is known as the *Mahakavi* of Nepali literature?
   (a) Bhanubhakta Acharya (b) Parijat (c) Laxmi Prasad Devkota (d) Lekhnath Paudyal
4. Nepal's first constitution was
   (a) Nepal Sarkar Vaidhanik Kanoon, 1948 (b) the Constitution of 1959 (c) the Constitution of 1962 (d) the Interim Constitution of 2007
5. Matrika Prasad Koirala was
   (a) the first Rana prime minister (b) the first prime minister after Rana rule ended in 1951 (c) the first president (d) the first Mukhtiyar
6. Bhimsen Thapa is widely counted as Nepal's first
   (a) president (b) king (c) prime minister after 1951 (d) Mukhtiyar and prime minister
7. Nepal's first woman prime minister (interim, September 2025) was
   (a) Sushila Karki (b) Bidya Devi Bhandari (c) Sahana Pradhan (d) Onsari Gharti
8. Balendra Shah was sworn in as Prime Minister in
   (a) 2023 (b) 2025 (c) 2026 (d) 2024
9. The general election of 5 March 2026 was won by
   (a) the Nepali Congress (b) CPN (UML) (c) the Maoist Centre (d) the Rastriya Swatantra Party
10. The deepest lake of Nepal is
    (a) Rara (b) Shey Phoksundo (c) Phewa (d) Gosaikunda
11. The longest river of Nepal is the
    (a) Koshi (b) Gandaki (c) Karnali (d) Bagmati
12. The lowest point of Nepal, Kechana Kawal, is in
    (a) Jhapa (b) Kailali (c) Parsa (d) Rautahat

::: note Answers and explanations — Set B
**1.** (d) — 59 members.
**2.** (b) — 165 FPTP and 110 proportional seats.
**3.** (c) — Devkota; Bhanubhakta is the Aadikavi.
**4.** (a) — issued under Padma Shamsher in 1948.
**5.** (b) — he led the first government after 1951.
**6.** (d) — Mukhtiyar from 1806; often counted as the first prime minister.
**7.** (a) — Sushila Karki.
**8.** (c) — 27 March 2026.
**9.** (d) — RSP won 182 of the 275 seats.
**10.** (b) — Shey Phoksundo in Dolpa, about 145 m deep.
**11.** (c) — Karnali; Koshi has the greatest volume.
**12.** (a) — Kechana Kawal in Jhapa.
:::

**Set C — Application (8 questions)**

1. Kanchenjunga (8,586 m) is the world's
   (a) highest peak (b) second highest peak (c) third highest peak (d) fourth highest peak
2. The Constitution of Nepal describes the country as
   (a) a secular federal democratic republic (b) a Hindu kingdom (c) a unitary monarchy (d) a military state
3. As of May 2026, the record number of Everest summits is
   (a) 21 (b) 25 (c) 29 (d) 32
4. The number of metropolitan cities in Nepal is
   (a) 5 (b) 6 (c) 7 (d) 4
5. The capital of Koshi Province is
   (a) Biratnagar (b) Janakpur (c) Hetauda (d) Pokhara
6. The capital of Gandaki Province is
   (a) Hetauda (b) Biratnagar (c) Pokhara (d) Surkhet
7. The capital of Karnali Province is
   (a) Dhangadhi (b) Birendranagar (c) Dailekh (d) Jumla
8. Republic Day (Ganatantra Diwas) is observed on
   (a) 7 Falgun (b) 3 Ashwin (c) 1 Baisakh (d) 15 Jestha

::: note Answers and explanations — Set C
**1.** (c) — after Everest and K2.
**2.** (a) — secular, federal, democratic and republican.
**3.** (d) — Kami Rita Sherpa, 32 summits on 17 May 2026.
**4.** (b) — Kathmandu, Pokhara, Lalitpur, Bharatpur, Birgunj, Janakpur.
**5.** (a) — Biratnagar.
**6.** (c) — Pokhara.
**7.** (b) — Birendranagar, Surkhet.
**8.** (d) — 15 Jestha 2065.
:::
