---
subject: General Knowledge and IT
grade: BCA
unit: 2
title: The World: Geography, Organisations, Sports and Science
hours: 2
area: General Knowledge
---

World GK is the other half of the general knowledge questions: records, capitals, nicknames, the UN, the Olympics and football/cricket world cups, inventors and awards. The Dean's Office model asked who won the FIFA World Cup 2018, which discipline has no Nobel Prize, and the "Father of Computer". **Sports results below are dated; revise from the latest news.**

::: key What the paper asks from this chapter
- **Records**: largest, smallest, tallest, longest, deepest.
- **Capitals and nicknames** of places.
- **UN and regional organisations**: founding year, headquarters, members.
- **Sports**: World Cup winners (football, cricket), Olympic hosts.
- **Inventions and awards**: inventor of the telephone, WWW; Nobel categories.
:::

## 2.1 World records, capitals and nicknames

| Record | Answer |
|---|---|
| Largest country / smallest country | Russia / Vatican City |
| Most populous country (since 2023) | India |
| Largest continent / ocean | Asia / Pacific |
| Longest river (commonly cited) | Nile |
| Tallest building | Burj Khalifa, Dubai (828 m) |
| Largest hot desert | Sahara |
| Deepest point of the oceans | Mariana Trench |
| Highest mountain | Everest |

| Country | Capital | Country | Capital |
|---|---|---|---|
| Japan | Tokyo | Australia | Canberra |
| Canada | Ottawa | Bhutan | Thimphu |
| Pakistan | Islamabad | Bangladesh | Dhaka |
| Brazil | Brasília | Switzerland | Bern |

Nicknames: Japan — Land of the Rising Sun; Bhutan — Land of the Thunder Dragon; New York — the Big Apple; Rome — the Eternal City; Jaipur — the Pink City; Africa — the Dark Continent.

```photogrid label="2.1" cols="4" ratio="1.1" caption="Four world records from the table above: (a) Burj Khalifa, Dubai, the tallest building at 828 m; (b) St Peter's Square and Vatican City, the smallest country (about 0.44 km2); (c) the Sahara, the largest hot desert; (d) Everest, the highest mountain above sea level."
@ photo id="bcagk/burj" cap="Burj Khalifa, 828 m"
focus 0.55 0.45
@ photo id="bcagk/vatican" cap="Vatican City: smallest country"
focus 0.4 0.5
@ photo id="bcagk/sahara" cap="Sahara: largest hot desert"
focus 0.5 0.5
@ photo id="bcagk/everest" cap="Everest: highest peak"
focus 0.4 0.4
```

```svgfig label="2.1" caption="The Burj Khalifa to scale against other famous towers (bars) and against Everest (row of blocks). Everest is 8,848.86 / 828 = 10.7 Burj Khalifas tall, so the highest mountain is more than ten times the tallest building."
tw = [("Burj Khalifa, Dubai", 828), ("Shanghai Tower", 632), ("Taipei 101", 508), ("Eiffel Tower, Paris", 330)]
assert [t[1] for t in tw] == sorted((t[1] for t in tw), reverse=True)
n = round(8848.86 / 828, 1); assert n == 10.7
f = Fig(760, 300); L = 190; sc = lambda h: L + h / 828 * 380
for i, (nm, h) in enumerate(tw):
    y = 14 + i * 34
    f.box(L, y, sc(h) - L, 24, "", fill=("#fecaca" if i == 0 else "#dbeafe"), stroke=(RED if i == 0 else NAVY), r=3)
    f.text(L - 8, y + 12, nm, size=10.5, color=NAVY, bold=True, anchor="end", vmid=True)
    f.text(sc(h) + 8, y + 12, f"{h} m", size=10.5, color=SLATE, anchor="start", vmid=True)
f.text(380, 172, f"Everest (8,848.86 m) = {n} Burj Khalifas stacked", size=11, color=RED, bold=True)
for k in range(11):
    w = 52 if k < 10 else 52 * 0.7
    f.box(60 + k * 56, 190, w, 40, "828 m" if k < 10 else "", fill="#fecaca", stroke=RED, size=9.5, bold=True, r=3)
f.text(60 + 10 * 56 + 18, 250, "0.7", size=9.5, color=RED, bold=True)
f.text(380, 282, "Each red block = one Burj Khalifa", size=9.5, color=SLATE)
```

