---
file: NEBians-IOE-Past-Paper-Operating-System-ENCT254-2083-Baishakh.pdf
subject: Operating System
level: BE · Year II / Part II
code: ENCT254
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Difference between UEFI and Legacy Boot. How does an operating system act as an intermediary between user applications and hardware components? Explain. [[2+4]]

@q 2
Explain different components of process control block. For given process, draw a Gantt Chart and calculate average waiting time for: Shortest Job First (SJF) and Round Robin (with Quantum Time = 4). Their arrival time, service time in milliseconds. [[3+5]]

| Process | Arrival Time | Burst Time |
|---|---|---|
| P1 | 0 | 10 |
| P2 | 2 | 5 |
| P3 | 4 | 2 |
| P4 | 4 | 5 |
| P5 | 0 | 8 |

@q 3
(a) Define Critical Region and Mutex. Explain how producer-consumer problem can be solved using semaphore with its respective pseudo-code implementations. [[2+5]]

(b) Under what condition does the solution to the Dinning philosopher using semaphore leads to a deadlock conditions? Consider a system with 5 processes (p0,p1,p2,p3,p4) and 4 resource types (R0,R1,R2,R3). The number of instances of each resource type in the systems are: 6,4,4,2 respectively. Allocation table and Maximum claim table are shown below. Is the state safe? If so, show the safe execution of the processes. [[2+6]]

| Allocation | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| P0 | 2 | 0 | 1 | 1 |
| P1 | 1 | 1 | 0 | 0 |
| P2 | 1 | 1 | 0 | 0 |
| P3 | 1 | 0 | 1 | 0 |
| P4 | 0 | 1 | 0 | 1 |

| Maximum Need | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| P0 | 3 | 2 | 1 | 1 |
| P1 | 1 | 2 | 0 | 2 |
| P2 | 1 | 1 | 2 | 0 |
| P3 | 3 | 2 | 1 | 0 |
| P4 | 2 | 1 | 0 | 1 |

@q 4
(a) Explain how Atomic Writes helps to achieve the concept of stable storage. A SATA HDD with capacity of 1 Tera Bytes costs NPR. 5,700 and A SATA SSD with capacity of 256 Giga Bytes cost NPR. 7,500. Now, calculate the cost of storing a file with capacity of 100 Mega Bytes on each device. Which device is cost efficient and by how much? Explain. [[2+4]]

(b) Given references to the following pages by a program 1, 2, 3, 2, 1, 5, 2, 1, 6, 2, 5, 6, 3, 1, 3, 6, 1, 2, 4, 3. How many page faults will occur if the program has three-page frames available to it and use LRU, FIFO and Optimal page replacement algorithm? [[5]]

@q 5
Explain the advantages and disadvantages of a contiguous file allocation scheme. [[3]]

@q 6
Explain private and public key cryptography with examples. [[4]]

@q 7
Explain how Dockers and Kubernetes are used for containerization? [[4]]

@q 8
State one real world application or device where your studied OS is used, and justify that why it is suitable for that environment. [[3]]

@q 9
Write short notes on: (Any Two) [[2×3]]

(a) Type 1 hypervisor

(b) Secure Boot

(c) Sandboxing

(d) PowerShell
<!-- SOLUTIONS -->

@s 1
**UEFI against Legacy boot.**

| Basis | Legacy BIOS boot | UEFI boot |
|---|---|---|
| Firmware | 16-bit BIOS, real mode, 1 MB address space | 32/64-bit UEFI firmware, a small OS of its own |
| Partition scheme | MBR: 4 primary partitions, disks up to 2 TB | GPT: 128 partitions by default, disks up to 9.4 ZB |
| Where the boot code lives | first 512-byte sector (MBR) of the disk, then chain-loading | `.efi` boot loader in the FAT32 EFI System Partition (ESP), chosen from NVRAM boot entries |
| Security | none (any code in the MBR runs) | **Secure Boot** checks the digital signature of the loader and drivers |
| Speed | slower POST, serial device probing | faster start-up, drivers loaded on demand, fast-boot |
| Interface | text-only, keyboard | graphical menu, mouse, network boot (PXE/HTTP), shell |
| Recovery | MBR can be overwritten by one bad sector or a boot-sector virus | GPT keeps a backup header and CRC32 protection |

