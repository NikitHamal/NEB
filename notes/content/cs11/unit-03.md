---
subject: Computer Science
grade: 11
unit: 3
title: Computer Software and Operating System
hours: 12
---

Hardware is the part of a computer you can hit with a hammer; software is the
part you can only swear at. Strip the software out of a laptop and you are left
with an expensive brick — silicon that can switch voltages but has no idea what
to switch them to. This unit looks at the instructions that bring the machine to
life: how software is classified, what an operating system does, how to work
confidently inside Windows, and why Linux and Android now run most of the
world's computers.

::: key What the examiner wants from this unit
This is a **description** unit, so marks come from complete, well-organised
lists. Know the five software categories with two examples each, the six or
seven functions of an operating system, and the precise difference between
multiprogramming, multitasking, multiprocessing and distributed processing.
The Windows sections are examined as practical steps — "write the steps to…" —
so learn them as numbered procedures.
:::

## 3.1 Definition of software and its categories

::: definition Software
**Software** is a set of programs, procedures and associated documentation that
tells a computer's hardware what to do and how to do it. A **program** is a
finite sequence of instructions written to solve a particular problem.
:::

Software is intangible: it has no weight and no moving parts, it does not wear
out, and it is copied for almost nothing. It does, however, "rot" in the sense
that it must be updated as hardware, standards and security threats change.

```figure caption="Classification of software. System software runs the machine; application software does the user's work. Web-based and mobile applications are simply application software delivered in a different way."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
GRN='#2e8b57'
def box(cx,cy,w,h,t,c,fs=8.0,bold=False):
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=c,lw=1.1,alpha=0.15,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc='none',ec=c,lw=1.1,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=fs,color=INK,zorder=4,
            fontweight='bold' if bold else 'normal')
def link(p,q,c):
    ax.plot([p[0],p[0],q[0]],[p[1],q[1],q[1]],color=c,lw=1.1,zorder=1)
box(5.35,5.60,2.60,0.62,'SOFTWARE',INK,9.6,True)
box(2.15,4.20,3.10,0.58,'System software',ACCENT,9.0,True)
box(8.55,4.20,3.10,0.58,'Application software',GRN,9.0,True)
ax.plot([2.15,2.15,8.55],[4.49,4.95,4.95],color=INK,lw=1.1,zorder=1)
ax.plot([8.55,8.55],[4.95,4.49],color=INK,lw=1.1,zorder=1)
ax.plot([5.35,5.35],[5.29,4.95],color=INK,lw=1.1,zorder=1)
left=['Operating system','Utility software','Language translators','Device drivers']
right=['General purpose packages','Tailor-made (custom)','Web-based applications','Mobile applications']
ys=[3.05,2.35,1.65,0.95]
for name,y in zip(left,ys):
    box(2.45,y,3.00,0.52,name,ACCENT,7.4); link((0.80,3.91),(0.95,y),ACCENT)
for name,y in zip(right,ys):
    box(9.05,y,3.40,0.52,name,GRN,7.0); link((7.20,3.91),(7.35,y),GRN)
ax.set_xlim(0.0,10.85); ax.set_ylim(0.30,6.10); ax.set_aspect('equal'); ax.axis('off')
```

**1. System software** controls and coordinates the hardware and provides a
platform on which application software runs. It includes the operating system,
language translators (compiler, interpreter, assembler), device drivers and
system utilities. It is normally supplied by the hardware or OS vendor.

**2. Utility software** (service programs) performs housekeeping tasks that keep
the system healthy: antivirus, disk defragmenter, disk cleanup, backup and
restore, file compression (WinRAR, 7-Zip), and disk partitioning tools. Utility
software is strictly a sub-class of system software, but the NEB syllabus lists
it separately because it is what a user actually notices.

**3. Application software** is written to solve a user's problem rather than to
run the machine. It splits into:

- **General purpose (packaged) software** — sold ready-made to everybody: MS
  Word, MS Excel, Photoshop, VLC, Chrome.
- **Tailor-made (custom or bespoke) software** — written for one organisation:
  the billing system of Nepal Electricity Authority, a school's own result
  processing program.

**4. Web-based software** runs on a remote server and is used through a browser,
so nothing is installed on your machine. Examples: Gmail, Google Docs, Google
Sheets, Facebook, Canva, GitHub, and government portals such as the online
passport and PAN registration systems. This model is also called **SaaS**
(Software as a Service).

**5. Mobile applications (apps)** are written for smartphones and tablets, are
touch-first and battery-aware, and are distributed through stores such as Google
Play and the Apple App Store. Examples used daily in Nepal include eSewa, Khalti,
Nagarik App, Pathao, Hamro Patro and IMEPay.

| Category | Purpose | Installed where | Examples |
|---|---|---|---|
| System software | run and manage the hardware | on the machine | Windows 11, Linux, device drivers, compilers |
| Utility software | maintain and protect the system | on the machine | antivirus, disk cleanup, WinRAR, backup |
| Application software | do the user's work | on the machine | MS Word, Excel, Photoshop, VLC |
| Web-based software | do the user's work online | on a remote server | Gmail, Google Docs, Canva, Facebook |
| Mobile apps | do the user's work on a handset | on the phone | eSewa, Khalti, WhatsApp, Nagarik App |

::: example Worked example 3.1 — classify the software
**Problem.** Classify each of the following and give one reason: (a) a printer
driver, (b) 7-Zip, (c) the result-processing program written for your school,
(d) Google Docs, (e) Khalti.

**Solution.**
(a) **System software** (device driver) — it translates the OS's generic print
commands into the signals that one particular printer model understands.
(b) **Utility software** — it does housekeeping (compressing and archiving
files), not the user's primary work.
(c) **Application software, tailor-made** — written to the requirements of a
single organisation and not sold to others.
(d) **Web-based software** — it runs on Google's servers and is reached through
a browser with nothing installed locally.
(e) **Mobile application** — distributed through an app store and designed for a
touch screen handset.
:::

::: caution "Free" is not the same as "open source"
Freeware (Adobe Reader, Skype) costs nothing but its **source code is closed**.
Open-source software (Linux, LibreOffice, Firefox) publishes its source code
under a licence that lets you read, modify and redistribute it. Proprietary
software (Windows, MS Office) is both paid and closed.
:::

## 3.2 Introduction, role and functions of an operating system

::: definition Operating system
An **operating system (OS)** is the system software that acts as an interface
between the user and the hardware. It manages all the resources of the computer
system — processor, memory, files and devices — and provides an environment in
which application programs can run conveniently and efficiently.
:::

Without an OS, every program would have to contain its own code for reading a
keyboard, drawing on a screen and writing to a disk. The OS provides these
services once, for everybody.

