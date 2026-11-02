#!/usr/bin/env python3
"""Verifier for BCA 152 Microprocessor and Computer Architecture.

Contains a small Intel 8085 assembler + simulator (the subset used in the book, with the real opcodes
and T-state counts), runs every assembly program printed in the book against its stated test data,
and recomputes the numeric examples (Booth multiplication, pipeline speed-up, cache/AMAT, address
splitting, FIFO/LRU page faults, two's complement ranges). Exit status 1 if any check fails.

    python3 bca/tools/check_mpca.py            # run checks
    python3 bca/tools/check_mpca.py --listing  # also print each program's hex listing + T-states
"""
import re, sys

REG = {"B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "M": 6, "A": 7}
RP = {"B": 0, "D": 1, "H": 2, "SP": 3, "PSW": 3}
COND = {"JNZ": 0xC2, "JZ": 0xCA, "JNC": 0xD2, "JC": 0xDA, "JPO": 0xE2, "JPE": 0xEA, "JP": 0xF2, "JM": 0xFA}
SIMPLE = {"XCHG": 0xEB, "RLC": 0x07, "RRC": 0x0F, "RAL": 0x17, "RAR": 0x1F, "CMA": 0x2F, "STC": 0x37,
          "CMC": 0x3F, "DAA": 0x27, "HLT": 0x76, "NOP": 0x00, "RET": 0xC9, "PCHL": 0xE9, "SPHL": 0xF9,
          "XTHL": 0xE3, "EI": 0xFB, "DI": 0xF3, "RIM": 0x20, "SIM": 0x30}
ALU = {"ADD": 0x80, "ADC": 0x88, "SUB": 0x90, "SBB": 0x98, "ANA": 0xA0, "XRA": 0xA8, "ORA": 0xB0, "CMP": 0xB8}
IMM = {"ADI": 0xC6, "ACI": 0xCE, "SUI": 0xD6, "SBI": 0xDE, "ANI": 0xE6, "XRI": 0xEE, "ORI": 0xF6, "CPI": 0xFE,
       "IN": 0xDB, "OUT": 0xD3}
ADDR16 = {"JMP": 0xC3, "CALL": 0xCD, "LDA": 0x3A, "STA": 0x32, "LHLD": 0x2A, "SHLD": 0x22, **COND}


def num(tok, labels=None):
    tok = tok.strip()
    if labels and tok in labels:
        return labels[tok]
    if tok.upper().endswith("H"):
        return int(tok[:-1], 16)
    return int(tok)


def split(line):
    line = line.split(";")[0].strip()
    label = None
    if ":" in line:
        label, line = [x.strip() for x in line.split(":", 1)]
    if not line:
        return label, None, []
    parts = line.split(None, 1)
    ops = [o.strip() for o in parts[1].split(",")] if len(parts) > 1 else []
    return label, parts[0].upper(), ops


def encode(mn, ops, labels):
    o = [x.upper() if x.upper() in REG or x.upper() in RP else x for x in ops]
    if mn in SIMPLE: return [SIMPLE[mn]]
    if mn == "MOV": return [0x40 | REG[o[0]] << 3 | REG[o[1]]]
    if mn == "MVI": return [0x06 | REG[o[0]] << 3, num(o[1], labels) & 255]
    if mn == "LXI":
        v = num(o[1], labels); return [0x01 | RP[o[0]] << 4, v & 255, v >> 8]
    if mn in ALU: return [ALU[mn] | REG[o[0]]]
    if mn in IMM: return [IMM[mn], num(o[0], labels) & 255]
    if mn == "INR": return [0x04 | REG[o[0]] << 3]
    if mn == "DCR": return [0x05 | REG[o[0]] << 3]
    if mn == "INX": return [0x03 | RP[o[0]] << 4]
    if mn == "DCX": return [0x0B | RP[o[0]] << 4]
    if mn == "DAD": return [0x09 | RP[o[0]] << 4]
    if mn == "LDAX": return [0x0A | RP[o[0]] << 4]
    if mn == "STAX": return [0x02 | RP[o[0]] << 4]
    if mn == "PUSH": return [0xC5 | RP[o[0]] << 4]
    if mn == "POP": return [0xC1 | RP[o[0]] << 4]
    if mn in ADDR16:
        v = num(o[0], labels); return [ADDR16[mn], v & 255, v >> 8]
    raise ValueError(mn)


def assemble(src, org=0x2000):
    prog, labels, addr = [], {}, org
    for ln in src.strip().splitlines():
        label, mn, ops = split(ln)
        if label: labels[label] = addr
        if mn:
            n = len(encode(mn, ops, {k: 0 for k in re.findall(r"[A-Za-z_]\w*", " ".join(ops))}))
            prog.append((addr, mn, ops)); addr += n
    mem, listing = {}, []
    for a, mn, ops in prog:
        b = encode(mn, ops, labels)
        for i, x in enumerate(b): mem[a + i] = x
        listing.append((a, b, mn, ops))
    return mem, listing, labels


class CPU:
    def __init__(self, mem):
        self.m = dict(mem); self.r = [0] * 8; self.sp = 0xFFFF; self.pc = 0x2000
        self.S = self.Z = self.AC = self.P = self.CY = 0; self.T = 0

    def flags(self, v, cy=None, ac=None):
        v &= 255; self.S = v >> 7; self.Z = int(v == 0); self.P = int(bin(v).count("1") % 2 == 0)
        if cy is not None: self.CY = cy
        if ac is not None: self.AC = ac
        return v

    def hl(self): return self.r[4] << 8 | self.r[5]
    def rd(self, a): return self.m.get(a & 0xFFFF, 0)
    def get(self, i): return self.rd(self.hl()) if i == 6 else self.r[i]
    def put(self, i, v):
        if i == 6: self.m[self.hl()] = v & 255
        else: self.r[i] = v & 255
    def pair(self, p):
        if p == 3: return self.sp
        return self.r[p * 2] << 8 | self.r[p * 2 + 1]
    def setpair(self, p, v):
        v &= 0xFFFF
        if p == 3: self.sp = v
        else: self.r[p * 2], self.r[p * 2 + 1] = v >> 8, v & 255
    def cond(self, c):
        return [not self.Z, self.Z, not self.CY, self.CY, not self.P, self.P, not self.S, self.S][c]

    def alu(self, op, b):
        a = self.r[7]
        if op in (0, 1):
            c = self.CY if op == 1 else 0; t = a + b + c
            self.AC = int((a & 15) + (b & 15) + c > 15); self.r[7] = self.flags(t, int(t > 255)); return
        if op in (2, 3, 7):
            c = self.CY if op == 3 else 0; t = a - b - c
            self.AC = int((a & 15) - (b & 15) - c >= 0)
            res = self.flags(t, int(t < 0))
            if op != 7: self.r[7] = res
            return
        if op == 4: self.AC = 1; self.r[7] = self.flags(a & b, 0)
        elif op == 5: self.AC = 0; self.r[7] = self.flags(a ^ b, 0)
        elif op == 6: self.AC = 0; self.r[7] = self.flags(a | b, 0)

    def run(self, limit=2_000_000):
        names = {0xC2, 0xCA, 0xD2, 0xDA, 0xE2, 0xEA, 0xF2, 0xFA}
        while limit:
            limit -= 1
            pc = self.pc; op = self.rd(pc); n1, n2 = self.rd(pc + 1), self.rd(pc + 2)
            w = n2 << 8 | n1; self.pc += 1; hi = op >> 6; d = op >> 3 & 7; s = op & 7
            if op == 0x76: self.T += 5; return
            if op == 0x00: self.T += 4; continue
            if hi == 1:
                self.put(d, self.get(s)); self.T += 7 if 6 in (d, s) else 4; continue
            if hi == 2:
                self.alu(d, self.get(s)); self.T += 7 if s == 6 else 4; continue
            if hi == 0 and s == 6:
                self.put(d, n1); self.pc += 1; self.T += 10 if d == 6 else 7; continue
            if hi == 0 and s == 4:
                v = self.get(d) + 1; self.AC = int((self.get(d) & 15) == 15)
                self.put(d, self.flags(v)); self.T += 10 if d == 6 else 4; continue
            if hi == 0 and s == 5:
                v = self.get(d) - 1; self.AC = int((self.get(d) & 15) != 0)
                self.put(d, self.flags(v)); self.T += 10 if d == 6 else 4; continue
            if op in (0x01, 0x11, 0x21, 0x31): self.setpair(op >> 4, w); self.pc += 2; self.T += 10; continue
            if op in (0x03, 0x13, 0x23, 0x33): self.setpair(op >> 4, self.pair(op >> 4) + 1); self.T += 6; continue
            if op in (0x0B, 0x1B, 0x2B, 0x3B): self.setpair(op >> 4, self.pair(op >> 4) - 1); self.T += 6; continue
            if op in (0x09, 0x19, 0x29, 0x39):
                t = self.hl() + self.pair(op >> 4); self.CY = int(t > 0xFFFF); self.setpair(2, t); self.T += 10; continue
            if op in (0x0A, 0x1A): self.r[7] = self.rd(self.pair(op >> 4)); self.T += 7; continue
            if op in (0x02, 0x12): self.m[self.pair(op >> 4)] = self.r[7]; self.T += 7; continue
            if op == 0x3A: self.r[7] = self.rd(w); self.pc += 2; self.T += 13; continue
            if op == 0x32: self.m[w] = self.r[7]; self.pc += 2; self.T += 13; continue
            if op == 0x2A: self.r[5], self.r[4] = self.rd(w), self.rd(w + 1); self.pc += 2; self.T += 16; continue
            if op == 0x22: self.m[w], self.m[w + 1] = self.r[5], self.r[4]; self.pc += 2; self.T += 16; continue
            if op == 0xEB: self.r[2], self.r[4] = self.r[4], self.r[2]; self.r[3], self.r[5] = self.r[5], self.r[3]; self.T += 4; continue
            if op in (0xC6, 0xCE, 0xD6, 0xDE, 0xE6, 0xEE, 0xF6, 0xFE):
                self.alu(op >> 3 & 7, n1); self.pc += 1; self.T += 7; continue
            if op == 0xC3: self.pc = w; self.T += 10; continue
            if op in names:
                if self.cond(d): self.pc = w; self.T += 10
                else: self.pc += 2; self.T += 7
                continue
            if op == 0xCD:
                self.sp -= 2; self.m[self.sp], self.m[self.sp + 1] = (pc + 3) & 255, (pc + 3) >> 8
                self.pc = w; self.T += 18; continue
            if op == 0xC9:
                self.pc = self.rd(self.sp) | self.rd(self.sp + 1) << 8; self.sp += 2; self.T += 10; continue
            if op in (0xC5, 0xD5, 0xE5):
                v = self.pair((op >> 4) & 3); self.sp -= 2; self.m[self.sp], self.m[self.sp + 1] = v & 255, v >> 8; self.T += 12; continue
            if op in (0xC1, 0xD1, 0xE1):
                self.setpair((op >> 4) & 3, self.rd(self.sp) | self.rd(self.sp + 1) << 8); self.sp += 2; self.T += 10; continue
            if op == 0x07: a = self.r[7]; self.CY = a >> 7; self.r[7] = (a << 1 | a >> 7) & 255; self.T += 4; continue
            if op == 0x0F: a = self.r[7]; self.CY = a & 1; self.r[7] = (a >> 1 | (a & 1) << 7) & 255; self.T += 4; continue
            if op == 0x17: a = self.r[7]; c = self.CY; self.CY = a >> 7; self.r[7] = (a << 1 | c) & 255; self.T += 4; continue
            if op == 0x1F: a = self.r[7]; c = self.CY; self.CY = a & 1; self.r[7] = (a >> 1 | c << 7) & 255; self.T += 4; continue
            if op == 0x2F: self.r[7] ^= 255; self.T += 4; continue
            if op == 0x37: self.CY = 1; self.T += 4; continue
            if op == 0x3F: self.CY ^= 1; self.T += 4; continue
            if op == 0x27:
                a = self.r[7]; add = 0; cy = self.CY
                if (a & 15) > 9 or self.AC: add |= 6
                if (a >> 4) > 9 or cy or ((a >> 4) >= 9 and (a & 15) > 9): add |= 0x60; cy = 1
                t = a + add; self.AC = int((a & 15) + (add & 15) > 15); self.r[7] = self.flags(t, cy); self.T += 4; continue
            raise RuntimeError(f"unimplemented opcode {op:02X} at {pc:04X}")
        raise RuntimeError("step limit")


def run(src, data=None, regs=None, cy=0):
    mem, listing, labels = assemble(src)
    cpu = CPU(mem)
    for a, v in (data or {}).items(): cpu.m[a] = v
    for k, v in (regs or {}).items(): cpu.r[REG[k]] = v
    cpu.CY = cy
    cpu.run()
    return cpu, listing


FAILS = []
SHOW = "--listing" in sys.argv


def check(name, got, want):
    ok = got == want
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"  got={got!r} want={want!r}"))
    if not ok: FAILS.append(name)