*Boot sequence.* Legacy: POST → BIOS reads the MBR → boot loader (GRUB/NTLDR) → kernel. UEFI: platform initialisation → firmware reads the boot entry from NVRAM → loads the `.efi` loader from the ESP (signature checked with Secure Boot) → kernel.

**OS as an intermediary (abstraction).** Hardware is complicated, differs from machine to machine and cannot be shared safely, so the operating system sits between the user application and the hardware and plays two roles:

1. *Extended (virtual) machine.* It hides hardware details behind simple, uniform interfaces. A program asks for `read(fd, buf, n)`; it never programs the disk controller, handles interrupts or knows the number of heads. Disk blocks become **files**, RAM becomes a private **virtual address space**, the CPU becomes many **processes/threads**, network cards become **sockets**.
2. *Resource manager.* It allocates CPU, memory, disks and devices among competing programs, enforces **protection** (a process cannot touch another process or kernel memory) and keeps accounting.

The application talks to the OS only through the **system-call interface** (the OS runs in kernel mode, applications in user mode); the OS talks to the hardware through **device drivers** and the hardware abstraction layer. The same application therefore runs unchanged on a different disk or printer: only the driver changes. Example: when a word processor prints, it calls `write()` on a file; the OS spools the data, schedules the printer, and the driver converts it to the commands of that particular printer.

```figure caption="The operating system as the intermediary between user applications and the hardware: applications reach it only through system calls; it hides the hardware behind drivers and the HAL."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.6,3.0)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,7.4)
rows=[("User applications (browser, editor, compiler, games)","#e8eefb",6.3),("System-call interface  (open, read, fork, exec, socket ...)","#cfdcf7",5.1),
("Kernel:  processes | memory | files | I/O + network | protection","#b6caf2",3.9),("Device drivers  +  hardware abstraction layer (HAL)","#9ab5ec",2.7),("Hardware:  CPU | RAM | disks | NIC | display | keyboard","#f1e3c8",1.5)]
for t,c,y in rows:
    ax.add_patch(mp.FancyBboxPatch((0.5,y-0.45),9,0.9,boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=INK,lw=1.0)); ax.text(5,y,t,ha="center",va="center",fontsize=7.6)
for y in (5.7,4.5,3.3,2.1):
    ax.annotate("",xy=(9.3,y-0.05),xytext=(9.3,y+0.05),arrowprops=dict(arrowstyle="<->",color=ACCENT,lw=1.2))
ax.text(0.3,0.5,"OS = resource manager + extended (virtual) machine",fontsize=8,color=ACCENT)
```

@s 2
**Process control block (PCB).** The PCB (task control block) is the data structure the OS keeps for every process; it is created with the process, linked in the scheduling queues, and saved/restored at every context switch. Its components:

| Component | Content |
|---|---|
| Process identification | process ID (PID), parent PID, user ID/group ID |
| Process state | new, ready, running, waiting, terminated |
| Program counter | address of the next instruction to execute |
| CPU registers | accumulator, index registers, stack pointer, flags - saved when the process is pre-empted |
| CPU-scheduling information | priority, pointers to scheduling queues, time slice used |
| Memory-management information | base/limit registers, page-table or segment-table pointers |
| Accounting information | CPU time used, time limits, job number |
| I/O status information | list of open files, allocated I/O devices, pending I/O requests |

**Given:** five processes (times in ms). P1 and P5 arrive together at 0 and P3, P4 together at 4; ties are broken in the listed order (FCFS).

**(i) Shortest Job First (non-pre-emptive).** At each completion the shortest job among the arrived ones is chosen. At $t = 0$ only P1 (10) and P5 (8) are present: P5 runs first. At $t = 8$ the ready jobs are P1 (10), P2 (5), P3 (2), P4 (5): P3 (shortest) runs to 10; at $t = 10$ P2 and P4 (both 5, P2 arrived earlier) then P1 (10).

