---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 7
title: Problem Solving Techniques
area: BCA 106 · Hardware Workshop · Unit 7
---

A good technician is not someone who knows every fault but someone who follows a method. This unit gives you that method: look first, change one thing at a time, read what the machine tells you, keep a log, and always follow the sequence Identify, Test, Isolate, Fix, Verify.

::: key What this unit gives you
- Visual inspection: loose cables, damaged ports, swollen capacitors, dust and burn marks.
- The elimination method: test one part at a time, and the minimum configuration test.
- Reading BIOS/UEFI messages and beep codes; network tests with ping, ipconfig/ifconfig and a cable tester.
- The troubleshooting log, and the five-step cycle Identify, Test, Isolate, Fix, Verify.
:::

## 7.1 The systematic approach: Identify, Test, Isolate, Fix, Verify

```svgfig label="7.1" caption="The troubleshooting cycle. If Verify fails, go back to Identify with what you have learned; if it passes, document the result. Never skip the last box, because a fix that is not verified and recorded will come back."
f = Fig(760, 190)
steps = [("1 Identify", "Ask, observe,\nreproduce the fault"), ("2 Test", "Make a theory;\ncheck it simply"), ("3 Isolate", "Narrow to one\npart or one link"), ("4 Fix", "Reseat, replace,\nreconfigure"), ("5 Verify", "Check full function;\nask the user")]
for i, (a, b) in enumerate(steps):
    x = 10 + i * 150
    f.box(x, 24, 132, 70, a + "\n" + b, fill=BLUE if i < 4 else SOFT, stroke=NAVY, size=11, bold=(i == 99))
    if i < 4: f.arrow([(x + 132, 59), (x + 150, 59)], color=NAVY)
f.arrow([(692, 94), (692, 130), (76, 130), (76, 94)], color=RED, label="not fixed: back to Identify", lpos=(384, 120))
f.text(380, 168, "Then: Document findings, actions and outcome in the log.", size=11, color=NAVY, bold=True)
```

1. **Identify.** Ask the user what changed (new software, power cut, moved, spilled liquid); when did it start; does it happen always or sometimes; any error messages. Reproduce the fault yourself. *Back up data first* if the machine still runs.
2. **Test (establish a theory).** From the symptoms list the likely causes, starting with the **simplest and most probable**: power cable, loose connector, wrong setting, then component failure.
3. **Isolate.** Test one cause at a time until the fault is confined to one part, one cable or one setting.
4. **Fix.** Reseat, clean, reconfigure, update or replace; change **one thing at a time**.
5. **Verify.** Confirm the original complaint is gone and nothing new is broken. Then document.

## 7.2 Start with a visual inspection

Most faults are found before any tool is used. Switch off, unplug and look.

| Look at | What you may find | Action |
|---|---|---|
| Power cable and socket | Loose plug, cut cable, dead extension board | Reseat, swap |
| Internal cables | SATA, 24-pin or front-panel cable half-inserted | Reseat firmly |
| Ports (USB, HDMI, RJ45, charging) | Bent pins, broken tab, dirt | Replace the port or cable |
| Capacitors on the board | Domed tops, leaked brown fluid | Replace the board or PSU |
| CPU cooler and fans | Dust, stopped fan, loose clip | Clean, replace |
| RAM and cards | Not fully seated, dust on contacts | Reseat, clean with isopropyl alcohol |
| Burn marks or smell | Short circuit | Isolate; do not power on |
| Liquid damage | Corrosion, white deposits | Dry, clean, test after 48 hours |

**Network equivalent.** Check the link LEDs, plug both ends, look for kinked or crushed cable and wrong ports before touching any setting.

## 7.3 The elimination method

**Test one part at a time.** Remove everything that is not essential and add parts back one by one until the fault returns. For a PC that will not boot use the **minimum configuration**: motherboard, CPU and cooler, one RAM stick in the slot named in the manual, PSU, a speaker or POST display. No drives, cards or USB devices. If that boots, add RAM, then GPU, then drive, then peripherals; the last item added is the suspect.

**Swap with a known good part.** Replace the suspected RAM stick, cable or PSU with one that works. If the fault stays, the original part was not the cause. This is the quickest and most reliable test in a lab with spare parts.