```figure caption="The layered view of a computer system. Each layer speaks only to its immediate neighbours, so a word processor never touches the disk controller directly — it asks the operating system."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
bands=[('USER',            INK,      0.55),
       ('Application software\n(Word, Chrome, games)', SERIES[1], 0.85),
       ('Utility and system software\n(antivirus, compilers, drivers)', SERIES[2], 0.85),
       ('OPERATING SYSTEM\n(kernel: process, memory, file, device, security)', ACCENT, 1.00),
       ('HARDWARE\n(CPU, memory, storage, I/O devices)', SERIES[4], 0.85)]
y=0.30
W=7.40
for i,(t,c,h) in enumerate(reversed(bands)):
    ax.add_patch(FancyBboxPatch((0.40,y),W,h,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc=c,ec=c,lw=1.2,alpha=0.16,zorder=2))
    ax.add_patch(FancyBboxPatch((0.40,y),W,h,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc='none',ec=c,lw=1.2,zorder=3))
    ax.text(0.40+W/2,y+h/2,t,ha='center',va='center',fontsize=8.4,color=INK,zorder=4)
    y += h+0.18
top=y-0.18
ax.annotate('',xy=(0.10,top-0.10),xytext=(0.10,0.40),zorder=4,
    arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.2,mutation_scale=11))
ax.text(0.00,(top+0.40)/2,'requests for service travel down',rotation=90,
        ha='right',va='center',fontsize=7.6,color=MUTED)
ax.annotate('',xy=(8.10,0.40),xytext=(8.10,top-0.10),zorder=4,
    arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.2,mutation_scale=11))
ax.text(8.20,(top+0.40)/2,'results travel up',rotation=270,
        ha='left',va='center',fontsize=7.6,color=MUTED)
ax.set_xlim(-0.75,9.25); ax.set_ylim(0.05,top+0.30); ax.set_aspect('equal'); ax.axis('off')
```

### Role of the operating system

- **As a resource manager** it decides which program gets the CPU, how much
  memory each one receives, and in what order printing jobs are served.
- **As an extended (virtual) machine** it hides the ugly detail of the hardware
  behind simple commands such as "open this file".
- **As an interface** it gives the user a command line or a graphical desktop
  through which to give instructions.

### Functions of the operating system

```figure caption="The main functions of an operating system. The kernel is the part of the OS that is always resident in memory and performs these functions."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
fig, ax = plt.subplots(figsize=(4.6,4.0))
ax.add_patch(Circle((0,0),1.25,fc=ACCENT,ec=ACCENT,lw=1.4,alpha=0.16,zorder=2))
ax.add_patch(Circle((0,0),1.25,fc='none',ec=ACCENT,lw=1.4,zorder=3))
ax.text(0,0.16,'OPERATING',ha='center',va='center',fontsize=9.2,color=INK,fontweight='bold')
ax.text(0,-0.20,'SYSTEM',ha='center',va='center',fontsize=9.2,color=INK,fontweight='bold')
items=[(90,'Process\nmanagement'),(150,'Memory\nmanagement'),(210,'File\nmanagement'),
       (270,'Device (I/O)\nmanagement'),(330,'Security and\nprotection'),
       (30,'User interface\nand job control')]
R=3.40; W,H=2.60,0.78
for k,(ang,t) in enumerate(items):
    a=np.radians(ang); cx,cy=R*np.cos(a),R*np.sin(a)
    c=SERIES[k%6]
    ax.add_patch(FancyBboxPatch((cx-W/2,cy-H/2),W,H,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=c,lw=1.1,alpha=0.16,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-W/2,cy-H/2),W,H,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc='none',ec=c,lw=1.1,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=7.8,color=INK,zorder=4)
    ax.plot([1.30*np.cos(a),(R-H*0.75)*np.cos(a)],[1.30*np.sin(a),(R-H*0.75)*np.sin(a)],
            color=c,lw=1.2,zorder=1)
ax.set_xlim(-4.60,4.60); ax.set_ylim(-4.10,4.10); ax.set_aspect('equal'); ax.axis('off')
```

1. **Process management** — creates, schedules, suspends and terminates
   processes; allocates CPU time; handles deadlocks and inter-process
   communication.
2. **Memory management** — keeps track of which parts of main memory are free,
   allocates memory to processes, protects one process from another and
   implements **virtual memory** so that programs larger than RAM can run.
3. **File management** — creates, opens, reads, writes, renames and deletes
   files; organises them into directories; keeps track of free disk space; and
   enforces file permissions.
4. **Device (I/O) management** — communicates with every peripheral through its
   device driver, maintains buffers and queues, and implements **spooling** so
   that a slow printer does not hold up the CPU.
5. **Security and protection** — user accounts, passwords, access rights,
   encryption and a firewall; keeps one user's data away from another's.
6. **User interface and job control** — provides the CLI or GUI and the means to
   start, stop and monitor jobs.
7. **Error detection and system performance monitoring** — reports hardware
   faults and keeps statistics such as CPU and memory usage (Task Manager).

::: memory The six managers
Remember **P-M-F-D-S-U**: **P**rocess, **M**emory, **F**ile, **D**evice,
**S**ecurity, **U**ser interface. Every OS question about "functions" can be
answered from these six.
:::

| OS type | Response required | Typical use | Example |
|---|---|---|---|
| Batch | none (jobs grouped, run later) | payroll, billing runs | early IBM mainframe OS |
| Single-user, single-task | immediate | very old desktops | MS-DOS |
| Multi-user, time-sharing | fast, fair | servers, university systems | UNIX, Linux |
| Real-time | guaranteed deadline | ATMs, robots, medical devices | RTOS, VxWorks |
| Distributed | fast, over a network | cloud, clusters | Linux clusters |
| Embedded / mobile | immediate, low power | phones, TVs, routers | Android, iOS |

## 3.3 OS terminology: multiprogramming, multitasking, multiprocessing and distributed processing

These four words are constantly confused. The distinguishing questions are:
*how many jobs are in memory?*, *how many CPUs are there?*, and *how many
computers are involved?*

```figure caption="The four processing modes. Filled bars mean the job is using a processor; pale bars mean it is waiting. Multiprogramming and multitasking share one CPU, multiprocessing uses several CPUs in one machine, and distributed processing uses several machines on a network."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axs = plt.subplots(2,2, figsize=(5.1,3.3))
def strip(ax,rows,title,sub):
    ax.set_title(title, fontsize=8.6, color=INK, pad=2.0)
    ax.text(0.5,-0.14,sub,transform=ax.transAxes,ha='center',va='top',
            fontsize=6.6,color=MUTED)
    for i,(lab,segs) in enumerate(rows):
        y=len(rows)-1-i
        ax.text(-0.25,y+0.35,lab,ha='right',va='center',fontsize=7.2,color=INK)
        for x0,w,busy in segs:
            ax.add_patch(Rectangle((x0,y+0.10),w,0.50,
                fc=SERIES[i%6],ec=SERIES[i%6],lw=0.8,
                alpha=0.75 if busy else 0.16))
    ax.set_xlim(-1.55,10.2); ax.set_ylim(-0.10,len(rows))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
# multiprogramming: long CPU bursts, switch on I/O wait
strip(axs[0,0],[('Job 1',[(0,3,1),(3,4,0),(7,3,1)]),
                ('Job 2',[(0,3,0),(3,2.5,1),(5.5,4.5,0)]),
                ('Job 3',[(0,5.5,0),(5.5,1.5,1),(7,3,0)])],
      'Multiprogramming','one CPU; switches only\nwhen a job waits for I/O')
# multitasking: short time slices
rows=[]
for i in range(3):
    segs=[]
    for k in range(10):
        segs.append((k,1,1 if k%3==i else 0))
    rows.append(('Task %d'%(i+1),segs))
strip(axs[0,1],rows,'Multitasking','one CPU; fixed time slices,\nfeels simultaneous')
# multiprocessing: two CPUs
strip(axs[1,0],[('CPU 1',[(0,4.5,1),(4.5,5.5,1)]),
                ('CPU 2',[(0,6,1),(6,4,1)])],
      'Multiprocessing','two or more CPUs in ONE\ncomputer, truly at the same time')
ax=axs[1,1]
ax.set_title('Distributed processing', fontsize=8.6, color=INK, pad=2.0)
ax.text(0.5,-0.14,'many computers on a network\nshare one job',
        transform=ax.transAxes,ha='center',va='top',fontsize=6.6,color=MUTED)
ax.plot([0.6,5.4],[1.55,1.55],color=MUTED,lw=1.4,zorder=1)
for k,x in enumerate([1.0,2.2,3.4,4.6]):
    ax.add_patch(Rectangle((x-0.36,0.55),0.72,0.56,fc=SERIES[k%6],ec=SERIES[k%6],
                 lw=1.0,alpha=0.30,zorder=3))
    ax.plot([x,x],[1.11,1.55],color=MUTED,lw=1.1,zorder=2)
    ax.text(x,0.83,'PC%d'%(k+1),ha='center',va='center',fontsize=6.8,color=INK,zorder=4)
ax.text(3.0,1.72,'network',ha='center',va='bottom',fontsize=7.2,color=MUTED)
ax.set_xlim(0.2,5.8); ax.set_ylim(0.35,2.20)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout()
```

