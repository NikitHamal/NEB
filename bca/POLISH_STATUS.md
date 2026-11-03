# BCA polish status (5 Quality Pillars)
Legend: [ ] pending, [~] in progress, [x] done. Toolchain: AGENTS.md "BCA polish session 10".

## BCA 101 computer-fundamentals (semester-1/computer-fundamentals) -- [x] DONE, 100 pp, qa fails=0
Real units (NOT the brief's guess): U1 Intro, U2 Software, U3 OS, U4 DBMS, U5 Networks, U6 Internet/Web, U7 Contemporary Tech.
- [x] U1: SVG 1.1-1.6; Plates 1.1 (5-up generations), 1.2 (ENIAC/IBM 1401/punch card), 1.3 (labelled micro-ATX board + CPU), 1.4 (2x2 SRAM/DRAM/NVMe/pen drive with callouts), 1.5 (3-up HDD platter/arm/DVD with numbered key).
- [x] U2 Software: SVG 2.1 classification, 2.2 compile/link/load vs interpret, 2.3 flowchart; 3 medium + 2 long model answers (Q3, Q7, Q5; Q13, Q14).
- [x] U3 OS: SVG 3.1-3.2, Plate 3.1 (CLI vs GUI 4-up). Existing long answers OK.
- [x] U4 DBMS: SVG 4.1 file vs DBMS, 4.2 three-schema, 4.3 college ER; 8-point DBMS applications (4.1.1); 3 medium (Q2, Q12, Q4) + 2 long (Q13, Q14). No photo (not applicable). Do NOT run fill_script_outputs.py on this book.
- [x] U5 Networks: SVG 5.1-5.2, Plate 5.1 (cables 4-up), Plate 5.2 (devices 3-up).
- [x] U6 Internet: SVG 6.1 DNS, 6.2 HTTPS cycle; Q9 (5 marks), Q12, Q13, Q14 long. TODO optional: GIS/IoT photos, 7-8 point application lists.
- [x] U7 Contemporary Tech: SVG 7.1 IaaS/PaaS/SaaS, 7.2 digital signature, 7.3 e-governance models; Plate 7.1 (VR, Raspberry Pi, PIR, 3D print); Q10 (5 marks), Q14, Q15, Q16 long.
- Session 11: U1 memory/storage plates done; BCA 101 closed.

## BCA 103 digital-logic (semester-1/digital-logic) -- [x] DONE (session 11), 45 pp, qa fails=0
- U1: SVG 1.2 voltage bands, 1.3 clock waveform; Plate 1.1 (scope photo + sampling/quantisation SVG pair), Plate 1.2 (7447 ceramic DIP + HC00 die photo + 7400 pinout SVG, 3-up); 8-point advantages (1.5); 2 medium + 1 long answers.
- U2: SVG 2.1 conversion, 2.2 two's complement ring, 2.3 IEEE-754 layout; Plate 2.1 (7-segment LED photo + segment/BCD SVG); 8 reasons (2.6); 2 medium + 1 long.
- U3: SVG 3.1 gate symbols, 3.2 K-map with groups, 3.3 full adder; Plate 3.1 (breadboard + HP logic analyzer photos); 8 applications (3.7); 2 medium + 1 long.
- U4: SVG 4.1 ripple counter + timing, 4.2 shift register; 8 uses (4.4); 1 medium + 1 long.
- U5: SVG 5.1 101-detector state diagram; 1 medium + 1 long (design).
- Photos (bca103/): scope, ic7447, hc00, breadboard, seg7, logican (all licence-gated via assets.py).
- Not done: Unit 5 has no photo (abstract topic); units 2-5 only have the new model answers listed above (old short Practice answers kept).

## BCA 102 programming-in-c (semester-1/programming-in-c) -- [x] DONE (session 12), 78 pp, qa fails=0
- U1: Plate 1.1 (3-up: Thompson+Ritchie 1973, PDP-11/20, UNIX V5 screenshot; bca102/ photos), SVG 1.1 build pipeline; 8 features of C (1.5.1); 1 medium + 1 long answer.
- U2: SVG 2.1 type sizes to scale, SVG 2.2 operator precedence; 8 common mistakes (2.7); medium (data types) + long (operators, evaluated expression).
- U3: SVG 3.1 flowcharts if-else/while/do-while; 8 uses of loops/decisions (3.5); medium (if ladder vs switch + program) + long (loops).
- U4: SVG 4.1 array/string/2-D memory layout, SVG 4.2 bubble sort passes; 8 uses of arrays/strings (4.5); medium (bubble sort, program run) + long (strings, program run).
- U5: SVG 5.1 call stack of factorial(3), SVG 5.2 storage classes; 8 advantages of functions (5.5); medium (value vs address, run) + long (recursion + storage classes, run).
- U6: SVG 6.1 pointer/array arithmetic, SVG 6.2 malloc/realloc/free; 8 uses of pointers (6.6); medium (dynamic allocation) + long (pointers, program run).
- U7: Plate 7.1 (4-up punched card / HDD head / NVMe / pen drive, bca101 photos reused), SVG 7.1 struct vs union, SVG 7.2 file life cycle; 8 uses (7.5); medium (struct vs union) + long (file handling, binary file program run).
- All C programs in the new answers were compiled with gcc -Wall and the printed output pasted from the real run.

## BCA 106 hardware-workshop (semester-1/hardware-workshop) -- [x] DONE (session 12), 40 pp, qa fails=0
- Photos (bca106/, all licence-gated): strap, meter, crimpkit, psu, gpu, jpanel, paste, postcard, tester, toner, gparted (+ bca101 mobo/cpu-i7/ram/nvme/rj45/ubuntu/win10b reused).
- U1: Plate 1.1 (3-up tools with callouts), Plate 1.2 (3-up PSU/GPU/motherboard), SVG 1.1 PC block diagram; 8 safety rules (1.6); medium (safety/ESD) + long (components, compatibility, PSU calc).
- U2: Plate 2.1 (4-up CPU/DIMM/M.2/cooler), Plate 2.2 (front-panel header photo + SVG pin pairs), SVG 2.1 assembly order, SVG 2.2 no-boot decision tree; 8 assembly mistakes (2.5); medium (CPU/cooler/RAM) + long (assembly + POST).
- U3: Plate 3.1 (GParted + Ubuntu + Windows desktops), SVG 3.1 boot sequence, SVG 3.2 MBR vs GPT layout; 8 install tips (3.6); medium (MBR vs GPT, 2 TiB calc) + long (BIOS/UEFI, dual boot).
- U4: Plate 4.1 (4-up POST card/tester/patch cables/toner), SVG 4.1 T568B colours, SVG 4.2 troubleshooting cycle; 8 maintenance tasks (4.6); medium (straight cable) + long (troubleshooting method + fault table).

## BCA 104 mathematics-1 (semester-1/mathematics-1) -- [x] DONE (session 13), 56 pp, qa fails=0
- New helper: `Axes` class in `notes/pipeline/svgkit.py` (grid/axes/curve/area/bars/pt/hline/vline/tag) for plotted graphs inside ```svgfig / `@ svg` cells. Photos (bca104/, all licence-gated): dish, arch, newton, leibniz, cauchy, weier, speedo, taylor, riemann, archimedes, kgdam, coffee, ecoli, spring (+ bca103/scope reused).
- U1 Functions: Fig 1.1 gallery of 6 standard graphs, Plate 1.1 (3-up dish/arch/oscilloscope), Fig 1.2 inverse (e^x, ln x, y=x), Fig 1.3 transformations; 8 uses (1.6); 2 medium + 1 long.
- U2 Limits: Fig 2.1 hole/jump/infinite, Plate 2.1 (Cauchy, Weierstrass + eps-delta SVG), Fig 2.2 squeeze, Fig 2.3 IVT; 8 uses (2.5); 2 medium + 1 long.
- U3 Differentiation: Fig 3.1 secant to tangent + table, Plate 3.1 (speedometer, Newton, Leibniz), Fig 3.2 f and f', Fig 3.3 implicit circle; 8 uses (3.7); 2 medium + 1 long.
- U4 Applications: Fig 4.1 ladder, Fig 4.2 can optimisation, Fig 4.3 MVT, Plate 4.1 (Taylor portrait + Maclaurin sin x + e^0.1 error); 8 uses (4.8); 2 medium + 1 long.
- U5 Integration: Plate 5.1 (Archimedes, Riemann, Kaligandaki dam), Fig 5.1 Riemann sums, Fig 5.2 area between curves + disc volume, Fig 5.3 improper integrals; 8 uses (5.8); 2 medium + 1 long.
- U6 Differential equations: Fig 6.1 slope field, Fig 6.2 method decision chain, Fig 6.3 damping cases, Fig 6.4 cooling + logistic, Plate 6.1 (coffee, E. coli, spring); 8 uses (6.8); 2 medium + 1 long.
- Every numeric claim in the new answers was recomputed with SymPy; `check_math1.py --verify` prints ALL OK.

## BCA 105 professional-communication-ethics (semester-1/professional-communication-ethics) -- [x] DONE (session 13), 48 pp, qa fails=0
- Photos (bca105/, licence-gated): phone (candlestick telephone), speaker (conference talk), pen (handwritten letter), scrum (team stand-up briefing). Abstract topics (ethics, IP law) have no suitable photo; SVG used instead. Rejected after viewing: Morse key texture, GPO search hit, CC icon graphic with black alpha artefacts.
- U1: Fig 1.1 communication process (noise + feedback), Plate 1.1 (3-up telephone/speaker/letter channels); 8 reasons (1.7); medium (verbal vs non-verbal) + long (process, barriers, 7 Cs).
- U2: Fig 2.1 10-minute talk timeline to scale, Plate 2.1 (speaker photo + poor/good slide SVG); 8 habits (2.6); medium (active listening) + long (presentation).
- U3: Fig 3.1 annotated email anatomy, Plate 3.1 (letter photo + full-block layout SVG); 8 rules (3.8); medium (plagiarism) + long (email vs letter).
- U4: Plate 4.1 (team stand-up photo + Tuckman curve SVG), Fig 4.1 Eisenhower matrix; 8 team characteristics (4.7); medium (Tuckman) + long (teamwork, conflict, SBI, time).
- U5: Fig 5.1 ethical decision flow, Fig 5.2 IP types and licence spectrum; 8 responsibilities (5.8); medium (MIT vs GPL) + long (ethics, IP, ETA 2063; no penalty figures given).

## BCA 256 project-1 (semester-4/project-1) -- [x] DONE (session 14), qa fails=0
Project I has no TU topic list, so this is a reconstructed companion handbook (README says so) built around one running example, CampusShelf (invented college library book-issue system). 5 units, 16,401 raw words (gen_status count, code listings included), 49 pp.
- Photos (bca256/, licence-gated, all viewed): pitch (hackathon pitch), kanban (3-column board), scrum (task board), pair (pair programming), poster (poster-session presenter).
- U1 Scoping: Plate 1.1 (pitch photo + idea-funnel SVG), Fig 1.2 life cycle; feasibility score script (executed); 8 reasons projects fail (1.7); 2 medium + 1 long answers.
- U2 Planning: Fig 2.1 Gantt to scale (matches critical-path script), Plate 2.1 (3-up kanban/scrum/pair photos with callouts), Fig 2.2 Git branches; critical-path script + real `git` run output; 8 team practices (2.6); 2 medium + 1 long.
- U3 Analysis/design: Fig 3.1 use case, 3.2 DFD level 0, 3.3 DFD level 1, 3.4 ER; sqlite schema script (FK rejection shown); Plate 3.1 (3 wireframe SVGs); 8 benefits (3.6); 2 medium + 1 long.
- U4 Build/test: Fig 4.1 three layers, 4.2 V-model, 4.3 bug life cycle; full `campusshelf.py` listing run by fill_script_outputs; `unittest` file (fence tag `py`, NOT `python`, so fill_script_outputs does not wipe its hand-pasted output; regenerate with /tmp/cs recipe in AGENTS.md); 8 reasons (4.7); 2 medium + 1 long.
- U5 Report/viva: Fig 5.1 report map, Plate 5.1 (poster photo + clean-slide SVG), report-budget script, 12 viva Q&A, illustrative rubric (flagged as not official); 8 habits (5.8); 2 medium + 1 long.
- Known cosmetic: the Level-1 DFD labels render at about 6 pt (qa warn only).

## BCA 306 project-2 (semester-5/project-2) -- [x] DONE (session 15), 47 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **ClinicQ** (invented health-post token queue; REST API + security + deployment), different from Project I's CampusShelf. 5 units, 15,586 raw words.
- Photos (bca306/, licence-gated, all viewed): rack (NERSC server rack, CC0), switch (rack switch + patch panels), tech (technician at server rack, CC0), padlock, code (code on monitor, CC0).
- U1 Scope/architecture: Fig 1.1 three-tier, Plate 1.1 (3-up rack/switch/technician with callouts); stack table, REST table, user stories; 8 reasons web projects fail (1.7); 2 medium + 1 long.
- U2 API/database: Fig 2.1 ER, Fig 2.2 request life; 78-line stdlib REST API (http.server + sqlite3) run over a real local port; race-condition script (barrier forces duplicates; UNIQUE + retry fixes; output deterministic); 8 reasons (2.6); 2 medium + 1 long.
- U3 Security: Fig 3.1 login flow, Plate 3.1 (padlock photo + defence-in-depth SVG); executed PBKDF2 salt demo, HMAC token (issue/verify/expiry/forgery), SQL injection bad vs placeholder, brute-force arithmetic; attack table; 8 practices (3.7); 2 medium + 1 long.
- U4 Testing/deploy: Plate 4.1 (code photo + test pyramid SVG), Fig 4.1 pipeline; 9-test unittest suite (per-test PASS lines, deterministic), 10-row test-case table, Little's-law capacity script, systemd + Nginx files (not executed); 8 practices (4.6); 2 medium + 1 long.
- U5 Docs/demo/viva: Fig 5.1 report map, Plate 5.1 (technician photo + demo timeline SVG); generated API-doc script, demo-plan script; 12 viva Q&A; 8 habits (5.5); 2 medium + 1 long.
- Gotchas: `Fig.arrow` takes a list of points (`f.arrow([(x1,y1),(x2,y2)], color=)`), not four numbers; literal `<role>` in prose is stripped as HTML (use square brackets); the Unit 2 API deliberately has no login (Unit 3 adds it conceptually; routes table in 5.2 shows the protected version).
- Not done: Unit 2 has no photo; Unit 3 login/hash code is not wired into the Unit 2 server (separate self-contained demos).

## BCA 356 project-3 (semester-6/project-3) -- [x] DONE (session 16)
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **KhetSense** (invented soil-moisture and weather monitor for a hill-farm cooperative; ESP32 nodes, MQTT-style messages, SQLite analysis, Android offline-first client), different from CampusShelf (Project I) and ClinicQ (Project II). 5 units.
- Photos (bca356/, licence-gated, all viewed): esp32, rpi, uno, soil, dht22, drip, terrace, phone.
- U1 Scope/architecture: Fig 1.1 four-layer IoT, Plate 1.1 (3-up ESP32/Pi/Uno), Plate 1.2 (3-up soil probe/DHT22/drip); BOM script (v1 Rs 34,900 over budget, v2 Rs 26,700); 8 reasons sensor projects fail (1.6); 2 medium + 1 long.
- U2 Sensors/data path: Plate 2.1 (ESP32 photo + wiring SVG), Fig 2.1 calibration plot (Axes); calibration, median filter, QoS0 vs QoS1 loss simulation and battery scripts all executed; 8 rules (2.6); 2 medium + 1 long.
- U3 Storage/analysis: Fig 3.1 pipeline, Plate 3.1 (terrace photo + advice bands SVG); SQLite constraints script, MAD cleaning, anomaly rules, drying-curve forecast vs persistence (executed); 8 uses (3.7); 2 medium + 1 long.
- U4 Mobile client: Plate 4.1 (phone photo + 2 wireframe SVGs), Fig 4.1 sync sequence; offline-first sync simulation, stale-label tests (executed); 8 features (4.7); 2 medium + 1 long.
- U5 Field test/report/viva: Fig 5.1 report map, Plate 5.1 (Pi photo + demo timeline SVG); field-test PASS/FAIL table script (O1 honestly FAILS), report page budget; 12 viva Q&A, illustrative rubric, 8 habits (5.7); 2 medium + 1 long.
- Gotchas: python fences need a closing ``` (an unclosed fence swallows the unit); no `fill_script_outputs` problems since every block is self-contained; numbers in prose were copied from real runs (seeded, so re-runs match). Calibration figure is drawn with ideal positions (caption says so). No unit-5 real field photo exists (no real deployment).

## BCA 404 project-4 (semester-7/project-4) -- [x] DONE (session 17), 64 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **SikshyaSignal** (invented early-warning tool ranking 600 simulated first-year students by risk of failing; NumPy logistic regression written from scratch, seed 404). Different from CampusShelf (P1), ClinicQ (P2), KhetSense (P3). 5 units, 24,169 raw words.
- Photos (bca404/, licence-gated, all viewed): students (Sankhu school building, CC BY-SA), gpu (Radeon card), datacenter (CERN hall). Reused: bca306/code, bca306/tech, bca256/poster.
- U1 Framing/ethics: Fig 1.1 pipeline, Plate 1.1 (3-up school/GPU/datacentre), Fig 1.2 accuracy trap bars, Fig 1.3 should-we-use-ML chart; dataset + baseline script; 8 reasons (1.6); 2 medium + 1 long.
- U2 Data: Fig 2.1 histogram, 2.2 split, 2.3 leakage timeline, Plate 2.1 (code photo + cleaning flow SVG); cleaning, features/correlation/split, leakage-AUC scripts; 8 habits (2.6); 2 medium + 1 long.
- U3 Modelling: Fig 3.1 logistic regression, 3.2 learning curve (Axes), 3.3 confusion matrix, 3.4 precision-recall trade-off; training log, threshold sweep + test report, 5-fold CV + group fairness + bootstrap; 8 ways models mislead (3.5); 2 medium + 1 long. No photo (abstract topic).
- U4 Deployment: Fig 4.1 request life, 4.2 PSI + AUC bars, Plate 4.1 (technician photo + deployment-levels SVG); model.json + predict service, 8 PASS-line tests, PSI drift on 3 batches (covariate vs concept drift); privacy table, Dockerfile (fence tag `text`, not run); 8 habits (4.6); 2 medium + 1 long.
- U5 Defence: Fig 5.1 report map, 5.2 talk timeline, Plate 5.1 (poster photo + results-slide SVG); report page budget, 15-minute plan, shingle-similarity, rubric scripts; 12 viva Q&A; 8 habits (5.7); 2 medium + 1 long.
- Gotchas: `Axes.tag(x, y, s)` takes DATA coordinates (not ax.X/ax.Y pixels); `Axes.axes(xl, yl)` writes labels inside the plot corners and collides with tick labels, so pass empty strings and draw labels with `f.text` outside; every python block repeats a 12-line data generator (blocks must be self-contained for fill_script_outputs); text near-empty p3 warning is only the TOC overflow (warn, not fail).

## BCA 452 internship (semester-8/internship) -- [x] DONE (session 18), 49 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **InternTrail**: invented 8-week placement of Anisha Gurung at the invented Lalitpur agency Himal Digital; different from CampusShelf, ClinicQ, KhetSense, SikshyaSignal. 5 units, 17,628 raw words.
- Photos (bca452/, licence-gated, all viewed): berlin (open-plan office), cowork (lounge), handshake, interview (career-fair table), lanyard (ID badge). Rejected after viewing: NIH "Interns" (black-and-white lab). Reused: bca256/kanban, bca256/pair, bca256/poster, bca306/code, bca306/tech, bca105/speaker, bca105/pen.
- U1 Placement search: Fig 1.1 12-week search timeline, Fig 1.2 CV anatomy, Plate 1.1 (3-up office/interview/handshake); weighted shortlist script (Himal 4.25, sensitivity 4.10); 8 reasons (1.6); 2 medium + 1 long.
- U2 Conduct: Fig 2.1 four information levels, Fig 2.2 15-minute rule, Plate 2.1 (lounge + badge photos + channel-guide SVG); secrets-scanner script (4 findings, masked); 8 habits (2.5); 2 medium + 1 long.
- U3 Weeks: Fig 3.1 hours-per-week stacked bars (from script output), Fig 3.2 8-week plan chart, Plate 3.1 (kanban + pair photos + log-card SVG); simulated 40-day log analysis (276.5 h, 33 of 40 days >= 6 h so L3 honestly fails); 8 rules (3.5); 2 medium + 1 long.
- U4 Technical: Fig 4.1 ticket life cycle, Plate 4.1 (code + technician photos + review-request SVG); HD-31 VAT rounding bug reproduced (float 0.565 -> 55.25 vs Decimal 55.26, 2 of 4 invoices) and a 6-test suite (6 passed); 8 practices (4.7); 2 medium + 1 long.
- U5 Report/viva: Fig 5.1 report map, Fig 5.2 skills before/after bars, Plate 5.1 (speaker + letter + poster photos); report page budget script (40 pp, ch 4+5 = 40%), skills self-assessment script (2.25 -> 4.00); 12 viva Q&A; 8 habits (5.7); 2 medium + 1 long.
- Gotchas: square `@ svg` cells inside photogrid need font size >= 12.5 on a 300 px canvas (scale ~0.53) or text drops below 6 pt; always close python fences; heredoc with quoted EOF keeps `\"` literally (run `sed -i 's/\\"/"/g'` on the file); `fill_script_outputs.py` can leave a duplicate trailing fence, check fence count is even.

## BCA 154 mathematics-2 (semester-2/mathematics-2) -- [x] POLISHED (session 18), 34 pp (was 23), qa fails=0
Math-heavy, so SVG figures and worked answers rather than photographs (no suitable real photo; none claimed).
- U1: Fig 1.1 determinant as area (det 5 vs singular det 0); 1.5 eight uses of matrices; Q1 (5 marks) adjoint inverse of a 3x3, Q2 (10 marks) matrix operations, determinant properties.
- U2: Fig 2.1 three line pictures (unique / none / infinite) via Axes; 2.7 eight uses of linear systems; Q1 Gaussian elimination (1,2,3), Q2 rank test + Cramer.
- U3: Fig 3.1 four subspaces; 3.7 eight uses; Q1 rank/nullity/bases of a 3x3, Q2 independence, basis, dimension, linear maps, kernel/image.
- U4: Fig 4.1 circle to ellipse with eigen-axes; 4.5 eight uses; Q1 eigen-decomposition of [[2,1],[1,2]] and A^5, Q2 diagonalisation + Markov steady state (5/6, 1/6).
- U5: Fig 5.1 plane, normal, distance; 5.6 eight uses; Q1 line through two points, Q2 plane through three points, distance 5/7, triangle area 3.5.
- Every number in the new answers was recomputed with SymPy; `check_math2.py` still prints ALL OK. Not done: no photographs; units 1 to 5 keep their original short Practice answers.

## BCA 151 discrete-structure (semester-2/discrete-structure) -- [x] POLISHED (sessions 18-19): all 6 units; 49 pp, qa fails=0
Math-heavy: SVG figures and worked answers, no photographs (none claimed).
- U1: Fig 1.1 proof-technique decision chain; 1.7 eight uses of logic; Q1 contrapositive truth table, Q2 proof techniques with examples.
- U2: Fig 2.1 injective / surjective / bijective mapping diagrams; 2.6 eight uses; Q1 equivalence relation mod 3, Q2 function types, composition, inverse, 2^n subsets.
- U3: Fig 3.1 Pascal's triangle; 3.9 eight uses; Q1 KATHMANDU arrangements (181,440; A's together 40,320), Q2 counting toolkit (74, 67, D4 = 9).
- U4: Fig 4.1 merge-sort recursion tree; 4.6 eight uses; Q1 induction (sum of odd numbers), Q2 recurrence a(n)=2*3^n-2^n verified numerically, Hanoi 1,023, merge sort.
- U5 (session 19): Fig 5.1 weighted graph with MST (thick teal) and Dijkstra distances (red); 5.7 eight uses; Q1 Kruskal MST (13), Q2 Dijkstra table + BFS/MST comparison.
- U6 (session 19): Fig 6.1 clock arithmetic mod 12 + toy RSA message path; 6.7 eight uses; Q1 extended Euclid (gcd 21 = 5*105 - 2*252), Q2 RSA + group/ring/field. `check_discrete.py` ALL OK.