def show(title, listing, cpu):
    if not SHOW: return
    print(f"--- {title}  (T={cpu.T})")
    for a, b, mn, ops in listing:
        print(f"{a:04X}  {' '.join(f'{x:02X}' for x in b):<9} {mn} {','.join(ops)}")


# ------------------------------------------------------------------ programs
P_ADD8 = """
      LDA 2050H
      MOV B,A
      LDA 2051H
      ADD B
      STA 2052H
      MVI A,00H
      ADC A
      STA 2053H
      HLT
"""
c, l = run(P_ADD8, {0x2050: 0xF5, 0x2051: 0x1B}); show("ADD8", l, c)
check("add8 sum F5+1B", (c.m[0x2052], c.m[0x2053]), (0x10, 1))
c, _ = run(P_ADD8, {0x2050: 0x23, 0x2051: 0x14}); check("add8 23+14", (c.m[0x2052], c.m[0x2053]), (0x37, 0))

P_ADD16 = """
      LHLD 2050H
      XCHG
      LHLD 2052H
      DAD D
      SHLD 2054H
      MVI A,00H
      ADC A
      STA 2056H
      HLT
"""
c, l = run(P_ADD16, {0x2050: 0xF3, 0x2051: 0x45, 0x2052: 0x1E, 0x2053: 0xFA}); show("ADD16", l, c)
t = 0x45F3 + 0xFA1E
check("add16 45F3+FA1E", (c.m[0x2054], c.m[0x2055], c.m[0x2056]), (t & 255, (t >> 8) & 255, t >> 16))