**Multiprogramming.** Several programs are loaded in main memory at once, but
there is only **one CPU**. Whenever the running program stops to wait for a slow
input or output operation, the OS gives the CPU to another program. The aim is to
keep the CPU busy and maximise **throughput**. A program keeps the CPU until it
blocks; it is not forcibly interrupted.

**Multitasking (time sharing).** A refinement of multiprogramming in which the OS
also **forcibly** takes the CPU away after a fixed **time slice** (a few
milliseconds) and gives it to the next task in turn. Because the switching is so
fast, the user believes that Word, Chrome and VLC are all running at once. The
aim is fast **response time**. Multitasking may be *co-operative* (the program
yields voluntarily, as in old Windows 3.x) or *pre-emptive* (the OS decides, as
in every modern system).

**Multiprocessing.** A single computer contains **two or more processors** (or
cores) that execute instructions **genuinely simultaneously**. Work really is
done in parallel, so speed and reliability both improve — if one processor
fails the others carry on. Every modern phone and laptop is a multiprocessing
system.

**Distributed processing.** Several **independent computers**, each with its own
CPU and memory, are connected by a network and co-operate on one problem under
the control of a **distributed operating system**. The user sees a single
system. Examples: cloud data centres, computing clusters, and the servers behind
eSewa or a bank's core banking system.

| | Number of CPUs | Number of computers | Switching trigger | Main aim |
|---|---|---|---|---|
| Multiprogramming | one | one | job waits for I/O | CPU utilisation |
| Multitasking | one | one | time slice expires | response time |
| Multiprocessing | two or more | one | no switching — true parallelism | speed, reliability |
| Distributed | many | many | job split over the network | scale, resource sharing |

::: caution Multitasking is not multiprocessing
In multitasking one CPU *appears* to do many things because it switches quickly;
in multiprocessing several CPUs *actually* do many things at the same instant.
Also note **multi-threading**, which is a single program split into several
threads that can be scheduled independently — a property of the program, not of
the machine.
:::

## 3.4 Windows OS: a GUI based OS and its features

A **GUI (Graphical User Interface)** lets the user work with pictures — windows,
icons, menus and a pointer — instead of typed commands. The four elements are
often abbreviated **WIMP**. Microsoft Windows, first released in 1985 and now at
**Windows 11** (mainstream support for Windows 10 ended in **October 2025**), is
the most widely used desktop GUI operating system in the world; as of 2025 it
holds roughly **70 %** of the desktop market, with macOS and Linux (including
ChromeOS) sharing most of the rest.

| CLI (command line) | GUI (graphical) |
|---|---|
| Commands are typed exactly | Objects are clicked or tapped |
| Must memorise the command set | Options are visible on screen |
| Very little memory and CPU needed | Needs much more memory, CPU and a graphics adapter |
| Very fast for an expert; scriptable | Slower for bulk work, but easy for a beginner |
| Examples: MS-DOS, Linux bash, PowerShell | Examples: Windows 11, macOS, GNOME, Android |

### Features of Windows

- **Desktop metaphor** with icons, wallpaper, taskbar and Recycle Bin.
- **Multitasking and multi-user** support with separate accounts and profiles.
- **Plug and Play** — a newly connected device is detected and its driver
  installed automatically.
- **File Explorer** for a hierarchical view of drives, folders and files.
- **Snap layouts, virtual desktops and Task View** for arranging many windows
  (Windows 10 and 11).
- **Built-in security**: Windows Hello sign-in, Microsoft Defender antivirus,
  Windows Firewall, BitLocker drive encryption and User Account Control.
- **Accessibility**: Narrator, Magnifier, high-contrast themes, speech
  recognition.
- **OneDrive cloud integration**, Microsoft Store, and Windows Update.
- **Support for a huge range of hardware and legacy software** — the main reason
  Windows still dominates offices in Nepal.

