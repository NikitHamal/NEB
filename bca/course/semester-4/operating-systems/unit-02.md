---
subject: Operating Systems
grade: BCA Semester 4
unit: 2
title: Operating System Structure
hours: 2
area: BCA 251 · Operating Systems · Unit 2
---

A kernel with ten million lines of code cannot be a heap of functions calling each other at will. How the parts are arranged decides whether the system is fast, safe, and possible to maintain. This unit surveys the main designs: monolithic, layered, microkernel, exokernel, client-server and virtual machines, and the shell through which users meet the OS.

::: key What this unit gives you
- The layered approach and its limits.
- The kernel and its types: monolithic (macro), micro and exo-kernel.
- The client-server model, virtual machines and hypervisors.
- The shell: command interpreter and GUI; system calls as the interface.
:::

## 2.1 System components and system calls

The OS offers services to programs through **system calls**, entry points into the kernel. In C you usually call library wrappers (`read`, `write`, `fork`) which put the call number in a register and execute a trap instruction. The kernel runs the service and returns to user mode.

| Category | POSIX examples | Windows examples |
|---|---|---|
| Process control | `fork`, `exec`, `exit`, `wait` | `CreateProcess`, `ExitProcess` |
| File management | `open`, `read`, `write`, `close` | `CreateFile`, `ReadFile` |
| Device management | `ioctl`, `read`, `write` | `DeviceIoControl` |
| Information | `getpid`, `time` | `GetCurrentProcessId` |
| Communication | `pipe`, `socket`, `shmget` | `CreatePipe`, `WSASocket` |

Most programmers use an **API** (POSIX, Win32) rather than raw system calls, which keeps source code portable between kernels.

::: example The journey of one printf
`printf("Hi\n")` is a C library function that formats text into a buffer. When the buffer is flushed the library calls `write(1, buffer, 3)`. This executes a trap; the kernel checks that descriptor 1 is open, copies the bytes to the terminal driver and returns the count (3). Only the last step is the kernel's.
:::

## 2.2 Monolithic and layered structure

### Simple (monolithic) structure

In a **monolithic kernel** the whole OS is one large program running in kernel mode. Any procedure may call any other. Linux, traditional UNIX and, in practice, much of Windows are of this kind.

- **Advantage:** very fast. A call between components is an ordinary function call, with no message passing and no mode switch.
- **Disadvantage:** a bug in any driver can crash the whole system; the code is hard to understand and verify.

Linux softens the problem with **loadable kernel modules**: drivers and file systems can be inserted into the running kernel and removed again, so the kernel stays modular in source and deployment while still monolithic in memory.

### Layered system

The OS is divided into layers, each built on the one below. Layer 0 is hardware, the top layer is the user interface. A layer uses only the services of lower layers.

| Layer | Function (THE system, Dijkstra 1968) |
|---|---|
| 5 | the operator / user programs |
| 4 | user programs and buffering of I/O |
| 3 | operator-console device driver |
| 2 | memory management (segment controller) |
| 1 | CPU scheduling and semaphores |
| 0 | hardware |

**Strength:** each layer can be debugged on its own, assuming lower layers are correct, so verification is easy. **Weakness:** careful ordering is needed (does the disk driver sit below or above memory management? the swap area needs both) and every request passes through many layers, which costs time. Modern kernels use layering loosely, with fewer and wider layers.

## 2.3 The kernel and its types

The **kernel** is the part of the OS that always resides in memory and runs in privileged mode. Designs differ in how much functionality is placed inside it.

### Monolithic (macro) kernel

All services (scheduling, memory, file systems, device drivers, networking) run in kernel space. Examples: Linux, FreeBSD, classic UNIX, MS-DOS (no protection at all).

### Microkernel

Only the minimum stays in the kernel: low-level address spaces, thread scheduling and **inter-process communication (IPC)**. File systems, device drivers and networking run as ordinary user-mode **servers** that exchange messages.

| Aspect | Monolithic | Microkernel |
|---|---|---|
| Kernel size | large | small (tens of thousands of lines) |
| Speed | fast (function calls) | slower (message passing, extra mode switches) |
| Reliability | one faulty driver can crash the system | a crashed driver is restarted like any process |
| Extensibility | recompile or load module | add a server |
| Examples | Linux, Unix | MINIX 3, QNX, L4, Mach (basis of macOS XNU, partly) |

::: note Hybrid kernels
Windows NT and macOS (XNU) are called **hybrid**: microkernel-inspired structure, but many services, such as the graphics and file system code, run in kernel mode for speed. The labels are a spectrum, not a strict classification.
:::

### Exokernel

An **exokernel** (MIT, 1990s) goes further: the kernel only *securely multiplexes* raw hardware (hands out disk blocks, physical pages, time slices) and checks ownership. Abstractions such as files or virtual memory are implemented by **library operating systems** linked into each application. Applications therefore choose their own abstractions, which can bring large speed-ups. It remains largely a research design.

## 2.4 Client-server model

A variant of the microkernel idea: processes are either **clients** that request a service, or **servers** that provide it. The kernel's only job is to carry messages between them.

1. A user process (client) sends a message "read file X" to the file server.
2. The file server may contact the disk driver server.
3. The reply returns to the client.