P_SUB = """
      LDA 2050H
      MOV B,A
      LDA 2051H
      MOV C,A
      MOV A,B
      SUB C
      STA 2052H
      JNC DONE
      CMA
      INR A
      STA 2052H
      MVI A,01H
      JMP SAVE
DONE: MVI A,00H
SAVE: STA 2053H
      HLT
"""
c, l = run(P_SUB, {0x2050: 0x4B, 0x2051: 0x2C}); show("SUB", l, c)
check("sub 4B-2C", (c.m[0x2052], c.m[0x2053]), (0x1F, 0))
c, _ = run(P_SUB, {0x2050: 0x2C, 0x2051: 0x4B}); check("sub 2C-4B (negative, magnitude)", (c.m[0x2052], c.m[0x2053]), (0x1F, 1))

P_MUL = """
      LDA 2050H
      MOV E,A
      MVI D,00H
      LDA 2051H
      MOV C,A
      LXI H,0000H
      MOV A,C
      ORA A
      JZ STORE
LOOP: DAD D
      DCR C
      JNZ LOOP
STORE: SHLD 2052H
      HLT
"""
c, l = run(P_MUL, {0x2050: 0xC8, 0x2051: 0x0A}); show("MUL", l, c)
check("mul C8*0A=07D0", (c.m[0x2052], c.m[0x2053]), (0xD0, 0x07))
c, _ = run(P_MUL, {0x2050: 0xFF, 0x2051: 0xFF}); check("mul FF*FF", (c.m[0x2053] << 8 | c.m[0x2052]), 255 * 255)
c, _ = run(P_MUL, {0x2050: 0x07, 0x2051: 0x00}); check("mul 7*0", (c.m[0x2053] << 8 | c.m[0x2052]), 0)