```svgfig label="2.2" caption="The capital is often not the biggest or best-known city. These five pairs account for most capital-city questions in entrance papers: the guessed city is in red and the real capital in green."
rows = [("Australia", "Sydney", "Canberra"), ("Canada", "Toronto", "Ottawa"), ("Brazil", "Rio de Janeiro", "Brasília"),
        ("Switzerland", "Zurich", "Bern"), ("Pakistan", "Karachi", "Islamabad")]
f = Fig(760, 250)
f.text(120, 18, "Country", size=10.5, color=NAVY, bold=True); f.text(340, 18, "Common guess", size=10.5, color=RED, bold=True); f.text(590, 18, "Capital", size=10.5, color=TEAL, bold=True)
for i, (c, g, k) in enumerate(rows):
    y = 30 + i * 42
    f.box(40, y, 160, 32, c, fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.box(250, y, 180, 32, g, fill=ROSE, stroke=RED, size=11, bold=True)
    f.line(262, y + 16, 418, y + 16, color=RED, sw=1.2, dash=True)
    f.arrow([(440, y + 16), (505, y + 16)], color=SLATE)
    f.box(510, y, 180, 32, k, fill=MINT, stroke=TEAL, size=11, bold=True)
```

```photogrid label="2.2" cols="3" ratio="1.3" caption="Three capitals from the table and the trap list: (a) Parliament Hill, Ottawa, capital of Canada (not Toronto); (b) Parliament House, Canberra, capital of Australia (not Sydney); (c) Tashichho Dzong, Thimphu, capital of Bhutan and seat of its government."
@ photo id="bcagk/ottawa" cap="Ottawa: Parliament Hill, Peace Tower"
focus 0.5 0.5
@ photo id="bcagk/canberra" cap="Canberra: Parliament House"
focus 0.5 0.5
@ photo id="bcagk/thimphu" cap="Thimphu: Tashichho Dzong, Bhutan"
focus 0.5 0.55
```

## 2.2 United Nations and other organisations

- **United Nations**: founded 24 October 1945, headquarters New York, **193** member states; five permanent members of the Security Council (USA, UK, France, Russia, China). Nepal joined in 1955.
- **SAARC**: founded 1985 in Dhaka; secretariat in **Kathmandu**. WHO and WTO: Geneva. UNESCO: Paris. IMF and World Bank: Washington, D.C.

```photogrid label="2.3" cols="2" ratio="1.5" caption="Two headquarters worth recognising: (a) the United Nations Headquarters on the East River, New York; (b) the SAARC Secretariat in Kathmandu, the one regional organisation of South Asia that is based in Nepal."
@ photo id="bcagk/unhq" cap="UN Headquarters, New York"
focus 0.45 0.4
@ photo id="bcagk/saarc" cap="SAARC Secretariat, Kathmandu"
focus 0.5 0.5
```

