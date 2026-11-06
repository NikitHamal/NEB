---
subject: Computer Science
grade: 8
unit: 13
title: Computer Virus
hours: 0
area: Web, Communication and Society
---

A computer virus is not a germ. It is a **program** — a set of instructions written by a person — that hides inside other files, copies itself to more files and more computers, and does things the owner never asked for: it slows the machine, deletes or locks files, shows unwanted adverts or steals passwords. This lesson explains what viruses and other harmful programs are, where they came from and how they travel, how to tell that a computer is infected, how antivirus software finds them, and the everyday habits that keep a computer safe.

::: key What the examination asks from this lesson
Expect **definitions** (computer virus, malware, worm, Trojan horse, spyware, adware, ransomware, antivirus), **two-point differences** (virus and worm, spyware and adware, antivirus and firewall), **lists** (ways a virus spreads, symptoms of infection, examples of antivirus programs, ways of protection) and a **long question** on the types of malware or on how to protect a computer. Scenario questions describe a computer's symptoms and ask you to name the malware and say what to do.
:::

## 13.1 Computer virus: meaning, history and how it spreads

::: definition Computer virus
A **computer virus** is a harmful program that **attaches itself to another file or program**, **copies itself** into other files and disks when the infected file is run, and damages data or disturbs the working of the computer **without the user's knowledge**. Any program made to harm a computer or its user is called **malware** (from *malicious software*); a virus is one kind of malware.
:::

The name comes from biology. Like a living virus, a computer virus needs a **host** (a file to live in), **multiplies** inside it, **spreads** from one computer to another, and **harms** its host. In 1983 Fred Cohen, a student in the United States, showed a program that could infect other programs; his teacher Leonard Adleman suggested the name **"computer virus"**, which Cohen used in his 1984 paper.

People write malware to show off, to steal passwords and money, to spy, to damage a rival, or to demand a ransom. Making and spreading a virus that destroys or damages data is a crime in Nepal under section 46 of the Electronic Transactions Act, 2063 (Lesson 12).

### A short history

| Year | Event |
|---|---|
| 1971 | **Creeper**, written by Bob Thomas at BBN in the USA, moved from computer to computer on ARPANET showing "I'M THE CREEPER : CATCH ME IF YOU CAN". It did no harm. Ray Tomlinson then wrote **Reaper** to find and delete it — the first antivirus-like program. |
| 1982 | **Elk Cloner**, written by Rich Skrenta, a 15-year-old school student, spread on Apple II floppy disks and showed a short poem every fiftieth time the computer was started. |
| 1983–84 | Fred Cohen demonstrated a self-copying program and named it a **computer virus**. |
| 1986 | **Brain**, made by the brothers Basit and Amjad Farooq Alvi in Lahore, Pakistan, infected the boot sector of floppy disks. It was the first virus for IBM PC computers. |
| 1988 | The **Morris worm**, released on 2 November 1988, copied itself across the young Internet and slowed thousands of computers. |
| 2000 | **ILOVEYOU** arrived in May 2000 as an e-mail with the attachment LOVE-LETTER-FOR-YOU.TXT.vbs; opening it overwrote picture and music files and mailed itself to everyone in the address book. |
| 2017 | **WannaCry** ransomware struck on 12 May 2017. It locked the files of more than 200,000 computers in over 150 countries and demanded 300 US dollars in Bitcoin from each victim. |

```figure caption="Fifty years of malware, in order (the spacing is not to scale). Early programs were experiments and jokes; today's malware is made mostly to steal or to demand money."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 2.9))
ev = [("1971", "Creeper moves\non ARPANET"), ("1982", "Elk Cloner\n(Apple II)"), ("1984", "the name\n'computer virus'"),
      ("1986", "Brain: first\nPC virus"), ("1988", "Morris worm\nslows the Internet"), ("2000", "ILOVEYOU\ne-mail worm"), ("2017", "WannaCry\nransomware")]
n = len(ev)
xs = np.arange(n) + 0.5
ax.plot([0, n], [0, 0], color=MUTED, lw=2, zorder=1)
for i, (x, (yr, txt)) in enumerate(zip(xs, ev)):
    up = i % 2 == 0
    c = SERIES[(i + 1) % 6]
    s = 1 if up else -1
    ax.plot([x, x], [0, 0.5 * s], color=c, lw=1.2, zorder=1)
    ax.plot(x, 0, "o", color=c, ms=7, zorder=3)
    ax.text(x, 0.58 * s, yr, ha="center", va="bottom" if up else "top", fontsize=9, fontweight="bold", color=c)
    ax.text(x, 1.05 * s, txt, ha="center", va="bottom" if up else "top", fontsize=7.4, color=INK, linespacing=1.15)
ax.set_xlim(-0.15, n + 0.15); ax.set_ylim(-2.0, 2.0); ax.axis("off")
```

```photo id="cs8/vir-brain-bootsector" caption="The Brain virus (1986) seen in the boot sector of an infected floppy disk. The left part shows the bytes as hexadecimal numbers; the right column shows the same bytes as text: the authors' names, the name of their shop in Lahore, its address and phone numbers." width="88"
box 0.775 0.04 0.215 0.80
```

### How a virus spreads

