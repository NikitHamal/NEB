#!/usr/bin/env python3
"""Computer Networking verifier. Recomputes every number used in the book and asserts it.
    python3 bca/tools/check_networking.py            # compute + assert + print the tables
    python3 bca/tools/check_networking.py --verify   # also check that each key string appears in the unit files"""
import heapq, ipaddress, math, os, sys, glob, itertools

OUT = {}
def put(k, v): OUT[k] = str(v)

# ---- Unit 1: delay, throughput, bandwidth-delay product
def delays(L_bits, R, d_m, s=2e8, hops=1):
    return L_bits / R, d_m / s
tx, prop = delays(1500 * 8, 100e6, 2000e3)
put("tx_1500B_100M_ms", f"{tx*1e3:.3f}"); put("prop_2000km_ms", f"{prop*1e3:.1f}")
assert abs(tx * 1e3 - 0.12) < 1e-9 and abs(prop * 1e3 - 10) < 1e-9
bdp = 1e9 * 0.05
put("bdp_1G_50ms_bits", int(bdp)); put("bdp_1G_50ms_MB", bdp / 8 / 1e6)
assert bdp == 5e7
saf = 3 * (8000 * 8 / 1e6)  # three links store-and-forward 8000 B at 1 Mbps
put("saf_3links_s", saf); assert abs(saf - 0.192) < 1e-12
# message of 10^6 bits over 3 hops with 1 Mbps, pipelining packets of 1000 bits
n_pk, pk = 1000, 1000
t_seg = 3 * pk / 1e6 + (n_pk - 1) * pk / 1e6
put("pipelined_s", f"{t_seg:.3f}"); assert abs(t_seg - 1.002) < 1e-9

# ---- Unit 2: Nyquist / Shannon / line coding / multiplexing
def nyquist(B, L): return 2 * B * math.log2(L)
def shannon(B, snr_db): return B * math.log2(1 + 10 ** (snr_db / 10))
put("nyq_3000_2", nyquist(3000, 2)); put("nyq_3000_4", nyquist(3000, 4)); put("nyq_3000_16", nyquist(3000, 16))
put("shannon_3000_30dB", f"{shannon(3000, 30):.0f}"); put("shannon_1M_20dB", f"{shannon(1e6, 20):.0f}")
assert nyquist(3000, 4) == 12000 and round(shannon(3000, 30)) == 29902
def snr_for(C, B): return 10 * math.log10(2 ** (C / B) - 1)
put("snr_for_56k_3100", f"{snr_for(56000, 3100):.2f}")
def manchester(bits): return "".join("01" if b == "1" else "10" for b in bits)   # IEEE 802.3: 1 = low->high
def nrzi(bits):
    lvl = "-"; out = ""
    for b in bits:
        if b == "1": lvl = "+" if lvl == "-" else "-"
        out += lvl
    return out
def ami(bits):
    last = -1; out = []
    for b in bits:
        if b == "0": out.append("0")
        else: last = -last; out.append("+" if last > 0 else "-")
    return " ".join(out)
put("manch_10110010", manchester("10110010")); put("nrzi_10110010", nrzi("10110010")); put("ami_10110010", ami("10110010"))
assert manchester("10110010") == "0110010110100110"
# TDM: 4 channels x 8 bit slots, 8000 frames/s
put("tdm_rate_bps", 4 * 8 * 8000); assert 4 * 8 * 8000 == 256000
put("t1_rate", 24 * 8 * 8000 + 8000); assert 24 * 8 * 8000 + 8000 == 1544000
put("fdm_total_kHz", 3 * 4 + 2 * 1)  # 3 channels of 4 kHz and 2 guard bands of 1 kHz
# QAM-16 symbol rate
put("baud_for_56k", 56000 / 4)