```svgfig label="2.3" caption="The six principal organs of the UN. The Security Council has 15 members: five permanent members with a veto (USA, UK, France, Russia, China) and ten elected for two years. A resolution needs at least 9 of the 15 votes and no veto from a permanent member. The Trusteeship Council suspended operations in 1994."
p5 = ["USA", "UK", "France", "Russia", "China"]; assert len(p5) + 10 == 15 and 15 // 2 + 1 == 8 and 9 > 15 / 2
f = Fig(780, 330)
f.box(190, 8, 400, 40, "United Nations: 24 Oct 1945, New York, 193 members", fill="#dbeafe", stroke=NAVY, size=10.5, bold=True)
organs = [("General\nAssembly", "193 members,\none vote each"), ("Security\nCouncil", "15 members,\n5 with veto"), ("ECOSOC", "economic and\nsocial work"),
          ("Trusteeship\nCouncil", "suspended\n1994"), ("International\nCourt of Justice", "The Hague"), ("Secretariat", "led by the\nSecretary-General")]
for i, (a, b) in enumerate(organs):
    x = 14 + i * 126
    f.arrow([(390, 48), (x + 57, 80)], color=SLATE, sw=1.1)
    f.box(x, 80, 114, 46, a, fill=(MINT if i == 1 else BLUE), stroke=(TEAL if i == 1 else NAVY), size=10, bold=True)
    f.text(x + 57, 144, b, size=9, color=SLATE)
f.box(120, 178, 540, 140, "", fill="#f0fdfa", stroke=TEAL, r=8)
f.text(390, 196, "Inside the Security Council (15 seats)", size=11, color=TEAL, bold=True)
for i, c in enumerate(p5):
    f.box(145 + i * 104, 210, 92, 34, c, fill="#fecaca", stroke=RED, size=10.5, bold=True)
f.text(390, 262, "5 permanent members (veto)", size=9.5, color=RED, bold=True)
for i in range(10):
    f.circle(160 + i * 52, 288, 15, fill="#bfdbfe", stroke=NAVY, label=str(i + 1), size=9.5)
f.text(390, 313, "10 elected members (2-year terms): 5 + 10 = 15; passing a resolution needs 9 votes and no veto", size=9.5, color=NAVY, bold=True)
```

```svgfig label="2.4" caption="Where the organisations sit. Questions ask for the city, so learn the cluster: Geneva holds WHO, WTO and ILO; Washington, D.C. holds the IMF and World Bank; Paris holds UNESCO; New York holds the UN and UNICEF; Kathmandu holds SAARC; The Hague holds the ICJ."
cl = [("Geneva", ["WHO", "WTO", "ILO"], "#fecaca"), ("Washington, D.C.", ["IMF", "World Bank"], "#bfdbfe"), ("Paris", ["UNESCO"], "#e9d5ff"),
      ("New York", ["UN", "UNICEF"], "#bbf7d0"), ("Kathmandu", ["SAARC"], "#fde68a"), ("The Hague", ["ICJ"], "#fbcfe8")]
assert sum(len(c[1]) for c in cl) == 10
f = Fig(780, 190)
for i, (city, orgs, col) in enumerate(cl):
    x = 12 + i * 128
    f.box(x, 14, 118, 34, city, fill=col, stroke=SLATE, size=10.5, bold=True)
    for j, o in enumerate(orgs):
        f.box(x + 10, 60 + j * 38, 98, 30, o, fill="#ffffff", stroke=SLATE, size=10.5, bold=True)
f.text(390, 182, "10 organisations, 6 cities", size=9.5, color=SLATE)
```

## 2.3 Olympics, football and cricket world cups

| Event | Result |
|---|---|
| FIFA World Cup 2018 (Russia) | France |
| FIFA World Cup 2022 (Qatar) | Argentina |
| FIFA World Cup 2026 (USA, Canada, Mexico) | **Spain** beat Argentina 1–0 after extra time, 19 July 2026 |
| Euro 2024 | Spain |
| ODI Cricket World Cup 2023 | Australia |
| Women's ODI World Cup 2025 | India |
| Olympics 2024 / 2028 | Paris / Los Angeles |

```photogrid label="2.4" cols="2" ratio="1.5" caption="Two global sporting symbols: (a) the Olympic rings hung on the Eiffel Tower for the Paris 2024 Games; (b) the FIFA World Cup trophy on display in the FIFA World Football Museum."
@ photo id="bcagk/olymp" cap="Olympic rings on the Eiffel Tower, Paris 2024"
focus 0.5 0.5
@ photo id="bcagk/wcup" cap="FIFA World Cup trophy"
focus 0.5 0.35
```