## BCA 153 oop-in-java (semester-2/oop-in-java) -- [x] POLISHED (session 19), 66 pp (was 41), qa fails=0
- Photos (bca153/, licence-gated, all viewed): gosling (James Gosling portrait), simchip (smart-card chip die, Java Card context), socdie (SoC die, threads/cores), dcrack (data-centre aisle, JDBC servers).
- U1: Plate 1.1 (Gosling + SIM-chip die), Fig 1.1 write-once-run-anywhere pipeline, Fig 1.2 four pillars on an Account class diagram; 1.7 eight features; Q1 JDK/JRE/JVM, Q2 pillars + BankDemo run.
- U2: Fig 2.1 stack vs heap references; 2.8 eight benefits; Q1 pass-by-value (PassDemo run), Q2 Student class with equals/hashCode in HashSet (StudentDemo run).
- U3: Fig 3.1 payroll interface/abstract/subclass design; 3.7 eight uses; Q1 abstract class vs interface (PayDemo run), Q2 overloading/overriding/dispatch (DispatchDemo run).
- U4: Fig 4.1 Throwable family, Fig 4.2 string pool; 4.5 eight benefits; Q1 exceptions (ExcDemo run), Q2 String/StringBuilder (StringDemo run).
- U5: Fig 5.1 collections map, Fig 5.2 stream pipeline; 5.7 eight uses; Q1 List/Set/Map (CollDemo run), Q2 lambdas/streams/generics (StreamDemo run).
- U6: Plate 6.1 (SoC die + data-centre aisle), Fig 6.1 thread states, Fig 6.2 JDBC architecture; 6.6 eight uses; Q1 threads/race/executor (RaceDemo run), Q2 JDBC on H2 in-memory (JdbcDemo run).
- All new Java programs compiled and run with JDK 17 (`fill_java_outputs.py`); needs `sudo apt-get install openjdk-17-jdk-headless libh2-java libslf4j-java libservlet-api-java`. After fill, run `/tmp/fixblank.py`-style pass: add a blank line after every closing ```output fence when text follows directly (otherwise tables/paragraphs may merge into the code placeholder).
- Not done: old short Practice answers kept; no photograph for abstract units 2-5 (none claimed).

## System Analysis and Design (semester-3/system-analysis-and-design) -- [x] POLISHED (session 19), 51 pp (was 33), qa fails=0
Had ZERO figures before. Photos are reuses of already-licensed assets (no new downloads): bca256 kanban/scrum/pair, bca452 interview, bca101 atm-nepal/android, bca306 rack, bca404 datacenter.
- U1: Fig 1.1 SDLC waterfall with cost multipliers, Plate 1.1 (3-up agile practice photos); 1.11 eight reasons; Q1 SDLC phases, Q2 model comparison + recommendation.
- U2: Fig 2.1 cumulative discounted net benefit (payback 2.35 yr), Fig 2.2 Gantt to scale; 2.7 eight reasons; Q1 six feasibility types, Q2 library NPV/ROI/payback/BCR (all recomputed in Python: NPV 125,229; BCR 1.30; IRR 30.7%; discounted payback 2.64 yr).
- U3: Plate 3.1 (interview photo + techniques SVG), Fig 3.1 context diagram, 3.2 level-0 DFD, 3.3 ER with LOAN associative entity; 3.5 eight benefits; Q1 DFD symbols/rules, Q2 library models.
- U4: Fig 4.1 normalisation 1NF-3NF, Plate 4.1 (ATM + smartphone UI), Fig 4.2 annotated admission form; 4.6 eight rules; Q1 normalise ORDER_FORM, Q2 form/report/interface guidelines.
- U5: Fig 5.1 V-model testing, 5.2 installation strategies timeline, 5.3 maintenance 2x2, Plate 5.1 (rack + data-centre photos); 5.4 eight reasons; Q1 test levels, Q2 installation + maintenance types.
- Not done: old short Practice answers kept; no checks script exists for this book (numbers verified ad hoc).

## BCA 205 probability-and-statistics (semester-3/probability-and-statistics) -- [x] POLISHED (session 20), 57 pp (was 35), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca205/, licence-gated, all viewed): hollerith (CHM replica, CC0), pearson (public domain), galton (Galton board, CC BY-SA), gosset (1908 portrait, PD), guinness (Gosset plaque, CC BY-SA). Fisher snapshot rejected (family photo, no value).
- U1: Fig 1.1 data-type tree, Plate 1.1 (Hollerith photo + 5-step study pipeline SVG); 8 reasons (1.6); 2 medium + 1 long.
- U2: Fig 2.1 grouped histogram with mean/median/mode, Fig 2.2 skewness trio, Fig 2.3 box plot; 8 uses (2.4); 2 medium (grouped averages, CV compare) + 1 long (six dispersion measures, computed).
- U3: Fig 3.1 three scatter plots (r = +0.98, -0.19, -0.96), Plate 3.1 (Pearson portrait + least-squares residual SVG), Fig 3.2 two regression lines; 8 uses (3.4); 2 medium (r + regression; Spearman) + 1 long.
- U4: Fig 4.1 Bayes natural-frequency tree, Plate 4.1 (Galton board photo + 68-95-99.7 SVG), Fig 4.2 binomial and Poisson bars, Fig 4.3 normal areas; 8 uses (4.6); 2 medium (Bayes, normal) + 1 long (binomial vs Poisson, approximation compared).
- U5: Fig 5.1 survey life cycle with error entry points, Fig 5.2 sample size vs margin, Fig 5.3 bias-vs-scatter targets (no photo: no suitable free Nepal survey photo found); 8 rules (5.6); 2 medium + 1 long.
- U6: Fig 6.1 four sampling designs on a 10x10 grid, Plate 6.1 (Gosset portrait + Guinness plaque + t vs z SVG, 3-up), Fig 6.2 CLT, Fig 6.3 chi-square tail; 8 designs/tools (6.10); 2 medium (SRSWOR, Neyman) + 1 long (t-test with CI, z compared).
- U7: Fig 7.1 variation split (strip plot + stacked SS bar), Fig 7.2 F(2,12) tail, Fig 7.3 randomised block layout, Fig 7.4 two-way SS partition (no photo: abstract topic); 8 uses (7.7); 2 medium + 1 long (two-way ANOVA).
- All new numbers recomputed with numpy/scipy before writing; `check_stats.py --assert` still passes. No fill_script_outputs run needed (no code blocks).

## BCA 206 applied-economics (semester-3/applied-economics) -- [x] POLISHED (session 21), 66 pp (was 34), qa fails=0 warns=1 (p3 near-empty, pre-existing)
Had ZERO figures before (graphs "described in words"). 27 figures/plates, 10 photos (bca206/, licence-gated, all viewed): smith, marshall, keynes (portraits), asan (vegetable seller), spice (Asan spice lane), kalimati (wholesale market street), ntc (Nepal Telecom head office), note (old NRB banknote), nrb (Thapathali), dryport (Birgunj customs). Rejected after viewing: Kulekhani (lake shot, no dam).
- U1: Fig 1.1 PPF with U/X points and growth shift, Fig 1.2 equilibrium + ceiling | demand shift + tax, Plate 1.1 (3-up Smith/Marshall/Asan); 8 applications (1.7); 2 medium + 1 long (equilibrium, CS 1,156, DWL 15).
- U2: Fig 2.1 five elasticity cases, Fig 2.2 linear demand elasticity zones + revenue curve, Plate 2.1 (spice photo + bumper-harvest SVG); 8 uses (2.6); 2 medium + 1 long.
- U3: Fig 3.1 TU/MU, Fig 3.2 equi-marginal bars, Fig 3.3 IC + budget + Hicks A->C->B; 8 uses (3.5); 2 medium + 1 long. No photo (abstract).
- U4: Fig 4.1 total and unit cost curves from the schedule, Fig 4.2 LAC envelope, Fig 4.3 revenue curves (3 panels); 8 uses (4.6); 2 medium + 1 long. No photo (abstract).
- U5: Plate 5.1 (3-up Kalimati/spice/NTC), Fig 5.1 price-taker cases, 5.2 monopoly + DWL 800, 5.3 price discrimination, 5.4 kinked demand + prisoner's-dilemma pay-offs; 8 lessons (5.8); 3 medium + 1 long.
- U6: Fig 6.1 four-sector circular flow, 6.2 Keynesian cross + multiplier chain, 6.3 GDP->DI waterfall, Plate 6.1 (Keynes/Kalimati/Asan); 8 uses (6.6); 2 medium + 1 long.
- U7: Plate 7.1 (note/NRB/dry port), Fig 7.1 deposit creation, 7.2 AD-AS demand-pull and cost-push, 7.3 policy transmission chain, 7.4 BoP waterfall; 8 roles (7.6); 2 medium + 2 long.
- All new numbers recomputed with Python (check_economics.py still passes). No fill_script_outputs needed (no code blocks).

## BCA 354 technical-writing (semester-6/technical-writing) -- [x] POLISHED (session 22), 59 pp (was 36), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca354/, licence-gated, all viewed): typewriter (Olympia Simplex 1935), manual (car owner's manual), warning (tsunami hazard sign), library (Graz reading room). Reused: bca306 code/rack, bca105 scrum/pen, bca452 handshake/interview.
- U1: Plate 1.1 (3-up typewriter/manual/sign), Fig 1.1 inverted pyramid, Fig 1.2 writing-process loop; 1.8.1 eight habits; Q1, Q2 (5 marks), Q3 (10 marks).
- U2: Fig 2.1 FK/Fog bars from the executed program numbers, Fig 2.2 sentence surgery; 2.5.1 eight benefits of plain language; Q1, Q2 (FRE 64.71, FK 7.96 computed), Q3.
- U3: Plate 3.1 (code/rack/briefing), Fig 3.1 Diataxis 2x2, Fig 3.2 requirement anatomy + postmortem timeline; 3.7.1 eight reasons to document; Q1-Q3.
- U4: Plate 4.1 (library photo + IMRaD hourglass SVG), Fig 4.1 APA vs IEEE anatomy; 4.6.1 eight habits; Q1-Q3.
- U5: Fig 5.1 lie factor 20 vs 1, Fig 5.2 chart chooser, Fig 5.3 WCAG contrast swatches; 5.7.1 eight rules; Q1-Q3.
- U6: Plate 6.1 (letter/handshake/career fair), Fig 6.1 four editing levels, Fig 6.2 concision 44 to 22 words; 6.6.1 eight habits; Q1-Q3 (e-mail specimen).
- No code was added or changed, so fill_script_outputs.py was NOT run; existing executed outputs untouched.

## BCA 403 financial-accounting (semester-7/financial-accounting) -- [x] POLISHED (session 22), 65 pp (was 37), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca403/, licence-gated, all viewed): ledger2 (1855 merchant ledger page), ledger (bound account book), register (antique cash register, Darjeeling), cheque (1909 cheque), note (old Nepal Rastra Bank 5-rupee note), warehouse (racked cartons). Reused bca306/code.
- Section numbering: new "seeing the ideas" section is inserted BEFORE the old "Summary and exercises", which is renumbered (+1). Helper `/tmp/ins3.py` (recreate: regex on `## U.K Summary and exercises`, `@S@` placeholder for U.K).
- U1: Plate 1.1 (ledger/register/cheque), Fig 1.1 equation in 3 transactions, Fig 1.2 accounting cycle; 1.7.1 eight uses of accounting information; Q1-Q3 (Q3 10 marks).
- U2: Plate 2.1 (note photo + tax-invoice SVG), Fig 2.1 Dr/Cr rules, Fig 2.2 Cash T-account (4,92,000); 2.8.1 eight controls; Q1-Q3 with trial balance 7,31,000.
- U3: Plate 3.1 (account book + three-column cash book SVG), Fig 3.1 subsidiary books, Fig 3.2 transposition hunt (900); 3.7.1 eight habits; Q1-Q3 (suspense).
- U4: Plate 4.1 (cheque + anatomy SVG), Fig 4.1 reconciliation bridge (49,050), Fig 4.2 sorting differences; 4.7.1 eight benefits; Q1-Q3.
- U5: Plate 5.1 (warehouse + FIFO layers SVG), Fig 5.1 SLM vs WDV curves, Fig 5.2 disposal (gain 24,000); 5.7.1 eight reasons; Q1-Q3 (FIFO 14,900 vs WAC 15,555.56).
- U6: Fig 6.1 profit waterfall, Fig 6.2 balance sheet to scale (7,69,000), Fig 6.3 adjustments double effect (no photo: abstract); 6.8.1 eight checks; Q1-Q3.
- U7: Plate 7.1 (code photo + ledger-tables SVG), Fig 7.1 ratio dashboard, Fig 7.2 DuPont tree; 7.9.1 eight uses; Q1-Q3.
- All figures use numbers already produced by the book's executed programs (no code changed, fill_script_outputs.py NOT run). Gotcha: a heading directly above a figure can be stranded at a page bottom (qa FAIL): add one sentence under the heading.