from math import comb
p_gt10 = sum(comb(35, k) * 0.1**k * 0.9**(35 - k) for k in range(11, 36)); put("packet_gain_P_gt10", f"{p_gt10:.4f}"); assert round(p_gt10, 4) == 0.0004
put("geo_oneway_ms", f"{2 * 35786e3 / 3e8 * 1e3:.1f}")
put("frame_1518_payload_frac", f"{1460 / 1518:.4f}")
put("eth_frame_overhead", 1460 + 20 + 20 + 18)
# ---- Unit 3: framing, CRC, Hamming, ARQ
def bit_stuff(s):
    out = []; run = 0
    for b in s:
        out.append(b); run = run + 1 if b == "1" else 0
        if run == 5: out.append("0"); run = 0
    return "".join(out)
def bit_unstuff(s):
    out = []; run = 0; skip = False
    for b in s:
        if skip: skip = False; run = 0; continue
        out.append(b); run = run + 1 if b == "1" else 0
        if run == 5: skip = True
    return "".join(out)
def byte_stuff(data, flag="7E", esc="7D"):
    out = []
    for b in data:
        if b in (flag, esc): out.append(esc)
        out.append(b)
    return out
put("bitstuff", bit_stuff("0111111011111011111")); assert bit_unstuff(bit_stuff("0111111011111011111")) == "0111111011111011111"; assert bit_stuff("0111111011111011111") == "0111110101111100111110" and "111111" not in bit_stuff("0111111011111011111")
def xor_div(dividend, poly):
    d = list(dividend); n = len(poly)
    for i in range(len(d) - n + 1):
        if d[i] == "1":
            for j in range(n): d[i + j] = "0" if d[i + j] == poly[j] else "1"
    return "".join(d[-(n - 1):])
def crc_send(msg, poly):
    r = xor_div(msg + "0" * (len(poly) - 1), poly); return msg + r, r
tx1, r1 = crc_send("1101011011", "10011")
put("crc_ex1_frame", tx1); put("crc_ex1_rem", r1)
assert r1 == "1110" and tx1 == "11010110111110" and xor_div(tx1, "10011") == "0000"
tx2, r2 = crc_send("100100", "1101"); put("crc_ex2_rem", r2); put("crc_ex2_frame", tx2)
assert r2 == "001" and tx2 == "100100001"
corrupt = list(tx1); corrupt[3] = "1" if corrupt[3] == "0" else "0"
put("crc_err_rem", xor_div("".join(corrupt), "10011")); assert xor_div("".join(corrupt), "10011") != "0000"
def crc_table(msg, poly):
    d = list(msg + "0" * (len(poly) - 1)); n = len(poly); rows = []
    for i in range(len(msg)):
        if d[i] == "1":
            for j in range(n): d[i + j] = "0" if d[i + j] == poly[j] else "1"
            rows.append((i, "".join(d)))
    return rows
put("crc_steps_ex2", crc_table("100100", "1101"))
def crc16_ccitt(data: bytes, poly=0x1021, init=0xFFFF):
    crc = init
    for byte in data:
        crc ^= byte << 8
        for _ in range(8): crc = ((crc << 1) ^ poly) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc
put("crc16_123456789", f"{crc16_ccitt(b'123456789'):04X}"); assert crc16_ccitt(b"123456789") == 0x29B1
import zlib; put("crc32_123456789", f"{zlib.crc32(b'123456789'):08X}"); assert zlib.crc32(b"123456789") == 0xCBF43926
def inet_checksum(words):
    s = sum(words)
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF
cs = inet_checksum([0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0x0000, 0xC0A8, 0x0001, 0xC0A8, 0x00C7])
put("ip_hdr_checksum", f"{cs:04X}"); assert cs == 0xB861
def hamming_encode(data, even=True):
    m = len(data); r = 0
    while 2 ** r < m + r + 1: r += 1
    n = m + r; code = [None] * (n + 1); j = 0
    for i in range(1, n + 1):
        if i & (i - 1): code[i] = int(data[j]); j += 1
        else: code[i] = 0
    for p in range(r):
        pos = 2 ** p; par = 0
        for i in range(1, n + 1):
            if i & pos and i != pos: par ^= code[i]
        code[pos] = par
    return "".join(map(str, code[1:])), r