```svgfig label="2.5" caption="Four-year cycles on one axis. FIFA World Cup years leave remainder 2 when divided by 4 (2018, 2022, 2026); the Summer Olympics (2016, 2020, 2024, 2028) and the European Championship (2024) fall in leap years. Tokyo 2020 was held in 2021, and the next ODI Cricket World Cup is scheduled for 2027."
fifa = [y for y in range(2016, 2029) if y % 4 == 2]; oly = [y for y in range(2016, 2029) if y % 4 == 0]
assert fifa == [2018, 2022, 2026] and oly == [2016, 2020, 2024, 2028]
fw = {2018: "France", 2022: "Argentina", 2026: "Spain"}; ow = {2016: "Rio", 2020: "Tokyo*", 2024: "Paris", 2028: "Los Angeles"}
cw = {2019: "Australia (2023)"}
f = Fig(780, 300); X0, X1 = 215, 745; ax = lambda y: X0 + (y - 2015) * (X1 - X0) / 14
f.line(X0 - 20, 40, X1, 40, color=SLATE, sw=1.2)
for y in range(2015, 2030):
    f.line(ax(y), 36, ax(y), 44, color=SLATE, sw=1); f.text(ax(y), 28, str(y), size=9.5, color=(NAVY if y % 4 in (0, 2) else SLATE), bold=(y % 4 in (0, 2)))
for r, (lab, ys, w, col, ec) in enumerate([("FIFA World Cup\n(year mod 4 = 2)", fifa, fw, "#bbf7d0", TEAL), ("Summer Olympics\n(leap years)", oly, ow, "#bfdbfe", NAVY)]):
    y0 = 70 + r * 70
    f.text(X0 - 20, y0 + 20, lab, size=10, color=ec, bold=True, anchor="end", vmid=True)
    for y in ys:
        f.box(ax(y) - 40, y0, 80, 40, f"{y}\n{w[y]}", fill=col, stroke=ec, size=10, bold=True)
y0 = 70 + 2 * 70
f.text(X0 - 20, y0 + 20, "ODI Cricket World Cup\n(2019, 2023, 2027)", size=10, color=AMBER, bold=True, anchor="end", vmid=True)
for y, w in [(2019, "England"), (2023, "Australia"), (2027, "scheduled")]:
    f.box(ax(y) - 40, y0, 80, 40, f"{y}\n{w}", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(390, 285, "Euro 2024: Spain.   Women's ODI World Cup 2025: India.   * Tokyo 2020 was held in 2021.", size=9.5, color=SLATE)
```

## 2.4 Inventions, discoveries and awards

| Invention / discovery | Person |
|---|---|
| Telephone | Alexander Graham Bell |
| Light bulb (practical) | Thomas Edison |
| World Wide Web | Tim Berners-Lee |
| Father of the computer (analytical engine) | Charles Babbage |
| Theory of relativity | Albert Einstein |
| Penicillin | Alexander Fleming |

**Nobel Prizes** are given in Physics, Chemistry, Physiology or Medicine, Literature, Peace and Economic Sciences (the last added in 1969). **There is no Nobel Prize in computer science**; its highest award is the Turing Award. The Peace Prize is awarded in Oslo, the others in Stockholm.

```photogrid label="2.5" cols="4" ratio="0.95" caption="Four names from the inventions table: (a) Alexander Graham Bell, telephone; (b) Albert Einstein, theory of relativity; (c) Alexander Fleming at work in his laboratory, penicillin; (d) Charles Babbage, designer of the Analytical Engine."
@ photo id="bcagk/bell" cap="A. G. Bell: telephone (1876)"
focus 0.5 0.4
@ photo id="bcagk/einstein" cap="A. Einstein: relativity"
focus 0.5 0.4
@ photo id="bcagk/fleming" cap="A. Fleming: penicillin (1928)"
focus 0.5 0.5
@ photo id="bcagk/babbage" cap="C. Babbage: Analytical Engine"
focus 0.5 0.4
```