A virus cannot do anything until its host file is **opened or run**. It then copies itself into other files, into the boot sector of disks, or onto any pen drive plugged into the computer, and each copy waits for the next person to run it. The common routes into a computer are:

- **infected pen drives** and external disks passed from computer to computer, a very common route in school labs and print shops;
- **pirated software, cracked games and "free" copies of paid programs** from untrusted websites;
- **e-mail attachments** from strangers, or from friends whose computers are infected;
- **links in SMS, chat and social media** that lead to infected downloads;
- **fake apps** installed from outside the official app stores, and **fake pop-ups** saying "Your PC is infected — download this cleaner";
- **networks**: worms travel by themselves to computers that are missing security updates, and viruses spread through shared folders.

```figure caption="The usual ways malware reaches a computer. In every case except the worm, a person helps it in by opening, running or installing something."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.set_aspect("equal"); ax.axis("off")
cx, cy = 5.0, 3.1
src = [("infected\npen drive", 1.75, 5.1), ("pirated software,\ncracked games", 1.75, 3.1), ("e-mail\nattachment", 1.75, 1.1),
       ("fake links in\nSMS and chats", 8.25, 5.1), ("fake apps and\npop-up 'cleaners'", 8.25, 3.1), ("network worm\n(no update)", 8.25, 1.1)]
w, h = 3.1, 1.35
for i, (t, x, y) in enumerate(src):
    c = SERIES[i % 6]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.18", fc=c, ec="none", alpha=0.95, zorder=2))
    ax.text(x, y, t, ha="center", va="center", color="white", fontsize=7.8, fontweight="bold", linespacing=1.2, zorder=3)
    ex = x + (w / 2 if x < cx else -w / 2)
    tx = cx + (-0.95 if x < cx else 0.95)
    ty = cy + (y - cy) * 0.28
    ax.annotate("", xy=(tx, ty), xytext=(ex, y), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, mutation_scale=10), zorder=1)
ax.add_patch(Rectangle((cx - 0.9, cy - 0.45), 1.8, 1.25, fc="white", ec=INK, lw=1.5, zorder=3))
ax.add_patch(Rectangle((cx - 0.72, cy - 0.28), 1.44, 0.92, fc="#eaf2fb", ec="none", zorder=4))
ax.add_patch(Rectangle((cx - 0.15, cy - 0.85), 0.3, 0.4, fc=INK, ec="none", zorder=3))
ax.add_patch(Rectangle((cx - 0.6, cy - 0.95), 1.2, 0.12, fc=INK, ec="none", zorder=3))
ax.text(cx, cy + 0.18, "your\ncomputer", ha="center", va="center", fontsize=7.6, color=INK, fontweight="bold", zorder=5, linespacing=1.1)
```

::: caution "Virus" is not the name of every harmful program
Students often call every harmful program a virus. **Malware** is the general name. A virus is the kind that hides inside other files; a worm, a Trojan horse, spyware, adware and ransomware are different kinds, as the next section shows. Write "malware" when you mean all of them.
:::

```photogrid label="13.H" cols="3" ratio="1.3" caption="Malware, from the first PC virus to today. (a) The boot sector of a floppy disk, the place where the Brain virus of 1986 hid. (b) The map of countries hit by the WannaCry ransomware in May 2017. (c) ClamTk, a free antivirus program for Linux that scans files for known threats. A virus enters through a disk, a network or a download; the antivirus is the guard that scans for it."
@ photo id="cs8/vir-brain-bootsector" cap="(a) Brain virus, 1986"
@ photo id="cs8/vir-wannacry-map" cap="(b) WannaCry spread, 2017"
@ photo id="cs8/vir-clamtk" cap="(c) An antivirus scanner"
```

## 13.2 Types of malware: virus, worm, Trojan horse, spyware, adware and ransomware

```figure caption="The malware family. Each kind is named by what it does: how it spreads (virus, worm), how it gets in (Trojan horse) or what harm it does (spyware, adware, ransomware)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.5))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.add_patch(FancyBboxPatch((0.01, 0.42), 0.17, 0.16, boxstyle="round,pad=0.005,rounding_size=0.02", fc=INK, ec="none"))
ax.text(0.095, 0.5, "Malware", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
kids = [("Virus", "attaches to a file; spreads when the infected\nfile is run (boot sector, file, macro)"),
        ("Worm", "a separate program that copies itself\nover a network all by itself"),
        ("Trojan horse", "looks like a useful program but does\nharm once it is installed"),
        ("Spyware", "secretly records what you do and sends it\nto someone else (e.g. a keylogger)"),
        ("Adware", "fills the screen with unwanted adverts\nand may track your browsing"),
        ("Ransomware", "locks the computer or its files and\ndemands money to unlock them")]
ys = np.linspace(0.92, 0.08, 6)
for i, ((t, d), y) in enumerate(zip(kids, ys)):
    c = SERIES[i % 6]
    ax.plot([0.18, 0.22, 0.22, 0.25], [0.5, 0.5, y, y], color=MUTED, lw=1.0)
    ax.add_patch(FancyBboxPatch((0.25, y - 0.055), 0.2, 0.11, boxstyle="round,pad=0.004,rounding_size=0.02", fc=c, ec="none"))
    ax.text(0.35, y, t, ha="center", va="center", color="white", fontsize=8.2, fontweight="bold")
    ax.text(0.47, y, d, ha="left", va="center", color=INK, fontsize=7.4, linespacing=1.15)
```

