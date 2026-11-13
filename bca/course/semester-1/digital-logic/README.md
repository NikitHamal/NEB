# Digital Logic — BCA 103 (old code CACS105)

Semester I (revised curriculum, 2082 batch) · 3 credits. The same subject is CACS105 in the 2074 curriculum.

| Unit | Title | TU syllabus unit |
|---|---|---|
| 1 | Introduction: Digital Signals, Logic Levels and the Clock | Unit 1 Introduction (digital signals and waveforms, digital logic operations, digital computer and ICs, clock waveform) |
| 2 | Number Systems, Binary Arithmetic and Codes | Unit 2 Number Systems (5 h): conversions, signed numbers, floating point, binary arithmetic, BCD, ASCII, Excess-3, Gray, error detecting and correcting codes |
| 3 | Combinational Logic Design | Unit 3 (16 h): gates, universal gates, Boolean algebra, canonical forms, K-maps, SOP/POS, encoders/decoders, adders, MUX/DEMUX, parallel adder, parity, programmable logic |
| 4 | Flip-Flops, Counters and Registers | Unit 4 (16 h): RS, JK, master-slave, D, T, triggering, excitation tables, ripple/ring/modulus counters, synchronous design, digital watch, frequency counter, shift registers |
| 5 | Sequential Logic Design: State Machines | Unit 5 (6 h): sequential machine models, state diagram, state reduction, flip-flop realisation, counter design |

Laboratory work in the TU syllabus (gates from discrete components, half/full adder, 16:1 MUX, 1:16 DEMUX, digital watch with counters, shift registers) is covered by the circuits designed in units 3 and 4; build them on a breadboard or in a free simulator (Logisim-evolution, Falstad).

## Verification

- Every conversion, complement, IEEE-754 encoding, Gray code and Hamming codeword in unit 2 was checked with a script (`int`, `struct.pack`).
- Every K-map answer in unit 3 was checked against SymPy's minimiser (`SOPform`), including the don't-care case.
- The MOD-3 JK counter, the 2-bit Gray counter, the Johnson counter, the overlapping and non-overlapping "101" detectors and the "11" detector in units 4 and 5 were simulated bit by bit and the printed state sequences and outputs match.

## Additions (session 46)

- Unit 1: logic-family parameters with worked fan-out, power-delay and CMOS dynamic-power numbers; totem-pole, open-collector (pull-up sizing) and tri-state outputs; Schmitt trigger and debouncing; sampling, quantisation and SNR.
- Unit 3: five-variable maps, Quine-McCluskey, static hazards, BCD adder and carry-lookahead worked through, BCD to seven-segment design.
- Unit 4: up/down and presettable counters, frequency division and the digital-watch chain, metastability and synchronisers, LFSR.
- Unit 5: analysis of a given circuit, Mealy/Moore conversion, state assignment, traffic-light controller.
- These go beyond the printed TU outline (QM, hazards, LFSR, metastability are standard textbook extensions) and are marked as extensions in the text. Every number was recomputed by `bca/tools/check_digital.py`.

## Source and honesty

Unit titles, hours and topic lists follow the CACS105 Digital Logic syllabus as reproduced on benchpartner.com, notebahadur.com and the college micro-syllabus (neporesult.com), which agree with each other. The revised BCA 103 PDF itself could not be retrieved; the new subject is a re-coding of CACS105 as far as the secondary sources show. **Diagrams are given as text tables and ASCII; this book contains no gate-level drawings**, so draw each circuit by hand as you read the equations. TU's marks distribution per unit is not stated here because it was not found in a primary source.