```figure caption="SJF (non-pre-emptive) Gantt chart: P5 0-8, P3 8-10, P2 10-15, P4 15-20, P1 20-30"
segs=[('P5', 0, 8), ('P3', 8, 10), ('P2', 10, 15), ('P4', 15, 20), ('P1', 20, 30)]
fig,ax=plt.subplots(figsize=(6.2,1.35))
cols=[ACCENT,'#2a7a4b','#b46a00','#7a3fb0','#b00020','#0c7c8c']
names=sorted({s[0] for s in segs}); cm={n:cols[i%6] for i,n in enumerate(names)}
for n,a,b in segs:
    ax.barh(0,b-a,left=a,height=0.6,color=cm[n],alpha=0.85,edgecolor='white')
    ax.text((a+b)/2,0,n,ha='center',va='center',fontsize=8,color='white',fontweight='bold')
ts=sorted({s[1] for s in segs}|{s[2] for s in segs}); ax.set_xticks(ts); ax.tick_params(labelsize=7)
ax.set_yticks([]); ax.set_ylim(-0.5,0.5)
for sp_ in ('top','right','left'): ax.spines[sp_].set_visible(False)
fig.tight_layout()
```

| Process | Arrival | Burst | Completion | Turnaround (CT - AT) | Waiting (TAT - BT) |
|---|---|---|---|---|---|
| P1 | 0 | 10 | 30 | 30 | 20 |
| P2 | 2 | 5 | 15 | 13 | 8 |
| P3 | 4 | 2 | 10 | 6 | 4 |
| P4 | 4 | 5 | 20 | 16 | 11 |
| P5 | 0 | 8 | 8 | 8 | 0 |

$$\text{Average waiting time (SJF)} = \frac{20 + 8 + 4 + 11 + 0}{5} = 8.6\ \text{ms}$$

Average turnaround time = 14.6 ms. *If the pre-emptive form (SRTF) is intended:* the order is P5 0-2, P2 2-4, P3 4-6, P2 6-9, P4 9-14, P5 14-20, P1 20-30; waiting times P1 = 20, P2 = 2, P3 = 0, P4 = 5, P5 = 12; average waiting time = **7.8 ms**.

**(ii) Round Robin, quantum = 4 ms.** New arrivals join the ready queue before the pre-empted process: the queue starts P1, P5; after P1's first slice it is P5, P2, P3, P4, P1, and so on.

```figure caption="Round Robin (q = 4) Gantt chart: P1 0-4, P5 4-8, P2 8-12, P3 12-14, P4 14-18, P1 18-22, P5 22-26, P2 26-27, P4 27-28, P1 28-30"
segs=[('P1', 0, 4), ('P5', 4, 8), ('P2', 8, 12), ('P3', 12, 14), ('P4', 14, 18), ('P1', 18, 22), ('P5', 22, 26), ('P2', 26, 27), ('P4', 27, 28), ('P1', 28, 30)]
fig,ax=plt.subplots(figsize=(6.2,1.35))
cols=[ACCENT,'#2a7a4b','#b46a00','#7a3fb0','#b00020','#0c7c8c']
names=sorted({s[0] for s in segs}); cm={n:cols[i%6] for i,n in enumerate(names)}
for n,a,b in segs:
    ax.barh(0,b-a,left=a,height=0.6,color=cm[n],alpha=0.85,edgecolor='white')
    ax.text((a+b)/2,0,n,ha='center',va='center',fontsize=8,color='white',fontweight='bold')
ts=sorted({s[1] for s in segs}|{s[2] for s in segs}); ax.set_xticks(ts); ax.tick_params(labelsize=7)
ax.set_yticks([]); ax.set_ylim(-0.5,0.5)
for sp_ in ('top','right','left'): ax.spines[sp_].set_visible(False)
fig.tight_layout()
```

| Process | Arrival | Burst | Completion | Turnaround (CT - AT) | Waiting (TAT - BT) |
|---|---|---|---|---|---|
| P1 | 0 | 10 | 30 | 30 | 20 |
| P2 | 2 | 5 | 27 | 25 | 20 |
| P3 | 4 | 2 | 14 | 10 | 8 |
| P4 | 4 | 5 | 28 | 24 | 19 |
| P5 | 0 | 8 | 26 | 26 | 18 |

$$\text{Average waiting time (RR)} = \frac{20 + 20 + 8 + 19 + 18}{5} = 17.0\ \text{ms}$$

Average turnaround time = 23.0 ms.

| Algorithm | Average waiting time | Average turnaround |
|---|---|---|
| SJF | 8.6 ms | 14.6 ms |
| Round Robin (q = 4) | 17.0 ms | 23.0 ms |