P_DIV = """
      LDA 2050H
      MOV B,A
      LDA 2051H
      MOV C,A
      MVI D,00H
      MOV A,B
LOOP: CMP C
      JC DONE
      SUB C
      INR D
      JMP LOOP
DONE: STA 2053H
      MOV A,D
      STA 2052H
      HLT
"""
c, l = run(P_DIV, {0x2050: 100, 0x2051: 7}); show("DIV", l, c)
check("div 100/7", (c.m[0x2052], c.m[0x2053]), (14, 2))

P_MAX = """
      LDA 2050H
      MOV C,A
      LXI H,2051H
      MOV A,M
      DCR C
LOOP: INX H
      CMP M
      JNC SKIP
      MOV A,M
SKIP: DCR C
      JNZ LOOP
      STA 2060H
      HLT
"""
arr = [0x25, 0x9C, 0x41, 0xF0, 0x08, 0x7E]
c, l = run(P_MAX, {0x2050: len(arr), **{0x2051 + i: v for i, v in enumerate(arr)}}); show("MAX", l, c)
check("largest of array", c.m[0x2060], 0xF0)

P_MIN = P_MAX.replace("JNC SKIP", "JC SKIP").replace("2060H", "2061H")
c, l = run(P_MIN, {0x2050: len(arr), **{0x2051 + i: v for i, v in enumerate(arr)}})
check("smallest of array (CMP M; JC keeps A)", c.m[0x2061], 0x08)

