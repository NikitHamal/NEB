---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 3
title: Operating System
hours: 4
area: BCA 101 · Computer Fundamentals and Applications · Unit 3
---

The **operating system (OS)** is the manager of the computer: it shares the CPU, memory and devices among programs, protects them from each other, and gives users a way to work. This unit introduces what an OS does, the main kinds, and how it handles processes, memory, files and booting. (The Semester IV subject *Operating Systems* goes much deeper.)

::: key What this unit gives you
- Functions of an OS and its two roles: resource manager and virtual machine.
- Types of OS: batch, multiprogramming, time-sharing, real-time, distributed, network, mobile.
- Processes, process states and CPU scheduling with worked numeric examples.
- Memory management: partitioning, paging, virtual memory.
- Files, directories, user interfaces, the boot sequence, and a first look at Windows and Linux.
:::

## 3.1 What an OS does

An OS has two faces:

- **Resource manager**: allocates CPU time, memory, disk and I/O devices fairly and safely.
- **Extended machine**: hides ugly hardware details behind simple interfaces ("save this file" instead of "move the disk head to cylinder 213").

| Function | Meaning |
|---|---|
| Process management | create, schedule, suspend and terminate programs in execution |
| Memory management | give each process memory, keep processes out of each other's space |
| File management | organise data in files and folders, control access |
| Device management | drive hardware through **device drivers**, queue requests, buffer data |
| Security and protection | user accounts, permissions, isolation |
| User interface | command line or graphical |
| Error handling and accounting | detect faults, log resource use |

The **kernel** is the always-resident core of the OS; **system calls** are the doorway through which programs ask the kernel for services (open a file, create a process).

## 3.2 Types of operating system

| Type | Idea | Example / use |
|---|---|---|
| **Batch** | similar jobs grouped and run one after another without user interaction | early mainframe payroll runs |
| **Multiprogramming** | several jobs kept in memory; when one waits for I/O the CPU switches to another, so the CPU stays busy | all modern systems |
| **Multitasking / time-sharing** | the CPU is switched among processes so rapidly (each gets a *time slice* or quantum) that each user feels the machine is theirs | Unix, Windows, Linux |
| **Multiprocessing** | more than one CPU/core executes processes truly in parallel | servers, every multi-core PC |
| **Real-time (RTOS)** | must respond within a guaranteed deadline. *Hard*: a missed deadline is failure; *soft*: it only degrades quality | airbag controller, flight control, industrial robots |
| **Distributed** | many computers cooperate and appear as one system | large web services, clusters |
| **Network OS** | runs on a server that provides shared files, printers, logins to client machines | Windows Server, Novell NetWare |
| **Mobile OS** | built for touch, battery and sensors | Android, iOS |
| **Embedded OS** | built into an appliance with a fixed job | smart TV, router, washing machine |

**Single-user vs multi-user**: DOS was single-user, single-tasking; Linux and Windows Server are multi-user, multitasking.

## 3.3 Process management

A **program** is a passive file on disk; a **process** is a program in execution, with its own memory, registers and program counter. Each process has a **process control block (PCB)** in the kernel that stores its state, PC, registers, memory limits and open files.

**Process states**

```text
   admitted        dispatch (scheduler picks it)
 New ─────▶ Ready ◀──────────────────────▶ Running ─────▶ Terminated
              ▲      timeout / pre-emption     │  exit
              │                                │ waits for I/O or event
              └──────── Waiting (Blocked) ◀───┘
                  I/O or event completes → back to Ready
```

A **context switch** saves the PCB of the running process and loads that of the next; it is pure overhead, so the OS wants few of them.

**CPU scheduling.** Several ready processes compete for one CPU; the **scheduler** chooses. Measures used:

- **Turnaround time** = completion time − arrival time.
- **Waiting time** = turnaround time − burst time (time spent in the ready queue).
- **Response time** = time from arrival to first execution.

| Algorithm | Rule | Pre-emptive? | Remark |
|---|---|---|---|
| FCFS | first come, first served | no | simple; short jobs suffer behind a long one (*convoy effect*) |
| SJF | shortest burst first | no (SRTF is the pre-emptive form) | gives minimum average waiting time; needs burst estimates; long jobs may starve |
| Priority | highest priority first | either | starvation fixed by *aging* |
| Round robin | each process gets a quantum, then goes to the tail of the queue | yes | fair, good response for time-sharing |

::: example Worked example: FCFS, SJF and round robin
Four processes arrive together at time 0 with burst times P1 = 5, P2 = 3, P3 = 8, P4 = 6 (ms).