SJF gives the smallest average waiting time (it is optimal for a given set of ready jobs) but the long job P1 waits longest; Round Robin is fairer with better response time but a larger average waiting time.

@s 3
**(a)**

**Critical region.** The part of a program where a process accesses shared data (a shared variable, buffer, file or device) that must not be accessed by another process at the same time. A solution to the critical-section problem must satisfy three conditions: **mutual exclusion** (only one process inside), **progress** (a process outside cannot block others from entering) and **bounded waiting** (no process waits for ever).

**Mutex (mutual exclusion lock).** A lock with the two atomic operations `acquire()` (lock) and `release()` (unlock). It is a binary object owned by one thread at a time: the thread that locks it must unlock it. A binary semaphore initialised to 1 behaves as a mutex.

**Semaphore.** An integer $S$ accessed only through two atomic operations:

```
wait(S):   while (S <= 0) ;  S = S - 1;        // P, down
signal(S): S = S + 1;                          // V, up
```

**Producer–consumer (bounded buffer) with semaphores.** Buffer of $N$ slots, shared by one or more producers and consumers. Three semaphores are used: `mutex = 1` (exclusive access to the buffer), `empty = N` (number of empty slots), `full = 0` (number of filled slots).

```
semaphore mutex = 1, empty = N, full = 0;

Producer:                         Consumer:
do {                              do {
    item = produce_item();            wait(full);     // wait for a filled slot
    wait(empty);   // free slot?      wait(mutex);    // enter critical region
    wait(mutex);   // enter CR        item = remove_item();
    insert_item(item);                signal(mutex);  // leave critical region
    signal(mutex); // leave CR        signal(empty);  // one more empty slot
    signal(full);  // one more full   consume_item(item);
} while (true);                   } while (true);
```

The producer blocks when the buffer is full (`empty = 0`), the consumer blocks when it is empty (`full = 0`), and `mutex` stops them from changing the buffer together. The order of the two `wait` calls matters: if the producer did `wait(mutex)` before `wait(empty)` and the buffer were full, it would sleep while holding the mutex and the consumer could never enter, i.e. a **deadlock**.

**(b)**

**Dining philosophers.** Five philosophers sit round a table with one chopstick (fork) between each pair; a philosopher needs both neighbours' chopsticks to eat. Each chopstick is a semaphore `chopstick[5]`, all initialised to 1:

```
Philosopher i:
do {
    think();
    wait(chopstick[i]);            // pick left
    wait(chopstick[(i+1) % 5]);    // pick right
    eat();
    signal(chopstick[i]);
    signal(chopstick[(i+1) % 5]);
} while (true);
```

**Deadlock condition.** Mutual exclusion is guaranteed, but if **all five philosophers become hungry at the same time and each picks up the left chopstick**, every `chopstick[i]` is 0 and each philosopher waits for the right one, which is held by the neighbour: mutual exclusion, **hold-and-wait**, no pre-emption and **circular wait** all hold, so nobody ever eats (the system deadlocks).

**Remedies.** (a) Allow at most 4 philosophers at the table (a counting semaphore `room = 4` around the picking code) so at least one can always eat; (b) pick up both chopsticks only if both are free, inside a critical section or monitor; (c) asymmetric rule: odd philosophers pick left first, even philosophers right first (breaks the circular wait); (d) resource ordering (always pick the lower numbered chopstick first).

**Banker's algorithm (is the state safe?).**

**Data.** Total instances: R0 = 6, R1 = 4, R2 = 4, R3 = 2.

*Allocation*

| | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| P0 | 2 | 0 | 1 | 1 |
| P1 | 1 | 1 | 0 | 0 |
| P2 | 1 | 1 | 0 | 0 |
| P3 | 1 | 0 | 1 | 0 |
| P4 | 0 | 1 | 0 | 1 |

*Maximum claim*

| | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| P0 | 3 | 2 | 1 | 1 |
| P1 | 1 | 2 | 0 | 2 |
| P2 | 1 | 1 | 2 | 0 |
| P3 | 3 | 2 | 1 | 0 |
| P4 | 2 | 1 | 0 | 1 |

**Available** = Total - sum of Allocation = (1, 1, 2, 0) (R0: 6 - 5; R1: 4 - 3; R2: 4 - 2; R3: 2 - 2).