### Virus

A virus attaches itself to a host — a program, a document or the boot sector of a disk — and runs whenever the host is used. It spreads only when a person runs or opens the infected host, and it may delete or corrupt files, fill the disk, or slow the computer. Viruses are grouped by where they hide:

| Kind of virus | Where it hides | What happens |
|---|---|---|
| Boot sector virus | the boot sector, the part of a disk the computer reads first when it starts | it loads into memory before the operating system and infects every disk used; e.g. Brain |
| File (program) virus | program files such as those ending in `.exe` | it runs each time the program is opened and infects other programs |
| Macro virus | the macros (small programs) inside Word or Excel documents | it spreads when the document is opened and shared; e.g. Melissa (1999) |
| Multipartite virus | both the boot sector and program files | it is hard to remove because it hides in two places |

### Worm

A **worm** is a separate program that **copies itself from computer to computer over a network without needing a host file and without anyone running it**. It uses weaknesses in software that has not been updated. Even when it does nothing else, a worm uses up network bandwidth and slows everything down. The Morris worm (1988) was one; WannaCry spread as a worm.

| Virus | Worm |
|---|---|
| needs a host file or program | is a complete program by itself |
| spreads when a person runs the infected file | spreads by itself over networks |
| spreads mainly through files and disks | spreads mainly through networks and e-mail |
| damages files on the computer it infects | mainly uses up network speed and computer resources (and may carry other harm) |
| example: Brain | example: Morris worm |

### Trojan horse

A **Trojan horse** is a harmful program **disguised as something useful or attractive**: a free game, a "crack" for paid software, a "phone speed booster". It does not copy itself; it waits for the user to install it. Once inside, it may steal passwords, open a hidden **backdoor** that lets a criminal control the computer, or download other malware. The name comes from the old Greek story in which soldiers hid inside a wooden horse that was given to the city of Troy as a gift, and opened the gates at night.

### Spyware

**Spyware** secretly **watches what you do** and sends the information to someone else: the websites you visit, your messages, your location, or even your camera. A **keylogger** is spyware that records every key you press, so it captures passwords and PINs as you type them.

### Adware

**Adware** fills the screen with **unwanted advertisements** — pop-ups, new tabs, banners — changes the browser's home page or search engine, and often tracks your browsing to choose the adverts. It usually comes bundled with "free" programs downloaded from untrusted sites.

| Spyware | Adware |
|---|---|
| hides and works secretly | makes itself very visible with adverts |
| steals information: passwords, messages, browsing | earns money by showing adverts |
| the user often notices nothing | the user notices pop-ups and a changed home page |
| example: a keylogger | example: a toolbar that keeps opening shopping sites |

### Ransomware

**Ransomware** **locks the computer or encrypts the files** so that they cannot be opened, then shows a message demanding a **ransom**, usually in a cryptocurrency such as Bitcoin, to unlock them. Paying does not guarantee that the files come back, and it encourages the criminals. The real defence is a **backup** kept away from the computer and up-to-date software: WannaCry attacked Windows computers that had not installed a security update released in March 2017, two months earlier.

```photo id="cs8/vir-wannacry-map" caption="Countries (in red) where WannaCry ransomware infected computers in the first hours of the attack on 12 May 2017. It spread as a worm through Windows computers that were missing a security update." width="86"
```

| Type | Needs a host? | Copies itself? | How it gets in | Main harm | Example |
|---|---|---|---|---|---|
| Virus | yes | yes | running an infected file or disk | damages or deletes files | Brain |
| Worm | no | yes | networks, by itself | slows networks; carries other harm | Morris worm |
| Trojan horse | no | no | the user installs a fake "useful" program | backdoor, theft of data | fake game cracks |
| Spyware | no | no | bundled downloads, Trojans | steals private information | keyloggers |
| Adware | no | no | bundled free software | unwanted adverts, tracking | pop-up toolbars |
| Ransomware | no | some do | attachments, worms, Trojans | locks files for money | WannaCry |

::: example Worked example 13.1 — name the malware
**Problem.** Which type of malware is described? (a) A "free version" of a paid video editor works, but it secretly sends the user's saved passwords to a stranger. (b) A program spreads to every unprotected computer on a college network overnight, although nobody opened anything. (c) After a free download, a browser keeps opening betting and shopping adverts. (d) A screen says "Your files are encrypted. Pay to get them back." (e) A program hidden inside an Excel file infects other spreadsheets when it is opened.

**Solution.** (a) A **Trojan horse** carrying **spyware**: it was disguised as a useful program. (b) A **worm**: it spread by itself through the network. (c) **Adware**. (d) **Ransomware**. (e) A **macro virus**.
:::

## 13.3 Symptoms of an infected computer

A computer that is infected usually shows one or more of these signs.

