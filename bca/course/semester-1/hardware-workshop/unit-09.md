---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 9
title: Final Practical Assessment
area: BCA 106 · Hardware Workshop · Unit 9
---

The course ends with a practical examination in five stations: identify and handle hardware, assemble and disassemble a PC, set up a wired LAN, solve simulated faults, and carry out maintenance tasks. This unit gives you the checklist for each station, a sample marking scheme, 40 viva questions with answers and a revision plan.

::: key What this unit gives you
- Station-by-station task lists matching the syllabus: hardware identification and handling, PC assembly/disassembly, network setup, troubleshooting simulations and maintenance tasks.
- A sample 50-mark rubric (colleges set their own split; use it for self-assessment).
- A bank of viva questions with model answers, and a timed practice plan.
:::

## 9.1 How the assessment works

```svgfig label="9.1" caption="The five assessment stations. Each station checks one outcome of the course and takes about 10 to 15 minutes. The examiner watches safety habits (strap, power off, tools) at every station, and follows each task with viva questions."
f = Fig(760, 200)
st = [("A", "Identify and\nhandle hardware", "Label parts, state\nfunctions, use ESD strap"), ("B", "Assemble and\ndisassemble a PC", "Build to POST,\nthen strip down"), ("C", "Wired LAN\nsetup", "Crimp, assign IPs,\nping test"), ("D", "Troubleshooting\nsimulation", "POST card, beeps,\nconnectivity fix"), ("E", "Maintenance\ntasks", "Clean, repaste,\ncheck PSU")]
for i, (k, a, b) in enumerate(st):
    x = 8 + i * 150
    f.box(x, 20, 134, 54, k + "  " + a, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    f.box(x, 90, 134, 54, b, fill="#ffffff", stroke=TEAL, size=10)
    if i < 4: f.arrow([(x + 134, 47), (x + 150, 47)], color=NAVY)
f.text(380, 176, "Safety is marked throughout: strap on, power off and unplugged, correct tools, no forcing.", size=11, color=NAVY, bold=True)
```

## 9.2 Station A: hardware identification and handling

**Tasks.** (1) Put on an **ESD strap** and set up the workbench. (2) Identify and label the parts on a demo board or opened PC: case and front-panel connectors, motherboard, CPU and cooler, RAM, ROM/BIOS chip and CMOS battery, PSU, storage drives, expansion cards. (3) State the function and one specification of each. (4) Identify RAM generations (SDRAM, DDR1 to DDR5) by notch and pin count, ROM types and a real versus a fake SSD. (5) Name the port or connector on the rear panel.

**Checklist.** Strap used; case opened safely; each label correct; functions stated in one sentence; no part touched by its contacts.

## 9.3 Station B: PC assembly and disassembly

**Tasks.** Assemble a PC from components to a first boot (Unit 4): install the CPU and apply paste, fit the cooler, RAM, M.2 or SATA drive, mount the board on standoffs, fit the PSU, connect the 24-pin, EPS and PCIe power, front-panel connectors and fans, then power on and reach BIOS. Set the boot order, a password, and read the POST result. Afterwards **disassemble** in reverse order and return the parts to their labelled places.

**Common marks lost:** missing I/O shield, forgotten EPS CPU cable, front-panel pins reversed (power switch has no polarity; LEDs do), RAM not clicked in, no paste, cables blocking fans.

## 9.4 Station C: network setup

**Tasks.** (1) Crimp one straight-through cable with T568B, test it. (2) Connect two PCs to a switch, set static addresses in 192.168.10.0/24 with mask 255.255.255.0 (or an address given by the examiner), (3) ping from PC1 to PC2 and to the gateway, (4) share a folder and read a file across the network, and (5) show `ipconfig /all`, `arp -a` and `tracert` output. A **wireless** extension: set an SSID and WPA2 password on the AP.

**Checklist.** Tester shows 1 to 8 in order; unique IPs and the same subnet; ping replies; the share path is correct; default password changed.

## 9.5 Station D: troubleshooting simulations

**Tasks.** The examiner introduces one fault: loose RAM, unplugged GPU power, a missing EPS cable, a bad patch cord, a wrong boot order, a disabled NIC. You: (1) describe the symptom, (2) give your theory, (3) test with the minimum configuration, POST card or tester, (4) fix, (5) verify, and (6) enter the finding in the log. Marks go to the **method**, not just to the cure.

