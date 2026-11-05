# Cyber Security and Ethical Hacking — BCA 401 (Semester VII, 3 credits)

A defender's and auditor's course: foundations, the CIA triad, threat modelling and CVSS scoring; network protocol analysis and discovery governance; authentication, entropy, key derivation and access control; secure application engineering; network defence architecture (DNSSEC, Wi-Fi key hierarchy, rate limiting, ACLs); intrusion detection statistics, incident response and digital forensics; security audits, penetration-test rules of engagement and Nepal's cyber law.

| Unit | Title | Hours |
|---|---|---|
| 1 | Foundations, the CIA Triad, Threat Modelling and CVSS Scoring | 6 |
| 2 | Network Protocol Analysis, TCP Flag Math and Asset Discovery Governance | 6 |
| 3 | Authentication, Entropy, Key Derivation and Access Control Models | 7 |
| 4 | Secure Application Engineering | 8 |
| 5 | Network Defence Architecture, DNSSEC, Wi-Fi Keys, Rate Limiting and ACLs | 6 |
| 6 | Intrusion Detection, Alert Statistics, Incident Response and Digital Forensics | 6 |
| 7 | Security Audits, Penetration Testing Rules of Engagement and Nepal Cyber Law | 6 |

## Verification

`bca/tools/check_cybersec.py` plus `fill_script_outputs.py`: every Python block is executed and its output inserted; the checker validates them independently (published CVSS v3.1 reference scores for the six vectors, hand-written truth tables for SameSite and ACL decisions, the IEEE 802.11i PMK test vector, coreutils `sha256sum`, an exact-product birthday search, an arrival-curve model of the token bucket, exact fractions for Bayes and sampling) and `--verify` demands every expected line and prose figure is present.

## Scope and safety

The book is deliberately **defensive, analytical and mathematical**: it contains no exploit strings, attack payloads, password-cracking code or packet-crafting tools. Offensive topics appear only as categories to defend against, as detection rules or as governance (authorisation, rules of engagement, law).

## Legal note

Penalty figures for the Electronic Transactions Act 2063 are the commonly reported maxima (Sections 44, 45, 46: 3 years / Rs 2 lakh; 47: 5 years / Rs 1 lakh; 52 computer fraud: 2 years / Rs 1 lakh). Secondary sources disagree on some labels; this is study material, not legal advice. National Cyber Security Policy 2080 is summarised from public reporting; the proposed IT and Cyber Security Bill had not been enacted at the time of writing.
