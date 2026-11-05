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