| Fault planted | Expected diagnosis |
|---|---|
| Continuous beeps | RAM unseated: reseat, test each stick |
| Fans spin, no display, no beeps | CPU or GPU power unplugged, or monitor on the wrong input |
| "No bootable device" | Boot order or the drive cable; check the BIOS drive list |
| Link LED dark | Bad cable or port: tester, swap cable |
| 169.254 address | DHCP failure: cable, switch, `ipconfig /renew` |
| Printer offline | Cable, port, "use offline" setting, spooler service |

## 9.6 Station E: maintenance tasks

**Tasks.** Safely clean the interior (compressed air, brush, isopropyl alcohol), replace thermal paste on a demo CPU, **verify the PSU** (visual, tester, or paperclip test and multimeter on the 3.3, 5 and 12 V rails), check SMART status and temperatures with software, and tidy the cables for airflow.

**Checklist.** Power off and unplugged first; fan held while blowing; PSU not opened; paste amount about a pea; voltages inside ±5 %; log entry written.

## 9.7 Sample marking scheme (50 marks)

| Station | Marks | Examiner looks for |
|---|---|---|
| A. Identification and handling | 8 | Correct labels and functions, ESD practice |
| B. Assembly / disassembly | 14 | Correct order, secure fitting, successful POST |
| C. Network setup | 10 | Correct cable, IP plan, successful ping and share |
| D. Troubleshooting | 10 | Method, correct diagnosis, log |
| E. Maintenance | 5 | Cleaning, paste, PSU check |
| Viva voce | 3 | Clear, correct answers |
| **Total** | **50** | |

This split is a practice model. Use the marks your college or department announces for the real examination.

## 9.8 Viva question bank with answers

**Safety and tools**

1. *Why wear an ESD strap?* To discharge static electricity that can destroy chips; it is connected to bare chassis metal or a grounded point.
2. *Why should a PC be unplugged before opening?* The PSU keeps standby 5 V live on the board even when switched off.
3. *Name three tools in your kit.* Phillips screwdriver, anti-static strap, cable crimper, multimeter, tweezers.

**Components**

4. *What is the CPU socket?* The mechanical and electrical interface that decides which processors fit the board (LGA1700, AM5).
5. *What does the CMOS battery do?* Powers the real-time clock and keeps BIOS settings; a CR2032.
6. *Difference between DDR4 and DDR5?* Different notch, 288 pins on both but the notch differs; DDR5 is faster and runs at 1.1 V.
7. *RAM versus ROM?* RAM is volatile working memory; ROM keeps firmware without power.
8. *SSD versus HDD?* SSD is flash with no moving parts, faster and quieter; HDD is magnetic platters, cheaper per GB.
9. *What is NVMe?* A protocol for SSDs over PCIe, in the M.2 slot, much faster than SATA.
10. *What are the PSU rails?* +3.3 V, +5 V, +12 V, with −12 V and +5 VSB.
11. *How do you test a PSU?* Visual inspection, PSU tester, paperclip test (green pin 16 to black) with multimeter checks within ±5 %.
12. *What is TDP?* Thermal design power: the heat in watts the cooler must remove.
13. *What does the northbridge do?* It linked the CPU to memory and graphics; in modern CPUs the memory controller is inside the processor.
14. *Which connector powers a GPU?* 6+2 pin PCIe, or 12VHPWR on new cards.

**Assembly and OS**

15. *What is POST?* Power-on self-test run by firmware before booting.
16. *Why use standoffs?* They keep the board off the metal tray and prevent short circuits.
17. *Why apply a pea of thermal paste?* To fill microscopic gaps for heat transfer; too much spills and insulates.
18. *What is the UEFI secure boot?* A feature that allows only signed bootloaders to start.
19. *Difference between MBR and GPT?* MBR: up to 2 TB and four primary partitions; GPT: huge disks and 128 partitions, used with UEFI.
20. *How do you install an OS from USB?* Create a bootable drive, select it in the boot menu, partition, install, drivers, updates.

**Networking**

21. *Hub versus switch?* Hub repeats to all ports; switch forwards to the one destination port by MAC.
22. *Which cable joins PC to PC (old hardware)?* Crossover.
23. *Write the T568B order.* Wh/orange, orange, wh/green, blue, wh/blue, green, wh/brown, brown.
24. *Maximum UTP length?* 100 m.
25. *What is a subnet mask?* It separates the network part and the host part of an IP address.
26. *Usable hosts in a /26?* 2⁶ − 2 = 62.
27. *What is the default gateway?* The router address used to reach other networks.
28. *What does DNS do?* Translates names to IP addresses.
29. *What does ping use?* ICMP echo request and reply.
30. *What does `ipconfig /renew` do?* Requests a new DHCP lease.
31. *Why is MAC filtering weak?* MAC addresses can be copied.
32. *What is a topology?* The arrangement of devices and links; star is the standard.

