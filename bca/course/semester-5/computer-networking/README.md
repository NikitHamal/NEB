# Computer Networking — BCA 301 (Semester V, 3 credits)

Old code CACS303 (2074 curriculum, Semester V; the revised BCA list numbers it BCA 301). 45 teaching hours.

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to Computer Networks (types, topologies, OSI, TCP/IP, delay and throughput) | 4 |
| 2 | The Physical Layer (signals, Nyquist and Shannon, line coding, media, multiplexing, switching) | 7 |
| 3 | The Data Link Layer and LANs (framing, CRC, Hamming, ARQ, MAC protocols, Ethernet, Wi-Fi) | 12 |
| 4 | The Network Layer: Addressing and Routing (IPv4, CIDR, VLSM, IPv6, Dijkstra, distance vector, OSPF, BGP) | 10 |
| 5 | The Transport Layer (UDP, TCP, flow and congestion control) | 6 |
| 6 | The Application Layer (DNS, HTTP, FTP, e-mail, SNMP, Wireshark) | 4 |
| 7 | Network Security (cryptography, TLS, IPsec, firewalls) | 3 |

## Verification

`bca/tools/check_networking.py` recomputes and asserts every number in the book: delay and bandwidth–delay products, Nyquist and Shannon capacities, Manchester/NRZI/AMI encodings, T1 and E1 rates, bit stuffing (with an unstuffing round trip), CRC remainders for both worked examples, CRC-16 and CRC-32 check values (`zlib`), the IPv4 header checksum, Hamming codewords and syndromes (including the minimum distance of the (7,4) code over all 120 codeword pairs), stop-and-wait and sliding-window utilisation, the Go-Back-N and Selective Repeat transmission counts, ALOHA throughput, Ethernet slot time and backoff, every subnet row and the VLSM plan (Python `ipaddress`), supernet aggregation, longest-prefix match, fragmentation, IPv6 compression and EUI-64, Dijkstra and Bellman–Ford on the six-router network (both must agree for every pair of routers), count-to-infinity, Tahoe/Reno congestion windows, Jacobson's RTO, the Mathis throughput and the DNS message sizes. `--verify` checks that the key values appear in the unit files. Every ```python block in the units was executed with `fill_script_outputs.py` and its output is the real output (sockets, DNS wire format, a local HTTP exchange, `ip`, `ss` and `ping` on the build machine, and the cryptography examples).

**What the verification caught while writing:** (1) a first bit-stuffing function that replaced every "11111" by "111110" gave the wrong answer because the run counter must restart after a stuffed 0; (2) the distance from router A to C on the six-router network is 3, not the 4 first assumed (the path A → D → E → C, found by both Dijkstra and Bellman–Ford); (3) a first Go-Back-N count assumed that a lost frame 3 in a window of 4 costs extra frames, but the loss of the *last* frame of a window costs no more than Selective Repeat; the example now loses frame 2 (GBN 12 transmissions, SR 11); (4) a broken `struct` format in the DNS reply parser was found when the book code was executed.

## Source and honesty

The unit list follows the TU CACS303 syllabus as published (physical, data link, network, transport and application layers and network security; the course description names DNS, DHCP, WWW, HTTP, HTTPS, Telnet, FTP, SMTP, POP, IMAP, SNMP, MRTG, PRTG, Packet Tracer and Wireshark), see `bca/SOURCES.md`. The revised BCA 301 PDF was not retrievable; the exact hour split per unit is a reconstruction totalling the 45 hours. The order of material follows Tanenbaum's *Computer Networks* and Kurose and Ross's *Computer Networking: A Top-Down Approach*; all text and examples are original. RFC and IEEE figures (Ethernet slot time, TCP and DNS formats, OSPF cost formula, RIP limits, Wi-Fi interframe spaces) are standard published values. Satellite, optical-fibre attenuation and throughput comments are textbook typical values, not machine-checkable.