```figure caption="Anatomy of the Windows desktop. The taskbar carries the Start button, search box, pinned and running applications, and the notification area with the clock."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
fig, ax = plt.subplots(figsize=(5.1,3.2))
SW,SH = 9.40, 5.40
ax.add_patch(FancyBboxPatch((0.0,0.0),SW,SH,
    boxstyle="round,pad=0,rounding_size=0.12",fc=ACCENT,ec=INK,lw=1.4,alpha=0.10,zorder=1))
ax.add_patch(FancyBboxPatch((0.0,0.0),SW,SH,
    boxstyle="round,pad=0,rounding_size=0.12",fc='none',ec=INK,lw=1.4,zorder=4))
# desktop icons
for k,nm in enumerate(['This PC','Recycle Bin','Class 11']):
    y = SH-0.90-k*1.35
    ax.add_patch(Rectangle((0.42,y-0.42),0.60,0.52,fc=SERIES[k%6],ec=SERIES[k%6],
                 lw=0.9,alpha=0.45,zorder=3))
    ax.text(0.72,y-0.52,nm,ha='center',va='top',fontsize=6.0,color=INK,zorder=3)
# an open window
ax.add_patch(Rectangle((2.55,1.45),5.40,3.15,fc='white',ec=INK,lw=1.1,zorder=3))
ax.add_patch(Rectangle((2.55,4.24),5.40,0.36,fc=ACCENT,ec=INK,lw=1.1,alpha=0.35,zorder=4))
ax.text(2.72,4.42,'Documents',ha='left',va='center',fontsize=6.8,color=INK,zorder=5)
for k,s in enumerate(['–','□','×']):
    ax.text(7.90-0.30*(2-k),4.42,s,ha='center',va='center',fontsize=6.6,color=INK,zorder=5)
# taskbar
TB=0.62
ax.add_patch(Rectangle((0.0,0.0),SW,TB,fc=INK,ec=INK,lw=1.0,alpha=0.18,zorder=4))
ax.add_patch(Rectangle((0.22,0.14),0.34,0.34,fc=ACCENT,ec=ACCENT,lw=0.9,alpha=0.70,zorder=5))
ax.add_patch(FancyBboxPatch((0.72,0.14),1.55,0.34,
    boxstyle="round,pad=0,rounding_size=0.16",fc='white',ec=MUTED,lw=0.8,zorder=5))
ax.text(0.86,0.31,'Search',ha='left',va='center',fontsize=6.0,color=MUTED,zorder=6)
for k in range(4):
    ax.add_patch(Rectangle((2.55+k*0.52,0.14),0.34,0.34,fc=SERIES[k%6],ec=SERIES[k%6],
                 lw=0.8,alpha=0.55,zorder=5))
for k in range(3):
    ax.add_patch(Circle((6.85+k*0.30,0.31),0.09,fc=MUTED,ec=MUTED,lw=0.7,alpha=0.7,zorder=5))
ax.text(9.15,0.31,'2:40 PM',ha='right',va='center',fontsize=6.0,color=INK,zorder=5)
def call(p,q,t,ha='left'):
    ax.annotate('',xy=p,xytext=q,zorder=7,
        arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.9))
    ax.text(q[0]+(0.10 if ha=='left' else -0.10),q[1],t,ha=ha,va='center',
            fontsize=7.0,color=MUTED,zorder=7)
call((0.72,4.60),(-0.55,5.20),'desktop icons','right')
call((5.25,4.42),(10.00,4.90),'title bar')
call((7.85,4.42),(10.00,4.10),'minimise, maximise, close')
call((5.25,2.90),(10.00,2.60),'open window')
call((0.39,0.31),(-0.55,1.05),'Start button','right')
call((1.50,0.31),(-0.55,0.35),'search box','right')
call((3.20,0.31),(4.40,-0.70),'pinned and running apps')
call((7.55,0.31),(10.00,-0.70),'notification area and clock')
ax.set_xlim(-2.65,13.30); ax.set_ylim(-1.30,5.70); ax.set_aspect('equal'); ax.axis('off')
```

## 3.5 Working in a desktop application and the window environment

A **window** is a rectangular area of the screen in which one application runs.
Every Windows application window has the same furniture, so once you can drive
one you can drive them all.

```figure caption="Parts of an application window. Every Windows program uses the same furniture, which is why a user who knows one program can find their way around another."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.1))
W,H = 8.40, 4.60
ax.add_patch(Rectangle((0,0),W,H,fc='white',ec=INK,lw=1.4,zorder=3))
ax.add_patch(Rectangle((0,H-0.52),W,0.52,fc=ACCENT,ec=INK,lw=1.1,alpha=0.30,zorder=4))
ax.text(0.20,H-0.26,'Report.docx  —  Word',ha='left',va='center',fontsize=7.4,color=INK,zorder=5)
for k,s in enumerate(['–','□','×']):
    ax.text(W-1.15+0.42*k,H-0.26,s,ha='center',va='center',fontsize=7.6,color=INK,zorder=5)
ax.add_patch(Rectangle((0,H-0.96),W,0.44,fc=MUTED,ec=INK,lw=0.9,alpha=0.12,zorder=4))
for k,m in enumerate(['File','Home','Insert','Review','View']):
    ax.text(0.28+k*1.50,H-0.74,m,ha='left',va='center',fontsize=6.6,color=INK,zorder=5)
ax.add_patch(Rectangle((0,H-1.74),W,0.78,fc=SERIES[1],ec=INK,lw=0.9,alpha=0.12,zorder=4))
for k in range(9):
    ax.add_patch(Rectangle((0.24+k*0.62,H-1.58),0.42,0.46,fc=SERIES[k%6],ec=SERIES[k%6],
                 lw=0.7,alpha=0.40,zorder=5))
ax.add_patch(Rectangle((0,0),W,0.42,fc=MUTED,ec=INK,lw=0.9,alpha=0.12,zorder=4))
ax.text(0.20,0.21,'Page 1 of 3      620 words      100%',ha='left',va='center',
        fontsize=6.6,color=INK,zorder=5)
ax.add_patch(Rectangle((W-0.34,0.42),0.34,H-2.16,fc=MUTED,ec=INK,lw=0.8,alpha=0.12,zorder=4))
ax.add_patch(Rectangle((W-0.30,H-3.40),0.26,1.05,fc=MUTED,ec=MUTED,lw=0.8,alpha=0.55,zorder=5))
ax.text(0.45,(H-2.16)/2+0.42,'work area  /  document area',ha='left',va='center',
        fontsize=7.6,color=MUTED,zorder=5)
def call(p,q,t,ha='left'):
    ax.annotate('',xy=p,xytext=q,zorder=7,
        arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.9))
    ax.text(q[0]+(0.12 if ha=='left' else -0.12),q[1],t,ha=ha,va='center',
            fontsize=7.2,color=MUTED,zorder=7)
call((2.40,H-0.26),(-0.40,H+0.70),'title bar','right')
call((W-0.75,H-0.26),(W+0.40,H+0.70),'minimise / maximise / close')
call((4.20,H-0.74),(-0.40,H-0.55),'menu bar','right')
call((3.00,H-1.35),(-0.40,H-1.60),'toolbar / ribbon','right')
call((W-0.17,H-2.90),(W+0.40,H-2.40),'scroll bar')
call((3.60,0.21),(W+0.40,-0.75),'status bar')
call((W,1.30),(W+0.40,1.60),'border (drag to resize)')
ax.set_xlim(-3.30,12.20); ax.set_ylim(-1.30,5.80); ax.set_aspect('equal'); ax.axis('off')
```

| Part of the window | What it does |
|---|---|
| Title bar | shows the document and program name; drag it to move the window |
| Control buttons | minimise (to taskbar), maximise / restore, close |
| Menu bar / ribbon | groups every command of the program into tabs |
| Toolbar / quick access | one-click buttons for common commands (save, undo) |
| Work area | where the document, image or web page is displayed |
| Scroll bars | move the view vertically or horizontally |
| Status bar | shows page number, word count, zoom level, mode |
| Border and corners | drag to resize the window |

**Working with windows.** Move a window by dragging its title bar; resize by
dragging a border; maximise by double-clicking the title bar or pressing
`Windows + Up`; snap two windows side by side by dragging one to the left or
right edge (or `Windows + Left` / `Windows + Right`); switch between windows
with `Alt + Tab`; see all open windows and virtual desktops with `Windows + Tab`;
minimise everything with `Windows + D`.

::: example Worked example 3.2 — starting and using a desktop application
**Problem.** Write the steps to open MS Word, type and save a document named
`Essay.docx` inside a folder `Class11` on drive D, and then close the program.

**Solution.**
1. Click **Start** → type `Word` in the search box → press **Enter** (or click
   the Word tile).
2. Choose **Blank document**.
3. Type the text in the work area.
4. Click **File → Save As → Browse**; in the dialog navigate to `D:\Class11`.
5. Type `Essay` in the *File name* box, leave *Save as type* as *Word Document*,
   and click **Save**. (The shortcut `Ctrl + S` does the same job.)
