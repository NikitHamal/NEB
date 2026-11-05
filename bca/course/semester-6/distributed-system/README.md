# Distributed System — BCA 355 (Semester VI, 3 credits)

Architectures and goals of distributed systems, communication (sockets, RPC, RMI, gRPC, marshalling, message queues), physical and logical time, mutual exclusion and election, distributed transactions and deadlocks, replication, consistency models and consensus (Paxos, Raft), fault tolerance (Byzantine agreement, snapshots) and distributed file systems (NFS, AFS, GFS, HDFS). 50 teaching hours in this reconstruction (old TU CACS352 *Distributed System*; revised list BCA 355).

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction, Goals, Architectures and Naming | 7 |
| 2 | Communication: Sockets, RPC, RMI, gRPC and Message Queues | 8 |
| 3 | Time, Clocks and Global State | 8 |
| 4 | Coordination: Mutual Exclusion and Leader Election | 7 |
| 5 | Distributed Transactions and Concurrency Control | 7 |
| 6 | Replication, Consistency Models and Consensus | 8 |
| 7 | Fault Tolerance and Distributed File Systems | 5 |

## Verification

`bca/tools/check_distributed.py` plus `fill_script_outputs.py`: every Python block in the book is **executed** and its output inserted; the checker then recomputes every printed line with independent code or closed forms and `--verify` demands that each expected line is present. Independent references: popcount of the clockwise distance for Chord hop counts; the Cristian, Berkeley and NTP formulas written out from the definitions; a happened-before graph with transitive closure to validate every Lamport and vector-clock comparison; Ricart–Agrawala message totals 2N(N−1) and the (timestamp, id) entry order; grid-quorum intersection by brute force; Bully and Ring message counts by closed form; two-phase commit decisions; a Floyd–Warshall closure on the wait-for graph; a permutation search for linearizability and sequential consistency; exhaustive enumeration of read/write quorum pairs; Raft commit index from sorted match indexes; the OM(1) Byzantine algorithm checked against every traitor strategy at n = 3 and n = 4 plus the 3f + 1 table; a conserved-total check on the Chandy–Lamport snapshot; and exact `math.comb` arithmetic for HDFS block loss. All practice answers computed by hand in the text are asserted too.

## Source and honesty

No TU unit list for BCA 355 was retrieved; the seven units are a reconstruction from the topic list in the course brief and the standard chapters of Tanenbaum and van Steen, *Distributed Systems*, and Coulouris et al., *Distributed Systems: Concepts and Design*. Check the official TU syllabus for the examined scope.