| Area | Symptoms |
|---|---|
| Speed | the computer becomes very slow; programs take long to open; it freezes or restarts by itself |
| Files | files are missing, renamed, damaged or locked; file sizes change; strange new files and icons appear |
| Pen drives | folders on a pen drive turn into **shortcuts** and the real files seem to disappear |
| Screen | pop-up adverts, strange messages or a ransom note; the browser's home page or search engine changes by itself |
| Security | the antivirus is switched off and cannot be turned on; Task Manager or Settings will not open |
| Network | the Internet is slow, data packs finish quickly, or the disk and network lights flash when you are doing nothing |
| Accounts | friends receive messages, e-mails or links that you never sent |
| Phones | the battery drains fast, the phone gets hot, and unknown apps appear |

::: caution A slow computer does not always have a virus
A computer can also be slow because its disk is nearly full, too many programs start with it, it is old, or it is overheating. Do not "format the computer" or blame a virus at the first sign. Run a full antivirus scan first; if it finds nothing, look at the disk space and the list of programs that start with Windows.
:::

::: example Worked example 13.2 — reading the symptoms
**Problem.** What is the likely cause of each problem, and what should be done? (a) In the school lab, the folders on Dipa's pen drive have become shortcuts. (b) Every file on the office computer has a new extension and will not open, and a note on the desktop asks for money. (c) Since Sagar installed a free "video downloader", his browser shows adverts on every page. (d) Classmates get "Look at this video of you!" links from Anjali's account.

**Solution.** (a) A **virus or worm on the pen drive** that hides the real folders and creates shortcuts that run it. Do not click the shortcuts; scan the pen drive with an updated antivirus on a protected computer, then show hidden files and copy them to safety. (b) **Ransomware**. Disconnect the computer from the network at once so that it cannot spread, do not pay, report it, and restore the files from a backup after the computer has been cleaned. (c) **Adware** that came with the free program. Uninstall the program, remove unknown browser extensions, reset the browser and scan. (d) Her **account has been hacked** (or her device infected). She should change the password from a safe device, switch on two-step verification, log out of all other devices, and warn friends not to open the link.
:::

## 13.4 Antivirus software: how it works and examples

::: definition Antivirus software
**Antivirus software** is a utility program that **detects, blocks and removes** viruses and other malware from a computer, a phone or a storage device.
:::

### How antivirus software works

1. **Signature checking.** Every known virus contains a recognisable pattern of code, its **signature**. The antivirus keeps a **database of signatures** (also called virus definitions) and compares files with it. New malware appears every day, so the database must be **updated** regularly, usually automatically over the Internet.
2. **Heuristic (behaviour) checking.** To catch new malware that is not yet in the database, the antivirus also watches for suspicious **behaviour**, such as a program trying to change hundreds of files, to hide itself or to switch off the antivirus.
3. **Real-time protection.** The antivirus runs all the time in the background and checks each file the moment it is opened, downloaded, copied or arrives on a pen drive.
4. **Scanning.** The user can also run a **quick scan** (the places malware usually hides), a **full scan** (every file on every disk) or a **custom scan** (one folder or pen drive), and schedule scans automatically.
5. **Action.** When it finds malware, the antivirus can **clean** (repair) the file, **quarantine** it — move it into a locked area where it cannot run or spread, so that it can be checked or restored later — or **delete** it.

```figure caption="How an antivirus program checks a file in real time. The signature check catches known malware; the behaviour check is there for new malware that is not yet in the database."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Ellipse
fig, ax = plt.subplots(figsize=(4.8, 3.9))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
def rbox(x, y, w, h, t, c, tc="white"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.005,rounding_size=0.04", fc=c, ec="none", zorder=2))
    ax.text(x, y, t, ha="center", va="center", fontsize=7.6, color=tc, zorder=3, linespacing=1.15)
def diamond(x, y, w, h, t):
    ax.add_patch(Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]], closed=True, fc="#fdf1dc", ec=SERIES[3], lw=1.3, zorder=2))
    ax.text(x, y, t, ha="center", va="center", fontsize=7.4, color=INK, zorder=3, linespacing=1.1)
def arrow(p, q, lab="", lx=0.0, ly=0.0):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, mutation_scale=10), zorder=1)
    if lab:
        ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, lab, ha="center", va="center", fontsize=7.4, color=INK, fontweight="bold")
rbox(0.5, 0.93, 0.44, 0.1, "a file is opened,\ndownloaded or copied", ACCENT)
diamond(0.5, 0.66, 0.38, 0.2, "matches a known\nsignature?")
rbox(0.865, 0.66, 0.25, 0.12, "clean, quarantine\nor delete it", SERIES[1])
diamond(0.5, 0.35, 0.38, 0.2, "behaves like\nmalware?")
rbox(0.865, 0.35, 0.25, 0.12, "block it and\nwarn the user", SERIES[1])
rbox(0.5, 0.07, 0.34, 0.1, "allow the file to run", SERIES[2])
arrow((0.5, 0.88), (0.5, 0.765))
arrow((0.69, 0.66), (0.738, 0.66), "Yes", -0.014, 0.05)
arrow((0.5, 0.56), (0.5, 0.455), "No", 0.045, 0.0)
arrow((0.69, 0.35), (0.738, 0.35), "Yes", -0.014, 0.05)
arrow((0.5, 0.25), (0.5, 0.125), "No", 0.045, 0.0)
ax.add_patch(Rectangle((0.06, 0.60), 0.13, 0.1, fc="#eaf2fb", ec=ACCENT, lw=1.1, zorder=2))
ax.add_patch(Ellipse((0.125, 0.70), 0.13, 0.04, fc="#eaf2fb", ec=ACCENT, lw=1.1, zorder=3))
ax.add_patch(Ellipse((0.125, 0.60), 0.13, 0.04, fc="#eaf2fb", ec=ACCENT, lw=1.1, zorder=1))
ax.text(0.125, 0.52, "signature\ndatabase,\nupdated daily", ha="center", va="top", fontsize=7.2, color=INK, linespacing=1.1)
arrow((0.195, 0.66), (0.305, 0.66))
```