**Troubleshooting and maintenance**

33. *Your five-step method?* Identify, test, isolate, fix, verify, then document.
34. *What is the minimum configuration test?* CPU, one RAM, PSU, speaker.
35. *Continuous beeps usually mean?* RAM problem.
36. *How often should a desktop be cleaned?* Every 6 months.
37. *What do you use to clean the contacts?* Isopropyl alcohol 90 % or more.
38. *What does a swollen laptop battery mean?* Cell damage; stop use and replace.
39. *What does SMART warn about?* Drive health; rising reallocated sectors predict failure.
40. *When do you update the BIOS?* Only for a security fix, new hardware support or a known bug, on stable power.

## 9.9 Revision plan and eight exam-day rules

**One-week plan.** Day 1 components and specifications (Units 1 and 3). Day 2 PSU and memory. Day 3 assembly (Unit 4). Day 4 cables, crimping and topologies (Units 2 and 5). Day 5 IP addressing and subnets (Unit 6). Day 6 troubleshooting scenarios (Unit 7). Day 7 maintenance (Unit 8) and a full timed mock of the five stations.

1. Arrive early and check the tools before the examiner calls you.
2. Strap on and power off before touching anything.
3. Say what you are doing aloud: the examiner marks the method.
4. Do not force connectors; read the keying.
5. Test every cable and every link before reporting success.
6. Keep your workspace tidy; return parts to their trays.
7. Write the log honestly, including what failed.
8. In the viva answer in short, exact sentences; say "I do not know" rather than guess.

## Chapter summary

- The practical exam has five stations and a viva; marks go to method, safety and verification as well as the result.
- Practise each station until it takes under 15 minutes, with the checklists above.
- Use the question bank to rehearse short, exact answers.

## Practice

1. Prepare the sequence of tasks for the PC assembly station in the order you will do them.
2. Draw the network diagram for Station C and list the commands you will run.
3. Write a log entry for a simulated "no display" fault.
4. List the PSU rails with colours and the allowed ranges.
5. Role-play a viva: ask a partner ten questions from 9.8 and time the answers.

::: note Answers and worked solutions
**1.** Strap and workspace; CPU; paste and cooler; RAM; M.2; mount board in case; PSU and cables; front panel; drives and GPU; cable tidy; first boot and BIOS; POST check; disassemble in reverse.
**2.** Two PCs and a switch (Figure 6.2 style); `ipconfig /all`, `ping gateway`, `ping PC2`, `arp -a`, `tracert`.
**3.** Date, PC ID, symptom "no display", tests (monitor on another PC, minimum configuration, RAM reseat, GPU swap), cause, fix, verification, time.
**4.** +3.3 V orange 3.135 to 3.465 V; +5 V red 4.75 to 5.25 V; +12 V yellow 11.4 to 12.6 V; −12 V blue; +5 VSB purple.
**5.** Aim for answers under 20 seconds, with the term, the definition and one example.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). List the tasks of a final practical assessment in Hardware Workshop.**

Hardware identification and handling (label parts, use anti-static measures); PC assembly and disassembly with guided practice; network setup (configure a wired LAN, assign IPs and test with ping); troubleshooting simulations (POST card, beep codes, connectivity fixes); and maintenance tasks (clean components, apply thermal paste, verify the power supply). Figure 9.1 shows the five stations.

**Q (10 marks). Describe how you would assemble a PC, test it and set up a two-PC network.**

*Introduction.* The task combines assembly, firmware, operating-system and networking skills.

*Assembly.* Strap on; install CPU, paste, cooler, RAM and M.2 on the board; fit the board in the case on standoffs; install the PSU and connect the 24-pin, EPS, PCIe, SATA and front-panel cables; tidy cables.

*First boot.* Power on, watch POST, enter BIOS, check detected devices, set boot order and password.

*Software.* Install the OS from USB, then drivers and updates.

*Network.* Crimp and test two straight-through cables, connect both PCs to a switch, set 192.168.10.20 and .21 with mask 255.255.255.0, ping each way, share a folder, and read it as `\\192.168.10.20\Notes`.

*Verification.* Record results (ipconfig, ping replies) in the log and sign off the checklist.