P_SUM = """
      LDA 2050H
      MOV C,A
      LXI H,2051H
      MVI A,00H
      MVI B,00H
LOOP: ADD M
      JNC NEXT
      INR B
NEXT: INX H
      DCR C
      JNZ LOOP
      STA 2060H
      MOV A,B
      STA 2061H
      HLT
"""
arr2 = [0xF0, 0xF0, 0x80, 0x33, 0x0A]
c, l = run(P_SUM, {0x2050: len(arr2), **{0x2051 + i: v for i, v in enumerate(arr2)}}); show("SUM", l, c)
check("sum of array with carry", (c.m[0x2061] << 8 | c.m[0x2060]), sum(arr2))

P_BLOCK = """
      LDA 2050H
      MOV C,A
      LXI H,2051H
      LXI D,3051H
LOOP: MOV A,M
      STAX D
      INX H
      INX D
      DCR C
      JNZ LOOP
      HLT
"""
c, l = run(P_BLOCK, {0x2050: 5, 0x2051: 1, 0x2052: 2, 0x2053: 3, 0x2054: 4, 0x2055: 5}); show("BLOCK", l, c)
check("block move 5 bytes", [c.m[0x3051 + i] for i in range(5)], [1, 2, 3, 4, 5])

P_ONES = """
      LDA 2050H
      MVI B,00H
      MVI C,08H
LOOP: RAR
      JNC SKIP
      INR B
SKIP: DCR C
      JNZ LOOP
      MOV A,B
      STA 2051H
      HLT
"""
c, l = run(P_ONES, {0x2050: 0b10110111}); show("ONES", l, c)
check("count ones in B7", c.m[0x2051], 6)

P_COMP2 = """
      LHLD 2050H
      MOV A,L
      CMA
      MOV L,A
      MOV A,H
      CMA
      MOV H,A
      INX H
      SHLD 2052H
      HLT
"""
c, l = run(P_COMP2, {0x2050: 0x34, 0x2051: 0x12}); show("COMP2", l, c)
check("2's complement of 1234H", (c.m[0x2053] << 8 | c.m[0x2052]), (-0x1234) & 0xFFFF)

P_BCD = """
      LDA 2050H
      MOV B,A
      LDA 2051H
      ADD B
      DAA
      STA 2052H
      MVI A,00H
      ADC A
      STA 2053H
      HLT
"""
c, l = run(P_BCD, {0x2050: 0x58, 0x2051: 0x67}); show("BCD", l, c)
check("BCD 58+67=125", (c.m[0x2053], c.m[0x2052]), (1, 0x25))
c, _ = run(P_BCD, {0x2050: 0x29, 0x2051: 0x13}); check("BCD 29+13=42", (c.m[0x2053], c.m[0x2052]), (0, 0x42))

P_SORT = """
      LDA 2050H
      MOV D,A
      DCR D
OUTER: LXI H,2051H
      MOV C,D
INNER: MOV A,M
      INX H
      CMP M
      JC NOSWAP
      JZ NOSWAP
      MOV B,M
      MOV M,A
      DCX H
      MOV M,B
      INX H
NOSWAP: DCR C
      JNZ INNER
      DCR D
      JNZ OUTER
      HLT
"""
c, l = run(P_SORT, {0x2050: len(arr), **{0x2051 + i: v for i, v in enumerate(arr)}}); show("SORT", l, c)
check("bubble sort ascending", [c.m[0x2051 + i] for i in range(len(arr))], sorted(arr))

P_EVEN = """
      LDA 2050H
      MOV C,A
      LXI H,2051H
      MVI B,00H
LOOP: MOV A,M
      RRC
      JC ODD
      INR B
ODD:  INX H
      DCR C
      JNZ LOOP
      MOV A,B
      STA 2060H
      HLT
"""
c, l = run(P_EVEN, {0x2050: len(arr), **{0x2051 + i: v for i, v in enumerate(arr)}}); show("EVEN", l, c)
check("count even numbers", c.m[0x2060], sum(1 for v in arr if v % 2 == 0))

# ---- delay routine T-state formulas
for n in (1, 5, 0xFF):
    src = f"      MVI B,{n:02X}H\nLOOP: DCR B\n      JNZ LOOP\n      HLT\n"
    c, l = run(src)
    check(f"delay one-loop n={n}: 14n+4", c.T - 5, 14 * n + 4)
    if n == 0xFF: show("DELAY1", l, c)
src = "      MVI B,02H\nOUT_: MVI C,03H\nIN_:  DCR C\n      JNZ IN_\n      DCR B\n      JNZ OUT_\n      HLT\n"
c, l = run(src)
inner = 7 + (4 + 10) * 2 + (4 + 7)
total = 7 + 2 * inner + (4 + 10) * 1 + (4 + 7)
check("nested delay formula (B=2,C=3)", c.T - 5, total)