**Need** = Maximum - Allocation

| | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| P0 | 1 | 2 | 0 | 0 |
| P1 | 0 | 1 | 0 | 2 |
| P2 | 0 | 0 | 2 | 0 |
| P3 | 2 | 2 | 0 | 0 |
| P4 | 2 | 0 | 0 | 0 |

**Safety algorithm.** Work = Available = (1, 1, 2, 0). Repeatedly pick an unfinished process whose Need $\le$ Work; it can run to completion and then returns its Allocation (Work = Work + Allocation).

| Step | Work before | Process chosen | Need | Work after |
|---|---|---|---|---|
| 1 | (1, 1, 2, 0) | P2 | (0, 0, 2, 0) | (2, 2, 2, 0) |
| 2 | (2, 2, 2, 0) | P0 | (1, 2, 0, 0) | (4, 2, 3, 1) |
| 3 | (4, 2, 3, 1) | P3 | (2, 2, 0, 0) | (5, 2, 4, 1) |
| 4 | (5, 2, 4, 1) | P4 | (2, 0, 0, 0) | (5, 3, 4, 2) |
| 5 | (5, 3, 4, 2) | P1 | (0, 1, 0, 2) | (6, 4, 4, 2) |

All five processes can finish, so the state is **SAFE** with the safe sequence

$$\boxed{\,\langle P_2, P_0, P_3, P_4, P_1 \rangle\,}$$

(Other safe orders exist; the algorithm returns the first one found by scanning the processes in index order.) Finally Work = (6, 4, 4, 2) = Total, as it must be when every process has released its resources.

@s 4
**(a)**

**Stable storage and atomic writes.** A disk write is *not* atomic: a crash or power cut in the middle of writing a block leaves a half-old, half-new (torn) block, or a metadata update that is only partly done. **Stable storage** is storage that survives such failures: every write is either done completely or not done at all. It is built on **atomic writes**:

1. Write the data to a *separate* place first (a log/journal, a second copy or a new block), never over the only valid copy.
2. Flush it and write a small **commit record** (a single sector write is atomic).
3. Only after the commit, apply it to the real location (or switch a pointer).
4. On recovery after a crash, the OS inspects the log: committed records are **redone**, uncommitted ones **discarded/undone**.

Classic realisations: the *two-copy stable-storage scheme* (write copy 1, verify with checksum, then copy 2; recovery copies the good one over the bad one), *journaling* file systems (ext4, NTFS), *copy-on-write* file systems (ZFS, Btrfs) and database write-ahead logs. The result is all-or-nothing updates and a consistent file system after a crash.

**Cost of storing the 100 MB file.**

Taking decimal units (1 TB = 1,000,000 MB, 1 GB = 1000 MB): cost of storing the file = (price / capacity in MB) $\times$ file size.

$$\begin{gathered}\text{SATA HDD (1 TB): }\ \frac{5700}{1,000,000}\times100 = \text{NPR }0.570 \\ \text{SATA SSD (256 GB): }\ \frac{7500}{256,000}\times100 = \text{NPR }2.930\end{gathered}$$

**SATA HDD (1 TB) is more cost-efficient**: it is cheaper by NPR 2.36 for this file (NPR 0.57 against NPR 2.93), i.e. 5.1 times cheaper per byte (81 % less). Cost per GB: SATA HDD (1 TB) NPR 5.70, SATA SSD (256 GB) NPR 29.30. (With binary units, 1 TB = 1,048,576 MB, the figures change slightly but the conclusion is the same.)

**(b)** Reference string (20 references), 3 frames; each column shows the frames after that reference (oldest page first for FIFO, least recently used first for LRU), and **F** marks a page fault.

**FIFO** - replace the page that has been in memory longest

| Ref | 1 | 2 | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 3 | 1 | 3 | 6 | 1 | 2 | 4 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 5 | 1 | 6 | 6 | 2 | 5 | 5 | 3 | 3 | 1 | 6 | 2 |
| Fr. 2 | – | 2 | 2 | 2 | 2 | 3 | 3 | 5 | 1 | 6 | 2 | 2 | 5 | 3 | 3 | 1 | 1 | 6 | 2 | 4 |
| Fr. 3 | – | – | 3 | 3 | 3 | 5 | 5 | 1 | 6 | 2 | 5 | 5 | 3 | 1 | 1 | 6 | 6 | 2 | 4 | 3 |
| Fault | F | F | F |  |  | F |  | F | F | F | F |  | F | F |  | F |  | F | F | F |