**FCFS** (order P1, P2, P3, P4): completions 5, 8, 16, 22. Waiting times 0, 5, 8, 16, so average = 29 / 4 = **7.25 ms**.

**SJF** (order P2, P1, P4, P3): P2 waits 0, P1 waits 3, P4 waits 8, P3 waits 14; average = 25 / 4 = **6.25 ms**, which is the minimum possible.

**Round robin, quantum 4 ms:** P1 runs 0–4 (1 left), P2 4–7 (done), P3 7–11 (4 left), P4 11–15 (2 left), P1 15–16 (done), P3 16–20 (done), P4 20–22 (done). Turnarounds: P1 = 16, P2 = 7, P3 = 20, P4 = 22. Waiting = turnaround − burst: 11, 4, 12, 16; average = 43 / 4 = **10.75 ms**. RR has the worst average wait here but every process starts within 11 ms, which is why interactive systems use it.
:::

**Deadlock.** Processes are deadlocked when each holds a resource the next one needs, forming a cycle. It needs four conditions together: mutual exclusion, hold-and-wait, no pre-emption, circular wait. Breaking any one prevents it.

## 3.4 Memory management

Every running program must be in main memory. The OS tracks which parts are free, allocates them and protects them.

- **Contiguous allocation**: each process gets one block. *Fixed partitions* waste space inside a partition (**internal fragmentation**); *variable partitions* leave scattered holes between processes (**external fragmentation**) that **compaction** can merge.
- **Paging**: logical memory is cut into equal **pages**, physical memory into equal **frames**; a **page table** maps page → frame. It removes external fragmentation; only the last page of a process can be partly empty.
- **Segmentation**: memory is divided by *meaning* (code, data, stack) into variable-size segments.
- **Virtual memory**: only the needed pages are kept in RAM; the rest stay on disk (swap space). A **page fault** occurs when a page is not in RAM and must be loaded. Too many faults is **thrashing**. Virtual memory lets programs be larger than physical RAM.

::: example Worked example: address translation with paging
Page size 1 KB = 1024 bytes. A process reads logical address **3500**. Page number = 3500 div 1024 = **3**; offset = 3500 mod 1024 = 3500 − 3072 = **428**. If the page table says page 3 is in frame 7, the physical address = 7 × 1024 + 428 = **7596**.
:::

**Page replacement.** When RAM is full, a victim page must go. FIFO removes the oldest page; LRU removes the least recently used; optimal removes the page not needed for longest (a yardstick, not implementable). Example, 3 frames, reference string 1 2 3 4 1 2 5: FIFO faults on pages 1, 2, 3 (load), 4 (evict 1), 1 (evict 2), 2 (evict 3), 5 (evict 4) → **7 faults**.

## 3.5 File and device management

A **file** is a named collection of related data. The OS keeps file **attributes** (name, type, size, location, owner, permissions, timestamps) and supports operations: create, open, read, write, seek, delete.

