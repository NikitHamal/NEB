---
subject: Operating Systems
grade: BCA Semester 4
unit: 10
title: Case Study: DOS, Windows, UNIX and Linux
hours: 2
area: BCA 251 · Operating Systems · Unit 10
---

Everything in Units 1 to 9 can be seen at work in real systems. This unit takes four of them, MS-DOS, Windows, UNIX and Linux, and asks the same questions of each: how is it structured, how does it manage processes, memory and files, and what did its design teach us? The Linux commands shown ran on a real Linux 6.1 machine.

::: key What this unit gives you
- MS-DOS: single-tasking, no protection; why it was simple and why it was replaced.
- Windows (NT family): hybrid kernel, processes and threads, NTFS, registry.
- UNIX: design philosophy, process creation, file-system view of everything.
- Linux: kernel structure, process states and the `/proc` file system, file hierarchy, licensing.
:::

## 10.1 MS-DOS

**Microsoft Disk Operating System** (1981, for the IBM PC) is a **single-user, single-tasking, 16-bit** operating system with a **command-line** interface.

| Aspect | MS-DOS design |
|---|---|
| Structure | simple layered structure with *no kernel protection*: programs can access hardware and overwrite the OS directly |
| Components | `IO.SYS` (hardware drivers), `MSDOS.SYS` (kernel, file management), `COMMAND.COM` (shell), `CONFIG.SYS` and `AUTOEXEC.BAT` (start-up files) |
| Processes | one program at a time; **TSRs** (terminate-and-stay-resident) programs give a crude form of background work |
| Memory | real mode: 1 MB address space, of which 640 KB is *conventional memory*; extra memory via EMS/XMS managers |
| File system | **FAT12/FAT16**: 8.3 file names, a file allocation table chaining clusters; no permissions |
| Interface | commands such as `DIR`, `COPY`, `DEL`, `FORMAT`, `CHKDSK`; batch files (`.BAT`); DOS services by software interrupt `INT 21h` |

Strengths: tiny, fast, very easy to understand and write for. Weaknesses: no multitasking, no memory protection (a crash takes down the machine), no real security, a 640 KB barrier. Windows 3.x/9x ran on top of DOS; the Windows NT line removed this dependence. Today the `cmd.exe` prompt keeps DOS-style commands, but the system underneath is NT.

## 10.2 Windows

Modern Windows (NT 3.1 in 1993, then 2000, XP, 7, 10, 11, and the Server editions) is a **32/64-bit, preemptive, multitasking, multiuser** system with a **hybrid kernel**.

### Structure

- **User mode**: environment subsystems (Win32), services, and applications; user-mode drivers.
- **Kernel mode**: the **executive** (object manager, process manager, virtual memory manager, I/O manager, security reference monitor), the **kernel** (scheduling, interrupts) and the **hardware abstraction layer (HAL)** that hides hardware differences. Drivers and many services run in kernel mode, which is the reason for the label *hybrid* rather than pure microkernel (Unit 2).

### Processes, threads and scheduling

