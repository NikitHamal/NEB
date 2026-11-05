---
subject: Operating Systems
grade: BCA Semester 4
unit: 1
title: Introduction to Operating Systems
hours: 2
area: BCA 251 · Operating Systems · Unit 1
---

Switch on a laptop in Kathmandu and within seconds you can run a browser, a music player and a download at the same time, each convinced it owns the machine. None of them talks to the disk, the screen or the network card directly. One program sits between them and the hardware and keeps order: the **operating system (OS)**.

::: key What this unit gives you
- What an OS is, through its two classic roles: resource manager and extended machine.
- A short history of OS generations, from vacuum tubes to smartphones.
- The main types of OS (batch, multiprogramming, time-sharing, real-time, distributed and others).
- The functions an OS performs, which become Units 3 to 8 of this book.
:::

## 1.1 What is an operating system?

A computer has hardware (CPU, memory, disks, keyboard, display, network card) and application software (a spreadsheet, a compiler, a game). Between them lies the **operating system**: the program that runs in privileged mode and manages the hardware on behalf of every other program.

::: definition Operating system
An operating system is system software that manages the computer's hardware resources and provides a convenient, safe and efficient environment in which user programs can run.
:::

Two goals pull against each other. **Convenience**: a programmer writes `fopen("marks.txt")` without knowing which disk sectors hold the file. **Efficiency**: the CPU, memory and disks should be kept busy and shared fairly. A phone OS leans towards convenience and battery life; a mainframe OS towards throughput.

### The two views: resource manager and extended machine

**OS as an extended machine (top-down view).** Raw hardware is ugly. Talking to a disk means programming a controller with block numbers, motor, head and error registers. The OS hides this behind clean abstractions: *files* instead of disk blocks, *processes* instead of CPU time slices, *address spaces* instead of physical RAM, *sockets* instead of network card registers. To the application programmer the OS makes the machine look easier to use than the real hardware, which is why it is called an extended (or virtual) machine.

**OS as a resource manager (bottom-up view).** A real machine has many resources and many competitors. Without control, two programs could print on the same page at once or overwrite each other's memory. The OS keeps track of who uses what, grants requests, resolves conflicts and accounts for usage. Sharing happens in two ways:

- **Time multiplexing**: users take turns (one CPU, one printer).
- **Space multiplexing**: each gets a part (memory divided among processes, a disk divided among files).

### Where the OS sits

| Layer | Examples | Mode |
|---|---|---|
| Application programs | browser, Word, games | user mode |
| Utilities / shell | `bash`, File Explorer, `ls` | user mode |
| **Operating system (kernel)** | scheduler, memory manager, file system, drivers | **kernel mode** |
| Hardware | CPU, RAM, disk, NIC | physical |

The CPU has at least two modes. In **kernel mode** every instruction is allowed. In **user mode** privileged instructions (I/O, changing the memory map, halting) cause a trap. An application asks the kernel for service through a **system call**, which switches the CPU into kernel mode, runs OS code and returns.

::: note Why the mode bit matters
If any program could execute a privileged instruction, a buggy or malicious program could disable interrupts or overwrite another program's memory. The mode bit is the hardware foundation of OS protection, which is why Unit 2 treats the kernel as special.
:::

## 1.2 History and generations of operating systems

| Generation | Years | Hardware | Software style |
|---|---|---|---|
| Zeroth | 1945–55 | vacuum tubes, plugboards | no OS; the programmer operated the machine directly |
| First | 1955–65 | transistors, mainframes | **batch systems**: jobs on punched cards, run one after another by a resident monitor (e.g. IBM FMS) |
| Second | 1965–80 | integrated circuits | **multiprogramming** and **time-sharing**: OS/360, CTSS, MULTICS, early UNIX (1969) |
| Third | 1980–90s | LSI, microprocessors, PCs | single-user PC systems (CP/M, MS-DOS), GUIs (Mac OS, Windows), UNIX workstations |
| Fourth | 1990s–now | cheap multicore, networks, mobile | Windows NT family, Linux (1991), Android, iOS, virtualisation, cloud OS |

The common theme: each step kept the expensive CPU busier. On a first-generation batch machine the CPU idled while an operator mounted tapes. **Multiprogramming** keeps several jobs in memory so that when one waits for I/O, the CPU switches to another. **Time-sharing** adds rapid switching so that many users, each at a terminal, get interactive response.

::: example Why multiprogramming raises CPU utilisation
Suppose each job spends 80 % of its time waiting for I/O. With one job, CPU utilisation is 20 %. With *n* jobs in memory, the probability that all are waiting is 0.8ⁿ, so the utilisation is 1 − 0.8ⁿ. For n = 4 that is 1 − 0.4096 = **59 %**; for n = 10 it is 1 − 0.107 = **89 %**. This is the classic degree-of-multiprogramming model; real systems do slightly worse because jobs are not perfectly independent.
:::

## 1.3 Types of operating systems

| Type | Idea | Example uses |
|---|---|---|
| **Batch** | similar jobs grouped, run without user interaction | payroll runs, bank end-of-day processing |
| **Multiprogramming** | several jobs in memory; CPU switches on I/O wait | most mainframes of the 1970s |
| **Time-sharing (multitasking)** | CPU switched among users every few milliseconds for interactive response | UNIX, Linux, Windows desktops |
| **Multiprocessor / parallel** | two or more CPUs share memory and bus | servers, multicore laptops (SMP) |
| **Real-time** | correct result *within a deadline*; **hard** (missing = failure) and **soft** (missing = degraded quality) | pacemakers, ABS brakes (hard); video streaming (soft); FreeRTOS, VxWorks |
| **Distributed** | many computers appear as one system | clusters, cloud back ends (Unit 9) |
| **Network OS** | machines know about each other; users log in to a specific one | file/print servers on a college LAN |
| **Embedded** | small fixed-function device, limited memory | routers, smart TVs, microwave controllers |
| **Mobile** | touch UI, power management, app sandboxing | Android, iOS |