6. Click the **×** button on the title bar, or press `Alt + F4`, to close Word.
:::

::: tip Dialog boxes are not windows
A **dialog box** asks you for information (Save As, Print, Font). It usually
cannot be resized and is **modal** — you must answer it or cancel it before the
program will accept anything else.
:::

## 3.6 Managing files and folders with File Explorer

::: definition File and folder
A **file** is a named collection of related data stored on a secondary storage
device. A **folder (directory)** is a container that holds files and other
folders, giving the storage a **hierarchical tree structure**.
:::

**File Explorer** (`Windows + E`) is the Windows tool for browsing that tree. Its
parts are the **navigation pane** on the left (Quick access, This PC, OneDrive,
Network), the **ribbon or command bar** at the top, the **address bar** showing
the current path, the **search box**, and the **content pane** listing the items.

```figure caption="A small part of a Windows folder tree. The full name of a file is its path: the drive, then every folder from the root, then the file name and extension."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
nodes=[(0,6.05,'C:\\',            0,'drive (root)'),
       (1,5.35,'Windows',         1,''),
       (1,4.65,'Program Files',   1,''),
       (1,3.95,'Users',           1,''),
       (2,3.25,'Sabina',          2,''),
       (3,2.55,'Documents',       3,''),
       (4,1.85,'Class 11',        4,''),
       (5,1.15,'Essay.docx',      5,'file'),
       (5,0.45,'Marks.xlsx',      5,'file')]
X0=0.55; DX=0.78
prev={}
for depth,y,name,k,note in nodes:
    x=X0+depth*DX
    isfile = note=='file'
    c = SERIES[3] if isfile else (ACCENT if depth==0 else SERIES[0])
    w = 0.16*len(name)+0.55
    ax.add_patch(FancyBboxPatch((x,y-0.24),w,0.48,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc=c,ec=c,lw=1.0,alpha=0.16,zorder=3))
    ax.add_patch(FancyBboxPatch((x,y-0.24),w,0.48,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc='none',ec=c,lw=1.0,zorder=4))
    ax.text(x+w/2,y,name,ha='center',va='center',fontsize=7.8,color=INK,zorder=5)
    if depth>0:
        px,py = prev[depth-1]
        ax.plot([px+0.22,px+0.22,x],[py-0.24,y,y],color=MUTED,lw=1.0,zorder=2)
    prev[depth]=(x,y)
ax.text(X0+1.35,6.05,'root of drive C',ha='left',va='center',fontsize=7.2,color=MUTED)
ax.text(X0,-0.25,'Path of the file:   C:\\Users\\Sabina\\Documents\\Class 11\\Essay.docx',
        ha='left',va='top',fontsize=8.0,color=INK)
ax.set_xlim(0.0,7.10); ax.set_ylim(-0.95,6.55); ax.set_aspect('equal'); ax.axis('off')
```

### Common file-management operations

| Task | How to do it |
|---|---|
| Create a folder | right-click empty space → **New → Folder**, type the name, press Enter |
| Rename | select, press **F2**, type the new name |
| Copy | select, **Ctrl + C**, open the destination, **Ctrl + V** |
| Move | select, **Ctrl + X**, open the destination, **Ctrl + V** (or drag within the same drive) |
| Delete to Recycle Bin | select, press **Delete** |
| Delete permanently | select, press **Shift + Delete** |
| Restore a deleted file | open **Recycle Bin**, right-click the item → **Restore** |
| Select several items | **Ctrl + click** for scattered items, **Shift + click** for a run, **Ctrl + A** for all |
| Search | type in the search box; use `*.docx` to find all Word files |
| See hidden files | **View → Show → Hidden items** |
| Check size / properties | right-click → **Properties** |

A file is identified by its **name** and its **extension**, separated by a dot.
The extension tells Windows which program should open the file.

| Extension | Type of file | Usual program |
|---|---|---|
| `.docx` | word processor document | MS Word |
| `.xlsx` | spreadsheet workbook | MS Excel |
| `.pptx` | presentation | MS PowerPoint |
| `.pdf` | portable document | Adobe Reader, browser |
| `.txt` | plain text | Notepad |
| `.jpg` `.png` | image | Photos |
| `.mp3` `.mp4` | audio, video | media player |
| `.exe` | executable program | Windows itself |
| `.zip` `.rar` | compressed archive | File Explorer, WinRAR |

::: example Worked example 3.3 — building a folder structure
**Problem.** Write the steps to create a folder `Class11` on drive D containing
sub-folders `Computer`, `Physics` and `Maths`, then copy a file `notes.docx`
from the Desktop into `Computer`, and finally write the full path of the copied
file.

**Solution.**
1. Press `Windows + E` to open File Explorer and click **This PC → Local Disk
   (D:)**.
2. Right-click in an empty part of the content pane → **New → Folder** → type
   `Class11` → Enter.
3. Double-click `Class11` to open it, and repeat step 2 three times to create
   `Computer`, `Physics` and `Maths`.
4. Minimise File Explorer, click `notes.docx` on the Desktop and press
   `Ctrl + C`.
5. Return to File Explorer, open `D:\Class11\Computer` and press `Ctrl + V`.
6. The full path of the copied file is
   **`D:\Class11\Computer\notes.docx`**.
:::

::: caution Shift + Delete does not go to the Recycle Bin
`Delete` moves an item to the Recycle Bin, from which it can be restored.
`Shift + Delete` removes it immediately. Files deleted from a USB flash drive
or a network drive also bypass the Recycle Bin.
:::

## 3.7 Customising the Start screen and desktop; installing and removing devices

### Customising the desktop

Right-click the desktop → **Personalise** to reach the settings for:

- **Background** — a picture, a solid colour or a slideshow.
- **Colours** — light or dark mode, accent colour, transparency.
- **Themes** — a saved bundle of wallpaper, colours, sounds and mouse pointers.
- **Lock screen** and **screen saver** (with "on resume, display logon screen"
  for security).
- **Taskbar** — alignment (centre or left), which icons appear, auto-hide,
  combine buttons.
- **Display settings** (right-click the desktop) — resolution, orientation,
  scaling, multiple monitors, night light.

Desktop icons are added through **Personalise → Themes → Desktop icon settings**
(This PC, Recycle Bin, Network) or by right-clicking a program → **Send to →
Desktop (create shortcut)**.

### Customising the Start menu

Open **Settings → Personalisation → Start** to choose whether recently added
apps, most used apps and recommended files are shown. To **pin** a program,
right-click it in the Start menu or in the app list and choose **Pin to Start**
(or **Pin to taskbar**); to remove it choose **Unpin from Start**. Tiles or
icons can be dragged into a new position and grouped into folders.

### Installing and removing devices

Most hardware today is **Plug and Play**: plug the device into a USB port and
Windows identifies it, finds a matching driver and configures it automatically.
If it does not:

1. Connect the device and switch it on.
2. Open **Settings → Bluetooth & devices → Add device** (for a Bluetooth or
   wireless device), or **Settings → Bluetooth & devices → Printers & scanners →
   Add device** for a printer.
