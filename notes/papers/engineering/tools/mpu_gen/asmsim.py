"""Tiny 8085 / 8051 subset interpreters used to verify the assembly programs in the MPMC papers."""
import re

def _num(s):
    s = s.strip().upper()
    if s.endswith('H'): return int(s[:-1], 16)
    if s.startswith('#'): return _num(s[1:])
    return int(s)

def parse(src):
    prog, labels = [], {}
    for line in src.splitlines():
        line = line.split(';')[0].strip()
        if not line: continue
        m = re.match(r'(\w+):\s*(.*)', line)
        if m: labels[m.group(1).upper()] = len(prog); line = m.group(2).strip()
        if not line: continue
        parts = line.split(None, 1)
        op = parts[0].upper()
        args = [a.strip() for a in parts[1].split(',')] if len(parts) > 1 else []
        prog.append((op, args))
    return prog, labels

def run8085(src, mem=None, steps=100000):
    prog, labels = parse(src)
    R = dict(A=0, B=0, C=0, D=0, E=0, H=0, L=0); F = dict(Z=0, CY=0, S=0)
    mem = dict(mem or {}); out = []
    def pair(p): return (R[p] << 8) | R[{'B': 'C', 'D': 'E', 'H': 'L'}[p]]
    def setpair(p, v): R[p] = (v >> 8) & 255; R[{'B': 'C', 'D': 'E', 'H': 'L'}[p]] = v & 255
    def getr(r): return mem.get(pair('H'), 0) if r == 'M' else R[r]
    def setr(r, v):
        if r == 'M': mem[pair('H')] = v & 255
        else: R[r] = v & 255
    def zs(v): F['Z'] = int((v & 255) == 0); F['S'] = (v >> 7) & 1
    pc = 0; n = 0
    while pc < len(prog) and n < steps:
        n += 1; op, a = prog[pc]; pc += 1
        if op == 'HLT': break
        elif op == 'LDA': R['A'] = mem.get(_num(a[0]), 0)
        elif op == 'STA': mem[_num(a[0])] = R['A']
        elif op == 'MOV': setr(a[0], getr(a[1]))
        elif op == 'MVI': setr(a[0], _num(a[1]))
        elif op == 'LXI': setpair(a[0], _num(a[1]))
        elif op == 'ADD':
            t = R['A'] + getr(a[0]); F['CY'] = int(t > 255); R['A'] = t & 255; zs(R['A'])
        elif op == 'ORA': R['A'] |= getr(a[0]); F['CY'] = 0; zs(R['A'])
        elif op == 'DCR': v = (getr(a[0]) - 1) & 255; setr(a[0], v); zs(v)
        elif op == 'INR': v = (getr(a[0]) + 1) & 255; setr(a[0], v); zs(v)
        elif op == 'DCX': setpair(a[0], (pair(a[0]) - 1) & 0xFFFF)
        elif op == 'INX': setpair(a[0], (pair(a[0]) + 1) & 0xFFFF)
        elif op == 'DAD':
            t = pair('H') + pair(a[0]); F['CY'] = int(t > 0xFFFF); setpair('H', t & 0xFFFF)
        elif op == 'CPI':
            v = _num(a[0]); F['CY'] = int(R['A'] < v); F['Z'] = int(R['A'] == v)
        elif op == 'STAX': mem[pair(a[0])] = R['A']
        elif op == 'OUT': out.append((_num(a[0]), R['A']))
        elif op in ('JNZ', 'JZ', 'JC', 'JNC', 'JMP'):
            c = dict(JNZ=not F['Z'], JZ=F['Z'], JC=F['CY'], JNC=not F['CY'], JMP=True)[op]
            if c: pc = labels[a[0].upper()]
        else: raise ValueError(op)
    return R, mem, out, n