- **Directory structure**: modern systems use a **tree** with a root (`C:\` or `/`); a **path** (`C:\Users\sita\notes.txt`, `/home/sita/notes.txt`) names a file. Absolute paths start at the root; relative paths start at the current directory.
- **File systems**: FAT32 (4 GB file limit), NTFS (Windows: permissions, journaling), ext4 (Linux), exFAT (flash drives), APFS (Apple).
- **Allocation**: contiguous, linked, or indexed (an index block lists the file's disk blocks).
- **Access permissions**: Linux uses read, write, execute for owner, group, others. `rwxr-xr--` is octal **754**.

**Devices** are driven through **drivers**. The OS uses **buffering** (temporary storage while data moves between devices of different speeds), **caching** and **spooling** (queueing output, e.g. print jobs, on disk so the program does not wait for the slow printer).

## 3.6 User interfaces and the boot process

- **CLI (command line interface)**: type commands; fast, scriptable, low resource use (Bash, PowerShell, `cmd`).
- **GUI (graphical user interface)**: windows, icons, menus, pointer (WIMP); easier for beginners.
- **Touch/voice interfaces** on mobiles and assistants.

**Booting** is starting the computer:

1. Power on; the CPU starts executing firmware (BIOS/UEFI).
2. **POST** (power-on self-test) checks CPU, RAM, keyboard and disks.
3. Firmware finds the boot device and loads the **boot loader** (e.g. Windows Boot Manager, GRUB).
4. The boot loader loads the **kernel** into RAM.
5. The kernel starts drivers and system services, then the login screen/shell appears.

*Cold boot* = from power-off; *warm boot* = restart without cutting power.

## 3.7 Some operating systems

| OS | Family | Notes |
|---|---|---|
| Windows | Microsoft, proprietary | GUI, NTFS, largest desktop share |
| Linux | open-source kernel (1991, Linus Torvalds) | distributions: Ubuntu, Fedora, Debian; servers, Android's kernel |
| macOS | Apple, Unix-based | proprietary, tight hardware integration |
| Android | Linux kernel + Google framework | most-used mobile OS |
| iOS | Apple | closed, mobile |

Useful Linux commands: `pwd` (where am I), `ls -l` (list with permissions), `cd dir`, `mkdir d`, `cp a b`, `mv a b`, `rm f`, `cat f`, `chmod 754 f`, `ps` (processes), `kill PID`, `sudo` (run as administrator).

## Formula and fact sheet

- Turnaround = completion − arrival. Waiting = turnaround − burst.
- SJF minimises average waiting time; FCFS is simplest; RR is for time-sharing.
- Physical address = frame × page size + offset; page = address div page size, offset = address mod page size.
- Deadlock needs mutual exclusion, hold-and-wait, no pre-emption, circular wait.
- Boot: power on → POST → boot loader → kernel → login.
- Linux permissions r = 4, w = 2, x = 1.

## Chapter summary

- The OS manages processes, memory, files and devices and provides the user interface.
- Multiprogramming keeps the CPU busy; time-sharing gives interactivity; real-time guarantees deadlines.
- Scheduling algorithms trade fairness, throughput and waiting time; SJF is optimal for average wait but needs knowledge of burst lengths.
- Paging maps pages to frames, virtual memory uses disk to extend RAM, and page faults cost time.
- Files live in a directory tree on a file system; booting loads the kernel through firmware and a boot loader.

## Practice

**A. Short questions**

1. Define operating system. State four of its functions.
2. Differentiate multiprogramming and multitasking.
3. What is a real-time OS? Differentiate hard and soft real-time.
4. Differentiate program and process. Draw the process state diagram.
5. What is a context switch?
6. What is virtual memory? What is a page fault?
7. Differentiate CLI and GUI.
8. What is a device driver? What is spooling?

**B. Numerical problems**

9. Processes P1 = 6, P2 = 2, P3 = 4 ms arrive at 0. Find average waiting time under FCFS and SJF.
10. Page size 2 KB. Find the page number and offset of logical address 9000. If that page is in frame 5, find the physical address.
11. The Linux permission string is `rwxr-x---`. Give the octal mode.
12. Reference string 7 0 1 2 0 3 with 3 frames; count the page faults for FIFO.

**C. Long questions**

13. Explain the types of operating systems.
14. Explain the booting process of a computer.
15. Explain paging and virtual memory.

::: note Answers and worked solutions
**1.** An OS is system software that manages hardware and provides services to programs and users. Functions: process, memory, file, device management, security, user interface.
**2.** Multiprogramming keeps several programs in memory to keep the CPU busy during I/O waits; multitasking (time-sharing) additionally switches the CPU by time slice so that users get quick, interactive response.
**3.** An OS that guarantees response within a deadline. Hard: missing a deadline is a failure (airbag); soft: it only reduces quality (video streaming).
**4.** A program is a passive file; a process is a running instance with a PCB. States: new, ready, running, waiting, terminated (diagram in §3.3).
**5.** Saving the state of the running process and loading the state of the next one.
**6.** Virtual memory keeps only the needed pages in RAM and the rest on disk. A page fault is the trap when a referenced page is not in RAM.
**7.** CLI: typed commands, efficient, scriptable. GUI: windows and icons, easy to learn, uses more resources.
**8.** A driver is software that lets the OS control a device. Spooling queues output on disk so the CPU need not wait for a slow device such as a printer.
**9.** FCFS order 6, 2, 4: waits 0, 6, 8 → 14 / 3 = **4.67 ms**. SJF order P2, P3, P1: waits 0, 2, 6 → 8 / 3 = **2.67 ms**.
**10.** Page = 9000 div 2048 = **4**; offset = 9000 − 8192 = **808**. Physical = 5 × 2048 + 808 = **11048**.
**11.** rwx = 7, r-x = 5, --- = 0, so **750**.
**12.** FIFO with 3 frames: 7, 0, 1 load (3 faults); 2 evicts 7 (fault); 0 is a hit; 3 evicts 0 (fault). Total **5 faults**.
**13.** Use the table in §3.2: batch, multiprogramming, time-sharing, multiprocessing, real-time, distributed, network, mobile, embedded, one line and example each.
**14.** Steps 1–5 in §3.6.
**15.** Paging: fixed-size pages and frames, page table, translation example in §3.4. Virtual memory: demand loading, page faults, replacement, thrashing.
:::