3. If no driver is found, install the driver supplied by the manufacturer on a
   disc or downloaded from the manufacturer's website.
4. Verify in **Device Manager** (right-click **Start → Device Manager**) that the
   device is listed without a yellow warning triangle.

To **remove** a device: right-click **Start → Device Manager**, right-click the
device → **Uninstall device**, tick *delete the driver software* if you want it
gone completely, then unplug the hardware. A USB flash drive should always be
removed through **Safely Remove Hardware** in the notification area so that any
buffered data is written out first.

To **uninstall a program**, go to **Settings → Apps → Installed apps**, click the
three dots beside the program and choose **Uninstall** (the old route was
**Control Panel → Programs and Features**).

::: definition Device driver
A **device driver** is a small system program that translates the operating
system's general commands into the specific signals a particular hardware device
understands. Without the correct driver a device either does not work at all or
works with reduced features.
:::

## 3.8 Managing passwords and privacy; Control Panel, system tools and accessories

### User accounts, passwords and privacy

Windows supports several account types: **Administrator** (can install software
and change system settings), **Standard user** (can run programs and change only
personal settings), and **Guest / Child** accounts with further restrictions.
Accounts are managed from **Settings → Accounts**.

To change a password: **Settings → Accounts → Sign-in options → Password →
Change**. Other sign-in options include a **PIN**, **Windows Hello** face or
fingerprint recognition, and a **picture password**.

::: key Rules for a strong password
Use at least 12 characters, mixing upper case, lower case, digits and symbols.
Do not use your name, your date of birth, `password` or `123456`. Use a
**different** password for every important account, change it if you suspect it
has leaked, never write it on a sticky note, and turn on **two-factor
authentication** wherever it is offered.
:::

**Privacy levels** are set in **Settings → Privacy & security**, where you decide
which apps may use the camera, microphone, location, contacts and notifications,
how much diagnostic data is sent to Microsoft, and whether an advertising ID is
used. Related security settings live in **Windows Security**: virus and threat
protection, firewall, account protection, and device encryption (BitLocker).
**User Account Control (UAC)** asks for confirmation before any program makes a
system-wide change.

### Control Panel

The **Control Panel** is the classic central place for configuring Windows. It is
opened by typing `control` in the search box, and its main categories are:

| Category | Typical settings |
|---|---|
| System and Security | system information, Windows Tools, backup, BitLocker |
| Network and Internet | network status, adapter settings, internet options |
| Hardware and Sound | devices and printers, power options, sound, AutoPlay |
| Programs | uninstall a program, default programs, Windows features |
| User Accounts | change account type, Credential Manager |
| Appearance and Personalisation | fonts, File Explorer options, taskbar |
| Clock and Region | date, time, time zone, formats |
| Ease of Access | Narrator, Magnifier, high contrast |

In Windows 11 most of these are being migrated into the modern **Settings** app,
but the Control Panel is still present and is still examinable.

### System tools and accessories

| Tool | What it does |
|---|---|
| **Disk Cleanup** | deletes temporary files, cached pages and Recycle Bin contents |
| **Disk Defragmenter / Optimise Drives** | rearranges fragmented files on a hard disk so reads are faster (not used on SSDs, which are "trimmed" instead) |
| **Backup and Restore / File History** | copies important files so they can be recovered |
| **System Restore** | returns system files and settings to an earlier restore point |
| **Task Manager** (`Ctrl + Shift + Esc`) | shows running processes, CPU, memory, disk and network usage; ends a hung program |
| **Disk Management** | creates, formats, shrinks and extends partitions |
| **Device Manager** | lists hardware and manages drivers |
| **Windows Security** | antivirus, firewall, threat history |
| **Character Map** | inserts symbols not on the keyboard |
| **Notepad / WordPad** | simple text editing |
| **Paint** | simple drawing and image editing |
| **Calculator** | standard, scientific, programmer (base conversion!) and date modes |
| **Snipping Tool** | captures part of the screen |
| **Command Prompt / PowerShell / Terminal** | command line access |

::: tip Programmer mode of the Calculator
Windows Calculator has a **Programmer** mode that converts between HEX, DEC, OCT
and BIN and performs bitwise AND, OR, XOR and NOT. Use it to *check* the answers
to Unit 2 conversions — but never to replace the hand method, because the
examination asks for the working.
:::

## 3.9 Open source operating systems: UNIX, Linux and Linux distributions

::: definition Open source software
**Open source software** is software whose **source code is published** under a
licence (such as the GNU GPL) that grants everyone the freedom to run, study,
modify and redistribute it. It is usually free of cost, but the essential point
is freedom of the code, not the price.
:::

**Advantages:** no licence fee; the code can be inspected, so security holes are
found and fixed quickly; it can be customised for local needs (for example
Nepali language support); it is not tied to one vendor; and it often runs well
on older hardware.

**Disadvantages:** commercial support may have to be bought separately; some
proprietary hardware lacks drivers; specialised commercial software (certain
accounting or engineering packages) may not be available; and the user interface
varies between distributions.

### UNIX

**UNIX** was developed at **AT&T Bell Laboratories in 1969** by **Ken Thompson**
and **Dennis Ritchie**, and was rewritten in the C language in 1973 — which is
why it could be moved from one machine to another. UNIX is a **multi-user,
multitasking, time-sharing** operating system with a hierarchical file system, a
powerful shell and the philosophy of "small tools that do one job well and can be
piped together". It is proprietary; modern descendants include IBM AIX, Oracle
Solaris, HP-UX and (through BSD) macOS.

### Linux

**Linux** is a free, open-source, UNIX-like operating system **kernel** written
by **Linus Torvalds** in **1991** while he was a student in Helsinki, and
released under the GNU GPL. Combined with the GNU tools of **Richard Stallman's**
GNU Project (begun in 1983) it forms a complete operating system, properly called
**GNU/Linux**. As of 2025 Linux runs essentially **all of the world's top 500
supercomputers**, the large majority of web servers and cloud instances, and —
through the Android kernel — most of the world's smartphones.

```figure caption="Layered architecture of a Linux system. Only the kernel talks to the hardware; the shell is the command interpreter between the user and the kernel."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.4,4.4))
rings=[(3.90,'Users and applications',SERIES[1],7.4),
       (3.00,'Utilities and libraries',SERIES[2],7.0),
       (2.10,'Shell (bash, zsh)',SERIES[0],7.0),
       (1.30,'KERNEL',ACCENT,7.4),
       (0.82,'Hardware',SERIES[4],6.8)]
for r,lab,c,fs in rings:
    ax.add_patch(Circle((0,0),r,fc=c,ec=c,lw=1.3,alpha=0.16,zorder=2))
    ax.add_patch(Circle((0,0),r,fc='none',ec=c,lw=1.3,zorder=3))
for k,(r,lab,c,fs) in enumerate(rings):
    inner = rings[k+1][0] if k+1 < len(rings) else 0.0
    y = 0.0 if k==len(rings)-1 else (r+inner)/2
    ax.text(0,y,lab,ha='center',va='center',fontsize=fs,color=INK,zorder=5)
ax.text(0,4.30,'a command typed in the shell is passed to the kernel,\n'
               'which is the only layer that touches the hardware',
        ha='center',va='bottom',fontsize=7.0,color=MUTED)
ax.set_xlim(-4.55,4.55); ax.set_ylim(-4.20,5.05); ax.set_aspect('equal'); ax.axis('off')
```