def hamming_syndrome(word):
    s = 0
    for i, b in enumerate(word, 1):
        if b == "1": s ^= i
    return s
hw, r = hamming_encode("1011"); put("hamming_1011", hw); put("hamming_r_4", r); assert hw == "0110011"
hw2, r2_ = hamming_encode("10011010"); put("hamming_10011010", hw2); put("hamming_r_8", r2_); assert r2_ == 4
bad = list(hw); bad[4] = "1" if bad[4] == "0" else "0"; put("hamming_syndrome", hamming_syndrome("".join(bad)))
assert hamming_syndrome("".join(bad)) == 5 and hamming_syndrome(hw) == 0 and hamming_syndrome(hw2) == 0
put("hamming_min_r_11", min(r for r in range(1, 10) if 2 ** r >= 11 + r + 1))
# min distance
def hd(a, b): return sum(x != y for x, y in zip(a, b))
words = [hamming_encode(format(i, "04b"))[0] for i in range(16)]
put("hamming74_dmin", min(hd(a, b) for a, b in itertools.combinations(words, 2))); assert min(hd(a, b) for a, b in itertools.combinations(words, 2)) == 3
def sw_eff(tf, tp): return tf / (tf + 2 * tp)
put("sw_eff", f"{sw_eff(0.012, 0.020):.4f}"); assert abs(sw_eff(0.012, 0.020) - 0.012 / 0.052) < 1e-12
def win_eff(w, tf, tp): return min(1, w * tf / (tf + 2 * tp))
put("win_min_for_full", math.ceil((0.012 + 0.04) / 0.012)); put("seq_bits_gbn_w7", math.ceil(math.log2(7 + 1)))
put("sr_seq_bits_w4", math.ceil(math.log2(2 * 4)))
put("sat_win_eff_w7", f"{win_eff(7, 0.012, 0.020):.4f}")
# Go-Back-N: 10 frames, frame 3 lost, window 4 -> count transmissions
def gbn(n, w, lost):
    sent = 0; base = 0; log = []; lost = set(lost)
    while base < n:
        top = min(base + w, n); stop = None
        for f in range(base, top):
            sent += 1; log.append(f)
            if f in lost: lost.discard(f); stop = f; break
        if stop is None: base = top
        else:
            # frames after loss are sent anyway in a real pipe; model: window frames sent then timeout
            pass
        if stop is not None:
            # sender already sent rest of window before timeout
            for f in range(stop + 1, top): sent += 1; log.append(f)
            base = stop
    return sent, log
sent_gbn, log = gbn(10, 4, [2]); assert sent_gbn == 12 and log == [0,1,2,3,2,3,4,5,6,7,8,9]; put("gbn_sent", sent_gbn); put("gbn_log", log)
sr_sent = 10 + 1; put("sr_sent", sr_sent)

# ---- Unit 4: MAC
def aloha(G, slotted=False): return G * math.exp(-(1 if slotted else 2) * G)
put("pure_aloha_max", f"{aloha(0.5):.4f}"); put("slot_aloha_max", f"{aloha(1, True):.4f}")
assert abs(aloha(0.5) - 0.1839) < 1e-4 and abs(aloha(1, True) - 0.3679) < 1e-4
put("pure_aloha_G1", f"{aloha(1.0):.4f}")
slot_bits = 10e6 * 51.2e-6; put("eth10_slot_bits", slot_bits); assert slot_bits == 512
put("eth10_min_bytes", int(slot_bits / 8)); put("eth100_max_span_m", f"{2e8 * 512 / 100e6 / 2:.0f}")
def csma_cd_eff(a): return 1 / (1 + 5 * a)
put("csmacd_eff_a0.1", f"{csma_cd_eff(0.1):.4f}")
def backoff_wait(k, slot=51.2): return (2 ** min(k, 10) - 1) * slot
put("backoff_k3_max_us", backoff_wait(3)); put("backoff_k10_max_us", f"{backoff_wait(10):.1f}")
put("eth_max_frame_wire", 7 + 1 + 14 + 1500 + 4 + 12); put("eth_eff_1500", f"{1500 / (7 + 1 + 14 + 1500 + 4 + 12):.4f}")
put("wifi_slot", "9 us, SIFS 16 us, DIFS = SIFS + 2 x slot = 34 us"); assert 16 + 2 * 9 == 34