def run8051(src, iram=None, ports=None, steps=100000):
    prog, labels = parse(src)
    R = [0] * 8; S = dict(A=0, B=0, CY=0); ports = dict(ports or {}); ram = dict(iram or {})
    def get(x):
        x = x.upper()
        if x == 'A': return S['A']
        if x == 'B': return S['B']
        if re.fullmatch(r'R[0-7]', x): return R[int(x[1])]
        if x.startswith('@R'): return ram.get(R[int(x[2])], 0)
        if x.startswith('#'): return _num(x[1:]) & 255
        if x in ('P1', 'P2'): return ports.get(x, 0)
        return ram.get(_num(x), 0)
    def put(x, v):
        x = x.upper(); v &= 255
        if x == 'A': S['A'] = v
        elif x == 'B': S['B'] = v
        elif re.fullmatch(r'R[0-7]', x): R[int(x[1])] = v
        elif x.startswith('@R'): ram[R[int(x[2])]] = v
        elif x in ('P1', 'P2'): ports[x] = v
        else: ram[_num(x)] = v
    pc = 0; n = 0
    while pc < len(prog) and n < steps:
        n += 1; op, a = prog[pc]; pc += 1
        if op == 'MOV': put(a[0], get(a[1]))
        elif op == 'ADD':
            t = S['A'] + get(a[1]); S['CY'] = int(t > 255); S['A'] = t & 255
        elif op == 'INC': put(a[0], get(a[0]) + 1)
        elif op == 'DEC': put(a[0], get(a[0]) - 1)
        elif op == 'CLR': put(a[0], 0)
        elif op == 'JNC':
            if not S['CY']: pc = labels[a[0].upper()]
        elif op == 'JC':
            if S['CY']: pc = labels[a[0].upper()]
        elif op == 'DJNZ':
            put(a[0], get(a[0]) - 1)
            if get(a[0]) != 0: pc = labels[a[1].upper()]
        elif op == 'SJMP':
            if a[0] == '$': break
            pc = labels[a[0].upper()]
        elif op == 'MUL':
            t = S['A'] * S['B']; S['A'] = t & 255; S['B'] = t >> 8
        elif op == 'DIV':
            q, r = divmod(S['A'], S['B']); S['A'] = q; S['B'] = r
        elif op == 'XCH':
            t = get(a[1]); put(a[1], S['A']); S['A'] = t
        else: raise ValueError(op)
    return S, R, ram, ports

if __name__ == '__main__':
    import random
    P1 = '''LXI H,0000H
LDA 8050H
ORA A
JZ DONE
MOV C,A
MVI B,00H
LOOP: DAD B
DCR C
JNZ LOOP
DONE: MOV A,L
OUT 41H
MOV A,H
OUT 42H
HLT'''
    for n in (0, 1, 5, 10, 22, 23, 100, 255):
        R, m, o, _ = run8085(P1, {0x8050: n}); assert (o[0][1] | o[1][1] << 8) == n * (n + 1) // 2, n
    P0 = '''LDA 8050H
MOV C,A
MVI A,00H
LOOP: ADD C
DCR C
JNZ LOOP
OUT 41H
HLT'''
    for n in range(1, 23):
        assert run8085(P0, {0x8050: n})[2][0][1] == n * (n + 1) // 2
    PX = '''LXI H,0000H
LDA 8050H
MOV E,A
MVI D,00H
ORA A
JZ DONE
LOOP: DAD D
DCX D
MOV A,D
ORA E
JNZ LOOP
DONE: MOV A,L
OUT 41H
MOV A,H
OUT 42H
HLT'''
    for n in range(0, 256):
        R, m, o, _ = run8085(PX, {0x8050: n}); assert (o[0][1] | o[1][1] << 8) == n * (n + 1) // 2, n
    P2 = '''LXI H,8050H
LXI D,9050H
MVI C,0AH
LOOP: MOV A,M
CPI 70H
JC STORE
MVI A,00H
STORE: STAX D
INX H
INX D
DCR C
JNZ LOOP
HLT'''
    d = [random.randrange(256) for _ in range(10)]; d[0] = 0x70; d[1] = 0x6F
    R, m, o, _ = run8085(P2, {0x8050 + i: v for i, v in enumerate(d)})
    assert [m[0x9050 + i] for i in range(10)] == [v if v < 0x70 else 0 for v in d]
    P3 = '''MOV R0,#40H
MOV R7,#0AH
MOV R2,#00H
MOV R3,#00H
AGAIN: MOV A,R2
ADD A,@R0
MOV R2,A
JNC SKIP
INC R3
SKIP: INC R0
DJNZ R7,AGAIN
SJMP $'''
    for _ in range(50):
        d = [random.randrange(256) for _ in range(10)]
        S, R, ram, _ = run8051(P3, {0x40 + i: v for i, v in enumerate(d)}); assert R[2] | R[3] << 8 == sum(d)
    d = [255] * 10; S, R, ram, _ = run8051(P3, {0x40 + i: v for i, v in enumerate(d)}); print('max sum', hex(R[3] << 8 | R[2]))
    P4 = '''MOV A,P1
MOV B,#05H
DIV AB
MOV R0,B
MOV B,#09H
MUL AB
MOV R1,A
MOV A,R0
MOV B,#09H
MUL AB
MOV B,#05H
DIV AB
ADD A,R1
ADD A,#32
MOV P2,A
SJMP $'''
    for c in range(0, 124):
        S, R, ram, ports = run8051(P4, ports={'P1': c}); assert ports['P2'] == (9 * c) // 5 + 32, c
    S, R, ram, ports = run8051(P4, ports={'P1': 100}); print('100C ->', ports['P2'])
    print('all programs verified')