The **kernel** is the core of Linux: it manages processes, memory, devices and
the file system. The **shell** (bash, zsh, fish) is the command interpreter that
reads what you type and asks the kernel to carry it out. Some everyday shell
commands:

```text
pwd                  print the working directory
ls -l                list files with details
cd /home/sabina      change directory
mkdir Class11        make a directory
cp notes.txt backup/ copy a file
mv old.txt new.txt   rename or move
rm -i notes.txt      remove, asking first
cat marks.txt        display a file
chmod 755 run.sh     change file permissions
sudo apt update      run a command as the superuser
man ls               read the manual page
```

### Linux distributions

A **distribution (distro)** is the Linux kernel packaged together with GNU
utilities, a desktop environment, a package manager and a collection of
applications, ready to install.

| Distribution | Family / package manager | Best known for |
|---|---|---|
| **Ubuntu** | Debian, `apt` | the easiest starting point; huge community |
| **Debian** | Debian, `apt` | rock-solid stability; the base of many others |
| **Linux Mint** | Debian/Ubuntu, `apt` | a familiar Windows-like desktop |
| **Fedora** | Red Hat, `dnf` | newest technology; upstream of RHEL |
| **Red Hat Enterprise Linux / CentOS Stream** | Red Hat, `dnf` | paid commercial support in servers |
| **openSUSE** | SUSE, `zypper` | the YaST configuration tool |
| **Arch Linux** | Arch, `pacman` | build-it-yourself, rolling release |
| **Kali Linux** | Debian, `apt` | penetration testing and security tools |

| Feature | Windows | Linux |
|---|---|---|
| Source code | closed, proprietary | open, GPL |
| Cost | paid licence | normally free |
| File system | NTFS, drive letters `C:` `D:` | ext4, one tree from `/` |
| Path separator | backslash `\` | forward slash `/` |
| Case sensitivity | file names not case sensitive | file names **are** case sensitive |
| Superuser | Administrator | `root` (reached with `sudo`) |
| Software source | Store, `.exe` installers | package manager repositories |
| Typical use | desktops, offices | servers, supercomputers, embedded, Android |

## 3.10 Mobile operating systems and their types

::: definition Mobile operating system
A **mobile operating system** is an operating system designed for handheld
devices — smartphones, tablets and wearables. It must support a touch screen,
manage a battery carefully, work over cellular and wireless networks, and use
sensors such as GPS, accelerometer and camera.
:::

Differences from a desktop OS: a **touch-first** interface; aggressive **power
management**; each app is **sandboxed** and must request permissions; apps are
installed from a controlled **app store**; the system must survive interruptions
such as an incoming call; and memory and storage are limited and not
user-upgradeable.

```figure caption="Share of the worldwide smartphone operating system market, approximate figures for 2025. Android leads globally, while iOS has a much larger share in high-income markets than in South Asia."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.6))
names=['Android','iOS','Others\n(HarmonyOS, KaiOS…)']
world=[72,27,1]
nepal=[93,6,1]
y=np.arange(len(names)); h=0.36
ax.barh(y+h/2,world,height=h,color=SERIES[0],label='World')
ax.barh(y-h/2,nepal,height=h,color=SERIES[2],label='Nepal')
for yy,v in zip(y+h/2,world):
    ax.text(v+1.5,yy,'%d %%'%v,va='center',fontsize=7.6,color=INK)
for yy,v in zip(y-h/2,nepal):
    ax.text(v+1.5,yy,'%d %%'%v,va='center',fontsize=7.6,color=INK)