### Examples of antivirus software

**Microsoft Defender** comes built into Windows 10 and 11 (in the Windows Security app). Other well-known programs are **Avast**, **AVG**, **Avira**, **Kaspersky**, **Norton 360**, **McAfee**, **Bitdefender**, **ESET NOD32** and **Quick Heal**; **ClamAV** is free and open-source, and **ClamTk** is a simple window for it on Linux. Phones have antivirus apps too, but on a phone the most important protection is to install apps only from the official store.

```photo id="cs8/vir-clamtk" caption="ClamTk, a free antivirus program for Linux. The Status panel shows that its virus definitions are current and when the last scan ran; the Quarantine menu holds files it has locked away." width="58"
```

::: caution Two antivirus programs are not better than one
Running two real-time antivirus programs together makes them fight over every file, which slows the computer and can make it crash. Use **one** good antivirus, keep it updated, and use a second program only for an occasional manual scan.
:::

An antivirus is not the same as a **firewall**, which you will study again in Grade 9. A firewall is a guard on the **network connection**; an antivirus is a guard on the **files**.

| Antivirus | Firewall |
|---|---|
| checks files and programs for malware | checks the data coming in and going out through the network |
| detects, quarantines and removes malware already on the computer | blocks unauthorised connections before they reach the computer |
| works with a database of virus signatures | works with rules about which programs and addresses may connect |
| example: Microsoft Defender Antivirus, Kaspersky | example: Windows Defender Firewall, the firewall in a router |

::: example Worked example 13.3 — why did one antivirus miss it?
**Problem.** Bina and Hari both copy the same game from a friend's pen drive. Hari's antivirus, updated this morning, quarantines it as a virus. Bina's antivirus has not been updated for four months and lets it run. Explain why, and say what Bina should do now.

**Solution.** Antivirus software finds known malware by comparing files with its **signature database**. The virus is new, so its signature was added to the database only recently: Hari's updated copy has it and Bina's old copy does not, and the behaviour check did not catch it either. Bina should **update** her antivirus at once, run a **full scan**, quarantine or delete what it finds, change her passwords from a safe device, and switch on automatic updates.
:::

## 13.5 Protecting a computer: safe browsing, updates, backups and strong passwords

No single tool gives complete protection; safety comes from good habits used together.

**Install antivirus and keep the firewall on.** Use one trusted antivirus with real-time protection and automatic updates, and keep the firewall of the operating system switched on.

**Update the operating system and apps.** Updates (patches) close the security holes that worms and hackers use. Switch on automatic updates for Windows, Android, the browser and every app. Old systems that no longer receive updates, such as Windows 7, should be replaced or upgraded.

**Browse and download safely.** Download software only from the official website or app store; never use cracked software. Do not click pop-ups that say your computer is infected. Check that a site's address is spelt correctly and starts with `https` before typing a password. Do not open e-mail attachments or links you were not expecting, even from friends, until you have checked with them.

**Scan pen drives.** Scan every pen drive before opening it, do not open unknown pen drives, and switch off **AutoPlay** so that nothing runs automatically when a drive is plugged in.

**Keep backups.** A **backup** is an extra copy of your files kept somewhere else, so that you can get them back after a virus, ransomware, theft or a disk failure. Follow the **3-2-1 rule**:

| 3 | 2 | 1 |
|---|---|---|
| keep **three** copies of important files | on **two** different kinds of storage, e.g. the computer and an external disk | with **one** copy away from the computer, e.g. in cloud storage or at another place |

Unplug the backup disk after copying: ransomware can lock files on any disk that is connected.

**Use strong passwords and MFA.** A strong password is **long** (at least 12 characters), mixes capital and small letters, numbers and symbols, contains no name or birthday, and is **different for every account**. A passphrase of unrelated words such as `Cloud-Tiger-Rice-73!` is easy to remember and hard to guess. Switch on **multi-factor authentication**, so that a stolen password alone is not enough to log in. Never share passwords, and lock the screen when you leave the computer.

**Use a standard account.** Do everyday work in a standard (non-administrator) user account, so that malware cannot easily install itself or change system settings.

::: example Worked example 13.4 — a safety plan for the school lab
**Problem.** The 20 computers in a school lab often catch viruses from students' pen drives, and last year the teacher lost the year's marks when a disk failed. Write a five-point plan for the lab.

**Solution.** (1) Install one antivirus on every computer, with **automatic updates** and **real-time scanning** of pen drives; switch off AutoPlay. (2) Turn on **automatic Windows updates** and keep the **firewall** on. (3) Give students **standard accounts** so that they cannot install programs; only the teacher's account is an administrator. (4) Keep the marks under the **3-2-1 rule**: on the office computer, on an external disk kept unplugged in a cupboard, and in the school's cloud storage. (5) Teach the rules: no pirated software, no unknown pen drives, no clicking on pop-ups, and strong, separate passwords for every account.
:::