::: example Worked example: PC powers on, fans run, no display
Visual check: the GPU power cable is plugged in. *Test:* the monitor works on another PC, so the monitor and cable are fine. *Isolate:* with the minimum configuration and integrated graphics the PC reaches the BIOS, so the CPU, board and RAM are good and the fault is the graphics card or its slot. *Fix:* reseat the card; the fault remains. Swap in a known good card: the display appears, so the first card has failed. *Verify:* reinstall the OS drivers, run a stress test and confirm. *Document:* "GPU failed, replaced, tested 30 minutes under load".
:::

## 7.4 Messages, beeps and POST codes

On power-up the firmware speaks in three ways: **text** on the screen (for example "No bootable device", "CMOS checksum error", "CPU fan error", "Memory test fail"), **beeps** from the case speaker and **POST codes** on a debug display. Match them with the manual of the board (Unit 4.11).

| Message or signal | Meaning | Fix |
|---|---|---|
| CMOS checksum error / date reset | CMOS battery flat | Replace the CR2032 |
| CPU fan error | Fan unplugged, stopped or wrong header | Reseat or replace; connect to CPU_FAN |
| No bootable device | Wrong boot order, empty drive, dead drive | Set the boot order, check the drive |
| Continuous beeps | RAM fault | Reseat, test one stick at a time |
| 1 long 2 short | Video fault | Reseat the GPU, change the cable |
| Random reboot under load | Overheating or weak PSU | Clean the cooler, test the PSU rails |
| Blue screen (Windows) with a stop code | Driver, RAM or disk fault | Note the stop code, update drivers, run a memory test |

## 7.5 Network problem solving

Use the **diagnostic ladder** of Unit 6.6, from the inside out.

1. **Physical:** link LEDs lit? Cable tested? Port working?
2. **IP configuration:** `ipconfig /all` (Windows) or `ip addr` / `ifconfig` (Linux). An address starting 169.254 means DHCP failed; a mask or gateway that does not match the subnet is a configuration fault.
3. **Local reachability:** `ping` the gateway.
4. **Internet:** `ping 8.8.8.8`, then `ping` a name to test DNS; `tracert` to see where the path breaks.
5. **Cable tester or loop-back plug** to prove the cable or NIC.

::: example Worked example: "the internet does not work in the lab"
Lab PC: `ping 127.0.0.1` passes, `ping 192.168.10.21` (own) passes, `ping 192.168.10.1` (gateway) fails, and the switch port LED is dark. The cable tester shows pair 4-5 open. *Fix:* re-crimp the plug. *Verify:* link LED lights, gateway ping passes, `ping 8.8.8.8` passes, `ping www.tu.edu.np` passes. Total fault: one bad crimp.
:::

## 7.6 The troubleshooting log

A log records what was tried so that repeated problems are solved faster, and so that the next technician does not repeat your tests. Keep one entry per job.

| Field | Example |
|---|---|
| Date and technician | 12 Baisakh, R. Sharma |
| Device and ID | Lab PC-07, serial 4F9K2 |
| Symptom as reported | No display after power cut |
| Tests made (in order) | Monitor on another PC: OK. Minimum configuration: boots. GPU swap: fixed |
| Root cause | Graphics card failed |
| Action | Replaced with spare, installed driver |
| Verification | 30 min stress test passed |
| Time spent | 40 minutes |

## 7.7 Common troubleshooting scenarios

| Symptom | Likely causes (in the order to check) |
|---|---|
| PC does not turn on at all | Mains and switch, PSU switch, 24-pin, front-panel power pins, PSU failure |
| Turns on, no display | Monitor cable and input, RAM seating, GPU power, CPU, board |
| Boots but very slow | Full disk, malware, HDD failing, too little RAM, thermal throttling |
| Overheats or shuts down | Dust, dead fan, dried paste, no airflow, weak PSU |
| Strange noises | Failing HDD (clicking), fan bearing, loose screw |
| No sound | Mute, wrong output device, driver, jack |
| USB device not recognised | Cable, port, power, driver, try another port |
| Cannot print | Offline, cable, spooler, paper, driver |
| Wi-Fi drops | Distance, channel congestion, driver, power-saving setting |

## 7.8 Eight rules of troubleshooting

