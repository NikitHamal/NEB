# Microprocessor and Computer Architecture — BCA 152 (Semester II, 3 credits)

From the Intel 8085 and assembly programming up to pipelines and multiprocessors: how a computer is built and why it is fast.

| Unit | Title |
|---|---|
| 1 | Microprocessors and the Intel 8085 |
| 2 | 8085 Instruction Set and Assembly Programming |
| 3 | Basic Computer Architecture |
| 4 | Microprogrammed and Hardwired Control |
| 5 | Central Processing Unit and Computer Arithmetic |
| 6 | Input–Output Organisation |
| 7 | Memory Organisation |
| 8 | Pipelining, Vector Processing and Multiprocessors |

## Verification

`bca/tools/check_mpca.py` contains a small **8085 assembler and simulator** (real opcodes and T-state counts). It assembles and runs every assembly program in Unit 2 against the test data printed in the book (13 programs, plus delay-loop, stack, CALL/RET and flag examples) and prints the hex listings that were pasted into the book. It also recomputes Booth multiplication, restoring division, IEEE-754 encodings, pipeline speed-up, cache address splits and AMAT, FIFO/LRU/OPT page-fault counts (and Belady's anomaly), disk capacity, DMA timing and Amdahl's law. Running it also caught three of the author's own arithmetic slips (AMAT, effective access time, a page-fault answer), which were fixed in the text. The 8255 interfacing snippet was assembled but not executed (no port hardware in the simulator).

## Source and honesty

The official TU BCA 152 / CACS155 syllabus PDF was not retrievable. The unit structure follows two published syllabi that agree on content: the 2074 TU BCA CACS155 unit list (Fundamentals of microprocessor, 8085 instruction set and programming/delay/interfacing, basic computer architecture, microprogrammed control, CPU, pipeline/vector/multiprocessors) and the TU-style CDCSIT BIT151 syllabus (adds I/O organisation, DMA, memory organisation, cache and virtual memory, RISC/CISC, Flynn's classification). I/O and memory are given their own units because the BIT151 syllabus treats them as such. Hours per unit are not stated. The textbook "basic computer" and microprogram examples follow M. Morris Mano, *Computer System Architecture*, the reference text for this subject; the 8085 material follows Gaonkar's *Microprocessor Architecture, Programming and Applications with the 8085*.
