# Operating Systems — BCA 251 (Semester IV, 3 credits)

Old code CACS251 (2074 curriculum, Semester IV, 3 credits: 45 teaching hours, plus tutorial and 2 lab hours per week).

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to Operating Systems | 2 |
| 2 | Operating System Structure | 2 |
| 3 | Process Management (processes, threads, IPC and synchronization, scheduling) | 15 |
| 4 | Deadlocks | 4 |
| 5 | Memory Management (basic memory management, virtual memory) | 7 |
| 6 | Input/Output Device Management (I/O hardware and software, disks) | 4 |
| 7 | File System Interface Management | 2 |
| 8 | Security Management | 3 |
| 9 | Distributed Operating Systems | 4 |
| 10 | Case Study: DOS, Windows, UNIX and Linux | 2 |

## Verification

- `bca/tools/check_os.py` recomputes every table in Units 3 to 6 and asserts the headline numbers: FCFS, SJF, SRTF, round robin (two sets), non-preemptive priority and HRRN; the Banker's safety algorithm, the three requests and the detection example; disk scheduling (FCFS, SSTF, SCAN both directions, LOOK, C-SCAN, C-LOOK); FIFO, OPT, LRU, second chance and Belady's anomaly; first/best/worst fit; address translation, TLB and demand-paging effective access times; and the answers to the numerical practice questions.
- `bca/tools/check_os_misc.py` recomputes the numbers of Units 7 to 9 (inode reach, password search times, the RFC 4226 HOTP test vectors, TOTP test vector, Cristian and Berkeley clocks, Lamport timestamps).
- The six runnable C programs in Unit 3 (`fork`/`waitpid`, a pipe, POSIX threads, a race condition with and without a mutex, a semaphore bounded buffer, dining philosophers) were compiled with `gcc -std=c11 -Wall` (gcc 12, glibc 2.36) and run; the output blocks are the real output. The race-condition line is non-deterministic by nature (this run lost about 33,000 of 2,000,000 increments), and it will differ on your machine.
- Shell output in Units 7 and 10 (`ls -l`, `stat`, `chmod`, `umask`, `/proc/self/status`) is the real output of a Linux 6.1 sandbox.
- **Bugs the scripts caught while writing:** (1) the Banker's safe sequence found by scanning from P0 is ⟨P1, P3, P0, P2, P4⟩, not the textbook's ⟨P1, P3, P4, P0, P2⟩ (both are valid; the text now says so); (2) the draft claimed P0's request (0, 2, 0) is unsafe in the *original* state; it is safe there and unsafe only *after* P1's grant, so the text was rewritten with the chained scenario; (3) SCAN going down first is 236 cylinders, not the 235 first assumed, and a C-SCAN that does not count the return jump is 183; (4) two hand-worked practice answers were wrong (first/best/worst fit set, and the 12-reference FIFO/LRU/OPT counts, which are 9, 9 and 7); (5) the disk-time practice answer was 17.65 ms, not 17.66.

## Source and honesty

Unit titles, topics and hours are the TU **CACS251** syllabus as reproduced on notebahadur.com (see `bca/SOURCES.md`). The revised BCA 251 PDF was not retrievable; the 2074 outline is used as the proxy. The old outline numbers its units 1–10 with the file-system and security units as 7 and 8; that numbering is kept. The page-based mirror shows unit 3 containing "Process Scheduling (5 hrs)" and "Inter-Process Communication and Synchronization (6 hrs)" as sub-parts, so they are chapters 3.3 and 3.4 here. The syllabus term "Block Mapping vs Direct Mapping" is ambiguous across textbooks; Section 5.2 states the reading adopted. Text books named by TU: Tanenbaum, *Modern Operating Systems* and Silberschatz, Galvin and Gagne, *Operating System Concepts*; all explanations here are original.

## Layout notes from the PDF QA

See the build record in `bca/course/CHANGELOG_BCA_COURSE.md`.