```photogrid label="2.6" cols="3" ratio="1.25" caption="Artefacts behind the names: (a) Edison's patent drawing of the carbon-filament electric lamp; (b) a working Babbage Difference Engine built from his plans at the Science Museum, London; (c) a Nobel Prize medal."
@ photo id="bcagk/edison" cap="Edison's lamp patent drawing"
fit 1.25
focus 0.5 0.3
@ photo id="bcagk/diffeng" cap="Babbage Difference Engine No. 2"
focus 0.5 0.5
@ photo id="bcagk/nobel" cap="Nobel Prize medal"
focus 0.5 0.5
```

```svgfig label="2.6" caption="Six discoveries on one time scale (tick = 10 years). Bell and Edison are only three years apart (1876 and 1879), but Berners-Lee's Web (1989) comes 152 years after Babbage's Analytical Engine (1837): the father of the computer lived long before any working computer."
ev = [(1837, "Babbage: Analytical\nEngine designed", "up", 1), (1876, "Bell: telephone", "up", 2), (1879, "Edison: practical\nlight bulb", "dn", 1),
      (1905, "Einstein: special\nrelativity", "up", 1), (1928, "Fleming: penicillin", "dn", 1), (1989, "Berners-Lee: WWW\nproposal", "up", 1)]
assert [e[0] for e in ev] == sorted(e[0] for e in ev) and 1879 - 1876 == 3 and 1989 - 1837 == 152
f = Fig(780, 250); X0, X1, A0, A1 = 50, 730, 1820, 2000; ax = lambda y: X0 + (y - A0) * (X1 - X0) / (A1 - A0); Y = 125
f.line(X0, Y, X1, Y, color=NAVY, sw=3)
for y in range(1820, 2001, 10):
    f.line(ax(y), Y - 4, ax(y), Y + 4, color=SLATE, sw=1)
    if y % 20 == 0: f.text(ax(y), Y + 22 if y % 40 else Y + 22, str(y), size=10, color=SLATE)
for yr, lab, d, lv in ev:
    x = ax(yr); s = -1 if d == "up" else 1; yy = Y + s * (22 + lv * 28)
    f.line(x, Y, x, yy, color=TEAL, sw=1.1); f.circle(x, Y, 4.5, fill=TEAL, stroke=TEAL)
    an = "end" if x > 690 else ("start" if x < 90 else "middle")
    t = f"{yr}\n{lab}"; nl = t.count("\n") + 1
    f.text(x, yy + (-(nl * 6 + 4) if d == "up" else (nl * 6 + 4)), t, size=10, color=NAVY, bold=True, anchor=an)
f.arrow([(ax(1837), 215), (ax(1989), 215)], color=AMBER, both=True, label="152 years", lpos=(ax(1913), 208))
```

```svgfig label="2.7" caption="Nobel Prize categories. The five prizes in Alfred Nobel's will were first awarded in 1901; Economic Sciences was added in 1969, 68 years later. Peace is announced in Oslo and the rest in Stockholm. Computer science and mathematics have no Nobel; their top awards are the Turing Award and the Fields Medal or Abel Prize."
orig = ["Physics", "Chemistry", "Physiology\nor Medicine", "Literature", "Peace"]; assert 1969 - 1901 == 68
f = Fig(780, 230)
f.text(300, 18, "First awarded 1901", size=11, color=NAVY, bold=True)
for i, o in enumerate(orig):
    f.box(14 + i * 112, 30, 104, 46, o, fill=("#bbf7d0" if o == "Peace" else "#dbeafe"), stroke=(TEAL if o == "Peace" else NAVY), size=10, bold=True)
    f.text(14 + i * 112 + 52, 92, "Oslo" if o == "Peace" else "Stockholm", size=9.5, color=(TEAL if o == "Peace" else SLATE), bold=True)
f.box(590, 30, 170, 46, "Economic Sciences\nadded 1969", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(675, 92, "Stockholm (68 years after 1901)", size=9, color=AMBER, bold=True)
f.box(14, 130, 746, 84, "", fill=ROSE, stroke=RED, r=8)
f.text(387, 150, "No Nobel Prize exists for:", size=11, color=RED, bold=True)
f.box(40, 162, 210, 40, "Computer science\nTuring Award (ACM)", fill="#ffffff", stroke=RED, size=10, bold=True)
f.box(285, 162, 210, 40, "Mathematics\nFields Medal, Abel Prize", fill="#ffffff", stroke=RED, size=10, bold=True)
f.box(530, 162, 210, 40, "Biology or Geography\n(no separate prize)", fill="#ffffff", stroke=RED, size=10, bold=True)
```