**FIFO: 14 page faults** (hit ratio 6/20).

**LRU** - replace the page unused for the longest time in the past

| Ref | 1 | 2 | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 3 | 1 | 3 | 6 | 1 | 2 | 4 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 1 | 1 | 1 | 1 | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 6 | 1 | 3 | 6 | 1 | 2 |
| Fr. 2 | – | 2 | 2 | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 3 | 1 | 3 | 6 | 1 | 2 | 4 |
| Fr. 3 | – | – | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 3 | 1 | 3 | 6 | 1 | 2 | 4 | 3 |
| Fault | F | F | F |  |  | F |  |  | F |  | F |  | F | F |  |  |  | F | F | F |

**LRU: 11 page faults** (hit ratio 9/20).

**Optimal** - replace the page whose next use is farthest in the future

| Ref | 1 | 2 | 3 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 5 | 6 | 3 | 1 | 3 | 6 | 1 | 2 | 4 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 2 | 4 | 4 |
| Fr. 2 | – | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Fr. 3 | – | – | 3 | 3 | 3 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Fault | F | F | F |  |  | F |  |  | F |  |  |  | F | F |  |  |  | F | F |  |

**Optimal: 9 page faults** (hit ratio 11/20).

| Algorithm | FIFO | LRU | Optimal |
|---|---|---|---|
| Page faults | 14 | 11 | 9 |

Optimal gives the fewest faults (it looks ahead, so it is a benchmark that cannot be built in a real system); LRU approximates it; FIFO is the simplest and can even show Belady's anomaly.

@s 5
**Contiguous allocation.** Each file occupies a set of consecutive disk blocks; the directory entry stores only the **start block** and the **length**.

| Advantages | Disadvantages |
|---|---|
| Very simple to implement and to manage (start + length) | **External fragmentation**: free space breaks into small holes; compaction is slow |
| Excellent performance: sequential access needs minimal seeks, the whole file can be read in one transfer | The file size must be known when it is created; a file cannot easily **grow** (it may have to be copied to a bigger hole) |
| **Direct (random) access** is trivial: block $i$ is at address $b + i$ | Over-estimating the size wastes space (internal fragmentation) |
| Only one seek is needed to reach the file; good for read-only media (CD/DVD) | Finding a hole for a new file needs first-fit / best-fit / worst-fit search |

@s 6
**Cryptography** converts readable *plaintext* into unreadable *ciphertext* with a key, to give confidentiality, integrity, authentication and non-repudiation.

**Private-key (symmetric) cryptography.** One **secret key** is used by both sender and receiver for encryption and decryption: $C = E_K(P)$, $P = D_K(C)$. It is fast and suited to bulk data, but the key must be shared securely beforehand and each pair of users needs its own key ($n(n-1)/2$ keys for $n$ users). *Examples:* AES, DES, 3DES, ChaCha20 (disk encryption, VPN data, HTTPS data transfer).

**Public-key (asymmetric) cryptography.** Every user has a **key pair**: a *public key* (published) and a *private key* (kept secret); what one key encrypts only the other can decrypt. To send a confidential message, encrypt with the receiver's public key; the receiver decrypts with the private key. To sign, the sender encrypts a hash with the *private* key and anybody can verify with the public key. It is slower than symmetric encryption and is used for key exchange, digital signatures and certificates. *Examples:* RSA, ECC, Diffie-Hellman.

*Small RSA example.* Choose primes $p = 3$, $q = 11$: $n = pq = 33$, $\varphi = (p-1)(q-1) = 20$. Take $e = 7$ (coprime with 20) and $d$ with $ed \equiv 1 \pmod{20}$: $d = 3$. Public key $(7, 33)$, private key $(3, 33)$. Encrypt $M = 4$: $C = 4^{7} \bmod 33 = 16$. Decrypt: $M = 16^{3} \bmod 33 = 4096 \bmod 33 = 4$ ✓.

