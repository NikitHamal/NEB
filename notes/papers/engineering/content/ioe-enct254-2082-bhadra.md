---
file: NEBians-IOE-Past-Paper-Operating-System-ENCT254-2082-Bhadra.pdf
subject: Operating System
level: BE · Year II / Part II
code: ENCT254
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Difference between MBR and GPT Partitions. How does an operating system provide abstraction to user level application from underlying hardware? Explain. [[2+4]]

@q 2
Describe the various states of the process. Schedule the following set of processes according to HRRN and Round Robin algorithm (Time quantum:4). [[3+6]]

| Process | Arrival time | Burst time |
|---|---|---|
| A | 0 | 12 |
| B | 2 | 8 |
| C | 5 | 7 |
| D | 10 | 9 |

(i) Draw Gantt Chart

(ii) Find average turnaround time and waiting time for each scheduling algorithm.

@q 3
(a) Define race condition. Explain how producer-consumer problem can be solved using semaphore with its respective pseudo-code implementations. [[1+5]]

(b) Consider a system with 5 concurrent processes (P0, P1, P2, P3, P4) and 4 resources (R0, R1, R2, R3) types in the system are 6, 4, 4, 2 respectively. Current allocation and maximum need/claim table are as follows: [[7]]

| Process | Allocation R1 | R2 | R3 | R4 | Maximum Claim R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|---|---|
| P0 | 2 | 0 | 1 | 1 | 3 | 2 | 1 | 1 |
| P1 | 1 | 1 | 0 | 0 | 1 | 2 | 0 | 2 |
| P2 | 1 | 1 | 0 | 0 | 1 | 1 | 2 | 0 |
| P3 | 1 | 0 | 1 | 0 | 3 | 2 | 1 | 0 |
| P4 | 0 | 1 | 0 | 1 | 2 | 1 | 0 | 1 |

Use Bankers algorithm to claim that the system is in safe state and show the safe sequence.

@q 4
(a) What is RAID? Explain how Write Ahead Logging (WAL) helps to achieve the concept of stable storage. A NVMe SSD with capacity of 2 Tera Bytes costs NPR. 15,000 and A SATA SSD with capacity of 1 Tera Bytes costs NPR. 5,500. Now, calculate the cost of storing a file with capacity of 160 Mega Bytes on each device. Which device is cost efficient and by how much? Explain [[1+2+4]]

(b) Consider the following page-reference storing 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1. Assuming 3 frames, how many page faults would occur for the following page replacement algorithms (i) FIFO (ii) Optimal (iii) LRU. [[5]]

@q 5
What is file attribute? Describe different file allocation methods. [[1+3]]

@q 6
Explain the types of attacks with suitable examples. [[3]]

@q 7
Explain about the Type 1 and Type 2 hypervisors in virtualization. [[4]]

@q 8
List any 2 key features of OS you studied as case study and explain how they contribute to its performance or usability. [[3]]

@q 9
Write short notes on: (Any Two) [[2×3]]

(a) Kubernetes and Docker

(b) Thrashing

(c) Sandboxing

(d) PowerShell
<!-- SOLUTIONS -->

@s 1
**MBR against GPT.**

| Basis | MBR (Master Boot Record) | GPT (GUID Partition Table) |
|---|---|---|
| Location | first sector (LBA 0), 512 bytes: 446 B boot code, 64 B partition table, 2 B signature `0x55AA` | LBA 1 (header) + LBA 2-33 (entries), protective MBR at LBA 0, backup copy at the end of the disk |
| Maximum disk size | 2 TB (32-bit LBA, 512 B sectors) | about 9.4 ZB (64-bit LBA) |
| Number of partitions | 4 primary (or 3 + 1 extended holding logical drives) | 128 by default, all primary |
| Partition identity | 1-byte type code | 128-bit GUID per partition and per disk, plus a name |
| Reliability | one copy, no checksum | primary + backup table, CRC32 checks, self-repair |
| Boot mode | Legacy BIOS | UEFI (BIOS possible only through a hybrid set-up) |
| Examples | old Windows 7 / XP installs, USB sticks | Windows 10/11, modern Linux, macOS, disks over 2 TB |

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
**Process states.** From creation to termination a process passes through these states:

| State | Meaning |
|---|---|
| **New** | the process is being created (PCB and address space set up) |
| **Ready** | in memory, has everything it needs except the CPU, waiting in the ready queue |
| **Running** | its instructions are being executed on the CPU |
| **Waiting (blocked)** | waiting for an event such as I/O completion or a signal |
| **Terminated** | finished execution; the OS reclaims its resources |

Transitions: new → ready (*admitted*); ready → running (*scheduler dispatch*); running → ready (*interrupt / time quantum expired* or pre-emption); running → waiting (*I/O or event wait*); waiting → ready (*I/O or event completion*); running → terminated (*exit*). Systems with swapping add the *suspended ready* and *suspended wait* states.

```figure caption="Process state diagram: new, ready, running, waiting (blocked) and terminated, with the events that move a process between them."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.8,2.8)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
pos={"New":(1.2,3),"Ready":(4.8,3),"Running":(9.0,3),"Terminated":(12.6,3),"Waiting":(6.9,0.7)}
for n,(x,y) in pos.items():
    ax.add_patch(mp.FancyBboxPatch((x-0.95,y-0.38),1.9,0.76,boxstyle="round,pad=0.02,rounding_size=0.2",fc="#e8eefb",ec=INK,lw=1.1)); ax.text(x,y,n,ha="center",va="center",fontsize=8.5,fontweight="bold")
def arr(a,b):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.2))
arr((2.18,3),(3.82,3)); ax.text(3.0,3.4,"admitted",ha="center",fontsize=7.2)
arr((5.78,3.15),(8.02,3.15)); ax.text(6.9,3.55,"dispatch",ha="center",fontsize=7.2)
arr((8.02,2.85),(5.78,2.85)); ax.text(6.9,2.45,"time-out",ha="center",fontsize=7.2)
arr((9.2,2.6),(7.8,1.0)); ax.text(9.6,1.6,"I/O or event wait",ha="left",fontsize=7.2)
arr((6.0,1.0),(4.6,2.6)); ax.text(4.2,1.6,"I/O or event\ncompletion",ha="right",fontsize=7.2)
arr((9.98,3),(11.62,3)); ax.text(10.8,3.4,"exit",ha="center",fontsize=7.2)
```

**(i) HRRN (Highest Response Ratio Next, non-pre-emptive).** Response ratio $RR = \dfrac{W + B}{B}$ ($W$ = waiting time so far, $B$ = burst time); when the CPU becomes free the ready process with the highest ratio runs to completion.

| Time | Ready processes | Response ratios | Chosen |
|---|---|---|---|
| 0 | A | A = 1.000 | **A** |
| 12 | B, C, D | B = 2.250; C = 2.000; D = 1.222 | **B** |
| 20 | C, D | C = 3.143; D = 2.111 | **C** |
| 27 | D | D = 2.889 | **D** |

(For example at $t = 12$: B: $(10 + 8)/8 = 2.25$, C: $(7 + 7)/7 = 2.0$, D: $(2 + 9)/9 = 1.22$; at $t = 20$: C: $(15 + 7)/7 = 3.14$, D: $(10 + 9)/9 = 2.11$.)

```figure caption="HRRN Gantt chart: A 0-12, B 12-20, C 20-27, D 27-36"
segs=[('A', 0, 12), ('B', 12, 20), ('C', 20, 27), ('D', 27, 36)]
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
| A | 0 | 12 | 12 | 12 | 0 |
| B | 2 | 8 | 20 | 18 | 10 |
| C | 5 | 7 | 27 | 22 | 15 |
| D | 10 | 9 | 36 | 26 | 17 |

$$\begin{gathered}\text{Average turnaround time} = \frac{12 + 18 + 22 + 26}{4} = 19.50\ \text{ms} \\ \text{Average waiting time} = \frac{0 + 10 + 15 + 17}{4} = 10.50\ \text{ms}\end{gathered}$$

**(ii) Round Robin, quantum = 4 ms.** The ready queue starts with A; B arrives at 2 and joins the queue before A returns after its first slice, C (at 5) and D (at 10) join in the same way.

```figure caption="Round Robin (q = 4) Gantt chart: A 0-4, B 4-8, A 8-12, C 12-16, B 16-20, D 20-24, A 24-28, C 28-31, D 31-35, D 35-36"
segs=[('A', 0, 4), ('B', 4, 8), ('A', 8, 12), ('C', 12, 16), ('B', 16, 20), ('D', 20, 24), ('A', 24, 28), ('C', 28, 31), ('D', 31, 35), ('D', 35, 36)]
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
| A | 0 | 12 | 28 | 28 | 16 |
| B | 2 | 8 | 20 | 18 | 10 |
| C | 5 | 7 | 31 | 26 | 19 |
| D | 10 | 9 | 36 | 26 | 17 |