## 2.5 Eight traps in world GK questions

World GK has no pattern to derive, so exam writers test whether you can separate two things that sound alike. These eight traps cover most of the world-GK questions in model papers.

1. **Largest by area is not largest by people.** Russia is the largest country by area, but India has been the most populous since 2023. Questions on "largest" nearly always name one measure in the stem, so underline it before you read the options. Do not pick China just because it feels big.
2. **The capital is rarely the biggest city.** Canberra, not Sydney; Ottawa, not Toronto; Brasília, not Rio; Bern, not Zurich; Islamabad, not Karachi (Fig 2.2). All five were planned or chosen as compromise capitals, which is why they are smaller than the rival city. Dhaka and Tokyo are the easy cases where the capital is also the largest city.
3. **Longest river depends on the measure.** The Nile is the commonly cited longest river, although some surveys place the Amazon first, and the Amazon is certainly first by volume of water. If the stem says "longest" choose the Nile, and if it says "largest discharge" choose the Amazon. Nepal's own pair works the same way: Karnali is longest, Koshi carries the most water.
4. **Tallest building, tallest mountain, highest point.** Burj Khalifa (828 m) is the tallest building and Everest is the highest point above sea level. Measured from its base on the sea floor, Mauna Kea in Hawaii is taller than Everest, which is a favourite trick. Read whether the question says "above sea level" or "from base to top".
5. **Know which city hosts which body.** The UN is in New York, WHO and WTO in Geneva, UNESCO in Paris, IMF and World Bank in Washington, D.C., and SAARC in Kathmandu (Fig 2.4). Many students write Geneva for everything. Keep the cluster picture in mind and the question becomes a lookup.
6. **Event year rules.** FIFA World Cup years leave remainder 2 when divided by 4 (2018, 2022, 2026), while the Olympics and the European Championship fall in years divisible by 4 (Fig 2.5). Use the rule to fix a year you half remember. The Tokyo Games, named 2020, were played in 2021, so read "held in" differently from "named".
7. **Host is not winner.** Russia hosted in 2018 but France won; Qatar hosted in 2022 but Argentina won; the 2026 hosts USA, Canada and Mexico were beaten by Spain. Always check whether the stem asks for host, winner or runner-up. The same applies to cricket: Australia won the 2023 ODI World Cup, which India hosted.
8. **Inventor, discoverer and popular name.** Bell patented the telephone, Edison made the *practical* light bulb (he did not invent the first lamp), Fleming discovered penicillin, and Berners-Lee invented the *World Wide Web* (not the Internet). Babbage is the father of the computer as the designer of the Analytical Engine, while Turing is the father of theoretical computer science. If the question says "father of computer" choose Babbage unless Turing is the only sensible name.

### 2.5.1 Worked checks

**Q. A resolution in the UN Security Council gets 10 yes votes, 4 abstentions and 1 no vote from Russia. What happens?** (a) It passes (b) It fails because of a veto (c) It passes after a vote in the General Assembly (d) It is sent to the ICJ

**Answer: (b).** The Council has 15 members and needs at least 9 yes votes, so 10 is enough, but a no vote from any of the five permanent members is a veto and the resolution fails (Fig 2.3). An abstention is not a veto, which is why the other 4 do not matter. This is the most common conceptual question on the UN.