| | Private-key | Public-key |
|---|---|---|
| Keys | one shared secret | public + private pair |
| Speed | fast | slow |
| Key distribution | difficult | easy (public key is open) |
| Use | bulk encryption | key exchange, signatures |

In practice both are combined (a hybrid, as in TLS/HTTPS): public-key cryptography exchanges a session key, then symmetric cryptography encrypts the data.

@s 7
**Containerization** packages an application together with its libraries and dependencies into a lightweight, isolated unit called a **container**. Containers share the host operating-system kernel (no guest OS per container), so they start in seconds and use far less memory than virtual machines. Isolation comes from Linux **namespaces** (separate process, network, mount and user views) and **cgroups** (limits on CPU, memory and I/O).

**Docker** is the tool that builds and runs containers.

1. A **Dockerfile** lists the base image, files to copy, packages to install and the start command.
2. `docker build` creates an immutable layered **image**; `docker run` starts a **container** from it; images are stored and shared through a **registry** (Docker Hub).
3. The same image runs identically on a laptop, a test server or the cloud ("build once, run anywhere"), which removes the "works on my machine" problem.

```
FROM python:3.12-slim
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

**Kubernetes (K8s)** is a *container orchestrator*: it runs and manages hundreds of containers over a **cluster** of machines.

- **Pod**: the smallest unit, one or more containers that share network and storage.
- **Node**: a worker machine; the **control plane** (API server, scheduler, etcd, controller manager) decides where each pod runs.
- **Deployment / ReplicaSet**: keeps the desired number of pod replicas, performs rolling updates and rollbacks and replaces failed pods (self-healing).
- **Service**: a stable IP/DNS name that load-balances traffic over the pods; **Ingress** exposes it outside the cluster; an **autoscaler** adds or removes pods with the load.

Together: Docker packages the application, Kubernetes deploys, scales, heals and updates it across many machines (micro-service architecture).

@s 8
The OS studied in the course is taken as **Linux**.

**Real-world application:** Linux runs the **web servers and cloud data centres** of the big internet companies, **Android** phones (Linux kernel) and all of the world's top-500 supercomputers.

**Why it is suitable.** It is free and open source (low cost, can be customised), highly **stable** (servers run for years without reboot), **multi-user and multi-tasking** with strict file permissions, **secure** (least privilege, SELinux/AppArmor, quick patches), **scalable** from tiny devices to thousands of cores, and it supports a huge range of hardware and server software (Apache, nginx, Docker, Kubernetes).

@s 9
*(Any two are required; all four are answered.)*

**(a) Type 1 hypervisor.** A bare-metal hypervisor installed directly on the server hardware that schedules the virtual machines itself (VMware ESXi, Hyper-V, Xen, KVM). Each VM has virtual CPUs, memory and devices; the hypervisor traps privileged instructions (hardware assist Intel VT-x / AMD-V) and isolates VMs from each other. Benefits: near-native speed, strong isolation, live migration, consolidation of many servers on one machine, which is the basis of cloud computing.

**(b) Secure Boot.** A UEFI feature that lets only trusted, digitally signed software run during start-up. The firmware holds a database of trusted keys (PK, KEK, db) and a revocation list (dbx); it checks the signature of the boot loader, and the loader checks the kernel and drivers (a *chain of trust*). Unsigned or tampered code (a boot-kit or rootkit) is refused. It protects the pre-OS stage; it can be disabled for dual-boot or custom kernels in the firmware set-up.

(c) **Sandboxing.** Running a program in a restricted, isolated environment so that a bug or malicious code cannot damage the rest of the system. The sandbox limits file access, network, system calls and memory (by namespaces/cgroups, `seccomp`, jails, virtual machines, the browser tab sandbox or the Android app sandbox with a separate user id for every app). It is used for testing untrusted software, malware analysis, running web content and mobile apps, and it applies the principle of least privilege.

(d) **PowerShell.** Microsoft's command-line shell and scripting language (built on .NET, cross-platform since PowerShell 7). Its commands, **cmdlets**, follow a *Verb-Noun* pattern (`Get-Process`, `Stop-Service`, `Get-ChildItem`) and pass **objects**, not text, through the pipeline (`Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU`). It is used for system administration and automation, remote management (WinRM/SSH remoting), configuration (Desired State Configuration) and scripting with variables, loops and functions; because of its power, attackers also misuse it, so execution policy and script logging are used.