::: tip How to answer the protection question
Name the habit **and** say what it protects against: "Install updates — they close the security holes that worms such as WannaCry use." A list of habits without reasons earns only half the marks.
:::

::: note Activity 13.1 — a lab health check
With your teacher: (1) Open the antivirus on a lab computer and note the date of its last update and last scan; run a quick scan of a pen drive. (2) Open the Quarantine list and see whether any files have been locked away. (3) Check whether Windows updates and the firewall are switched on. (4) Make a poster of the 3-2-1 backup rule for the lab wall, and find out where your school keeps its backups. (5) Write three warning signs of an infected pen drive on the board for the next class.
:::

## Chapter summary

- A **computer virus** is a harmful program that attaches itself to files, copies itself when the file is run, and damages data without the user's knowledge; **malware** is the general name for all harmful programs.
- History: Creeper (1971), Elk Cloner (1982), the name "computer virus" by Fred Cohen (1983–84), Brain from Lahore (1986, first PC virus), Morris worm (1988), ILOVEYOU (2000), WannaCry (2017).
- Viruses spread through pen drives, pirated software, e-mail attachments, fake links and apps, and networks.
- **Types**: virus (needs a host; boot sector, file, macro, multipartite), **worm** (spreads by itself over networks), **Trojan horse** (disguised as useful), **spyware** (secretly watches; keyloggers), **adware** (unwanted adverts), **ransomware** (locks files for money).
- **Symptoms**: slowness, crashes, missing or locked files, shortcut folders on pen drives, pop-ups, a disabled antivirus, messages sent without you.
- **Antivirus** detects, blocks and removes malware by signature checking, behaviour checking and real-time scanning, then cleans, quarantines or deletes; it must be updated. Examples: Microsoft Defender, Avast, Kaspersky, Norton, ClamAV. A firewall guards the network, an antivirus the files.
- **Protection**: antivirus and firewall, automatic updates, safe browsing and downloads, scanning pen drives, the **3-2-1 backup rule**, strong unique passwords with MFA, and standard user accounts.

## Practice questions

**Group A — Objective (1 mark each)**

1. A computer virus is a <span class="marks">[1]</span>
   (a) living germ (b) harmful program (c) hardware fault (d) kind of cable
2. The name "computer virus" was first used by <span class="marks">[1]</span>
   (a) Fred Cohen (b) Charles Babbage (c) Bill Gates (d) Tim Berners-Lee
3. Brain, the first virus for IBM PCs, appeared in <span class="marks">[1]</span>
   (a) 1971 (b) 1986 (c) 2000 (d) 2017
4. Malware that copies itself over a network without a host file is a <span class="marks">[1]</span>
   (a) Trojan horse (b) worm (c) macro virus (d) adware
5. A harmful program disguised as a useful game or tool is a <span class="marks">[1]</span>
   (a) worm (b) Trojan horse (c) firewall (d) cookie
6. Malware that locks your files and demands money is <span class="marks">[1]</span>
   (a) spyware (b) adware (c) ransomware (d) freeware
7. A program that secretly records every key you press is a kind of <span class="marks">[1]</span>
   (a) adware (b) spyware (c) antivirus (d) compiler
8. Which of these is NOT antivirus software? <span class="marks">[1]</span>
   (a) Kaspersky (b) Avast (c) Microsoft Defender (d) Microsoft Excel
9. Moving an infected file into a locked area where it cannot run is called <span class="marks">[1]</span>
   (a) formatting (b) quarantine (c) compressing (d) uploading
10. A boot sector virus infects <span class="marks">[1]</span>
    (a) the monitor (b) the part of a disk read first when the computer starts (c) only e-mails (d) the printer
11. Pop-up adverts and a browser home page that changes by itself are signs of <span class="marks">[1]</span>
    (a) adware (b) a full disk (c) a loose cable (d) a firewall
12. The 3-2-1 backup rule means keeping <span class="marks">[1]</span>
    (a) 3 copies on 2 kinds of storage with 1 copy elsewhere (b) 3 passwords for 2 accounts (c) 3 antivirus programs (d) only 1 copy
13. WannaCry spread mainly to Windows computers that <span class="marks">[1]</span>
    (a) had no keyboard (b) had not installed a security update (c) were switched off (d) had a strong password

::: note Answers to Group A
**1.** (b) — a virus is a program written by a person.
**2.** (a) — Fred Cohen, on the suggestion of Leonard Adleman, 1983–84.
**3.** (b) — 1986, by the Alvi brothers of Lahore.
**4.** (b) — a worm needs no host and spreads by itself.
**5.** (b) — named after the wooden horse of Troy.
**6.** (c) — ransomware demands a ransom.
**7.** (b) — a keylogger is spyware.
**8.** (d) — Excel is a spreadsheet program.
**9.** (b) — quarantine isolates the file safely.
**10.** (b) — the boot sector is read when the computer starts.
**11.** (a) — adware shows unwanted adverts and changes browser settings.
**12.** (a) — three copies, two media, one copy away from the computer.
**13.** (b) — Microsoft had released the patch two months earlier.
:::