**Q. Which of these has no Nobel Prize?** (a) Peace (b) Literature (c) Economic Sciences (d) Computer science

**Answer: (d).** The five original prizes began in 1901 and Economic Sciences followed in 1969 (Fig 2.7). Computer science has the Turing Award instead, so option (d) is the only field without a Nobel.

## Formula and fact sheet

| Quick facts | |
|---|---|
| UN | 1945, New York, 193 members |
| SAARC | 1985, Kathmandu |
| 2018 / 2022 / 2026 World Cup | France / Argentina / Spain |
| Nobel | no computer science |

## Chapter summary

- Russia is the largest, Vatican City the smallest; India is the most populous.
- Canberra, not Sydney; Ottawa, not Toronto.
- UN: 1945, New York, 193 members, five veto powers.
- World Cup winners 2018, 2022, 2026: France, Argentina, Spain.
- Babbage is the father of the computer; Berners-Lee invented the Web.

## Practice questions

**Set A — Recall (20 questions)**

1. The largest country in the world by area is
   (a) Canada (b) China (c) Russia (d) USA
2. The smallest country in the world is
   (a) Vatican City (b) Monaco (c) Nauru (d) Malta
3. The capital of Japan is
   (a) Osaka (b) Kyoto (c) Seoul (d) Tokyo
4. The capital of Australia is
   (a) Sydney (b) Canberra (c) Melbourne (d) Perth
5. The largest ocean is the
   (a) Atlantic (b) Indian (c) Arctic (d) Pacific
6. The headquarters of the United Nations is in
   (a) New York (b) Geneva (c) Paris (d) Vienna
7. The United Nations was founded in
   (a) 1919 (b) 1939 (c) 1945 (d) 1955
8. The tallest building in the world is
   (a) Shanghai Tower (b) Burj Khalifa (c) Taipei 101 (d) Eiffel Tower
9. The "Father of the Computer" is
   (a) Charles Babbage (b) Bill Gates (c) Mark Zuckerberg (d) Steve Jobs
10. The FIFA World Cup 2022 was won by
    (a) France (b) Croatia (c) Brazil (d) Argentina
11. The FIFA World Cup 2026 was won by
    (a) Argentina (b) France (c) Spain (d) England
12. The FIFA World Cup 2018 was won by
    (a) Croatia (b) France (c) Germany (d) Brazil
13. The 2024 Summer Olympics were held in
    (a) Paris (b) Tokyo (c) London (d) Los Angeles
14. Which of these has no Nobel Prize?
    (a) Physics (b) Literature (c) Computer Science (d) Peace
15. The longest river in the world, by common reckoning, is the
    (a) Amazon (b) Yangtze (c) Mississippi (d) Nile
16. The highest mountain in the world is
    (a) K2 (b) Everest (c) Kanchenjunga (d) Lhotse
17. The "Land of the Rising Sun" is
    (a) Japan (b) China (c) Korea (d) Vietnam
18. The "Land of the Thunder Dragon" is
    (a) Nepal (b) Tibet (c) Bhutan (d) Myanmar
19. The capital of Canada is
    (a) Toronto (b) Vancouver (c) Montreal (d) Ottawa
20. The telephone was invented by
    (a) Edison (b) Graham Bell (c) Marconi (d) Tesla

::: note Answers and explanations — Set A
**1.** (c) — Russia.
**2.** (a) — Vatican City, about 0.44 km².
**3.** (d) — Tokyo.
**4.** (b) — Canberra, not Sydney.
**5.** (d) — the Pacific.
**6.** (a) — New York.
**7.** (c) — 24 October 1945.
**8.** (b) — Burj Khalifa, 828 m.
**9.** (a) — Charles Babbage designed the Analytical Engine.
**10.** (d) — Argentina beat France on penalties.
**11.** (c) — Spain beat Argentina 1–0 after extra time on 19 July 2026.
**12.** (b) — France beat Croatia 4–2.
**13.** (a) — Paris.
**14.** (c) — computing's top award is the Turing Award.
**15.** (d) — the Nile (the Amazon is a rival claim).
**16.** (b) — Everest, 8,848.86 m.
**17.** (a) — Japan.
**18.** (c) — Bhutan.
**19.** (d) — Ottawa.
**20.** (b) — Alexander Graham Bell.
:::