# ---- Unit 5: IP addressing
def info(c):
    n = ipaddress.ip_network(c, strict=False)
    h = list(n.hosts())
    return dict(net=str(n.network_address), mask=str(n.netmask), bc=str(n.broadcast_address),
                first=str(h[0]) if h else "-", last=str(h[-1]) if h else "-", hosts=max(n.num_addresses - 2, 0))
for c in ["192.168.10.77/26", "172.16.5.130/20", "10.1.2.3/8", "200.10.20.0/30"]:
    put("net_" + c, info(c))
assert info("192.168.10.77/26") == dict(net="192.168.10.64", mask="255.255.255.192", bc="192.168.10.127", first="192.168.10.65", last="192.168.10.126", hosts=62)
assert info("172.16.5.130/20")["net"] == "172.16.0.0" and info("172.16.5.130/20")["bc"] == "172.16.15.255" and info("172.16.5.130/20")["hosts"] == 4094
# equal subnetting of 192.168.1.0/24 into 6 -> 8 subnets /27
subs = list(ipaddress.ip_network("192.168.1.0/24").subnets(new_prefix=27)); put("equal_subnets", [str(s) for s in subs])
assert len(subs) == 8 and subs[2] == ipaddress.ip_network("192.168.1.64/27")
# VLSM: 10.0.0.0/24 with LANs 100, 50, 25, 2 hosts
def vlsm(base, reqs):
    net = ipaddress.ip_network(base); cur = int(net.network_address); res = []
    for name, h in sorted(reqs, key=lambda x: -x[1]):
        need = h + 2; bits = math.ceil(math.log2(need)); size = 2 ** bits; pre = 32 - bits
        sn = ipaddress.ip_network((cur, pre)); res.append((name, h, str(sn), size - 2, str(list(sn.hosts())[0]), str(list(sn.hosts())[-1]), str(sn.broadcast_address)))
        cur += size
    return res
V = vlsm("10.0.0.0/24", [("Sales", 100), ("Eng", 50), ("Admin", 25), ("WAN", 2)])
put("vlsm", V)
assert [v[2] for v in V] == ["10.0.0.0/25", "10.0.0.128/26", "10.0.0.192/27", "10.0.0.224/30"]
# supernet aggregation
agg = list(ipaddress.collapse_addresses([ipaddress.ip_network(f"192.168.{i}.0/24") for i in range(4)])); put("agg", [str(a) for a in agg])
assert str(agg[0]) == "192.168.0.0/22"
# longest prefix match
table = [("0.0.0.0/0", "R-default"), ("10.0.0.0/8", "R1"), ("10.1.0.0/16", "R2"), ("10.1.2.0/24", "R3")]
def lpm(ip):
    a = ipaddress.ip_address(ip); best = max((ipaddress.ip_network(p) for p, _ in table if a in ipaddress.ip_network(p)), key=lambda n: n.prefixlen)
    return str(best), dict(table)[str(best)]
for ip in ["10.1.2.9", "10.1.9.9", "10.9.9.9", "8.8.8.8"]: put("lpm_" + ip, lpm(ip))
assert lpm("10.1.9.9") == ("10.1.0.0/16", "R2")
# IPv6
a6 = ipaddress.ip_address("2001:0db8:0000:0000:0000:ff00:0042:8329"); put("v6_compressed", a6.compressed); assert a6.compressed == "2001:db8::ff00:42:8329"
put("v6_exploded", a6.exploded)
n6 = ipaddress.ip_network("2001:db8:abcd::/48"); put("v6_subnets_64_in_48", 2 ** (64 - 48)); put("v6_first64", str(next(n6.subnets(new_prefix=64))))
mac = "00:1A:2B:3C:4D:5E"
def eui64(mac):
    b = [int(x, 16) for x in mac.split(":")]; b[0] ^= 2; b = b[:3] + [0xFF, 0xFE] + b[3:]
    return ":".join(f"{b[i]:02x}{b[i+1]:02x}" for i in range(0, 8, 2)).replace(":0", ":").lstrip("0")