1. Ask first, then look, then touch.
2. Back up data before you change anything.
3. Start with the simplest and most likely cause.
4. Change one thing at a time, and undo it if it does not help.
5. Use known good parts to test.
6. Observe the safety rules: unplug, strap, no force.
7. Verify with the user and document the fix.
8. Look for the root cause so the fault does not return.

## Formula and fact sheet

- Cycle: Identify, Test (theory), Isolate, Fix, Verify, Document.
- Minimum configuration: board, CPU and cooler, one RAM stick, PSU, speaker.
- Ladder: loopback, own IP, gateway, 8.8.8.8, DNS name.
- 169.254.x.x means DHCP failure. Beeps depend on the BIOS vendor.
- Rail limits (±5 %): +12 V 11.4 to 12.6 V; +5 V 4.75 to 5.25 V; +3.3 V 3.135 to 3.465 V.

## Chapter summary

- Troubleshooting is a method, not guesswork: identify, test, isolate, fix and verify.
- A visual inspection finds many faults at once: loose cables, damaged ports, swollen capacitors, dust.
- The elimination method uses the minimum configuration and known good parts, one change at a time.
- BIOS/UEFI messages, beep codes and POST codes name the subsystem; network faults are tackled from the inside out with ping and ipconfig.
- A log turns each repair into reusable knowledge.

## Practice

1. List the five steps of the troubleshooting cycle with one sentence each.
2. What should you check in a visual inspection of (a) a PC (b) a network link?
3. Describe the minimum configuration test and when to use it.
4. A PC shows "CMOS checksum error" at every start. Give the cause and fix.
5. Explain how a known good part helps and give two examples.
6. A user cannot browse but `ping 8.8.8.8` works and `ping www.google.com` fails. Diagnose.
7. Design a troubleshooting log entry for a PC that restarts under load.
8. Give four causes of overheating and a test for each.
9. Why must you change one thing at a time?
10. Write a flow for "no power" on a desktop in six steps.

::: note Answers and worked solutions
**1.** Identify (gather facts), Test (form and check a theory), Isolate (narrow to one part), Fix (repair or replace), Verify (full function), and document.
**2.** (a) power cable, internal cables, ports, capacitors, fans, dust, RAM seating, burns. (b) link LEDs, plugs, cable damage, correct port.
**3.** Boot with board, CPU, one RAM, PSU and speaker only, when the PC does not boot or posts nothing; add parts one by one.
**4.** Flat CMOS battery; replace the CR2032 and reset the date.
**5.** A good part removes one variable. Examples: a good RAM stick, a spare patch cord, a working PSU.
**6.** The network is up, but DNS fails: set a working DNS server (8.8.8.8), flush the cache.
**7.** Symptom: restarts under load; tests: temperature monitor, PSU rails under load, memory test; cause: dust-blocked cooler; action: cleaned and re-pasted; verification: 1-hour stress test at 72 °C.
**8.** Dust (look), dead fan (spin test), dried paste (temperatures at idle), no airflow (case obstruction, cable clutter).
**9.** Otherwise you cannot know which change cured or caused the problem.
**10.** Check the mains and socket; PSU switch; 24-pin and CPU cable; front-panel power pins; test the PSU (paperclip, multimeter); swap the PSU.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the systematic troubleshooting approach.**

A technician follows Identify, Test, Isolate, Fix, Verify. First gather facts and reproduce the fault; then form a theory from the simplest likely cause and test it; narrow the fault to one part by eliminating the others; fix it by reseating, replacing or reconfiguring; and finally verify that the original problem is gone and record the work in a log. Following this order prevents random part swapping and repeated faults (Figure 7.1).

**Q (10 marks). A desktop PC powers on but shows no display. Describe how you would troubleshoot it.**

*Introduction.* The fault may lie in the monitor, cable, RAM, graphics card, CPU or board, so I would isolate it step by step.

*Identify.* Ask what changed; check whether there are beeps, fans or LEDs.

*Visual inspection.* Check the monitor cable and input source, power to the monitor, the GPU power cable and seating of RAM and card.

*Test and isolate.* Try the monitor on another PC; boot with the minimum configuration and integrated graphics; read beep or POST codes; reseat RAM and test one stick at a time.

*Fix.* Replace the faulty part (known good swap).

*Verify and document.* Run a stress test, confirm the display, and record every test and its result in the log.