$$\begin{gathered}\text{Average turnaround time} = \frac{28 + 18 + 26 + 26}{4} = 24.50\ \text{ms} \\ \text{Average waiting time} = \frac{16 + 10 + 19 + 17}{4} = 15.50\ \text{ms}\end{gathered}$$

| Algorithm | Avg turnaround | Avg waiting |
|---|---|---|
| HRRN | 19.50 ms | 10.50 ms |
| Round Robin (q = 4) | 24.50 ms | 15.50 ms |

HRRN has the lower averages here and avoids starvation (a waiting process's ratio keeps rising); Round Robin gives every process the CPU regularly, so it has better response time but more context switches.

@s 3
**(a) Race condition.** A situation in which two or more processes/threads access and change shared data concurrently, and the final result depends on the *order* in which their instructions are interleaved. Example: `counter++` is compiled to *load, add, store*. With `counter = 5`, if a producer and a consumer both load 5, one computes 6 and the other 4, and whichever stores last wins, so the result is 6 or 4 instead of 5. The cure is to make the access a critical section protected by a semaphore or mutex.

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

**(b) Banker's algorithm.**

**Data.** Total instances: R1 = 6, R2 = 4, R3 = 4, R4 = 2.

*Allocation*

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| P0 | 2 | 0 | 1 | 1 |
| P1 | 1 | 1 | 0 | 0 |
| P2 | 1 | 1 | 0 | 0 |
| P3 | 1 | 0 | 1 | 0 |
| P4 | 0 | 1 | 0 | 1 |

*Maximum claim*

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| P0 | 3 | 2 | 1 | 1 |
| P1 | 1 | 2 | 0 | 2 |
| P2 | 1 | 1 | 2 | 0 |
| P3 | 3 | 2 | 1 | 0 |
| P4 | 2 | 1 | 0 | 1 |

**Available** = Total - sum of Allocation = (1, 1, 2, 0) (R1: 6 - 5; R2: 4 - 3; R3: 4 - 2; R4: 2 - 2).

**Need** = Maximum - Allocation

| | R1 | R2 | R3 | R4 |
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

**RAID (Redundant Array of Independent Disks)** combines several physical disks into one logical volume to get higher **speed** (parallel reads/writes, striping), **reliability** (redundancy: mirroring or parity) or both. The OS or a controller spreads data in stripes over the disks.

| Level | Method | Usable capacity ($n$ disks) | Fault tolerance | Remarks |
|---|---|---|---|---|
| RAID 0 | striping only | $n$ | none | fastest, any disk failure loses all |
| RAID 1 | mirroring | $n/2$ | 1 disk per pair | simple, 100 % overhead |
| RAID 5 | striping + distributed parity | $n-1$ | 1 disk | good read speed, slower writes |
| RAID 6 | striping + double parity | $n-2$ | 2 disks | for large arrays |
| RAID 10 | mirror of stripes | $n/2$ | 1 per mirror pair | fast and safe, expensive |

**Write-Ahead Logging (WAL).** Before any change is made to the data on disk, a *log record* describing the change (transaction id, old value, new value) is first written to a sequential log on stable storage, and the log is forced to disk at commit time. The data pages themselves may be written lazily later. After a crash the system *replays* the log: committed transactions are **redone**, uncommitted ones are **undone**. Because the log write is a single sequential append and the commit record is one atomic sector write, an update is either completely visible or completely absent: this gives the atomic writes that stable storage needs, and it also speeds things up (sequential log writes instead of many random writes). Journaling file systems, databases and RAID write-hole protection use WAL.

**Cost of storing the 160 MB file.**

Taking decimal units (1 TB = 1,000,000 MB, 1 GB = 1000 MB): cost of storing the file = (price / capacity in MB) $\times$ file size.

$$\begin{gathered}\text{NVMe SSD (2 TB): }\ \frac{15000}{2,000,000}\times160 = \text{NPR }1.200 \\ \text{SATA SSD (1 TB): }\ \frac{5500}{1,000,000}\times160 = \text{NPR }0.880\end{gathered}$$

**SATA SSD (1 TB) is more cost-efficient**: it is cheaper by NPR 0.32 for this file (NPR 0.88 against NPR 1.20), i.e. 1.4 times cheaper per byte (27 % less). Cost per GB: NVMe SSD (2 TB) NPR 7.50, SATA SSD (1 TB) NPR 5.50. (With binary units, 1 TB = 1,048,576 MB, the figures change slightly but the conclusion is the same.)

**(b)** Reference string (20 references), 3 frames; each column shows the frames after that reference (oldest page first for FIFO, least recently used first for LRU), and **F** marks a page fault.

**FIFO** - replace the oldest page

| Ref | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 7 | 7 | 7 | 0 | 0 | 1 | 2 | 3 | 0 | 4 | 2 | 2 | 2 | 3 | 0 | 0 | 0 | 1 | 2 | 7 |
| Fr. 2 | – | 0 | 0 | 1 | 1 | 2 | 3 | 0 | 4 | 2 | 3 | 3 | 3 | 0 | 1 | 1 | 1 | 2 | 7 | 0 |
| Fr. 3 | – | – | 1 | 2 | 2 | 3 | 0 | 4 | 2 | 3 | 0 | 0 | 0 | 1 | 2 | 2 | 2 | 7 | 0 | 1 |
| Fault | F | F | F | F |  | F | F | F | F | F | F |  |  | F | F |  |  | F | F | F |

**FIFO: 15 page faults** (hit ratio 5/20).

**Optimal** - replace the page not used for the longest time in the future

| Ref | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 7 | 7 |
| Fr. 2 | – | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Fr. 3 | – | – | 1 | 1 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Fault | F | F | F | F |  | F |  | F |  |  | F |  |  | F |  |  |  | F |  |  |

**Optimal: 9 page faults** (hit ratio 11/20).

**LRU** - replace the least recently used page

| Ref | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fr. 1 | 7 | 7 | 7 | 0 | 1 | 2 | 2 | 3 | 0 | 4 | 2 | 2 | 0 | 3 | 3 | 1 | 2 | 0 | 1 | 7 |
| Fr. 2 | – | 0 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 |
| Fr. 3 | – | – | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
| Fault | F | F | F | F |  | F |  | F | F | F | F |  |  | F |  | F |  | F |  |  |

**LRU: 12 page faults** (hit ratio 8/20).

| Algorithm | FIFO | Optimal | LRU |
|---|---|---|---|
| Page faults | 15 | 9 | 12 |

Optimal gives the fewest faults (it looks ahead, so it is a benchmark that cannot be built in a real system); LRU approximates it; FIFO is the simplest and can even show Belady's anomaly.

@s 5
**File attributes (metadata).** Information the OS keeps about every file, stored in the directory entry or the inode: **name** (human-readable), **identifier** (unique tag such as the inode number), **type**, **location** (device and disk address), **size**, **protection** (read/write/execute permissions for owner, group, others), and **time, date and owner** (creation, last access and last modification times, user id).

**File allocation methods** (how the blocks of a file are placed on the disk):

| Method | How it works | Pros | Cons |
|---|---|---|---|
| **Contiguous** | file in consecutive blocks; directory holds start and length | fast sequential and direct access, simple | external fragmentation, file cannot grow easily |
| **Linked** | each block holds a pointer to the next; directory holds first (and last) block | no external fragmentation, files grow easily | no efficient direct access, pointer overhead, one bad pointer breaks the file (FAT keeps the links in a table in memory to fix this) |
| **Indexed** | an *index block* holds the addresses of all the file's blocks (Unix inode: direct, single, double, triple indirect) | direct access without fragmentation, grows easily | index-block overhead, large files need multi-level indexes |

@s 6
**Types of attacks on a system** (security threats):

| Attack | Description | Example |
|---|---|---|
| **Virus** | code that attaches itself to a program or file and spreads when the host is run | file-infecting virus, macro virus in a document |
| **Worm** | self-replicating program that spreads over the network without a host file | Morris worm (1988), Blaster |
| **Trojan horse** | useful-looking program hiding malicious code, opens a back door | fake game or cracked software that installs a keylogger |
| **Ransomware** | encrypts the victim's files and demands payment | WannaCry (2017) |
| **Denial of Service (DoS/DDoS)** | floods a server or network so legitimate users cannot be served | Mirai botnet DDoS, SYN flood, ping flood |
| **Phishing / social engineering** | tricks users into revealing passwords or running malware | a fake bank e-mail asking for login details |
| **Buffer overflow** | writing past the end of a buffer to overwrite the return address and run attacker code | stack smashing on an unchecked `strcpy()` |
| **Man-in-the-middle** | attacker secretly relays and may alter the communication | rogue Wi-Fi hotspot reading unencrypted traffic |
| **Brute-force / password attack** | tries all or common passwords | dictionary attack on SSH |
| **SQL injection** | malicious SQL in an input field alters the database query | `' OR '1'='1` in a login form |
| **Privilege escalation, logic bomb, back door** | a user or code gains rights it should not have, or a hidden trigger runs | a program that deletes files on a given date |

Defences: authentication, access control, least privilege, patches, firewalls, anti-malware, encryption, sandboxing and logging.

@s 7
**Hypervisor (virtual machine monitor).** Software that creates and runs virtual machines by sharing the physical CPU, memory, disk and network among several guest operating systems, each of which believes it has a whole machine.

| Basis | Type 1 (bare-metal, native) | Type 2 (hosted) |
|---|---|---|
| Runs on | directly on the hardware, no host OS | as an application on a host OS |
| Layers | hardware → hypervisor → guest OS | hardware → host OS → hypervisor → guest OS |
| Performance | high, little overhead, direct hardware access | lower, every request goes through the host OS |
| Security / isolation | better (small attack surface) | depends on the host OS |
| Use | data centres, cloud servers, production | desktops, testing, learning |
| Examples | VMware ESXi, Microsoft Hyper-V, Xen, KVM (Linux) | Oracle VirtualBox, VMware Workstation/Player, Parallels |

@s 8
**Case study OS: Linux.** Two key features:

1. **Pre-emptive, fair multitasking scheduler (CFS / EEVDF) with a virtual-memory system.** The kernel gives every runnable task a fair share of CPU time (weighted by priority/nice value), pre-empts long-running tasks and uses demand paging with a page cache. *Contribution:* many programs run smoothly together, interactive tasks stay responsive, and RAM is used efficiently (unused memory caches disk data), which improves **performance**.
2. **Journaling file system with Unix permissions (ext4) and a modular kernel.** Each file has owner/group/other read-write-execute permissions, and ext4 logs metadata changes (write-ahead journal) so the file system is consistent after a crash; drivers load as modules without rebooting. *Contribution:* strong **security and reliability**, quick crash recovery and flexible hardware support, which improve **usability** and uptime.

@s 9
*(Any two are required; all four are answered.)*

(a) **Containerization** packages an application together with its libraries and dependencies into a lightweight, isolated unit called a **container**. Containers share the host operating-system kernel (no guest OS per container), so they start in seconds and use far less memory than virtual machines. Isolation comes from Linux **namespaces** (separate process, network, mount and user views) and **cgroups** (limits on CPU, memory and I/O).

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

(b) **Thrashing.** A condition in which the system spends more time **swapping pages in and out** than executing, so CPU utilisation collapses. *Cause:* the total working sets of the running processes exceed the physical memory; each page fault evicts a page that is soon needed again, so the fault rate becomes very high; the OS sees low CPU use and wrongly adds more processes, making it worse. *Cure:* the **working-set model** (give each process enough frames for its working set), **page-fault-frequency control**, local replacement, reducing the degree of multiprogramming (suspend/swap-out processes) and adding RAM.

(c) **Sandboxing.** Running a program in a restricted, isolated environment so that a bug or malicious code cannot damage the rest of the system. The sandbox limits file access, network, system calls and memory (by namespaces/cgroups, `seccomp`, jails, virtual machines, the browser tab sandbox or the Android app sandbox with a separate user id for every app). It is used for testing untrusted software, malware analysis, running web content and mobile apps, and it applies the principle of least privilege.

(d) **PowerShell.** Microsoft's command-line shell and scripting language (built on .NET, cross-platform since PowerShell 7). Its commands, **cmdlets**, follow a *Verb-Noun* pattern (`Get-Process`, `Stop-Service`, `Get-ChildItem`) and pass **objects**, not text, through the pipeline (`Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU`). It is used for system administration and automation, remote management (WinRM/SSH remoting), configuration (Desired State Configuration) and scripting with variables, loops and functions; because of its power, attackers also misuse it, so execution policy and script logging are used.