ax.set_yticks(y); ax.set_yticklabels(names,fontsize=8.0)
ax.set_xlim(0,108); ax.set_xlabel('share of smartphones in use (%)',fontsize=8.0)
ax.tick_params(labelsize=7.6)
ax.legend(fontsize=7.4,frameon=False,loc='upper right')
ax.grid(axis='x',color=GRID,lw=0.6); ax.set_axisbelow(True)
for s in ('top','right','left'): ax.spines[s].set_visible(False)
fig.tight_layout()
```

| Mobile OS | Owner | Kernel / base | Open source? | Notes |
|---|---|---|---|---|
| **Android** | Google (Open Handset Alliance) | Linux | yes (AOSP core) | largest share; used by Samsung, Xiaomi, Oppo, Vivo; apps from Google Play |
| **iOS / iPadOS** | Apple | Darwin (UNIX-like) | no | runs only on Apple hardware; App Store only; strong privacy record |
| **HarmonyOS** | Huawei | HarmonyOS/Linux | partly | developed after Huawei lost Google services; large in China |
| **KaiOS** | KaiOS Technologies | Linux | partly | for cheap feature phones with 4G |
| **Wear OS / watchOS** | Google / Apple | Linux / Darwin | no | smart watches |
| **Windows Phone** | Microsoft | Windows NT | no | **discontinued** in 2019 — historical only |
| **Symbian, BlackBerry OS** | Nokia / BlackBerry | — | no | dominant before 2010; now obsolete |

As of 2026 the current major releases are **Android 16** and **iOS 26**. Two
operating systems therefore account for almost the entire market, which is why
mobile application developers normally target only Android and iOS — or write
one **cross-platform** app with a framework such as Flutter or React Native.

::: example Worked example 3.4 — choosing an operating system
**Problem.** A school in Chitwan has 30 old desktop computers (4 GB RAM) for a
computer laboratory, a server for its student-record system, and wants an app so
that parents can check results on their phones. Recommend an operating system
for each, with reasons.

**Solution.**
- **Laboratory desktops:** a lightweight **Linux distribution** such as Linux
  Mint or Ubuntu with the Xfce desktop. There is no licence fee for 30 machines,
  it runs well in 4 GB of RAM, LibreOffice covers the office syllabus, and the
  students get exposure to open-source software.
- **Server:** **Ubuntu Server** or **Debian**. Linux dominates server use because
  it is stable, secure, remotely manageable over SSH and free.
- **Parents' phones:** an **Android** app first, because as of 2025 Android
  covers well over 90 % of smartphones in Nepal, followed by an **iOS** version
  if the budget allows — or a single **web-based** result portal, which needs no
  app store at all.
:::

## Chapter summary

- **Software** is the set of programs that tells hardware what to do. The
  syllabus categories are **system**, **utility**, **application**, **web-based**
  and **mobile apps**.
- An **operating system** is the interface between user and hardware and the
  manager of all resources. Its functions are **process, memory, file, device,
  security** and **user-interface** management.
- **Multiprogramming**: many jobs, one CPU, switch on I/O wait.
  **Multitasking**: many jobs, one CPU, switch on time slice.
  **Multiprocessing**: many CPUs in one machine, true parallelism.
  **Distributed**: many machines on a network acting as one.
- **Windows** is a GUI (WIMP) operating system whose desktop, taskbar, Start
  menu, windows and File Explorer follow one consistent design. Know the parts
  of a window and the standard file operations and shortcuts.
- A **file path** names a drive, the chain of folders and the file with its
  extension, for example `D:\Class11\Computer\notes.docx`.
- **Control Panel and Settings** configure the system; **system tools** such as
  Disk Cleanup, Task Manager, Device Manager and System Restore maintain it.
- **Open source** means the source code is published and may be modified.
  **UNIX** (Bell Labs, 1969) is the ancestor; **Linux** (Torvalds, 1991) is the
  free UNIX-like kernel, delivered as **distributions** such as Ubuntu, Debian,
  Fedora and Mint.
- **Mobile operating systems** are touch-first, power-aware and sandboxed.
  **Android** (Linux based, open) and **iOS** (Apple, closed) together hold
  almost the whole market.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** system software? <span class="marks">[1]</span>
   (a) device driver (b) compiler (c) MS Excel (d) operating system
2. Google Docs is an example of <span class="marks">[1]</span>
   (a) utility software (b) web-based software (c) system software (d) firmware
3. The part of the operating system that is always resident in main memory is
   the <span class="marks">[1]</span>
   (a) shell (b) kernel (c) compiler (d) driver
4. Executing several programs on a single CPU by giving each a fixed time slice
   is called <span class="marks">[1]</span>
   (a) multiprogramming (b) multiprocessing (c) multitasking (d) batch
   processing
5. Which key combination opens File Explorer in Windows? <span class="marks">[1]</span>
   (a) Windows + D (b) Windows + E (c) Ctrl + Shift + Esc (d) Alt + Tab
6. Linux was first developed by <span class="marks">[1]</span>
   (a) Dennis Ritchie (b) Richard Stallman (c) Linus Torvalds (d) Bill Gates
7. Which of the following is a Linux distribution? <span class="marks">[1]</span>
   (a) Fedora (b) Solaris (c) Darwin (d) Symbian
8. Android is based on which kernel? <span class="marks">[1]</span>
   (a) Windows NT (b) Darwin (c) Linux (d) Symbian
9. The tool used to remove temporary files and free disk space is <span class="marks">[1]</span>
   (a) Disk Cleanup (b) Device Manager (c) Task Manager (d) Character Map

::: note Answers to Group A
**1.** (c) — MS Excel is application software.
**2.** (b) — it runs on a remote server and is used through a browser.
**3.** (b) — the kernel.
**4.** (c) — the fixed time slice is the mark of multitasking.
**5.** (b) — Windows + E.
**6.** (c) — Linus Torvalds, 1991.
**7.** (a) — Fedora; Solaris and Darwin are UNIX-like but not Linux, and Symbian
was a mobile OS.
**8.** (c) — Linux.
**9.** (a) — Disk Cleanup.
:::

**Group B — Short answer (5 marks each)**

1. Define software. Explain the five categories of software given in the
   syllabus with two examples of each. <span class="marks">[5]</span>
2. What is an operating system? Explain any five functions of an operating
   system. <span class="marks">[5]</span>
3. Differentiate between multiprogramming and multitasking, and between
   multiprocessing and distributed processing. <span class="marks">[5]</span>
4. What is a GUI? List any six features of the Windows operating system and
   compare a GUI with a CLI. <span class="marks">[5]</span>
5. Write the steps to create a folder named `Project` on drive D, copy two files
   into it, rename one of them, and delete the other permanently. <span class="marks">[5]</span>
6. What is open source software? Write any four advantages of it and name four
   Linux distributions. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Software is a set of programs, procedures and documentation that tells
hardware what to do. *System*: Windows 11, device drivers. *Utility*: antivirus,
WinRAR. *Application*: MS Word, Photoshop. *Web-based*: Gmail, Google Docs.
*Mobile apps*: eSewa, Khalti.

**2.** An OS is system software that acts as an interface between the user and
the hardware and manages all resources. Five functions: process management,
memory management, file management, device (I/O) management, and security and
protection. (User-interface provision and error detection also earn the mark.)

**3.** *Multiprogramming vs multitasking* — both keep several programs in memory
on one CPU, but multiprogramming switches only when the running program waits for
I/O and aims at CPU utilisation, whereas multitasking switches after a fixed time
slice and aims at response time. *Multiprocessing vs distributed* —
multiprocessing uses two or more CPUs inside **one** computer sharing one memory;
distributed processing uses **many independent computers** with their own memory
linked by a network.

**5.** (i) `Windows + E` → **This PC → Local Disk (D:)**. (ii) Right-click empty
space → **New → Folder** → type `Project` → Enter. (iii) Select the two files,
`Ctrl + C`, open `D:\Project`, `Ctrl + V`. (iv) Click the first file, press
**F2**, type the new name, Enter. (v) Click the second file and press
**Shift + Delete**, then confirm — this bypasses the Recycle Bin.

**6.** Open source software publishes its source code under a licence allowing
anyone to run, study, modify and redistribute it. Advantages: no licence cost;
security flaws are found and fixed quickly because the code is public; it can be
customised (for example for Nepali); no vendor lock-in. Distributions: Ubuntu,
Debian, Fedora, Linux Mint (also openSUSE, Arch, Kali).
:::

**Group C — Long answer (8 marks each)**

1. (a) Define an operating system and explain its role as a resource manager and
   as an extended machine. <span class="marks">[3]</span>
   (b) Explain in detail any five functions of an operating system, and name one
   Windows tool associated with each. <span class="marks">[5]</span>
2. (a) With a suitable diagram, explain the parts of a window in a Windows
   application. <span class="marks">[4]</span>
   (b) Explain the steps to install a new printer, and the steps to uninstall an
   unwanted program from a Windows computer. <span class="marks">[4]</span>
3. (a) What is open source software? Compare Windows and Linux under any five
   headings. <span class="marks">[5]</span>
   (b) What is a mobile operating system? Explain any three types with their
   owners and note how a mobile OS differs from a desktop OS. <span class="marks">[3]</span>

::: note Answers to Group C
**1. (b)** *Process management* — scheduling the CPU among processes (Task
Manager). *Memory management* — allocating RAM and virtual memory (Task Manager
→ Performance). *File management* — creating, organising and protecting files
(File Explorer). *Device management* — drivers, buffering and spooling (Device
Manager). *Security* — accounts, passwords, firewall, antivirus (Windows
Security). Each point should be explained in two or three sentences with an
example.

**2. (b)** *Installing a printer*: connect the printer by USB or to the Wi-Fi
network and switch it on → **Settings → Bluetooth & devices → Printers &
scanners → Add device** → Windows searches and installs the driver → if it is
not found, click *Add manually* and supply the driver from the manufacturer's
disc or website → print a test page. *Uninstalling a program*: **Settings → Apps
→ Installed apps** → find the program → click the three dots → **Uninstall** →
confirm, and restart if asked. (Control Panel → Programs and Features does the
same job.)

**3. (b)** A mobile OS is an operating system for handheld devices, designed for
a touch screen, limited battery and cellular connectivity. *Android* (Google,
Linux kernel, open source, apps from Google Play); *iOS* (Apple, Darwin kernel,
closed, runs only on Apple hardware); *HarmonyOS* (Huawei) or *KaiOS* (for
feature phones). Differences from a desktop OS: touch-first interface, strict
power management, sandboxed apps with permissions, app-store-only installation,
and hardware that cannot be upgraded by the user.
:::