A Windows process owns an address space and resources; the *thread* is the unit of scheduling. Windows uses **priority-based, preemptive** scheduling with **32 priority levels** (1 to 15 variable for normal threads, 16 to 31 real-time; 0 is reserved for the system's zero-page thread) and a **round-robin** quantum within a level. The kernel temporarily boosts the priority of a thread that has finished waiting for I/O or is in the foreground window, to improve responsiveness. Objects such as mutexes, semaphores and events (the synchronization of Unit 3) are all kernel objects handled through handles.

### Memory and files

Virtual memory by **demand paging** with a per-process virtual address space of 4 GB (2 GB for the process by default on 32-bit Windows) or far larger on 64-bit, a **page file** on disk and a **working-set** policy per process. The file system is **NTFS**: a master file table (MFT) of records with attributes (small files live inside their MFT record), journaling for crash recovery, per-file **ACLs**, compression and encryption (EFS, BitLocker). Drives are named `C:`, `D:`; paths use `\`. System configuration lives in the **registry**, a hierarchical database of keys and values. Windows also offers **virtualization** (Hyper-V) and the Windows Subsystem for Linux.

## 10.3 UNIX

UNIX began at Bell Labs in 1969 (Ken Thompson, Dennis Ritchie) and was rewritten in **C** by 1973, which made it portable, a first for an OS. Its descendants include BSD, Solaris, AIX, macOS and, in spirit, Linux.

### Design philosophy

- **Everything is a file**: disks, terminals, printers and even processes are read and written through the same `open`, `read`, `write`, `close` calls.
- **Small tools that do one job well**, combined with **pipes**: `cat log | grep error | sort | uniq -c`.
- Text is the universal interface; configuration files are plain text.
- Multiuser and multitasking from the start; a single hierarchical file system.

### Structure

A **monolithic kernel** (Unit 2) with a thin hardware layer below and the system-call interface above; shell, utilities and libraries run in user mode. The kernel contains the process manager and scheduler, memory manager (swapping, later demand paging), file system with **inodes** (Unit 7) and device drivers (character and block).

### Processes

All processes are created by `fork`; `exec` loads a new program. The first process, **init** (PID 1), is the ancestor of all others and adopts orphans; a child that exits before its parent calls `wait` is a **zombie**. Scheduling is a multilevel feedback queue with priorities that decay with CPU usage, so that interactive jobs stay responsive. The shell loop of Unit 2 (read, `fork`, `exec`, `wait`) is the template.

## 10.4 Linux

Linux was started in 1991 by **Linus Torvalds**, a Finnish student, as a free UNIX-like kernel, and combined with the **GNU** tools of the Free Software Foundation to form a complete system. It is released under the **GNU General Public License (GPL)**: anyone may run, study, modify and redistribute it, provided derivative work stays free. A **distribution** (Ubuntu, Debian, Fedora, Red Hat) packages the kernel with tools, a package manager and a desktop.

### Kernel

Linux is a **monolithic kernel with loadable modules** (Unit 2): modules for drivers and file systems can be loaded and unloaded at run time (`lsmod`, `modprobe`). It is preemptive, multiuser, multitasking, supports multiple processors (SMP), demand-paged virtual memory, many file systems (ext4, XFS, Btrfs, FAT, NTFS) and a full network stack. Linux runs on everything from Android phones to all of the world's top supercomputers.

### Processes and threads

Linux treats processes and threads uniformly as **tasks** created by the `clone` system call; flags decide what is shared (address space, files). Threads of one process therefore get separate task IDs but one thread-group ID. Scheduling since kernel 2.6.23 is the **Completely Fair Scheduler (CFS)**, which tracks each task's *virtual runtime* and always runs the task that has received the least, held in a red-black tree: a practical form of the fair-share ideas of Unit 3. (Newer kernels use EEVDF with the same goal.)

Process states appear in the `State` field of every process in the `/proc` pseudo-file system, which exposes kernel data structures as files: R (running or runnable), S (sleeping, interruptible wait), D (uninterruptible disk wait), T (stopped), Z (zombie). Real output on the test machine, for the `grep` process that was reading its own status:

```text
$ grep -E "^(Name|State|Pid|PPid|Threads)" /proc/self/status
Name:	grep
State:	R (running)
Pid:	8181
PPid:	8160
Threads:	1
$ uname -sr
Linux 6.1.158+
$ ulimit -n; ulimit -s
1024
8192
```

This is the PCB of Unit 3 made visible: name, state, process ID, parent ID, thread count. The `ulimit` values are per-process limits: 1,024 open file descriptors and an 8,192 KB stack.

### File-system hierarchy

Linux has one tree starting at `/`; disks are **mounted** into it. The Filesystem Hierarchy Standard places things in standard directories:

```text
$ ls / | head -n 12
bin
boot
code
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
```

| Directory | Contents |
|---|---|
| `/bin`, `/sbin`, `/usr` | commands and programs |
| `/etc` | system configuration (text files) |
| `/home` | users' personal directories |
| `/dev` | device files (`/dev/sda` disk, `/dev/null`) |
| `/proc`, `/sys` | kernel and process information as files |
| `/boot` | kernel image and boot loader files |
| `/tmp`, `/var` | temporary files; logs and spool areas |
| `/mnt`, `/media` | mount points for disks and USB drives |

(The entry `code` above is specific to the test machine; the others are standard.) Permissions, links and `umask` behave as shown in Unit 7. Security: users, groups, `sudo`, SELinux or AppArmor mandatory access control, and a package system that signs software.

## 10.5 Comparison

| Feature | MS-DOS | Windows (NT) | UNIX | Linux |
|---|---|---|---|---|
| Users | single | multi | multi | multi |
| Tasking | single-task | preemptive multitask | preemptive multitask | preemptive multitask |
| Kernel | simple, no protection | hybrid | monolithic | monolithic + modules |
| Native file system | FAT | NTFS | UFS / ZFS and others | ext4 and others |
| Interface | command line | GUI first, PowerShell | shell, X11 GUIs | shell, many desktops |
| Licence | proprietary | proprietary | mixed (BSD open, others proprietary) | GPL, open source |
| Path separator | `\` | `\` | `/` | `/` |
| Typical use | legacy PCs, embedded | desktops, servers | servers, workstations | servers, cloud, Android, supercomputers |

## 10.6 Seeing the ideas: four systems side by side

The four systems of this unit are best understood by looking at what each one shows the user, and then at how each is built inside. The plate begins with real screens and a mascot: a DOS prompt, the Windows NT stop screen that appears when the kernel gives up, a UNIX V5 shell and the Linux penguin. The figures map the DOS memory, the layers of Windows NT, the `fork`, `exec` and `wait` life of a UNIX process (with a real run that captured a zombie), the layers of Linux, and a timeline that shows how the four systems overlap in history.

```photogrid label="10.1" cols="4" ratio="1.0" caption="Four systems, four faces. (a) MS-DOS: a text prompt, one program at a time, no protection. (b) A Windows NT stop screen (INACCESSIBLE_BOOT_DEVICE): in kernel mode a fault cannot be isolated, so the executive stops the whole machine and prints the driver list; compare Unit 2 on why drivers in kernel mode are risky. (c) The UNIX V5 shell on a PDP-11 emulator: the same shell, pipe and file ideas still run on Linux today. (d) Tux, the Linux penguin, here as a large mascot at a Linux Day event in Milan."
@ photo id="bca101/dos" cap="MS-DOS prompt"
fit 1.0
focus 0.3 0.35
call 0.5 0.62 0.04 0.9 "one task"
@ photo id="bca251/bsod" cap="Windows NT stop screen"
fit 1.0
focus 0.3 0.4
call 0.5 0.55 0.04 0.9 "kernel fault"
@ photo id="bca102/unix-v5" cap="UNIX V5 shell"
fit 1.0
focus 0.3 0.4
call 0.5 0.6 0.04 0.9 "a shell"
@ photo id="bca251/tux" cap="Tux, the Linux mascot"
fit 1.0
focus 0.5 0.55
call 0.5 0.9 0.04 0.9 "Linux"
```

```svgfig label="10.1" caption="The memory of MS-DOS to scale (1 KB = 0.2 px). The 8086 has 20 address lines, so it can reach 2^20 = 1,048,576 bytes = 1,024 KB. The lowest 640 KB is conventional memory, where DOS and your program live. The next 128 KB is reserved for video memory and the last 256 KB for adapter ROMs and the BIOS, so a program can never use them. The 64 KB just above 1 MB is the high memory area (HMA), reached by a trick on later CPUs; more memory above that is extended memory (XMS) through a driver such as HIMEM.SYS. Inside the 640 KB (right, not to scale) the first kilobyte holds the interrupt vector table."
f = Fig(580, 262)
f.text(30, 12, "1 MB real-mode address space", size=10.5, color=NAVY, bold=True, anchor="start")
def Y(kb): return 245 - 0.2 * kb
f.box(30, Y(1024), 90, Y(768) - Y(1024), "ROM + BIOS", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.box(30, Y(768), 90, Y(640) - Y(768), "video", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(30, Y(640), 90, Y(0) - Y(640), "conventional\n640 KB", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(30, Y(1024) - 11, 90, 11, "", fill=BLUE, stroke=NAVY)
f.text(135, Y(1024) - 4, "HMA 64 KB (above 1 MB)", size=9.5, color=NAVY, bold=True, anchor="start")
f.text(135, Y(896) + 4, "256 KB: ROMs and BIOS  (C0000 to FFFFF)", size=9.5, color=SLATE, anchor="start")
f.text(135, Y(704) + 4, "128 KB: video  (A0000 to BFFFF)", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(135, Y(320) + 4, "640 KB: DOS and programs  (00000 to 9FFFF)", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(22, Y(0) + 4, "0", size=9, color=SLATE, anchor="end")
f.text(22, Y(640) + 4, "640", size=9, color=SLATE, anchor="end")
f.text(22, Y(1024) + 4, "1 MB", size=9, color=SLATE, anchor="end")
names = ["interrupt vector table (1 KB)", "BIOS data area", "IO.SYS + MSDOS.SYS (kernel)", "COMMAND.COM (resident part)", "TSR programs", "your program: all that is left"]
fills = [SAND, SOFT, BLUE, BLUE, SAND, MINT]
for i, (nm, fl) in enumerate(zip(names, fills)):
    f.box(372, 130 + i * 20, 196, 19, nm, fill=fl, stroke=SLATE, size=9, bold=(i == 5))
f.arrow([(120, 222), (368, 222)], color=TEAL, sw=1.2, dash=True)
f.text(470, 122, "inside conventional memory", size=9.5, color=NAVY, bold=True)
f.text(135, 258, "B800:0000 = B800 x 16 + 0 = B8000 = 753,664 (text screen)", size=9, color=RED, bold=True, anchor="start")
f.text(470, 28, "no protection:", size=10, color=RED, bold=True)
f.text(470, 44, "any program can write", size=9.5, color=RED)
f.text(470, 58, "over DOS or the video", size=9.5, color=RED)
f.text(470, 72, "memory or the vectors", size=9.5, color=RED)
```

```svgfig label="10.2" caption="Layers of Windows NT. In user mode the applications, the Win32 subsystem and services run with limited rights and cannot touch the hardware. A call into ntdll.dll switches to kernel mode, where the executive (object manager, process manager, virtual memory manager, I/O manager, security reference monitor), the kernel and the drivers run together, and the hardware abstraction layer (HAL) hides the machine below them. Because the drivers and executive share one address space with full rights (as the stop screen in Plate 10.1 shows), the design is called hybrid rather than a pure microkernel."
f = Fig(580, 270)
f.box(8, 6, 564, 82, "", fill="#f8fafc", stroke=SLATE)
f.text(40, 20, "USER MODE", size=10, color=TEAL, bold=True)
for i, nm in enumerate(["applications\n(Notepad, browser)", "Win32 subsystem\n(window and console)", "services\n(spooler, updates)", "security\n(logon, lsass)"]):
    f.box(20 + i * 139, 30, 128, 46, nm, fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.line(8, 96, 572, 96, color=RED, sw=1.6, dash=True)
f.text(290, 107, "system call through ntdll.dll: user mode to kernel mode", size=9.5, color=RED, bold=True)
f.box(8, 114, 564, 120, "", fill="#f8fafc", stroke=SLATE)
f.text(60, 127, "KERNEL MODE", size=10, color=NAVY, bold=True)
f.text(330, 127, "executive", size=10, color=NAVY, bold=True)
for i, nm in enumerate(["object\nmanager", "process\nmanager", "virtual\nmemory", "I/O\nmanager", "security\nmonitor"]):
    f.box(16 + i * 111, 134, 103, 34, nm, fill=BLUE, stroke=NAVY, size=9, bold=True)
f.box(16, 174, 270, 26, "kernel: scheduler (32 priorities), interrupts", fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(294, 174, 270, 26, "device drivers and file systems (NTFS)", fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(16, 206, 548, 22, "hardware abstraction layer (HAL)", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.box(8, 242, 564, 22, "hardware: CPU, memory, disks, network card", fill="#e2e8f0", stroke=SLATE, size=10, bold=True)
```

```svgfig label="10.3" caption="The life of a UNIX process, with a real run. The parent (PID 2348) calls fork and gets a child (PID 2349). The child exits with status 7 at once, but its entry stays in the process table as a zombie (state Z) until the parent calls wait. The real ps output captured while the parent slept shows STAT Z for the child; after waitpid the entry is gone and the parent read exit status 7. In a shell, the child would call exec between fork and exit to become a new program."
f = Fig(580, 262)
f.text(8, 64, "parent 2348", size=10, color=NAVY, bold=True, anchor="start")
f.line(90, 60, 560, 60, color=NAVY, sw=3)
f.text(8, 164, "child 2349", size=10, color=AMBER, bold=True, anchor="start")
f.box(112, 36, 56, 20, "fork()", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(140, 62), (140, 154)], color=TEAL, sw=1.8)
f.line(140, 160, 300, 160, color=AMBER, sw=3)
f.text(220, 148, "runs, then exit(7)", size=9.5, color=AMBER, bold=True)
f.line(300, 160, 430, 160, color=RED, sw=3, dash=True)
f.text(365, 148, "ZOMBIE (state Z)", size=9.5, color=RED, bold=True)
f.text(365, 178, "no code, no memory;", size=9, color=RED)
f.text(365, 191, "only the table entry", size=9, color=RED)
f.text(220, 48, "sleep(1)", size=9.5, color=SLATE, bold=True)
f.box(404, 36, 52, 20, "wait()", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(430, 156), (430, 66)], color=TEAL, sw=1.8, dash=True)
f.text(500, 90, "status 7 collected", size=9.5, color=TEAL, bold=True)
f.text(500, 104, "child entry removed", size=9.5, color=TEAL, bold=True)
f.text(8, 222, "real ps output while the parent sleeps:   PID 2349  PPID 2348  STAT Z   z", size=9.5, color=NAVY, bold=True, anchor="start")
f.text(8, 238, "after waitpid:   only PID 2348 (STAT S) remains;   parent printed: exit status 7", size=9.5, color=NAVY, bold=True, anchor="start")
f.text(8, 254, "orphans are adopted by init (PID 1), which always calls wait, so they never stay zombies", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="10.4" caption="The layers of Linux. Applications and the shell call the C library, which uses the system-call interface to enter the kernel. Inside the monolithic kernel the main subsystems (scheduler, memory manager, virtual file system with ext4, network stack, device drivers) share one address space; drivers and file systems may be loadable modules added with modprobe and listed with lsmod. Below the kernel is the hardware. The /proc directory shows the kernel's tables as files, which is how the State line in Unit 10.4 was read."
f = Fig(580, 250)
f.box(8, 6, 372, 30, "applications: browser, python, gcc, database", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(8, 42, 372, 30, "shell and GNU tools: bash, ls, grep, sort", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(8, 78, 372, 26, "C library (glibc): open, read, fork, clone", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.line(8, 114, 380, 114, color=RED, sw=1.6, dash=True)
f.text(194, 126, "system-call interface: user mode to kernel mode", size=9.5, color=RED, bold=True)
f.box(8, 134, 372, 84, "", fill="#f8fafc", stroke=SLATE)
for i, nm in enumerate(["scheduler\n(CFS)", "memory\nmanager", "VFS +\next4", "network\nstack"]):
    f.box(16 + i * 90, 142, 82, 38, nm, fill=BLUE, stroke=NAVY, size=9, bold=True)
f.box(16, 186, 356, 26, "device drivers and loadable modules", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(8, 226, 372, 22, "hardware", fill="#e2e8f0", stroke=SLATE, size=10, bold=True)
f.box(404, 6, 168, 70, "/proc and /sys\nthe kernel's tables\nshown as files", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.box(404, 90, 168, 70, "tasks by clone()\nthreads and processes\nshare one structure", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.box(404, 174, 168, 70, "GPL licence\nsource open to all;\ndistribution = kernel + tools", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
```

```svgfig label="10.5" caption="How the four systems overlap in time (1 year = 7.5 px). UNIX (1969) is the oldest and its ideas continue in BSD, Solaris, macOS and Linux. MS-DOS (1981) was the base of the Windows 1.0 to Windows Me line, which ended in 2000. Windows NT (1993) is a separate design that is still the basis of Windows 10 and 11. Linux (1991) copies the UNIX interface, not the UNIX code. Milestones: 1973 UNIX rewritten in C; 1985 Windows 1.0; 1995 Windows 95."
f = Fig(580, 230)
def X(y): return 110 + (y - 1965) * 7.5
f.line(110, 196, 560, 196, color=SLATE, sw=1.4)
for yr in range(1970, 2030, 10):
    f.line(X(yr), 192, X(yr), 200, color=SLATE, sw=1.4)
    f.text(X(yr), 213, str(yr), size=9.5, color=SLATE, bold=True)
rows = [("UNIX", 1969, 2025, BLUE, NAVY, "UNIX 1969 ... BSD, Solaris, AIX, macOS"),
        ("MS-DOS", 1981, 2000, SAND, AMBER, "MS-DOS 1981-2000"),
        ("Windows on DOS", 1985, 2000, SAND, AMBER, "Windows 1.0 to Me"),
        ("Linux", 1991, 2025, MINT, TEAL, "Linux 1991 ... servers, Android, cloud"),
        ("Windows NT", 1993, 2025, BLUE, NAVY, "NT 1993 ... 2000, XP, 7, 10, 11")]
for i, (nm, a, b, fl, st, lab) in enumerate(rows):
    y = 14 + i * 33
    f.text(8, y + 15, nm, size=9.5, color=NAVY, bold=True, anchor="start")
    f.box(X(a), y, X(b) - X(a), 24, lab, fill=fl, stroke=st, size=9.5, bold=True)
f.line(X(1973), 10, X(1973), 190, color=RED, sw=1, dash=True)
f.text(X(1973), 6, "1973 C", size=9, color=RED, bold=True)
f.line(X(1995), 10, X(1995), 190, color=RED, sw=1, dash=True)
f.text(X(1995), 6, "1995", size=9, color=RED, bold=True)
```

### 10.6.1 Eight reasons why Linux is widely used

1. **No licence fee.** Linux and most of its software are free of charge, so a college or a small company can run many servers without paying for each copy. This matters in Nepal, where budgets for software are small. The money saved can be spent on hardware or training instead.
2. **Open source code.** Anyone can read, check and change the source under the GPL. A university can study how a scheduler or file system works, which is why Linux is the standard teaching system for operating systems. Security researchers can also find and fix errors in public.
3. **Stability and uptime.** A Linux server often runs for months without a restart, because a fault in one user program does not bring the kernel down. System updates usually do not need a reboot of the whole machine. This is why many web hosts and data centres choose it.
4. **Strong security model.** Linux has users, groups, permission bits, `sudo` and optional SELinux or AppArmor controls. Programs run with the least rights they need, so a damaged program cannot easily change the system files. Software is installed from signed repositories instead of random websites.
5. **Runs on almost any hardware.** The same kernel runs on a Raspberry Pi, an old college PC, a phone, a cloud server and a supercomputer. Old computers in a school lab can be given a light desktop and used again. Android, the most common phone system, is built on the Linux kernel.
6. **Modular and customisable.** Loadable modules let a driver or file system be added without rebuilding the kernel, and distributions such as Ubuntu or Debian choose their own tools and desktop. An organisation can build a small system for one task, such as a router or a kiosk. The user is not forced to accept one design.
7. **Powerful command line and automation.** Small tools joined by pipes, such as `sort | uniq -c`, and shell scripts let a system administrator repeat a job on many machines. A backup of a college server can be scheduled with a few lines. This saves time and avoids mistakes of manual work.
8. **Large community support.** Thousands of volunteers and companies write the code, test it and answer questions in forums and mailing lists. A student who meets an error message usually finds an answer online within minutes. The cost of this support is mostly the time to read and learn, and the weakness is that no single company is responsible for every problem.

## Formula and fact sheet

- DOS: single-user, single-task, FAT, real mode, 640 KB, no protection.
- Windows NT: hybrid kernel, HAL, 32 priority levels, NTFS, registry.
- UNIX: written in C, everything is a file, pipes, `fork`/`exec`, inodes.
- Linux: GPL, monolithic kernel with modules, tasks via `clone`, CFS scheduler, `/proc`.

## Chapter summary

- MS-DOS shows what a minimal OS looks like and why protection and multitasking were needed.
- Windows NT adds a layered hybrid design, preemptive priority scheduling, NTFS and a security model with ACLs.
- UNIX contributed portability, a unified file abstraction and small cooperating tools.
- Linux combines the UNIX design with open-source development, loadable modules and a fair scheduler.

## Practice

1. List four limitations of MS-DOS.
2. What is the role of the HAL in Windows? Why is the Windows kernel called hybrid?
3. Describe how Windows schedules threads.
4. Explain "everything is a file" with three examples.
5. How does UNIX create a new process? What are init and a zombie?
6. What is a loadable kernel module and what is its advantage?
7. What is the GPL? How does a Linux distribution differ from the Linux kernel?
8. Name five directories of the Linux hierarchy and their purpose.
9. Compare DOS, Windows and Linux on multitasking, security and file system.
10. What does the `State` line in `/proc/<pid>/status` tell you? Which letter means a zombie?

::: note Answers and worked solutions
**1.** Single-tasking; no memory protection; 640 KB conventional memory limit; no multi-user security or permissions; 8.3 filenames; command-line only.
**2.** The HAL hides hardware differences (interrupt controllers, buses) from the kernel, so one kernel runs on many machines. It is hybrid because it has a microkernel-like structure of separate components, but many (drivers, graphics, file system) run in kernel mode for speed.
**3.** Preemptive, priority-based scheduling over 32 levels; threads of equal priority share the CPU in round-robin quanta; priorities of waiting or foreground threads are temporarily boosted.
**4.** A disk partition appears as `/dev/sda1`; the terminal as `/dev/tty`; a process's information as `/proc/<pid>/status`. All are accessed with `open`, `read`, `write`.
**5.** `fork` copies the calling process; the child normally calls `exec` to load a new program. `init` (PID 1) is the root of the process tree and adopts orphans. A zombie is a finished process whose exit status has not yet been collected by its parent.
**6.** A piece of kernel code (such as a driver) loaded into or removed from the running kernel without rebooting. It keeps the kernel small, and allows hardware support to be added on demand.
**7.** The GNU General Public License lets anyone use, modify and distribute the software, requiring that derivative works remain under the same licence. The kernel alone is not a usable system; a distribution adds the GNU tools, libraries, package manager, installer and desktop.
**8.** `/bin` (essential commands), `/etc` (configuration), `/home` (user files), `/dev` (devices), `/proc` (process and kernel information), `/var` (logs, spool).
**9.** DOS: single task, no security, FAT. Windows NT: preemptive multitasking, ACL-based security, NTFS. Linux: preemptive multitasking, permission bits plus ACLs and SELinux, ext4 and others.
**10.** It shows the process's scheduling state: R running/runnable, S sleeping, D uninterruptible sleep, T stopped, **Z zombie**.
:::

## Model answers (5 and 10 marks)

**Q1. Describe MS-DOS: its structure, memory organisation and limitations. (5 marks)**

**MS-DOS** (Microsoft Disk Operating System, 1981, for the IBM PC) is a **single-user, single-tasking, 16-bit** system with a **command-line** interface. It is a simple layered design with no kernel protection.

**Structure.** `IO.SYS` holds the hardware drivers, `MSDOS.SYS` is the kernel that manages files and programs, and `COMMAND.COM` is the shell that reads commands such as `DIR`, `COPY` and `FORMAT`. `CONFIG.SYS` and `AUTOEXEC.BAT` set up the machine at start-up. Programs request services with the software interrupt `INT 21h`.

**Memory (Fig. 10.1).** DOS runs in real mode. The 8086 has 20 address lines, so the address space is 2^20 = 1 MB, and the top 384 KB is reserved for video memory and ROM. That leaves **640 KB of conventional memory** for DOS and the program. Extra memory is reached with managers such as `HIMEM.SYS` (XMS) or EMS.

**Files.** The file system is **FAT12/FAT16** with 8.3 file names; a file allocation table chains the clusters, and there are no permissions.

**Limitations.**

- Only one program runs at a time; **TSR** programs are a crude workaround.
- There is no memory protection, so one faulty program can crash the machine or overwrite DOS.
- There is no user security.
- The 640 KB barrier limits large programs.

DOS is still useful for teaching what a minimal operating system needs. Its limits are the reasons for protection, multitasking and virtual memory.

**Q2. Explain the UNIX design philosophy: "everything is a file" and pipes. (5 marks)**

UNIX began at Bell Labs in 1969 (Ken Thompson and Dennis Ritchie) and was rewritten in **C** by 1973, so it became the first portable operating system. Its design rests on a few ideas.

**Everything is a file.** Disks, terminals, printers and even process information are reached with the same calls: `open`, `read`, `write` and `close`. For example, a disk partition is `/dev/sda1`, the terminal is `/dev/tty`, and the state of a process is the file `/proc/<pid>/status`. A programmer learns one interface, and a program written for files can also work on devices.

**Small tools, joined by pipes.** Each tool does one job well, and the `|` operator connects the output of one program to the input of the next. A real run on the test machine:

```text
$ printf 'b\na\nc\na\nb\nb\n' | sort | uniq -c | sort -rn
      3 b
      2 a
      1 c
```

`sort` groups equal lines, `uniq -c` counts them, and `sort -rn` puts the biggest count first.

**Text as the common format.** Configuration files and tool output are plain text, so they can be read, searched and edited with the same tools.

**Multiuser and multitasking.** Many users and processes share one file tree; new processes are made by `fork` and `exec` (Fig. 10.3).

These ideas are the reason UNIX, and Linux after it, are still used on servers and phones.

**Q3. Explain the architecture of Windows NT. How does it manage processes, memory and files? (10 marks)**

**Introduction.** Windows NT (first released as NT 3.1 in 1993) is the base of Windows 2000, XP, 7, 10, 11 and the server editions. It is a 32/64-bit, preemptive, multitasking, multiuser system with a **hybrid kernel**, which means it has a layered, microkernel-like structure but runs most services in kernel mode for speed.

**Architecture (Fig. 10.2).** The system has two modes.

- **User mode:** applications, the Win32 subsystem, services (print spooler, updates) and the security logon process. They have limited rights and cannot touch hardware.
- **Kernel mode:** the **executive** with the object manager, process manager, virtual memory manager, I/O manager and security reference monitor; the **kernel** that schedules threads and handles interrupts; the device drivers; and the **hardware abstraction layer (HAL)**, which hides hardware differences so one kernel runs on many machines.

A system call goes through `ntdll.dll` to switch from user to kernel mode.

**Six points of management.**

1. **Processes and threads:** a process owns an address space and resources; the *thread* is the unit of scheduling.
2. **Scheduling:** priority-based and preemptive with **32 levels** (1 to 15 normal, 16 to 31 real-time) and round-robin quanta within one level. A thread that has just finished I/O gets a temporary boost.
3. **Virtual memory:** demand paging, a per-process virtual address space, a page file on disk and a working-set policy for each process.
4. **File system:** **NTFS** keeps a master file table, journals changes for crash recovery, and gives every file an access-control list (ACL).
5. **Security:** logon, access tokens and ACLs checked by the security reference monitor.
6. **Registry:** a central database of configuration settings.

| Feature | MS-DOS | Windows NT |
|---|---|---|
| Kernel | none, no protection | hybrid with protected kernel mode |
| Multitasking | none | preemptive, 32 priorities |
| Memory | 640 KB real mode | virtual memory, paging |
| File system | FAT | NTFS, journaled, ACLs |
| Users | one | many, with security |

**Weakness.** Because drivers run in kernel mode, a faulty driver can crash the whole machine and show a stop screen (Plate 10.1b).

**Conclusion.** Windows NT adds protection, preemptive scheduling, virtual memory and a security model to the simple ideas of DOS. The price of the hybrid design is that a bad driver can stop the system, while its gain is speed and a rich set of services.

**Q4. Explain Linux: its history and licence, kernel structure, process management and file-system hierarchy. (10 marks)**

**Introduction.** Linux was started in 1991 by **Linus Torvalds**, a Finnish student, as a free UNIX-like kernel. Combined with the GNU tools it forms a complete system. It is released under the **GNU General Public License (GPL)**, which lets anyone use, change and share it as long as derived work stays under the same licence. A **distribution** (Ubuntu, Debian, Fedora) adds the installer, package manager, libraries and desktop to the kernel.

**Kernel structure (Fig. 10.4).** Linux has a **monolithic kernel with loadable modules**. The scheduler, memory manager, virtual file system, network stack and drivers share one address space for speed, while drivers and file systems can be loaded or removed at run time with `modprobe`, without rebooting. The kernel is preemptive, multiuser, multitasking and supports several processors.

**Process management.**

- Processes and threads are both **tasks**, created by the `clone` system call; flags decide what is shared. Threads of one process get separate task IDs but one thread-group ID.
- The scheduler is the **Completely Fair Scheduler (CFS)**, which tries to give each runnable task a fair share of CPU time.
- Every process has a state, shown in `/proc/<pid>/status`: R running, S sleeping, D uninterruptible wait, T stopped, **Z zombie**.
- A real run (Fig. 10.3) showed a finished child in state Z until the parent called `wait`. Orphans are adopted by `init` (PID 1).

**File-system hierarchy.** There is one tree from `/`, and disks are mounted into it. The standard places are `/bin` and `/usr` (programs), `/etc` (configuration), `/home` (users), `/dev` (devices), `/proc` and `/sys` (kernel data as files), `/boot` (kernel image), `/var` and `/tmp` (logs and temporary files) and `/mnt` (mount points). The default file system is **ext4**, with permission bits and optional ACLs.

| Point | Windows NT | Linux |
|---|---|---|
| Source | closed | open (GPL) |
| Kernel | hybrid | monolithic with modules |
| Paths | `C:\Users` | `/home` |
| File system | NTFS | ext4 and others |
| Cost | licence fee | free |

**Conclusion.** Linux joins the UNIX design with open-source development. Its modules keep the kernel flexible, its scheduler is fair and its everything-is-a-file view makes the system easy to inspect.

**Q5. Compare MS-DOS, Windows, UNIX and Linux. (5 marks)**

The four systems differ most in tasking, protection and openness. DOS is the oldest and simplest, while Windows NT, UNIX and Linux are modern, protected, multitasking systems.

| Feature | MS-DOS | Windows (NT) | UNIX | Linux |
|---|---|---|---|---|
| Year | 1981 | 1993 | 1969 | 1991 |
| Users | single | multi | multi | multi |
| Tasking | single-task | preemptive | preemptive | preemptive |
| Kernel | simple, no protection | hybrid | monolithic | monolithic + modules |
| File system | FAT | NTFS | UFS and others | ext4 and others |
| Interface | command line | GUI, PowerShell | shell, X11 | shell, many desktops |
| Licence | proprietary | proprietary | mixed | GPL |

**Explanation.** DOS runs one program at a time and has no protection, so it was replaced for general use. Windows NT adds a protected kernel, 32-level priority scheduling, NTFS and ACLs. UNIX introduced portability through C, everything is a file, and pipes. Linux copies the UNIX interface in new code, adds loadable modules, and is free under the GPL. For servers and the cloud, Linux is the usual choice; for desktops and office software, Windows is the most common. A student choosing a system should ask three questions: how many users and tasks it must support, how much protection it needs, and whether the source code must be open. DOS fails the first two, which explains why it survives only in teaching and in a few old embedded machines.
