"""Writes the two Operating System (ENCT 254) markdown papers.  Run: python3 gen_os.py <outdir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oslib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

FM = """---
file: NEBians-IOE-Past-Paper-Operating-System-{code}-{tag}.pdf
subject: Operating System
level: BE · Year II / Part II
code: {code}
year_bs: {yr}
cal: BS
year_ad: {ad}
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. {kind} (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

"""

# ---------------------------------------------------------------- figures
FIG_LAYERS = '''```figure caption="The operating system as the intermediary between user applications and the hardware: applications reach it only through system calls; it hides the hardware behind drivers and the HAL."
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
'''

FIG_STATES = '''```figure caption="Process state diagram: new, ready, running, waiting (blocked) and terminated, with the events that move a process between them."
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
arr((6.0,1.0),(4.6,2.6)); ax.text(4.2,1.6,"I/O or event\\ncompletion",ha="right",fontsize=7.2)
arr((9.98,3),(11.62,3)); ax.text(10.8,3.4,"exit",ha="center",fontsize=7.2)
```
'''

def gantt(segs, cap):
    return '```figure caption="%s"\n%s```\n' % (cap, gantt_code(segs))

def seg_text(segs):
    return ", ".join("%s %d-%d" % s for s in segs)

def sched_table(rows):
    t = "| Process | Arrival | Burst | Completion | Turnaround (CT - AT) | Waiting (TAT - BT) |\n|---|---|---|---|---|---|\n"
    for n, a, b, ct, tat, wt in rows:
        t += "| %s | %d | %d | %d | %d | %d |\n" % (n, a, b, ct, tat, wt)
    return t

def mat(m, hdr):
    t = "| | " + " | ".join(hdr) + " |\n|---|" + "---|" * len(hdr) + "\n"
    for i, r in enumerate(m):
        t += "| P%d | " % i + " | ".join(str(x) for x in r) + " |\n"
    return t

# ---------------------------------------------------------------- shared theory
UEFI_TABLE = """| Basis | Legacy BIOS boot | UEFI boot |
|---|---|---|
| Firmware | 16-bit BIOS, real mode, 1 MB address space | 32/64-bit UEFI firmware, a small OS of its own |
| Partition scheme | MBR: 4 primary partitions, disks up to 2 TB | GPT: 128 partitions by default, disks up to 9.4 ZB |
| Where the boot code lives | first 512-byte sector (MBR) of the disk, then chain-loading | `.efi` boot loader in the FAT32 EFI System Partition (ESP), chosen from NVRAM boot entries |
| Security | none (any code in the MBR runs) | **Secure Boot** checks the digital signature of the loader and drivers |
| Speed | slower POST, serial device probing | faster start-up, drivers loaded on demand, fast-boot |
| Interface | text-only, keyboard | graphical menu, mouse, network boot (PXE/HTTP), shell |
| Recovery | MBR can be overwritten by one bad sector or a boot-sector virus | GPT keeps a backup header and CRC32 protection |

*Boot sequence.* Legacy: POST → BIOS reads the MBR → boot loader (GRUB/NTLDR) → kernel. UEFI: platform initialisation → firmware reads the boot entry from NVRAM → loads the `.efi` loader from the ESP (signature checked with Secure Boot) → kernel."""

MBR_TABLE = """| Basis | MBR (Master Boot Record) | GPT (GUID Partition Table) |
|---|---|---|
| Location | first sector (LBA 0), 512 bytes: 446 B boot code, 64 B partition table, 2 B signature `0x55AA` | LBA 1 (header) + LBA 2-33 (entries), protective MBR at LBA 0, backup copy at the end of the disk |
| Maximum disk size | 2 TB (32-bit LBA, 512 B sectors) | about 9.4 ZB (64-bit LBA) |
| Number of partitions | 4 primary (or 3 + 1 extended holding logical drives) | 128 by default, all primary |
| Partition identity | 1-byte type code | 128-bit GUID per partition and per disk, plus a name |
| Reliability | one copy, no checksum | primary + backup table, CRC32 checks, self-repair |
| Boot mode | Legacy BIOS | UEFI (BIOS possible only through a hybrid set-up) |
| Examples | old Windows 7 / XP installs, USB sticks | Windows 10/11, modern Linux, macOS, disks over 2 TB |"""

OS_ABSTRACTION = """**OS as an intermediary (abstraction).** Hardware is complicated, differs from machine to machine and cannot be shared safely, so the operating system sits between the user application and the hardware and plays two roles:

1. *Extended (virtual) machine.* It hides hardware details behind simple, uniform interfaces. A program asks for `read(fd, buf, n)`; it never programs the disk controller, handles interrupts or knows the number of heads. Disk blocks become **files**, RAM becomes a private **virtual address space**, the CPU becomes many **processes/threads**, network cards become **sockets**.
2. *Resource manager.* It allocates CPU, memory, disks and devices among competing programs, enforces **protection** (a process cannot touch another process or kernel memory) and keeps accounting.

The application talks to the OS only through the **system-call interface** (the OS runs in kernel mode, applications in user mode); the OS talks to the hardware through **device drivers** and the hardware abstraction layer. The same application therefore runs unchanged on a different disk or printer: only the driver changes. Example: when a word processor prints, it calls `write()` on a file; the OS spools the data, schedules the printer, and the driver converts it to the commands of that particular printer."""

CRIT = """**Critical region.** The part of a program where a process accesses shared data (a shared variable, buffer, file or device) that must not be accessed by another process at the same time. A solution to the critical-section problem must satisfy three conditions: **mutual exclusion** (only one process inside), **progress** (a process outside cannot block others from entering) and **bounded waiting** (no process waits for ever).

**Mutex (mutual exclusion lock).** A lock with the two atomic operations `acquire()` (lock) and `release()` (unlock). It is a binary object owned by one thread at a time: the thread that locks it must unlock it. A binary semaphore initialised to 1 behaves as a mutex."""

SEM_BODY = """**Semaphore.** An integer $S$ accessed only through two atomic operations:

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

The producer blocks when the buffer is full (`empty = 0`), the consumer blocks when it is empty (`full = 0`), and `mutex` stops them from changing the buffer together. The order of the two `wait` calls matters: if the producer did `wait(mutex)` before `wait(empty)` and the buffer were full, it would sleep while holding the mutex and the consumer could never enter, i.e. a **deadlock**."""

DINING = """**Dining philosophers.** Five philosophers sit round a table with one chopstick (fork) between each pair; a philosopher needs both neighbours' chopsticks to eat. Each chopstick is a semaphore `chopstick[5]`, all initialised to 1:

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

**Remedies.** (a) Allow at most 4 philosophers at the table (a counting semaphore `room = 4` around the picking code) so at least one can always eat; (b) pick up both chopsticks only if both are free, inside a critical section or monitor; (c) asymmetric rule: odd philosophers pick left first, even philosophers right first (breaks the circular wait); (d) resource ordering (always pick the lower numbered chopstick first)."""

def banker_section(names, alloc, mx, total):
    avail, need, order, steps, work = banker(alloc, mx, total)
    s = "**Data.** Total instances: " + ", ".join("%s = %d" % (n, t) for n, t in zip(names, total)) + ".\n\n"
    s += "*Allocation*\n\n" + mat(alloc, names) + "\n*Maximum claim*\n\n" + mat(mx, names) + "\n"
    s += "**Available** = Total - sum of Allocation = (" + ", ".join(str(a) for a in avail) + ") (" + "; ".join("%s: %d - %d" % (names[j], total[j], sum(alloc[i][j] for i in range(len(alloc)))) for j in range(len(total))) + ").\n\n"
    s += "**Need** = Maximum - Allocation\n\n" + mat(need, names) + "\n"
    s += "**Safety algorithm.** Work = Available = (%s). Repeatedly pick an unfinished process whose Need $\\le$ Work; it can run to completion and then returns its Allocation (Work = Work + Allocation).\n\n" % ", ".join(map(str, avail))
    s += "| Step | Work before | Process chosen | Need | Work after |\n|---|---|---|---|---|\n"
    for k, (i, w, nd) in enumerate(steps, 1):
        after = [w[j] + alloc[i][j] for j in range(len(w))]
        s += "| %d | (%s) | P%d | (%s) | (%s) |\n" % (k, ", ".join(map(str, w)), i, ", ".join(map(str, nd)), ", ".join(map(str, after)))
    seq = ", ".join("P_%d" % i for i in order)
    s += "\nAll five processes can finish, so the state is **SAFE** with the safe sequence\n\n$$\\boxed{\\,\\langle %s \\rangle\\,}$$\n\n" % seq
    s += "(Other safe orders exist; the algorithm returns the first one found by scanning the processes in index order.) Finally Work = (%s) = Total, as it must be when every process has released its resources.\n" % ", ".join(map(str, work))
    return s

def paging_section(refs, k, algos):
    s = "Reference string (%d references), %d frames; each column shows the frames after that reference (oldest page first for FIFO, least recently used first for LRU), and **F** marks a page fault.\n\n" % (len(refs), k)
    res = {}
    for name, f, note in algos:
        out, faults = f(refs, k); res[name] = faults
        s += "**%s** - %s\n\n" % (name, note) + trace_md(out, k) + "\n\n**%s: %d page faults** (hit ratio %d/%d).\n\n" % (name, faults, len(refs) - faults, len(refs))
    s += "| Algorithm | " + " | ".join(res) + " |\n|---|" + "---|" * len(res) + "\n| Page faults | " + " | ".join(str(v) for v in res.values()) + " |\n\nOptimal gives the fewest faults (it looks ahead, so it is a benchmark that cannot be built in a real system); LRU approximates it; FIFO is the simplest and can even show Belady's anomaly.\n"
    return s

def storage_cost(a_name, a_cap_mb, a_cost, b_name, b_cap_mb, b_cost, file_mb):
    ca = a_cost / a_cap_mb * file_mb; cb = b_cost / b_cap_mb * file_mb
    s = "Taking decimal units (1 TB = 1,000,000 MB, 1 GB = 1000 MB): cost of storing the file = (price / capacity in MB) $\\times$ file size.\n\n"
    s += "$$\\begin{gathered}\\text{%s: }\\ \\frac{%d}{%s}\\times%d = \\text{NPR }%.3f \\\\ \\text{%s: }\\ \\frac{%d}{%s}\\times%d = \\text{NPR }%.3f\\end{gathered}$$\n\n" % (a_name, a_cost, format(a_cap_mb, ","), file_mb, ca, b_name, b_cost, format(b_cap_mb, ","), file_mb, cb)
    cheap, cc, cd = (a_name, ca, cb) if ca < cb else (b_name, cb, ca)
    s += "**%s is more cost-efficient**: it is cheaper by NPR %.2f for this file (NPR %.2f against NPR %.2f), i.e. %.1f times cheaper per byte (%.0f %% less). Cost per GB: %s NPR %.2f, %s NPR %.2f. (With binary units, 1 TB = 1,048,576 MB, the figures change slightly but the conclusion is the same.)\n" % (cheap, cd - cc, cc, cd, cd / cc, (1 - cc / cd) * 100, a_name, a_cost / a_cap_mb * 1000, b_name, b_cost / b_cap_mb * 1000)
    return s

ATOMIC = """**Stable storage and atomic writes.** A disk write is *not* atomic: a crash or power cut in the middle of writing a block leaves a half-old, half-new (torn) block, or a metadata update that is only partly done. **Stable storage** is storage that survives such failures: every write is either done completely or not done at all. It is built on **atomic writes**:

1. Write the data to a *separate* place first (a log/journal, a second copy or a new block), never over the only valid copy.
2. Flush it and write a small **commit record** (a single sector write is atomic).
3. Only after the commit, apply it to the real location (or switch a pointer).
4. On recovery after a crash, the OS inspects the log: committed records are **redone**, uncommitted ones **discarded/undone**.

Classic realisations: the *two-copy stable-storage scheme* (write copy 1, verify with checksum, then copy 2; recovery copies the good one over the bad one), *journaling* file systems (ext4, NTFS), *copy-on-write* file systems (ZFS, Btrfs) and database write-ahead logs. The result is all-or-nothing updates and a consistent file system after a crash."""

RAID = """**RAID (Redundant Array of Independent Disks)** combines several physical disks into one logical volume to get higher **speed** (parallel reads/writes, striping), **reliability** (redundancy: mirroring or parity) or both. The OS or a controller spreads data in stripes over the disks.

| Level | Method | Usable capacity ($n$ disks) | Fault tolerance | Remarks |
|---|---|---|---|---|
| RAID 0 | striping only | $n$ | none | fastest, any disk failure loses all |
| RAID 1 | mirroring | $n/2$ | 1 disk per pair | simple, 100 % overhead |
| RAID 5 | striping + distributed parity | $n-1$ | 1 disk | good read speed, slower writes |
| RAID 6 | striping + double parity | $n-2$ | 2 disks | for large arrays |
| RAID 10 | mirror of stripes | $n/2$ | 1 per mirror pair | fast and safe, expensive |

**Write-Ahead Logging (WAL).** Before any change is made to the data on disk, a *log record* describing the change (transaction id, old value, new value) is first written to a sequential log on stable storage, and the log is forced to disk at commit time. The data pages themselves may be written lazily later. After a crash the system *replays* the log: committed transactions are **redone**, uncommitted ones are **undone**. Because the log write is a single sequential append and the commit record is one atomic sector write, an update is either completely visible or completely absent: this gives the atomic writes that stable storage needs, and it also speeds things up (sequential log writes instead of many random writes). Journaling file systems, databases and RAID write-hole protection use WAL."""

CONTIG = """**Contiguous allocation.** Each file occupies a set of consecutive disk blocks; the directory entry stores only the **start block** and the **length**.

| Advantages | Disadvantages |
|---|---|
| Very simple to implement and to manage (start + length) | **External fragmentation**: free space breaks into small holes; compaction is slow |
| Excellent performance: sequential access needs minimal seeks, the whole file can be read in one transfer | The file size must be known when it is created; a file cannot easily **grow** (it may have to be copied to a bigger hole) |
| **Direct (random) access** is trivial: block $i$ is at address $b + i$ | Over-estimating the size wastes space (internal fragmentation) |
| Only one seek is needed to reach the file; good for read-only media (CD/DVD) | Finding a hole for a new file needs first-fit / best-fit / worst-fit search |"""

FILE_ATTR = """**File attributes (metadata).** Information the OS keeps about every file, stored in the directory entry or the inode: **name** (human-readable), **identifier** (unique tag such as the inode number), **type**, **location** (device and disk address), **size**, **protection** (read/write/execute permissions for owner, group, others), and **time, date and owner** (creation, last access and last modification times, user id)."""

FILE_ALLOC = """**File allocation methods** (how the blocks of a file are placed on the disk):

| Method | How it works | Pros | Cons |
|---|---|---|---|
| **Contiguous** | file in consecutive blocks; directory holds start and length | fast sequential and direct access, simple | external fragmentation, file cannot grow easily |
| **Linked** | each block holds a pointer to the next; directory holds first (and last) block | no external fragmentation, files grow easily | no efficient direct access, pointer overhead, one bad pointer breaks the file (FAT keeps the links in a table in memory to fix this) |
| **Indexed** | an *index block* holds the addresses of all the file's blocks (Unix inode: direct, single, double, triple indirect) | direct access without fragmentation, grows easily | index-block overhead, large files need multi-level indexes |"""

CRYPTO = """**Cryptography** converts readable *plaintext* into unreadable *ciphertext* with a key, to give confidentiality, integrity, authentication and non-repudiation.

**Private-key (symmetric) cryptography.** One **secret key** is used by both sender and receiver for encryption and decryption: $C = E_K(P)$, $P = D_K(C)$. It is fast and suited to bulk data, but the key must be shared securely beforehand and each pair of users needs its own key ($n(n-1)/2$ keys for $n$ users). *Examples:* AES, DES, 3DES, ChaCha20 (disk encryption, VPN data, HTTPS data transfer).

**Public-key (asymmetric) cryptography.** Every user has a **key pair**: a *public key* (published) and a *private key* (kept secret); what one key encrypts only the other can decrypt. To send a confidential message, encrypt with the receiver's public key; the receiver decrypts with the private key. To sign, the sender encrypts a hash with the *private* key and anybody can verify with the public key. It is slower than symmetric encryption and is used for key exchange, digital signatures and certificates. *Examples:* RSA, ECC, Diffie-Hellman.

*Small RSA example.* Choose primes $p = 3$, $q = 11$: $n = pq = 33$, $\\varphi = (p-1)(q-1) = 20$. Take $e = 7$ (coprime with 20) and $d$ with $ed \\equiv 1 \\pmod{20}$: $d = 3$. Public key $(7, 33)$, private key $(3, 33)$. Encrypt $M = 4$: $C = 4^{7} \\bmod 33 = 16$. Decrypt: $M = 16^{3} \\bmod 33 = 4096 \\bmod 33 = 4$ ✓.

| | Private-key | Public-key |
|---|---|---|
| Keys | one shared secret | public + private pair |
| Speed | fast | slow |
| Key distribution | difficult | easy (public key is open) |
| Use | bulk encryption | key exchange, signatures |

In practice both are combined (a hybrid, as in TLS/HTTPS): public-key cryptography exchanges a session key, then symmetric cryptography encrypts the data."""

ATTACKS = """**Types of attacks on a system** (security threats):

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

Defences: authentication, access control, least privilege, patches, firewalls, anti-malware, encryption, sandboxing and logging."""

DOCKER_K8S = """**Containerization** packages an application together with its libraries and dependencies into a lightweight, isolated unit called a **container**. Containers share the host operating-system kernel (no guest OS per container), so they start in seconds and use far less memory than virtual machines. Isolation comes from Linux **namespaces** (separate process, network, mount and user views) and **cgroups** (limits on CPU, memory and I/O).

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

Together: Docker packages the application, Kubernetes deploys, scales, heals and updates it across many machines (micro-service architecture)."""

HYPERVISOR = """**Hypervisor (virtual machine monitor).** Software that creates and runs virtual machines by sharing the physical CPU, memory, disk and network among several guest operating systems, each of which believes it has a whole machine.

| Basis | Type 1 (bare-metal, native) | Type 2 (hosted) |
|---|---|---|
| Runs on | directly on the hardware, no host OS | as an application on a host OS |
| Layers | hardware → hypervisor → guest OS | hardware → host OS → hypervisor → guest OS |
| Performance | high, little overhead, direct hardware access | lower, every request goes through the host OS |
| Security / isolation | better (small attack surface) | depends on the host OS |
| Use | data centres, cloud servers, production | desktops, testing, learning |
| Examples | VMware ESXi, Microsoft Hyper-V, Xen, KVM (Linux) | Oracle VirtualBox, VMware Workstation/Player, Parallels |"""

CASE_LINUX = """The OS studied in the course is taken as **Linux**.

**Real-world application:** Linux runs the **web servers and cloud data centres** of the big internet companies, **Android** phones (Linux kernel) and all of the world's top-500 supercomputers.

**Why it is suitable.** It is free and open source (low cost, can be customised), highly **stable** (servers run for years without reboot), **multi-user and multi-tasking** with strict file permissions, **secure** (least privilege, SELinux/AppArmor, quick patches), **scalable** from tiny devices to thousands of cores, and it supports a huge range of hardware and server software (Apache, nginx, Docker, Kubernetes)."""

SHORT_T1 = """**(a) Type 1 hypervisor.** A bare-metal hypervisor installed directly on the server hardware that schedules the virtual machines itself (VMware ESXi, Hyper-V, Xen, KVM). Each VM has virtual CPUs, memory and devices; the hypervisor traps privileged instructions (hardware assist Intel VT-x / AMD-V) and isolates VMs from each other. Benefits: near-native speed, strong isolation, live migration, consolidation of many servers on one machine, which is the basis of cloud computing."""
SHORT_SB = """**(b) Secure Boot.** A UEFI feature that lets only trusted, digitally signed software run during start-up. The firmware holds a database of trusted keys (PK, KEK, db) and a revocation list (dbx); it checks the signature of the boot loader, and the loader checks the kernel and drivers (a *chain of trust*). Unsigned or tampered code (a boot-kit or rootkit) is refused. It protects the pre-OS stage; it can be disabled for dual-boot or custom kernels in the firmware set-up."""
SHORT_SBX = """**Sandboxing.** Running a program in a restricted, isolated environment so that a bug or malicious code cannot damage the rest of the system. The sandbox limits file access, network, system calls and memory (by namespaces/cgroups, `seccomp`, jails, virtual machines, the browser tab sandbox or the Android app sandbox with a separate user id for every app). It is used for testing untrusted software, malware analysis, running web content and mobile apps, and it applies the principle of least privilege."""
SHORT_PS = """**PowerShell.** Microsoft's command-line shell and scripting language (built on .NET, cross-platform since PowerShell 7). Its commands, **cmdlets**, follow a *Verb-Noun* pattern (`Get-Process`, `Stop-Service`, `Get-ChildItem`) and pass **objects**, not text, through the pipeline (`Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU`). It is used for system administration and automation, remote management (WinRM/SSH remoting), configuration (Desired State Configuration) and scripting with variables, loops and functions; because of its power, attackers also misuse it, so execution policy and script logging are used."""
SHORT_TH = """**Thrashing.** A condition in which the system spends more time **swapping pages in and out** than executing, so CPU utilisation collapses. *Cause:* the total working sets of the running processes exceed the physical memory; each page fault evicts a page that is soon needed again, so the fault rate becomes very high; the OS sees low CPU use and wrongly adds more processes, making it worse. *Cure:* the **working-set model** (give each process enough frames for its working set), **page-fault-frequency control**, local replacement, reducing the degree of multiprogramming (suspend/swap-out processes) and adding RAM."""

# ---------------------------------------------------------------- paper A: 2083 Baishakh
def paper_a():
    procs = [("P1", 0, 10), ("P2", 2, 5), ("P3", 4, 2), ("P4", 4, 5), ("P5", 0, 8)]
    sj_s, sj_r = sjf_np(procs); sr_s, sr_r = srtf(procs); rr_s, rr_r = rr(procs, 4)
    al = [[2, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]]
    mx = [[3, 2, 1, 1], [1, 2, 0, 2], [1, 1, 2, 0], [3, 2, 1, 0], [2, 1, 0, 1]]
    refs = [1, 2, 3, 2, 1, 5, 2, 1, 6, 2, 5, 6, 3, 1, 3, 6, 1, 2, 4, 3]
    d = FM.format(code="ENCT254", tag="2083-Baishakh", yr="2083 Baishakh", ad="2026", kind="Back")
    d += """@q 1
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

"""
    d += "@s 1\n**UEFI against Legacy boot.**\n\n" + UEFI_TABLE + "\n\n" + OS_ABSTRACTION + "\n\n" + FIG_LAYERS + "\n"
    d += "@s 2\n**Process control block (PCB).** The PCB (task control block) is the data structure the OS keeps for every process; it is created with the process, linked in the scheduling queues, and saved/restored at every context switch. Its components:\n\n"
    d += """| Component | Content |
|---|---|
| Process identification | process ID (PID), parent PID, user ID/group ID |
| Process state | new, ready, running, waiting, terminated |
| Program counter | address of the next instruction to execute |
| CPU registers | accumulator, index registers, stack pointer, flags - saved when the process is pre-empted |
| CPU-scheduling information | priority, pointers to scheduling queues, time slice used |
| Memory-management information | base/limit registers, page-table or segment-table pointers |
| Accounting information | CPU time used, time limits, job number |
| I/O status information | list of open files, allocated I/O devices, pending I/O requests |

"""
    d += "**Given:** five processes (times in ms). P1 and P5 arrive together at 0 and P3, P4 together at 4; ties are broken in the listed order (FCFS).\n\n"
    d += "**(i) Shortest Job First (non-pre-emptive).** At each completion the shortest job among the arrived ones is chosen. At $t = 0$ only P1 (10) and P5 (8) are present: P5 runs first. At $t = 8$ the ready jobs are P1 (10), P2 (5), P3 (2), P4 (5): P3 (shortest) runs to 10; at $t = 10$ P2 and P4 (both 5, P2 arrived earlier) then P1 (10).\n\n"
    d += gantt(sj_s, "SJF (non-pre-emptive) Gantt chart: " + seg_text(sj_s)) + "\n" + sched_table(sj_r)
    a_t, a_w = avg(sj_r)
    d += "\n$$\\text{Average waiting time (SJF)} = \\frac{%s}{5} = %.1f\\ \\text{ms}$$\n\n" % (" + ".join(str(r[5]) for r in sj_r), a_w)
    d += "Average turnaround time = %.1f ms. *If the pre-emptive form (SRTF) is intended:* the order is %s; waiting times %s; average waiting time = **%.1f ms**.\n\n" % (a_t, seg_text(sr_s), ", ".join("%s = %d" % (r[0], r[5]) for r in sr_r), avg(sr_r)[1])
    d += "**(ii) Round Robin, quantum = 4 ms.** New arrivals join the ready queue before the pre-empted process: the queue starts P1, P5; after P1's first slice it is P5, P2, P3, P4, P1, and so on.\n\n"
    rs = sorted(rr_r, key=lambda r: r[0])
    d += gantt(rr_s, "Round Robin (q = 4) Gantt chart: " + seg_text(rr_s)) + "\n" + sched_table(rs)
    ra_t, ra_w = avg(rr_r)
    d += "\n$$\\text{Average waiting time (RR)} = \\frac{%s}{5} = %.1f\\ \\text{ms}$$\n\n" % (" + ".join(str(r[5]) for r in rs), ra_w)
    d += "Average turnaround time = %.1f ms.\n\n| Algorithm | Average waiting time | Average turnaround |\n|---|---|---|\n| SJF | %.1f ms | %.1f ms |\n| Round Robin (q = 4) | %.1f ms | %.1f ms |\n\nSJF gives the smallest average waiting time (it is optimal for a given set of ready jobs) but the long job P1 waits longest; Round Robin is fairer with better response time but a larger average waiting time.\n\n" % (ra_t, a_w, a_t, ra_w, ra_t)
    d += "@s 3\n**(a)**\n\n" + CRIT + "\n\n" + SEM_BODY + "\n\n**(b)**\n\n" + DINING + "\n\n**Banker's algorithm (is the state safe?).**\n\n" + banker_section(["R0", "R1", "R2", "R3"], al, mx, [6, 4, 4, 2]) + "\n"
    d += "@s 4\n**(a)**\n\n" + ATOMIC + "\n\n**Cost of storing the 100 MB file.**\n\n" + storage_cost("SATA HDD (1 TB)", 1000000, 5700, "SATA SSD (256 GB)", 256000, 7500, 100) + "\n"
    d += "**(b)** " + paging_section(refs, 3, [("FIFO", fifo, "replace the page that has been in memory longest"), ("LRU", lru, "replace the page unused for the longest time in the past"), ("Optimal", opt, "replace the page whose next use is farthest in the future")]) + "\n"
    d += "@s 5\n" + CONTIG + "\n\n"
    d += "@s 6\n" + CRYPTO + "\n\n"
    d += "@s 7\n" + DOCKER_K8S + "\n\n"
    d += "@s 8\n" + CASE_LINUX + "\n\n"
    d += "@s 9\n*(Any two are required; all four are answered.)*\n\n" + SHORT_T1 + "\n\n" + SHORT_SB + "\n\n(c) " + SHORT_SBX + "\n\n(d) " + SHORT_PS + "\n"
    return d

# ---------------------------------------------------------------- paper B: 2082 Bhadra
def paper_b():
    procs = [("A", 0, 12), ("B", 2, 8), ("C", 5, 7), ("D", 10, 9)]
    hr_s, hr_r, hr_t = hrrn(procs); rr_s, rr_r = rr(procs, 4)
    al = [[2, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]]
    mx = [[3, 2, 1, 1], [1, 2, 0, 2], [1, 1, 2, 0], [3, 2, 1, 0], [2, 1, 0, 1]]
    refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    d = FM.format(code="ENCT254", tag="2082-Bhadra", yr="2082 Bhadra", ad="2025", kind="Regular")
    d += """@q 1
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

"""
    d += "@s 1\n**MBR against GPT.**\n\n" + MBR_TABLE + "\n\n" + OS_ABSTRACTION + "\n\n" + FIG_LAYERS + "\n"
    d += "@s 2\n**Process states.** From creation to termination a process passes through these states:\n\n"
    d += """| State | Meaning |
|---|---|
| **New** | the process is being created (PCB and address space set up) |
| **Ready** | in memory, has everything it needs except the CPU, waiting in the ready queue |
| **Running** | its instructions are being executed on the CPU |
| **Waiting (blocked)** | waiting for an event such as I/O completion or a signal |
| **Terminated** | finished execution; the OS reclaims its resources |

Transitions: new → ready (*admitted*); ready → running (*scheduler dispatch*); running → ready (*interrupt / time quantum expired* or pre-emption); running → waiting (*I/O or event wait*); waiting → ready (*I/O or event completion*); running → terminated (*exit*). Systems with swapping add the *suspended ready* and *suspended wait* states.

"""
    d += FIG_STATES + "\n"
    d += "**(i) HRRN (Highest Response Ratio Next, non-pre-emptive).** Response ratio $RR = \\dfrac{W + B}{B}$ ($W$ = waiting time so far, $B$ = burst time); when the CPU becomes free the ready process with the highest ratio runs to completion.\n\n"
    d += "| Time | Ready processes | Response ratios | Chosen |\n|---|---|---|---|\n"
    ch = {0: "A", 12: "B", 20: "C", 27: "D"}
    for t, lst in hr_t:
        d += "| %d | %s | %s | **%s** |\n" % (t, ", ".join(x[0] for x in lst), "; ".join("%s = %.3f" % x for x in lst), ch[t])
    d += "\n(For example at $t = 12$: B: $(10 + 8)/8 = 2.25$, C: $(7 + 7)/7 = 2.0$, D: $(2 + 9)/9 = 1.22$; at $t = 20$: C: $(15 + 7)/7 = 3.14$, D: $(10 + 9)/9 = 2.11$.)\n\n"
    d += gantt(hr_s, "HRRN Gantt chart: " + seg_text(hr_s)) + "\n" + sched_table(hr_r)
    h_t, h_w = avg(hr_r)
    d += "\n$$\\begin{gathered}\\text{Average turnaround time} = \\frac{%s}{4} = %.2f\\ \\text{ms} \\\\ \\text{Average waiting time} = \\frac{%s}{4} = %.2f\\ \\text{ms}\\end{gathered}$$\n\n" % (" + ".join(str(r[4]) for r in hr_r), h_t, " + ".join(str(r[5]) for r in hr_r), h_w)
    d += "**(ii) Round Robin, quantum = 4 ms.** The ready queue starts with A; B arrives at 2 and joins the queue before A returns after its first slice, C (at 5) and D (at 10) join in the same way.\n\n"
    rs = sorted(rr_r, key=lambda r: r[0])
    d += gantt(rr_s, "Round Robin (q = 4) Gantt chart: " + seg_text(rr_s)) + "\n" + sched_table(rs)
    r_t, r_w = avg(rr_r)
    d += "\n$$\\begin{gathered}\\text{Average turnaround time} = \\frac{%s}{4} = %.2f\\ \\text{ms} \\\\ \\text{Average waiting time} = \\frac{%s}{4} = %.2f\\ \\text{ms}\\end{gathered}$$\n\n" % (" + ".join(str(r[4]) for r in rs), r_t, " + ".join(str(r[5]) for r in rs), r_w)
    d += "| Algorithm | Avg turnaround | Avg waiting |\n|---|---|---|\n| HRRN | %.2f ms | %.2f ms |\n| Round Robin (q = 4) | %.2f ms | %.2f ms |\n\nHRRN has the lower averages here and avoids starvation (a waiting process's ratio keeps rising); Round Robin gives every process the CPU regularly, so it has better response time but more context switches.\n\n" % (h_t, h_w, r_t, r_w)
    d += "@s 3\n**(a) Race condition.** A situation in which two or more processes/threads access and change shared data concurrently, and the final result depends on the *order* in which their instructions are interleaved. Example: `counter++` is compiled to *load, add, store*. With `counter = 5`, if a producer and a consumer both load 5, one computes 6 and the other 4, and whichever stores last wins, so the result is 6 or 4 instead of 5. The cure is to make the access a critical section protected by a semaphore or mutex.\n\n" + SEM_BODY + "\n\n"
    d += "**(b) Banker's algorithm.**\n\n" + banker_section(["R1", "R2", "R3", "R4"], al, mx, [6, 4, 4, 2]) + "\n"
    d += "@s 4\n**(a)**\n\n" + RAID + "\n\n**Cost of storing the 160 MB file.**\n\n" + storage_cost("NVMe SSD (2 TB)", 2000000, 15000, "SATA SSD (1 TB)", 1000000, 5500, 160) + "\n"
    d += "**(b)** " + paging_section(refs, 3, [("FIFO", fifo, "replace the oldest page"), ("Optimal", opt, "replace the page not used for the longest time in the future"), ("LRU", lru, "replace the least recently used page")]) + "\n"
    d += "@s 5\n" + FILE_ATTR + "\n\n" + FILE_ALLOC + "\n\n"
    d += "@s 6\n" + ATTACKS + "\n\n"
    d += "@s 7\n" + HYPERVISOR + "\n\n"
    d += "@s 8\n**Case study OS: Linux.** Two key features:\n\n1. **Pre-emptive, fair multitasking scheduler (CFS / EEVDF) with a virtual-memory system.** The kernel gives every runnable task a fair share of CPU time (weighted by priority/nice value), pre-empts long-running tasks and uses demand paging with a page cache. *Contribution:* many programs run smoothly together, interactive tasks stay responsive, and RAM is used efficiently (unused memory caches disk data), which improves **performance**.\n2. **Journaling file system with Unix permissions (ext4) and a modular kernel.** Each file has owner/group/other read-write-execute permissions, and ext4 logs metadata changes (write-ahead journal) so the file system is consistent after a crash; drivers load as modules without rebooting. *Contribution:* strong **security and reliability**, quick crash recovery and flexible hardware support, which improve **usability** and uptime.\n\n"
    d += "@s 9\n*(Any two are required; all four are answered.)*\n\n(a) " + DOCKER_K8S + "\n\n(b) " + SHORT_TH + "\n\n(c) " + SHORT_SBX + "\n\n(d) " + SHORT_PS + "\n"
    return d

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ioe-enct254-2083-baishakh.md"), "w").write(paper_a())
open(os.path.join(OUT, "ioe-enct254-2082-bhadra.md"), "w").write(paper_b())
print("written")