## BCA 451 cloud-computing (semester-8/cloud-computing) -- [x] POLISHED (session 23), 65 pp (was 37), qa fails=0 warns=0
- Photos (bca451/, licence-gated, all viewed): facebook (data-centre aisle), xeon (Broadwell-EP die), meter (kWh meter), containers (Chittagong port), tape (tape library), hsm (nCipher HSM), queue (station ticket queue). Reused: bca101 hdd-platter/nvme/fibre-cable/router, bca306 padlock/switch, bca403 register.
- U1: Plate 1.1 (3-up aisle/Xeon die/meter), Fig 1.1 NIST 5-4-3, 1.2 who-manages-what grid, 1.3 elasticity vs fixed fleet (430 vs 1,200 server-hours); 1.8.1 eight benefits; Q1-Q3.
- U2: Plate 2.1 (container yard + image-layer SVG), Fig 2.1 type-1/type-2/containers stacks, 2.2 nested paging; 2.8.1 eight benefits; Q1-Q3.
- U3: Plate 3.1 (tape/HDD/NVMe), Fig 3.1 replication vs RS(4,2), 3.2 hash ring, 3.3 quorum; 3.5.1 eight features; Q1-Q3.
- U4: Plate 4.1 (fibre/switch/router), Fig 4.1 VPC two-AZ, 4.2 VXLAN packet to scale, 4.3 CDN + LB path; 4.7.1 eight benefits; Q1-Q3.
- U5: Plate 5.1 (queue photo + M/M/1 curve SVG), Fig 5.1 Kubernetes architecture, 5.2 HPA 4->8->5, 5.3 monolith vs microservices; 5.6.1 eight benefits; Q1-Q4 (M/M/1 lambda 90, mu 100 recomputed).
- U6: Plate 6.1 (padlock + HSM), Fig 6.1 shared responsibility, 6.2 IAM evaluation, 6.3 envelope encryption (600 MB vs 10 TB); 6.6.1 eight practices; Q1-Q4.
- U7: Plate 7.1 (meter/register/aisle), Fig 7.1 pricing index, 7.2 break-even 5,256 h, 7.3 series vs parallel availability, 7.4 nines (log bars); 7.7.1 eight FinOps practices; Q1-Q4.
- No code was changed, so fill_script_outputs.py was NOT run. Helper `/tmp/ins2.py` inserts figures before "K Summary and exercises" (renumbers it) and appends answers.