# ---- stack / subroutine demo
P_CALL = """
      LXI SP,27FFH
      MVI A,05H
      CALL DOUBLE
      STA 2050H
      HLT
DOUBLE: ADD A
      RET
"""
c, l = run(P_CALL); show("CALL", l, c)
check("CALL/RET double 5", c.m[0x2050], 10)

P_PUSHPOP = """
      LXI SP,27FFH
      LXI B,1234H
      LXI D,5678H
      PUSH B
      PUSH D
      POP B
      POP D
      HLT
"""
c, l = run(P_PUSHPOP); show("PUSHPOP", l, c)
check("push B,D / pop B,D swaps", (c.r[0], c.r[1], c.r[2], c.r[3]), (0x56, 0x78, 0x12, 0x34))

# ---- flag examples
c, _ = run("MVI A,9BH\nADI 75H\nHLT\n"); check("9B+75 -> 10, CY=1 Z=0", (c.r[7], c.CY, c.Z, c.S), (0x10, 1, 0, 0))
c, _ = run("MVI A,3EH\nADI 42H\nHLT\n"); check("3E+42 -> 80, S=1 CY=0 P=0", (c.r[7], c.S, c.CY, c.P), (0x80, 1, 0, 0))
c, _ = run("MVI A,05H\nSUI 05H\nHLT\n"); check("05-05 -> 0, Z=1 CY=0", (c.r[7], c.Z, c.CY), (0, 1, 0))
c, _ = run("MVI A,05H\nCPI 09H\nHLT\n"); check("CPI 09 with A=05: CY=1 Z=0, A kept", (c.r[7], c.CY, c.Z), (5, 1, 0))
c, _ = run("MVI A,0FH\nINR A\nHLT\n"); check("INR 0F: AC=1", (c.r[7], c.AC), (0x10, 1))

c, l = run("LXI H,2050H\nMOV A,M\nINX H\nADD M\nSTA 2052H\nHLT\n"); show("TSAMPLE", l, c)
check("T-states of LXI,MOV A M,INX,ADD M,STA,HLT", c.T, 10 + 7 + 6 + 7 + 13 + 5)


# ------------------------------------------------------------------ Booth
def booth(m, q, bits):
    mask = (1 << bits) - 1
    A, Q, q1, M = 0, q & mask, 0, m & mask
    rows = []
    for _ in range(bits):
        pair = (Q & 1, q1)
        if pair == (1, 0): A = (A - M) & mask
        elif pair == (0, 1): A = (A + M) & mask
        sign = A >> (bits - 1)
        q1 = Q & 1
        Q = (Q >> 1 | (A & 1) << (bits - 1)) & mask
        A = (A >> 1 | sign << (bits - 1)) & mask
        rows.append((format(A, f"0{bits}b"), format(Q, f"0{bits}b"), q1))
    prod = A << bits | Q
    if prod >> (2 * bits - 1): prod -= 1 << (2 * bits)
    return prod, rows


p, rows = booth(-9, -13, 5)
check("Booth (-9)x(-13) 5-bit", p, 117)
if SHOW:
    for r in rows: print("booth", r)
p, rows = booth(7, 3, 4); check("Booth 7x3 4-bit", p, 21)
if SHOW:
    for r in rows: print("booth 7x3", r)
check("Booth (-6)x5 5-bit", booth(-6, 5, 5)[0], -30)
p, rows = booth(-5, 3, 4); check("Booth (-5)x3 4-bit", p, -15)
if SHOW:
    for r in rows: print("booth -5x3", r)


# ------------------------------------------------------------------ pipeline
def pipe_time(k, n): return k + n - 1


check("pipeline 4 stages 100 tasks: 103 cycles", pipe_time(4, 100), 103)
check("speedup = 400/103 ~ 3.88", round(400 / 103, 2), 3.88)
check("efficiency 3.88/4 ~ 0.97", round(400 / 103 / 4, 2), 0.97)
check("pipeline k=5,n=20 -> 24 cycles vs 100", (pipe_time(5, 20), 5 * 20), (24, 100))
check("speedup k=5 n=20 = 4.17", round(100 / 24, 2), 4.17)