### Interactive versus batch: what changes?

A batch OS optimises *throughput* (jobs per hour); a time-sharing OS optimises *response time*; a real-time OS optimises *predictability*. These are different objectives and they lead to different schedulers (Unit 3).

::: caution Real-time does not mean fast
A hard real-time system may have a slower average speed than a desktop. What matters is that the *worst-case* response time is guaranteed. A desktop that is "usually fast" but occasionally stalls for a second is unacceptable in an airbag controller.
:::

## 1.4 Functions of an operating system

| Function | What it does | Covered in |
|---|---|---|
| Process management | creates, schedules, synchronises and terminates processes and threads | Unit 3 |
| Deadlock handling | prevents, avoids or detects circular waiting for resources | Unit 4 |
| Memory management | allocates RAM, virtual memory, protection | Unit 5 |
| I/O device management | drivers, buffering, disk scheduling | Unit 6 |
| File management | files, directories, access control | Unit 7 |
| Security and protection | authentication, authorisation, threat defence | Unit 8 |
| Networking and distribution | message passing, RPC | Unit 9 |
| User interface | command-line shell or GUI | Unit 2 |
| Accounting and error handling | usage statistics, recovery from hardware faults | all |

## 1.5 Key hardware ideas an OS relies on

- **Interrupts.** A signal from a device (disk finished, key pressed, timer expired) makes the CPU save its state and jump to an interrupt handler. Without interrupts the OS would have to poll every device continuously.
- **Timer.** A hardware clock that interrupts the CPU periodically. This lets the OS take the CPU back from a program that never gives it up, which is what makes preemptive multitasking possible.
- **Memory protection registers.** Base and limit registers stop one process from addressing another's memory.
- **DMA (direct memory access).** Lets a controller move blocks between a device and RAM without the CPU copying every byte (Unit 6).
- **Bootstrap.** At power-on, firmware (BIOS/UEFI) runs a tiny program that loads the kernel from disk into RAM and jumps to it.

::: example What happens when you press a key
1. The keyboard controller raises an interrupt. 2. The CPU finishes the current instruction, saves the program counter and switches to kernel mode. 3. The interrupt handler reads the scan code and queues it for the keyboard driver. 4. The OS wakes the process waiting for input (for example your text editor). 5. The scheduler eventually runs the editor, which draws the letter. Every step is OS work you never see.
:::

## Formula and fact sheet

- Multiprogramming CPU utilisation with n jobs, each waiting a fraction *p* of the time: **1 − pⁿ**.
- Two roles: **extended machine** (hides hardware) and **resource manager** (shares hardware).
- Two sharing styles: **time** multiplexing and **space** multiplexing.
- Two CPU modes: **user** and **kernel**. System call = controlled entry to kernel mode.
- Generations: tubes → transistors/batch → ICs/multiprogramming/time-sharing → PCs → networked/mobile.

## Chapter summary

- An OS is the privileged layer that manages hardware and offers abstractions (files, processes, address spaces) to applications.
- It acts both as an extended machine and as a resource manager.
- OS history is a history of keeping the CPU busy: batch, multiprogramming, time-sharing, personal computers, distributed and mobile systems.
- Batch, time-sharing, real-time, distributed, network, embedded and mobile OS types differ in their main goal: throughput, response time, deadlines, transparency, or power and footprint.
- Interrupts, a timer, protection registers and the user/kernel mode bit are the hardware that makes an OS possible.

## Practice

1. Define an operating system. Explain its two roles with one example each.
2. Why is the OS called an "extended machine"? Give three abstractions it provides.
3. Distinguish between multiprogramming and time-sharing.
4. A system keeps 5 jobs in memory; each waits for I/O 70 % of the time. Compute CPU utilisation.
5. Differentiate hard and soft real-time systems with an example of each.
6. Why must the OS run in kernel mode while applications run in user mode?
7. List four functions of an operating system and name the hardware support each needs.
8. Explain how a timer interrupt enables preemptive multitasking.

::: note Answers and worked solutions
**1.** An OS is system software that manages hardware and provides an environment for programs. *Resource manager*: it divides 8 GB of RAM among running processes and decides which one gets the CPU. *Extended machine*: it lets a program write `printf` output without knowing the display controller's registers.
**2.** It makes raw hardware look like a simpler, more powerful machine. Abstractions: **file** (instead of disk blocks), **process** (instead of CPU time), **virtual address space** (instead of physical memory); also socket, window.
**3.** *Multiprogramming* keeps several jobs in memory to use the CPU while one waits for I/O; switching happens mainly on I/O waits, so interactive response may be poor. *Time-sharing* extends this by switching on a timer every few milliseconds so that each interactive user sees quick response.
**4.** Utilisation = 1 − pⁿ = 1 − 0.7⁵ = 1 − 0.16807 = **0.832, i.e. 83.2 %**.
**5.** *Hard*: missing a deadline is a failure, e.g. a car airbag controller. *Soft*: a missed deadline only degrades quality, e.g. a dropped video frame during streaming.
**6.** Privileged instructions (I/O, memory-map changes, disabling interrupts) in the hands of any program would let it crash or spy on others. Mode separation confines these instructions to the trusted kernel; applications request them through system calls.
**7.** Process management (timer and interrupts); memory management (base/limit registers or an MMU); I/O management (interrupts and DMA); file management (disk controller); security (mode bit).
**8.** The timer raises an interrupt after a fixed interval. The handler enters the kernel, which can save the running process's state and give the CPU to another process, even if the first never called the OS. Without this, a looping program would hold the CPU forever.
:::