**Group B — Short answer (2 marks each)**

1. What is a computer virus? Write any two ways by which it spreads. <span class="marks">[2]</span>
2. Differentiate between a virus and a worm. <span class="marks">[2]</span>
3. What is a Trojan horse? Why is it given this name? <span class="marks">[2]</span>
4. What is ransomware? Write one way to protect your files from it. <span class="marks">[2]</span>
5. Differentiate between spyware and adware. <span class="marks">[2]</span>
6. Write any four symptoms of a computer infected by a virus. <span class="marks">[2]</span>
7. What is antivirus software? Name any two antivirus programs. <span class="marks">[2]</span>
8. What is a virus signature? Why must antivirus software be updated regularly? <span class="marks">[2]</span>
9. Differentiate between antivirus software and a firewall. <span class="marks">[2]</span>
10. What is a backup? Explain the 3-2-1 backup rule. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A computer virus is a harmful program that attaches itself to other files, copies itself when the infected file is run, and damages data without the user's knowledge. It spreads (any two) through infected pen drives, pirated software, e-mail attachments, fake links and downloads, and shared network folders.

**2.** A virus needs a host file and spreads only when a person runs the infected file; a worm is a complete program that copies itself over a network by itself. A virus mainly damages files; a worm mainly uses up network speed and computer resources.

**3.** A Trojan horse is a harmful program disguised as a useful or attractive one, such as a free game or a software crack; it does harm (steals data, opens a backdoor) once installed and does not copy itself. It is named after the Greek story of soldiers hidden in a wooden horse given to Troy as a gift.

**4.** Ransomware is malware that locks a computer or encrypts its files and demands money to unlock them. Protection (any one): keep a backup on a disk that is unplugged after use or in cloud storage; install security updates; do not open unknown attachments.

**5.** Spyware hides and secretly collects information such as passwords and browsing and sends it to someone; adware shows unwanted adverts and is very visible. Example: a keylogger is spyware; a toolbar that keeps opening shopping sites is adware.

**6.** Any four: the computer becomes slow or freezes; files go missing, change or will not open; folders on pen drives turn into shortcuts; pop-ups or strange messages appear; the antivirus is switched off by itself; friends receive messages you did not send; the Internet or data use is unusually high.

**7.** Antivirus software is a utility program that detects, blocks and removes viruses and other malware. Examples (any two): Microsoft Defender, Avast, AVG, Avira, Kaspersky, Norton 360, McAfee, Bitdefender, ESET NOD32, Quick Heal, ClamAV.

**8.** A virus signature is the recognisable pattern of code that identifies a known virus; antivirus programs keep a database of them. It must be updated because new malware appears every day, and an antivirus can recognise by signature only the malware whose signature is already in its database.

**9.** Antivirus software checks files and programs for malware and removes or quarantines it; a firewall checks the data entering and leaving through the network and blocks unauthorised connections. Antivirus uses a signature database; a firewall uses rules about which programs and addresses may connect.

**10.** A backup is an extra copy of files kept somewhere else so that they can be recovered after loss or damage. The 3-2-1 rule: keep **3** copies of important files, on **2** different kinds of storage, with **1** copy away from the computer (for example in cloud storage).
:::

**Group C — Long answer (4 marks each)**

1. What is malware? Explain any four types of malware with an example of each. <span class="marks">[1+3]</span>
2. Write a short history of computer viruses, describing any four important events. <span class="marks">[4]</span>
3. What is antivirus software? Explain how it detects and deals with malware. <span class="marks">[1+3]</span>
4. Explain any four ways of protecting a computer from viruses and other malware. <span class="marks">[4]</span>
5. A cyber café's computers have become slow, show adverts on every page, and the folders on customers' pen drives turn into shortcuts. Name the likely malware and write a plan to clean the computers and keep them safe. <span class="marks">[1+3]</span>

::: note Answers to Group C
**1.** Malware (malicious software) is any program made to harm a computer or its user (1 mark). Any four (3 marks): *Virus* — attaches itself to a file and spreads when the file is run; e.g. Brain (boot sector virus). *Worm* — a separate program that copies itself over networks by itself; e.g. the Morris worm. *Trojan horse* — disguised as a useful program, it does harm once installed; e.g. a fake game crack that steals passwords. *Spyware* — secretly records what the user does and sends it to someone; e.g. a keylogger. *Adware* — shows unwanted adverts and tracks browsing; e.g. a pop-up toolbar. *Ransomware* — locks the files and demands money; e.g. WannaCry (2017).

**2.** Any four, 1 mark each: *1971 Creeper* — Bob Thomas's program moved between ARPANET computers showing "I'M THE CREEPER : CATCH ME IF YOU CAN"; Reaper was written to delete it. *1982 Elk Cloner* — a 15-year-old's program spread on Apple II floppy disks and showed a poem. *1983–84* — Fred Cohen demonstrated a self-copying program and gave it the name computer virus. *1986 Brain* — made by the Alvi brothers in Lahore, Pakistan; infected the boot sector of floppy disks; the first PC virus. *1988 Morris worm* — spread over the Internet and slowed thousands of computers. *2000 ILOVEYOU* — an e-mail worm that overwrote picture and music files. *2017 WannaCry* — ransomware that locked over 200,000 computers in more than 150 countries.