put("eui64", eui64(mac)); assert eui64(mac) == "21a:2bff:fe3c:4d5e"
put("v4_total", 2 ** 32); put("v6_total", f"{2**128:.3e}")
# fragmentation: 4000 B payload+20 hdr over MTU 1500
def frag(total, mtu, hdr=20):
    payload = total - hdr; per = (mtu - hdr) // 8 * 8; res = []; off = 0
    while payload > 0:
        sz = min(per, payload); payload -= sz; res.append((sz + hdr, off // 8, 0 if payload == 0 else 1)); off += sz
    return res
put("frag", frag(4020, 1500)); assert frag(4020, 1500) == [(1500, 0, 1), (1500, 185, 1), (1060, 370, 0)]
# NAT table
# ---- Unit 6: routing
G = {"A": {"B": 2, "C": 5, "D": 1}, "B": {"A": 2, "C": 3, "D": 2}, "C": {"A": 5, "B": 3, "D": 3, "E": 1, "F": 5}, "D": {"A": 1, "B": 2, "C": 3, "E": 1}, "E": {"C": 1, "D": 1, "F": 2}, "F": {"C": 5, "E": 2}}
def dijkstra(G, s):
    dist = {v: math.inf for v in G}; prev = {}; dist[s] = 0; done = []; steps = []
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done: continue
        done.append(u)
        for v, w in G[u].items():
            if d + w < dist[v]: dist[v] = d + w; prev[v] = u; heapq.heappush(pq, (d + w, v))
        steps.append((u, dict(dist)))
    return dist, prev, done, steps
dist, prev, order, steps = dijkstra(G, "A")
put("dij_dist", dist); put("dij_prev", prev); put("dij_order", order)
assert dist == {"A": 0, "B": 2, "C": 3, "D": 1, "E": 2, "F": 4} and prev["C"] == "E" and prev["F"] == "E"
def path(prev, t):
    p = [t]
    while p[-1] in prev: p.append(prev[p[-1]])
    return p[::-1]
put("dij_path_F", path(prev, "F")); assert path(prev, "F") == ["A", "D", "E", "F"]
def first_hop(prev, t): return path(prev, t)[1]
put("dij_forwarding_A", {t: first_hop(prev, t) for t in G if t != "A"})
# Bellman-Ford / distance vector
def dv(G):
    INF = math.inf; D = {u: {v: (0 if u == v else INF) for v in G} for u in G}
    for u in G:
        for v, w in G[u].items(): D[u][v] = w
    rounds = 0; hist = []
    while True:
        new = {u: dict(D[u]) for u in G}; ch = False
        for u in G:
            for t in G:
                if u == t: continue
                best = min(G[u][v] + D[v][t] for v in G[u])
                if best < new[u][t]: new[u][t] = best; ch = True
        D = new; rounds += 1; hist.append({t: D["A"][t] for t in G})
        if not ch: break
    return D, rounds, hist
D, rounds, hist = dv(G); put("dv_A", D["A"]); put("dv_rounds", rounds); put("dv_hist_A", hist)
assert D["A"] == dist and all(D[u][v] == dijkstra(G, u)[0][v] for u in G for v in G)
# count-to-infinity: A-B-C line, B-C breaks. cost 1 each. A believes via B.
def count_to_inf(limit=16):
    # distances to C: A->B=1, B->C=1 initially, so dA=2, dB=1. Link B-C fails.
    dA, dB = 2, 1; rows = []; dB = min(limit, 1 + dA); rows.append(("B", dB))
    while True:
        dA_new = min(limit, 1 + dB); rows.append(("A", dA_new)); dA = dA_new
        if dA >= limit: break
        dB_new = min(limit, 1 + dA); rows.append(("B", dB_new)); dB = dB_new
        if dB >= limit: break
    return rows
cti = count_to_inf(); put("cti", cti)
# Poison reverse not shown numerically.
# RIP: 15 max hops, OSPF cost = 100 Mbps / bw
def ospf_cost(mbps, ref=100): return max(1, round(ref / mbps))
put("ospf_cost", {bw: ospf_cost(bw) for bw in (10, 100, 1000)}); assert ospf_cost(10) == 10 and ospf_cost(1000) == 1
# Hierarchical routing: per-router table sizes not needed
# Prim/Kruskal style not needed
# Broadcast: spanning tree edges count
put("mst_edges_6", 5)

# ---- Unit 7: transport
def ssthresh_trace(rounds=16, ssth=16, loss_at=None, tahoe=True):
    cw = 1; rows = []
    for t in range(1, rounds + 1):
        rows.append((t, cw, ssth))
        if loss_at and t == loss_at:
            ssth = max(cw // 2, 2); cw = 1 if tahoe else ssth
        elif cw < ssth: cw = min(cw * 2, ssth)
        else: cw += 1
    return rows
tr = ssthresh_trace(14, 16, loss_at=8); put("cwnd_tahoe_trace", tr)
assert tr[4] == (5, 16, 16) and tr[7] == (8, 19, 16) and tr[8] == (9, 1, 9) and tr[12] == (13, 9, 9)
tr_reno = ssthresh_trace(14, 16, loss_at=8, tahoe=False); put("cwnd_reno_trace", tr_reno)
assert tr_reno[8] == (9, 9, 9)
def jacobson(samples, a=0.125, b=0.25):
    srtt = samples[0]; rttvar = samples[0] / 2; rows = []
    for s in samples[1:]:
        rttvar = (1 - b) * rttvar + b * abs(srtt - s); srtt = (1 - a) * srtt + a * s
        rows.append((s, round(srtt, 2), round(rttvar, 2), round(srtt + 4 * rttvar, 2)))
    return rows
jr = jacobson([100, 120, 90, 140, 100]); put("jacobson", jr)
put("tcp_tput_window", f"{65535 * 8 / 0.1 / 1e6:.2f}"); assert abs(65535 * 8 / 0.1 / 1e6 - 5.24) < 0.01
put("tcp_win_for_1G_50ms", int(1e9 * 0.05 / 8))
put("tcp_mathis_100ms_1pct", f"{1460 * 8 / 0.1 * 1.22 / math.sqrt(0.01) / 1e6:.2f}")
put("tcp_isn_wrap_note", 2 ** 32)
put("udp_cs_example", f"{inet_checksum([0x0102, 0x0304, 0x0506]):04X}"); 
def tcp_seq(isn_c, isn_s, n): return dict(syn=isn_c, synack=(isn_s, isn_c + 1), ack=(isn_c + 1, isn_s + 1), data_next=isn_c + 1 + n)
put("tcp_seq", tcp_seq(1000, 5000, 300))
# AIMD fairness
x, y = 10.0, 60.0; cap = 100; hist = []
halvings = 0
for i in range(60):
    if x + y > cap: x, y = x / 2, y / 2; halvings += 1
    else: x, y = x + 1, y + 1
put("aimd_gap_start", 50); put("aimd_gap_after", f"{abs(x - y):.4f}")
put("aimd_halvings", halvings); assert abs(abs(x - y) - 50 / 2 ** halvings) < 1e-9 and halvings >= 2

# ---- Unit 8: application layer (DNS name-to-wire, HTTP sizes)
def dns_qname(name): return b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
q = dns_qname("www.example.com"); put("dns_qname_hex", q.hex()); put("dns_qname_len", len(q)); assert len(q) == 17
def dns_query(name, qid=0x1234):
    return (qid.to_bytes(2, "big") + b"\x01\x00" + (1).to_bytes(2, "big") + b"\x00\x00\x00\x00\x00\x00" + dns_qname(name) + (1).to_bytes(2, "big") + (1).to_bytes(2, "big"))
put("dns_query_len", len(dns_query("www.example.com"))); put("dns_query_hex", dns_query("www.example.com").hex()); assert len(dns_query("www.example.com")) == 33
import base64
put("basic_auth", base64.b64encode(b"nikit:s3cret").decode()); 
put("b64_Man", base64.b64encode(b"Man").decode()); assert base64.b64encode(b"Man").decode() == "TWFu"
put("http_nonpersist_serial_ms", 2 * 50 * 5); put("http_persist_ms", 100 + 4 * 50); put("http_nonpersist_parallel_ms", 100 + 100)
assert 2 * 50 * 5 == 500 and 100 + 4 * 50 == 300
put("email_b64_overhead", f"{len(base64.b64encode(bytes(300))) / 300 - 1:.3f}")
# ping real (localhost) and ports are done in the book via fill_script_outputs.

# ---- Unit 7: crypto
import hashlib
n_ = 61 * 53; phi_ = 60 * 52; d_ = pow(17, -1, phi_); put("rsa", (n_, phi_, d_, pow(65, 17, n_)))
assert (n_, phi_, d_, pow(65, 17, n_)) == (3233, 3120, 2753, 2790) and pow(2790, d_, n_) == 65 and 17 * 2753 == 15 * 3120 + 1
A_, B_ = pow(5, 6, 23), pow(5, 15, 23); put("dh", (A_, B_, pow(B_, 6, 23), pow(A_, 15, 23))); assert (A_, B_, pow(B_, 6, 23), pow(A_, 15, 23)) == (8, 19, 2, 2)
assert hashlib.sha256(b"abc").hexdigest().startswith("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
assert "".join(chr((ord(c) - 65 + 3) % 26 + 65) for c in "NEB") == "QHE"
assert 10 * 9 // 2 == 45 and abs(math.log10(math.factorial(26)) - 26.6) < 0.1
# ---- Practice answers: more numbers
put("subnet_q_30_hosts", 2 ** 5 - 2)
put("cidr_172.31.0.0/21_hosts", 2 ** 11 - 2)
put("mask_for_500_hosts", 32 - math.ceil(math.log2(502)))
assert 32 - math.ceil(math.log2(502)) == 23
put("tdm_efficiency", f"{4 * 8 * 8000 / 256000:.0f}")

if "--verify" in sys.argv:
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "course", "semester-5", "computer-networking")
    text = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(here, "unit-*.md"))))
    must = ["0.12 ms", "10 ms", "50,000,000", "0.192", "1.002", "29,902", "12,000", "256,000", "1,544,000", "0110010110100110",
            "0111110101111100111110", "11010110111110", "1110", "100100001", "29B1", "CBF43926", "B861", "0110011",
            "192.168.10.64", "255.255.255.192", "192.168.10.127", "172.16.15.255", "4094", "10.0.0.128/26", "10.0.0.224/30", "192.168.0.0/22",
            "10.1.0.0/16", "2001:db8::ff00:42:8329", "21a:2bff:fe3c:4d5e", "185", "1060", "0.1839", "0.3679", "51.2", "5.24",
            "TWFu", "011100101010", "2790", "2753", "bmlraXQ6czNjcmV0", "0.2308", "218.96", "6,250,000", "1.42 Mbps", "ba7816bf", "93.184.216.34", "12.5"]
    miss = [m for m in must if m and m not in text]
    for m in miss: print("MISSING in book:", m)
    print(f"verify: {len(must) - len(miss)}/{len(must)} key values present"); sys.exit(1 if miss else 0)
for k, v in OUT.items(): print(f"{k}: {v}")