## Queue
- [x] BCA 103 digital-logic DONE ( need DIP 74xx / breadboard photos via notes/pipeline/assets.py search)
- [x] programming-in-c DONE (session 12)
- [x] hardware-workshop DONE (session 12)
- [x] mathematics-1 (BCA 104) DONE (session 13)
- [x] professional-communication-ethics (BCA 105) DONE (session 13)
- [x] BCA 256 Project I DONE (session 14)
- [x] BCA 306 Project II DONE (session 15)
- [x] BCA 356 Project III DONE (session 16)
- [x] BCA 404 Project IV DONE (session 17)
- [x] BCA 452 Internship DONE (session 18)
- [x] BCA 154 Mathematics II polished (session 18, SVG + answers, no photos)
- [x] BCA 151 Discrete Structure units 5-6 (session 19)
- [x] BCA 153 OOP in Java (session 19, 66 pp)
- [x] BCA 153 OOP in Java and System Analysis and Design polished (session 19)
- [x] Probability and Statistics polished (session 20, 35 -> 57 pp)
- [x] Applied Economics polished (session 21, 34 -> 66 pp)
- [x] Technical Writing polished (session 22, 36 -> 59 pp)
- [x] Financial Accounting polished (session 22, 37 -> 65 pp)
- [x] Cloud Computing polished (session 23, 37 -> 65 pp)
- [ ] (NEXT SESSION STARTS HERE) polish remaining thin core books by page count: Numerical Methods (43), Cyber Security (43), then: the rest of Semesters II-VIII; apply the 5 pillars (photos where physical, SVGs, 8-point sections, 5/10-mark answers)
- [ ] 3 remaining non-core slots: BCA 402 (SPM, if not core), Elective I/II (BCA 405/406), Elective III/IV (BCA 453/454); the elective subjects are not named in CURRICULUM.md, pick from the TU list there; then polish semesters II-VIII one book at a time