**3.** Antivirus software is a utility program that detects, blocks and removes malware (1 mark). How it works (3 marks): *signature checking* — it compares files with a database of known virus signatures, which must be updated regularly; *behaviour (heuristic) checking* — it watches for suspicious actions such as a program changing hundreds of files, to catch new malware; *real-time protection* — it checks every file as it is opened, downloaded or copied, including pen drives, and the user can run quick, full or custom scans; *action* — infected files are cleaned, quarantined (locked away where they cannot run) or deleted.

**4.** Any four, 1 mark each, with the reason: *antivirus and firewall* — real-time scanning removes malware and the firewall blocks unauthorised connections; *updates* — patches close the security holes that worms use, as WannaCry showed; *safe browsing and downloading* — official sites and stores only, no cracked software, no pop-ups or unknown attachments; *scanning pen drives and switching off AutoPlay* — stops the commonest school route; *backups by the 3-2-1 rule* — files can be recovered after ransomware or disk failure; *strong unique passwords with MFA* — a stolen password alone cannot open the account; *standard user accounts* — malware cannot easily install itself.

**5.** The slowness and adverts point to **adware** (and possibly spyware) on the computers, and the shortcut folders to a **pen-drive virus or worm** (1 mark). Plan (3 marks): disconnect each infected computer from the network; update the antivirus and run a full scan, quarantining or deleting what it finds; uninstall unknown programs and browser extensions and reset the browsers; scan customers' pen drives and show hidden files so they can recover the real folders; install all Windows updates and keep the firewall on; switch off AutoPlay and give customers a standard account that cannot install programs; and keep a clean backup of the café's own files under the 3-2-1 rule.
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is a computer virus? Explain the types of malware and the symptoms of an infected computer. <span class="marks">[10]</span>
2. Explain how an antivirus works and eight ways of protecting a computer from malware. <span class="marks">[10]</span>

### Model answer D1: virus, malware and symptoms (10 marks)

**Introduction.** A **computer virus** is a harmful program that copies itself, attaches to other files and spreads from one computer to another, usually without the user's knowledge. It can delete files, slow the computer or steal data. The first PC virus, Brain, appeared in 1986 (Plate 13.H). **Malware** (malicious software) is the general name for all such harmful programs.

**How a virus spreads.** Through pen drives and other removable disks, e-mail attachments, downloads from unsafe websites, pirated software and infected networks.

**Types of malware.**

| Type | What it does | Example |
|---|---|---|
| Virus | Attaches itself to a file or program and needs the user to run it | Brain, Michelangelo |
| Worm | Spreads by itself through networks without a host file | ILOVEYOU, Blaster |
| Trojan horse | Looks like a useful program but hides a harmful one | Fake game or crack |
| Spyware | Secretly watches the user and steals passwords and habits | Keylogger |
| Adware | Shows unwanted advertisements, often slowing the system | Pop-up ads |
| Ransomware | Locks files and asks for money to open them | WannaCry (2017) |

**Symptoms of an infected computer.**

1. The computer becomes slow or hangs often.
2. Strange pop-ups, messages or advertisements appear.
3. Files or folders disappear, change size or cannot be opened.
4. Programs open or close by themselves.
5. The pen drive shows shortcut files instead of the real folders.
6. The antivirus or Task Manager is turned off by itself.
7. The browser's home page changes, or e-mails are sent without the user knowing.

**Conclusion.** Viruses and other malware can cause loss of data, money and privacy, so we must know their kinds and signs and act at once when we see them.

### Model answer D2: antivirus and protection (10 marks)

**Introduction.** An **antivirus program** is a utility that finds, blocks and removes malware. Examples are Windows Defender, Kaspersky, Avast, Quick Heal and ClamAV.

**How an antivirus works.**

1. **Signature scanning:** it compares files with a database of the known patterns (signatures) of viruses.
2. **Heuristic scanning:** it watches for suspicious behaviour, such as a program changing many files, to catch new viruses.
3. **Real-time protection:** it checks every file being opened, downloaded or copied, in the background.
4. **Action:** it **cleans** the file, puts it in **quarantine** or **deletes** it.
5. **Updates:** the signature database must be updated often, because new viruses appear every day.

**Eight ways to protect the computer.**

1. **Install an antivirus** and keep it turned on and updated, so that new threats can be caught.
2. **Update the operating system** and programs, because updates close the gaps that malware uses. WannaCry spread to computers that were not updated.
3. **Scan pen drives** before opening them; a shared pen drive is a common carrier in schools.
4. **Do not open unknown attachments or links**; phishing e-mails carry most ransomware.
5. **Download only from official sites** and avoid pirated or cracked software, which often hides a Trojan.
6. **Use strong passwords** of letters, numbers and symbols, different for every account, with two-step verification where possible.
7. **Take regular backups** on an external disk or in the cloud, so that nothing is lost even if ransomware locks the files.
8. **Use a firewall and safe browsing**: look for the HTTPS padlock and avoid doubtful sites.

**Conclusion.** No antivirus can stop everything, so protection needs both good software and good habits.