The model suits distributed systems because it does not matter whether the server is on the same computer or across a network (Unit 9). The overhead of message passing is the price.

## 2.5 Virtual machines

A **virtual machine (VM)** makes one physical computer behave as several complete computers. A layer of software, the **hypervisor** or **virtual machine monitor (VMM)**, multiplexes the real hardware among **guest** operating systems, each of which believes it owns the machine.

| Type | Where the hypervisor runs | Examples |
|---|---|---|
| **Type 1** (bare metal) | directly on hardware | Xen, VMware ESXi, Microsoft Hyper-V, KVM |
| **Type 2** (hosted) | as an application on a host OS | VirtualBox, VMware Workstation |

Uses: running Windows and Linux side by side, safe testing of malware or new kernels, **server consolidation** (ten lightly loaded servers on one machine) and cloud computing. A **Java Virtual Machine** is a different kind of VM: it virtualises a *language runtime* (bytecode), not hardware. **Containers** (Docker) share the host kernel and isolate processes with namespaces, which makes them lighter than full VMs but less strongly isolated.

::: example Server consolidation, with numbers
A Nepali ISP runs 12 physical servers each averaging 8 % CPU load. One 16-core machine hosting 12 VMs of 1 core each, at about 8 % load, would use roughly 12 × 0.08 = 0.96 cores of real work, leaving ample headroom. Eleven machines' hardware, power and cooling bills disappear, at the cost of the hypervisor's overhead (typically a few per cent).
:::

## 2.6 The shell

The **shell** is the program through which users give commands to the OS. It is *not* part of the kernel; it is an ordinary user process that reads commands and makes system calls.

| Kind | Examples | Features |
|---|---|---|
| Command-line interpreter (CLI) | `bash`, `zsh`, PowerShell, `cmd.exe` | commands, pipes, scripting, history |
| Graphical shell (GUI) | Windows Explorer, GNOME, macOS Finder | icons, windows, mouse |

A command-line shell works in a loop: print the prompt, read a line, parse it into a program name and arguments, `fork` a child, `exec` the program in the child, `wait` for it to finish, repeat. Pipes (`ls | wc -l`) connect one program's output to the next one's input. This simple design is why one can replace the shell without touching the kernel.

## Formula and fact sheet

- Monolithic: one kernel-mode program, fast, fragile. Micro: minimal kernel + user-mode servers, safer, slower. Exo: kernel only multiplexes hardware.
- Layered: layer *n* uses only layers below; easy to verify, slow, hard to order.
- Hypervisor Type 1 = on hardware; Type 2 = on a host OS.
- Shell = user-mode program using `fork`, `exec`, `wait`.

## Chapter summary

- System calls are the controlled entry into the kernel; most programs use APIs built on them.
- Monolithic kernels trade safety for speed; layered designs make verification easy; microkernels move services to user space for reliability; exokernels expose raw hardware.
- The client-server model and VMs extend the same idea of separating services from each other.
- The shell is only a program; the kernel is what makes it possible.

## Practice

1. What is a system call? Explain how it differs from an ordinary function call.
2. Compare monolithic and micro kernels with respect to speed and reliability.
3. Why did layered design not become dominant in practice?
4. What is a hypervisor? Distinguish Type 1 and Type 2 with an example each.
5. Explain the client-server model of an operating system.
6. Is the shell part of the kernel? Justify.
7. A microkernel system needs 4 message exchanges, each costing 3 µs, for an operation that costs 1 µs as a function call in a monolithic kernel. Compute the overhead factor.
8. What is an exokernel and how is it different from a microkernel?

::: note Answers and worked solutions
**1.** A system call is a request to the kernel for a privileged service, made with a trap instruction that switches the CPU to kernel mode and jumps to a fixed kernel entry point. An ordinary function call stays in user mode, jumps to any address in the program and cannot touch privileged resources.
**2.** Monolithic: all services in one address space, calls are cheap so performance is good, but a driver bug can crash everything. Microkernel: services are user-mode servers so a failure is contained and restartable, but each service request involves messages and mode switches, which cost time.
**3.** Every request crosses many layers (overhead); it is hard to decide strict ordering when components need each other (swapping vs. file system); and performance-critical code wants to bypass layers. Real kernels are only loosely layered.
**4.** A hypervisor is software that creates and runs virtual machines. Type 1 runs directly on hardware (Xen, ESXi, KVM, Hyper-V). Type 2 runs as an application on a host OS (VirtualBox, VMware Workstation).
**5.** The OS is a collection of server processes (file server, memory server, ...) and client processes. Clients send request messages through the kernel to servers and receive replies. The same pattern works across a network.
**6.** No. The shell is an ordinary user-mode program that reads commands and uses system calls (`fork`, `exec`, `wait`). Different shells (bash, zsh) run on the same kernel, and a crash of the shell does not crash the kernel.
**7.** Microkernel cost = 4 × 3 = 12 µs against 1 µs, an overhead factor of **12×** for that single operation. (Real systems reduce this with fast IPC paths and by batching.)
**8.** An exokernel only allocates and protects raw hardware resources (blocks, pages, time slices) and lets applications build their own abstractions through library OSes. A microkernel still defines abstractions (processes, address spaces, IPC) but runs most services as user servers.
:::