# ------------------------------------------------------------------ cache / memory
check("AMAT 0.95 hit, 2ns cache, 50ns memory = 4.5ns", round(0.95 * 2 + 0.05 * (2 + 50), 2), 4.5)
check("effective access (hit 0.9, 10ns, 100ns) = 20ns", round(0.9 * 10 + 0.1 * (10 + 100), 2), 20.0)
check("speedup from cache 100/20 = 5", round(100 / 20, 2), 5.0)
off, idx = 4, 6
check("direct map tag bits = 16-4-6", 16 - off - idx, 6)
addr = 0xA3C7
check("addr A3C7 split tag/index/offset", (addr >> 10, (addr >> 4) & 63, addr & 15), (0x28, 0x3C, 7))
check("4-way: sets = 64/4", 64 // 4, 16)
check("RAM chip addressing: 2K x 8 needs 11 address lines", (2048).bit_length() - 1, 11)
check("memory 64KB from 16K chips -> 4 chips, 2 select lines", (65536 // 16384, (65536 // 16384).bit_length() - 1), (4, 2))
check("hard disk: 8 surfaces x 1000 cyl x 63 sec x 512 B = 258,048,000 B", 8 * 1000 * 63 * 512, 258_048_000)
check("disk avg rotational latency @7200rpm = 4.17ms", round(60000 / 7200 / 2, 2), 4.17)


def faults(refs, frames, policy):
    mem, f = [], 0
    for p in refs:
        if p in mem:
            if policy == "LRU": mem.remove(p); mem.append(p)
            continue
        f += 1
        if len(mem) == frames: mem.pop(0)
        mem.append(p)
    return f


refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
check("FIFO 3 frames faults", faults(refs, 3, "FIFO"), 10)
check("LRU 3 frames faults", faults(refs, 3, "LRU"), 9)


def optimal(refs, frames):
    mem, f = [], 0
    for i, p in enumerate(refs):
        if p in mem: continue
        f += 1
        if len(mem) < frames: mem.append(p); continue
        nxt = {q: (refs[i + 1:].index(q) if q in refs[i + 1:] else 10**9) for q in mem}
        mem.remove(max(nxt, key=nxt.get)); mem.append(p)
    return f


check("OPT 3 frames faults", optimal(refs, 3), 7)
belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
check("Belady FIFO 3 frames = 9", faults(belady, 3, "FIFO"), 9)
check("Belady FIFO 4 frames = 10", faults(belady, 4, "FIFO"), 10)
check("virtual: 32-bit VA, 4KB page -> 20-bit page number", 32 - 12, 20)
check("page table 2^20 entries x 4 B = 4 MB", 2 ** 20 * 4, 4 * 2 ** 20)

# ------------------------------------------------------------------ misc numbers
check("8-bit two's complement range", (-(2 ** 7), 2 ** 7 - 1), (-128, 127))
check("8085 addressable memory 2^16", 2 ** 16, 65536)
check("8086 addressable memory 2^20", 2 ** 20, 1048576)
check("8086 physical address 2000:0150", (0x2000 << 4) + 0x0150, 0x20150)
check("MVI = 7 T at 3 MHz = 2.333 us", round(7 / 3, 3), 2.333)
check("FP add example 0.5+0.375=0.875", 0.5 + 0.375, 0.875)
check("Amdahl 90% parallel, 4 CPUs", round(1 / (0.1 + 0.9 / 4), 2), 3.08)
check("Amdahl limit 90% parallel", round(1 / 0.1, 1), 10.0)

# ------------------------------------------------------------------ IEEE 754, restoring division, address map
import struct
def f32(x): return struct.pack(">f", x).hex().upper()
check("IEEE 12.375 = 41460000", f32(12.375), "41460000")
check("IEEE -5.75 = C0B80000", f32(-5.75), "C0B80000")
check("IEEE 0.75 = 3F400000", f32(0.75), "3F400000")
check("IEEE 1.0 = 3F800000", f32(1.0), "3F800000")
check("IEEE decode 3F400000", struct.unpack(">f", bytes.fromhex("3F400000"))[0], 0.75)
check("IEEE decode C1480000 = -12.5", struct.unpack(">f", bytes.fromhex("C1480000"))[0], -12.5)
check("IEEE 12.375 fields", (format(0x41460000, "032b")[0], format(0x41460000, "032b")[1:9], format(0x41460000, "032b")[9:]),
      ("0", "10000010", "10001100000000000000000"))


def restoring(n, d, bits):
    A, Q, rows = 0, n, []
    for _ in range(bits):
        A = (A << 1 | Q >> (bits - 1)) & ((1 << (bits + 1)) - 1); Q = (Q << 1) & ((1 << bits) - 1)
        A -= d
        if A < 0: A += d; q = 0
        else: q = 1
        Q |= q; rows.append((A, format(Q, f"0{bits}b"), q))
    return Q, A, rows


qq, rr, rows = restoring(13, 3, 4)
check("restoring division 13/3 = 4 r 1", (qq, rr), (4, 1))
if SHOW:
    for r in rows: print("restoring", r)
check("memory map: RAM4 ends at 01FF, ROM 0200-03FF", (4 * 128 - 1, 0x200, 0x200 + 512 - 1), (0x1FF, 0x200, 0x3FF))
check("Mano basic computer: 4096 words = 12-bit address", (4096).bit_length() - 1, 12)
check("RAM 512 B from 128x8 chips -> 4 chips, 7 line each", (512 // 128, (128).bit_length() - 1), (4, 7))
check("control memory 128 x 20 = 2560 bits", 128 * 20, 2560)
check("microinstruction 3+3+3+2+2+7 = 20 bits", 3 + 3 + 3 + 2 + 2 + 7, 20)
check("ADD routine address from opcode 0000 = 0000000 (0); BRANCH 0001 -> 4", ((0 << 2), (1 << 2)), (0, 4))

# ------------------------------------------------------------------ numbers quoted in practice answers
check("nested delay 14BC+18B+4 for B=C=255", 14 * 255 * 255 + 18 * 255 + 4, 914_944)
check("nested delay B=5,C=213 = 15004 T", 14 * 5 * 213 + 18 * 5 + 4, 15004)
check("one-loop n=214 -> 3000 T (1 ms at 3 MHz)", 14 * 214 + 4, 3000)
check("one-loop FFH max 3574 T = 1.19 ms", (14 * 255 + 4, round((14 * 255 + 4) / 3000, 2)), (3574, 1.19))
check("16-bit counter: 15000/24 = 625 = 0x271", (15000 // 24, hex(625)), (625, "0x271"))
check("100-count loop at 2 MHz = 702 us", (14 * 100 + 4) * 0.5, 702.0)
check("Amdahl P=0.8 N=8", round(1 / (0.2 + 0.8 / 8), 2), 3.33)
check("pipeline k=5 n=20 t=5ns: 120 ns, S=4.17, eff 0.83", ((5 + 20 - 1) * 5, round(500 / 120, 2), round(500 / 120 / 5, 2)), (120, 4.17, 0.83))
check("pipeline 4 stages x100 x10ns = 1030 ns / 4000 ns", ((4 + 100 - 1) * 10, 4 * 100 * 10), (1030, 4000))
check("CPI with 20% one-cycle stalls = 1.2", round(1 + 0.2 * 1, 2), 1.2)
check("CPI branches 20% x 60% taken x 2 = 1.24", round(1 + 0.2 * 0.6 * 2, 2), 1.24)
check("matrix 3x3: 27 mul, 18 add", (3 ** 3, 3 ** 2 * (3 - 1)), (27, 18))
check("4800 baud, 12-bit frame = 400 cps; 9600/10 = 960", (4800 // 12, 9600 // 10), (400, 960))
check("disk 4x500x40x1KB = 81,920,000; 6000 rpm latency 5 ms", (4 * 500 * 40 * 1024, 60000 / 6000 / 2), (81_920_000, 5.0))
check("cache 8KB/32B direct: tag 11 bits", 24 - 8 - 5, 11)
check("AMAT 5ns/60ns/0.92 = 9.8 ns, speed-up 6.1", (round(5 + 0.08 * 60, 2), round(60 / 9.8, 1)), (9.8, 6.1))
check("page 0x3A7C: page 3, offset A7C, frame 1B -> 0x1BA7C", (0x3A7C >> 12, hex(0x3A7C & 0xFFF), hex(0x1B * 0x1000 + 0xA7C)), (3, "0xa7c", "0x1ba7c"))
check("DMA vs interrupt: 4096 x 20us = 81.9 ms; 4096 x 0.5us = 2.05 ms", (round(4096 * 20 / 1000, 1), round(4096 * 0.5 / 1000, 2)), (81.9, 2.05))
check("tests: bit stuffing 0111110111111 -> 011111001111101", "".join(
    [c + ("0" if (r := (lambda d: [sum(1 for _ in __import__("itertools").takewhile(lambda x: x == "1", reversed(d[:i + 1]))) for i in range(len(d))])("0111110111111")[i]) == 5 else "") for i, c in enumerate("0111110111111")]), "011111001111101")
check("arithmetic overflow 103+89 = 192 -> as signed -64", (103 + 89, ((103 + 89) & 255) - 256), (192, -64))
check("signed shift: 11100100 >> 1 arithmetic = 11110010 (-14)", (((0b11100100 >> 1) | 0b10000000), -14), (0b11110010, -14))

print()
print("ALL PASS" if not FAILS else f"{len(FAILS)} FAIL(S): {FAILS}")
sys.exit(1 if FAILS else 0)
