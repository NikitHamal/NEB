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

## Queue
- [x] BCA 103 digital-logic DONE ( need DIP 74xx / breadboard photos via notes/pipeline/assets.py search)
- [x] programming-in-c DONE (session 12)
- [x] hardware-workshop DONE (session 12)
- [ ] (NEXT SESSION STARTS HERE) mathematics-1 (BCA 104), then professional-communication-ethics (BCA 105)
- [ ] non-core slots (256, 356, 403 project, 452, electives), then semesters II-VIII