**Set B — Understanding (12 questions)**

1. The secretariat of SAARC is located in
   (a) Kathmandu (b) Dhaka (c) Delhi (d) Colombo
2. The number of permanent members of the UN Security Council is
   (a) 3 (b) 4 (c) 5 (d) 6
3. The ODI Cricket World Cup 2023 was won by
   (a) India (b) England (c) New Zealand (d) Australia
4. The capital of Bangladesh is
   (a) Chittagong (b) Dhaka (c) Sylhet (d) Khulna
5. The capital of Bhutan is
   (a) Paro (b) Punakha (c) Phuntsholing (d) Thimphu
6. The capital of Pakistan is
   (a) Islamabad (b) Karachi (c) Lahore (d) Rawalpindi
7. The "Big Apple" is
   (a) Los Angeles (b) Chicago (c) New York (d) Boston
8. The largest hot desert in the world is
   (a) the Gobi (b) the Sahara (c) the Thar (d) the Kalahari
9. The World Wide Web was invented by
   (a) Tim Berners-Lee (b) Bill Gates (c) Steve Jobs (d) Vint Cerf
10. The "Eternal City" is
    (a) Athens (b) Paris (c) Cairo (d) Rome
11. The Nobel Peace Prize is awarded in
    (a) Stockholm (b) Oslo (c) Geneva (d) Copenhagen
12. The largest continent is
    (a) Africa (b) Europe (c) Asia (d) North America

::: note Answers and explanations — Set B
**1.** (a) — Kathmandu.
**2.** (c) — USA, UK, France, Russia, China.
**3.** (d) — Australia beat India in the final.
**4.** (b) — Dhaka.
**5.** (d) — Thimphu.
**6.** (a) — Islamabad.
**7.** (c) — New York.
**8.** (b) — the Sahara (Antarctica is the largest desert overall).
**9.** (a) — Tim Berners-Lee, 1989.
**10.** (d) — Rome.
**11.** (b) — Oslo; the other prizes are in Stockholm.
**12.** (c) — Asia.
:::

**Set C — Application (8 questions)**

1. The "Pink City" of India is
   (a) Jodhpur (b) Jaipur (c) Udaipur (d) Agra
2. The most populous country in the world (since 2023) is
   (a) China (b) USA (c) Indonesia (d) India
3. The number of member states of the United Nations is
   (a) 193 (b) 195 (c) 190 (d) 200
4. The 2028 Summer Olympics will be held in
   (a) Brisbane (b) Paris (c) Los Angeles (d) Tokyo
5. The UEFA Euro 2024 was won by
   (a) Spain (b) England (c) France (d) Italy
6. The deepest point of the world's oceans is in the
   (a) Puerto Rico Trench (b) Java Trench (c) Sunda Trench (d) Mariana Trench
7. The Women's Cricket World Cup 2025 was won by
   (a) Australia (b) England (c) India (d) South Africa
8. The "Dark Continent" is
   (a) Asia (b) Africa (c) South America (d) Antarctica

::: note Answers and explanations — Set C
**1.** (b) — Jaipur.
**2.** (d) — India passed China in 2023.
**3.** (a) — 193, since South Sudan joined in 2011.
**4.** (c) — Los Angeles.
**5.** (a) — Spain beat England 2–1.
**6.** (d) — the Mariana Trench (Challenger Deep, about 10.9 km).
**7.** (c) — India beat South Africa in the final, November 2025.
**8.** (b) — Africa.
:::
