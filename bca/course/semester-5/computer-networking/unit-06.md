---
subject: Computer Networking
grade: BCA Semester 5
unit: 6
title: The Application Layer
hours: 4
area: BCA 301 · Computer Networking · Unit 6
---

Applications are why networks exist, and every application protocol is, underneath, just an agreement on what text or bytes to send over a TCP or UDP socket. This unit looks at the protocols the syllabus names (DNS, DHCP, WWW, HTTP, HTTPS, Telnet, FTP, SMTP, POP, IMAP) and at the tools used to look at them (SNMP, MRTG, PRTG, Packet Tracer, Wireshark). You will build a DNS message by hand, make a real HTTP request over a socket, and inspect real sockets with Linux tools.

::: key What this unit gives you
- Application architectures: client–server, peer-to-peer; the socket API.
- DNS: hierarchy, records, resolution, message format. DHCP in context.
- The Web: URLs, HTTP messages, methods, status codes, cookies, caching, HTTP/2 and HTTP/3; HTTPS.
- Remote login and file transfer: Telnet, SSH, FTP. E-mail: SMTP, POP3, IMAP, MIME.
- Network management and analysis: SNMP, MRTG, PRTG, Packet Tracer, Wireshark.
:::

## 6.1 Functions and architectures

The application layer provides the services that user programs see. An application protocol defines the **types** of messages (request, response), their **syntax**, **semantics** and the **rules** for when to send. Two architectures exist. **Client–server**: a server with a fixed, well-known address waits; clients start the conversation; the server can be a single machine or a farm behind a load balancer. **Peer-to-peer**: peers are clients and servers at once, which scales without server cost but is harder to manage and secure. An application chooses UDP when delay matters more than reliability and TCP when every byte must arrive.

## 6.2 The Domain Name System

People remember names; routers use addresses. **DNS** is a distributed, hierarchical database that translates names such as www.example.com to IP addresses. It runs over UDP port 53 (TCP for large replies and zone transfers).

### Hierarchy

The name space is a tree read right to left: the **root** (a dot), **top-level domains** (generic: com, org, edu, gov, net; country codes such as np for Nepal), **second-level domains** (example, or com.np, edu.np, gov.np below .np), then hosts. A **zone** is the part of the tree managed by one authority. Thirteen root server *identities* (a.root-servers.net … m.root-servers.net) exist, each replicated at hundreds of sites by anycast.

### Resource records

| Type | Meaning | Example |
|---|---|---|
| A | name → IPv4 address | www.example.com A 93.184.216.34 |
| AAAA | name → IPv6 address | |
| NS | name server of a zone | example.com NS a.iana-servers.net |
| CNAME | alias to the canonical name | www CNAME web.example.com |
| MX | mail server with preference (lowest first) | example.com MX 10 mail.example.com |
| TXT | free text: SPF, DKIM, verification | |
| PTR | address → name (reverse lookup under in-addr.arpa) | |
| SOA | start of authority for a zone: serial, refresh, TTL | |

### Resolution

A host asks its **local (recursive) resolver**, typically at the ISP or a public service. If the answer is not in its **cache**, the resolver queries the root, which refers it to the .com servers, which refer it to the example.com name server, which returns the answer. This is **iterative** querying by the resolver; the host's own query is **recursive** ("do all the work and bring me the answer"). Each record has a **TTL**, the number of seconds a cache may keep it; caching makes most lookups local. Attacks on DNS include cache poisoning (forged replies; DNSSEC adds signatures) and amplification DDoS (small spoofed queries produce large replies).

### Message format

A DNS message has a 12-byte header (ID, flags, counts of questions, answers, authority and additional records), then the question (name, type, class) and the records. A name is a list of labels, each preceded by its length, ending with a zero byte: www.example.com is 03 77 77 77 07 65 78 61 6d 70 6c 65 03 63 6f 6d 00, which is 17 bytes. A standard query for it is 12 + 17 + 4 = 33 bytes long. Replies use a 2-byte *compression pointer* (c0 0c points at offset 12) to avoid repeating the name.

## 6.3 DHCP and the bootstrap sequence

When you join a network, a chain of protocols runs in order: **DHCP** gives you an IP address, mask, default gateway and DNS server (Unit 4); **ARP** finds the gateway's MAC; **DNS** resolves the server's name; **TCP** connects; **HTTP** (inside TLS) fetches the page. When a page fails to load, test each step in turn: do I have an address (`ip addr`)? can I reach the gateway (`ping`)? does the name resolve (`dig` or `nslookup`)? does the port answer (`curl -v`)?

## 6.4 The World Wide Web and HTTP

A web page is a base HTML file referencing objects (images, scripts) each addressed by a **URL**: scheme://host[:port]/path?query#fragment, for example https://example.com:443/notes/unit6.html?v=2#dns. **HTTP** is the web's application protocol: text-based request/response over TCP, port 80, **stateless** (the server keeps no memory between requests).

A request is: a **request line** (method, target, version), **header lines**, a blank line and an optional body.

```
GET /index.html HTTP/1.1
Host: www.example.com
Accept: text/html
Connection: close
```

The response has a **status line**, headers, a blank line and the body.

| Methods | Use | Status codes | Meaning |
|---|---|---|---|
| GET | fetch (safe, idempotent) | 200 OK | success |
| HEAD | headers only | 301 / 302 / 304 | moved / found (redirect) / not modified |
| POST | send data to be processed | 400 / 401 / 403 / 404 | bad request / unauthenticated / forbidden / not found |
| PUT / DELETE | replace / remove a resource (idempotent) | 429 | too many requests |
| OPTIONS | ask what is allowed | 500 / 502 / 503 | server error / bad gateway / unavailable |

### Persistent connections and timing

HTTP/1.0 used a new TCP connection for every object (**non-persistent**); HTTP/1.1 keeps the connection open (**persistent**) and may *pipeline*. Compare the page-load time for a base file plus 4 small objects with RTT = 50 ms (transmission times negligible): each TCP connection costs one RTT (handshake) and each request/response another RTT.

| Mode | Time | Working |
|---|---|---|
| Non-persistent, serial | 500 ms | 5 objects × (50 + 50) |
| Non-persistent, 4 parallel connections for the objects | 200 ms | base 100 + parallel objects 100 |
| Persistent, no pipelining | 300 ms | one handshake 50, base 50, then 4 × 50 |

HTTP/2 multiplexes many streams over one TCP connection with header compression; **HTTP/3** runs over QUIC (UDP) to avoid TCP's head-of-line blocking and to combine the transport and TLS handshakes.

### State, cookies and caching

The server sets a **cookie** (`Set-Cookie: sid=abc123`); the browser returns it with every later request to that site, which lets the server recognise a session (login, shopping cart) but also lets sites track users. A **web cache** (browser or proxy) stores objects; a **conditional GET** (`If-Modified-Since` or `If-None-Match` with an ETag) returns 304 if unchanged, saving bandwidth. A **CDN** keeps copies near users.

### Authentication and HTTPS

HTTP *Basic* authentication sends `Authorization: Basic ` plus the Base64 of `user:password`; Base64 is an encoding, not encryption: nikit:s3cret becomes bmlraXQ6czNjcmV0 and anyone can reverse it. **HTTPS** is HTTP inside a TLS connection on port 443 (Unit 7), providing encryption, integrity and server authentication. Modern browsers warn on plain HTTP.

## 6.5 Remote login and file transfer

**Telnet** (TCP 23) gives a remote terminal with *no encryption*, so passwords cross the network in plaintext; it survives only on lab devices. **SSH** (TCP 22) replaces it with encryption and key authentication, and also carries file copy (scp, sftp) and port forwarding.

**FTP** uses **two connections**: a *control* connection on port 21 (commands USER, PASS, LIST, RETR, STOR; replies like 220, 230, 226) and a *data* connection per transfer. In **active mode** the server opens the data connection from port 20 to the client (blocked by firewalls and NAT); in **passive mode** the client opens both connections (PASV). FTP is out of band: control and data are separate, and the control connection holds state. FTPS adds TLS; SFTP is a different protocol over SSH.

## 6.6 Electronic mail

A message is composed in a **user agent** (Outlook, Thunderbird, webmail), sent to the sender's **mail server** over **SMTP** (TCP 25, or 587 with authentication), relayed server to server to the recipient's mail server (found by the MX record) and fetched by the recipient with **POP3** (TCP 110: download and usually delete; simple, offline) or **IMAP** (TCP 143: mailboxes stay on the server, folders synchronised across devices). SMTP is a *push* protocol (the sender pushes), POP3 and IMAP are *pull*.

A minimal SMTP dialogue:

```
S: 220 mail.example.com ESMTP
C: HELO client.example.org
S: 250 mail.example.com
C: MAIL FROM:<a@example.org>
S: 250 OK
C: RCPT TO:<b@example.com>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: Subject: Hello ... message ... then a line with a single dot
S: 250 Queued
C: QUIT
S: 221 Bye
```

SMTP carries 7-bit ASCII. **MIME** lets mail carry other content: headers such as `Content-Type: image/jpeg` and `Content-Transfer-Encoding: base64`. Base64 groups 3 bytes into four characters from a 64-letter alphabet (the bytes "Man" become TWFu), so binary attachments grow by one third (a 300-byte file becomes 400 characters). Spam defences use SPF, DKIM and DMARC records in DNS.

## 6.7 Network management and analysis tools

**SNMP** (UDP 161, traps on 162) lets a *manager* query and set variables on *agents* in routers, switches and servers. The variables are defined in a **MIB** (management information base), a tree of object identifiers; operations are GET, GETNEXT, SET and TRAP (agent-initiated alarm). Versions 1 and 2c authenticate with a plaintext "community string"; v3 adds real authentication and encryption. **MRTG** and **PRTG** poll SNMP counters (octets in and out of an interface, CPU load) on a schedule and draw traffic graphs; from two readings, utilisation = Δ octets × 8 / (Δ seconds × link speed). **Packet Tracer** (Cisco) simulates networks for teaching: build topologies, configure routers and watch packets move. **Wireshark** captures frames from an interface and dissects them layer by layer; a **display filter** such as `tcp.port == 80` or `dns` selects packets, a **capture filter** such as `host 10.0.0.5` limits what is stored. Capturing on a network you do not own or administer may be illegal and is certainly unethical.

## 6.8 Peer-to-peer and content delivery

In **BitTorrent** a file is cut into pieces; a tracker (or DHT) lists the peers; each peer downloads rarest pieces first and uploads to peers who upload to it (tit-for-tat). Distribution time for a file of size F to N peers with upload u_s from the server and u peer upload is at least max(F/u_s, F/d_min, N F/(u_s + N u)); for large N the peer-to-peer time stays almost flat while the client–server time N F / u_s grows linearly. A **CDN** places copies of popular content on servers near users and uses DNS to direct each user to a nearby copy.

## Practising the commands

This program builds a DNS query for www.example.com from raw bytes, builds a reply with a compression pointer, parses it, makes a real HTTP request to a tiny local web server and prints the Base64 values quoted in this unit.

```python
import base64, socket, struct, threading, http.server
def qname(name): return b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
query = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0) + qname("www.example.com") + struct.pack(">HH", 1, 1)
print(len(qname("www.example.com")), len(query), query.hex())
reply = struct.pack(">HHHHHH", 0x1234, 0x8180, 1, 1, 0, 0) + qname("www.example.com") + struct.pack(">HH", 1, 1)
reply += b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 3600, 4) + bytes([93, 184, 216, 34])
rid, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", reply[:12]); off = 12 + len(qname("www.example.com")) + 4
ptr, rtype, rclass, ttl, rdlen = struct.unpack(">HHHIH", reply[off:off + 12])
print("id=%#x flags=%#x answers=%d type=%d ttl=%d ip=%s" % (rid, flags, an, rtype, ttl, ".".join(map(str, reply[off + 12:off + 16]))))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"<h1>hello</h1>"; self.send_response(200); self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 50080), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
s = socket.create_connection(("127.0.0.1", 50080))
s.sendall(b"GET /index.html HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
resp = b""
while True:
    chunk = s.recv(4096)
    if not chunk: break
    resp += chunk
print(resp.decode().split("\r\n")[0]); print(resp.split(b"\r\n\r\n")[1].decode()); srv.shutdown()
print(base64.b64encode(b"Man").decode(), base64.b64encode(b"nikit:s3cret").decode(), len(base64.b64encode(bytes(300))))
```
```output
17 33 12340100000100000000000003777777076578616d706c6503636f6d0000010001
id=0x1234 flags=0x8180 answers=1 type=1 ttl=3600 ip=93.184.216.34
HTTP/1.0 200 OK
<h1>hello</h1>
TWFu bmlraXQ6czNjcmV0 400
```
The next program uses the Linux tools `ip` and `ss` and `ping` through the standard library to look at the sockets of the machine it runs on.

```python
import socket, subprocess
srv = socket.socket(); srv.bind(("127.0.0.1", 50009)); srv.listen(1)
c = socket.create_connection(("127.0.0.1", 50009)); conn, _ = srv.accept()
def run(*cmd): return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
print(run("ip", "-4", "-br", "addr", "show", "lo"))
for line in run("ss", "-tan", "sport", "=", ":50009").splitlines(): print(" ".join(line.split()[:4]))
print(run("ping", "-c", "1", "-W", "1", "127.0.0.1").splitlines()[0])
c.close(); conn.close(); srv.close()
```
```output
lo               UNKNOWN        127.0.0.1/8
State Recv-Q Send-Q Local
LISTEN 0 1 127.0.0.1:50009
ESTAB 0 0 127.0.0.1:50009
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
```
## 6.9 Seeing the ideas: names, pages, mail, transfers and monitors

Application protocols are agreements, and agreements have authors. Plate 6.1 shows three of them: Tim Berners-Lee (the Web), Paul Mockapetris (DNS) and, through the sign that celebrates him, Ray Tomlinson (e-mail with the @ sign). Plate 6.2 shows the machines behind the protocols: the first web server, a rack that really hosts a DNS root server, a VT100 terminal of the Telnet era and a data-centre hall. Plate 6.3 gives three analogies: a telephone directory for DNS, a post-office sorting rack for store-and-forward mail, and an FTP client with its two panes. Plate 6.4 pairs a real Wireshark capture of a DNS query with the bytes it decodes to. The figures that follow compute the unit's examples: the name tree, resolution time, the 33-byte query, HTTP messages, page-load time, caching, FTP ports, the mail path with Base64, peer-to-peer scaling, SNMP counters and the troubleshooting ladder.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Three people behind the application layer. (a) Sir Tim Berners-Lee (CC BY-SA 4.0), who invented the World Wide Web, HTTP, HTML and the URL at CERN in 1989-1991. (b) Paul Mockapetris (CC BY-SA 3.0), who designed the Domain Name System in 1983 so that people could use names instead of addresses. (c) A sign marking the world's first network e-mail, sent by Ray Tomlinson in 1971 (CC BY-SA 3.0); he chose the @ sign to separate the user from the host."
@ photo id="bca301/berners" cap="Tim Berners-Lee: the Web"
fit 1.0
focus 0.5 0.35
@ photo id="bca301/mockapetris" cap="Paul Mockapetris: DNS"
fit 1.0
focus 0.5 0.35
@ photo id="bca301/tomlinson" cap="Ray Tomlinson: e-mail and @"
fit 1.0
focus 0.5 0.5
```

```photogrid label="6.2" cols="4" ratio="1.0" caption="Machines behind the protocols. (a) The first web server, a NeXT computer at CERN (CC BY-SA 3.0), with the handwritten notice asking people not to switch it off. (b) A rack at an Amsterdam exchange that hosts K-root, one of the thirteen root name server identities (CC BY-SA 3.0): the labelled box answers queries for the top of the DNS tree. (c) A DEC VT100 terminal (CC BY 2.0), the kind of screen a Telnet session emulates; it sent keystrokes and showed characters, with no encryption. (d) A hall of rack-mounted servers in the CERN computer centre (CC BY-SA 3.0): the kind of place where web, mail and file servers live."
@ photo id="bca203/firstserver" cap="First web server (NeXT)"
fit 1.0
focus 0.5 0.5
@ photo id="bca301/rootk" cap="K-root DNS server rack"
fit 1.0
focus 0.45 0.45
call 0.7 0.9 0.5 0.62 "K-root"
@ photo id="bca301/vt100" cap="VT100: Telnet's terminal"
fit 1.0
focus 0.5 0.5
@ photo id="bca301/cernrack" cap="Server hall"
fit 1.0
focus 0.5 0.5
```

```photogrid label="6.3" cols="3" ratio="1.25" caption="Three analogies. (a) A telephone directory (CC BY 3.0): DNS is the Internet's directory, turning a name into a number, but distributed over millions of servers instead of one printed book. (b) The sorting racks of a travelling post office (CC BY-SA 4.0): mail is passed from one sorting point to the next and held until it can be delivered, like SMTP relaying a message from server to server. (c) The FileZilla client (CC0): the left pane is the local disk and the right pane the remote server, with one connection for commands and another for each file."
@ photo id="bca301/phonebook" cap="Directory: DNS lookup"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/sortrack" cap="Sorting racks: SMTP relay"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/filezilla" cap="FTP client: local and remote"
fit 1.25
focus 0.5 0.3
```

```photogrid label="6.4" cols="2" ratio="1.26" caption="A DNS query seen by a packet analyser. (a) A Wireshark window (CC BY-SA 4.0) showing a query for an A record: the top pane lists the packet, the middle pane decodes the layers (Ethernet, IPv4, UDP, DNS) and the bottom pane shows the raw hexadecimal bytes. (b) The same DNS fields turned into the bytes of Fig. 6.3: a standard query for www.example.com is 12 + 17 + 4 = 33 bytes, small enough to travel in one UDP datagram."
@ photo id="bca301/wireshark" cap="Wireshark: layers and bytes"
fit 1.26
focus 0.5 0.5
@ svg cap="Fields to bytes"
f = Fig(300, 238)
f.text(150, 16, "DNS query fields to bytes", size=13, color=NAVY, bold=True)
rows = [("Flags: query, RD", "01 00", BLUE, NAVY), ("Questions = 1", "00 01", BLUE, NAVY), ("Name www.example.com", "17 bytes", MINT, TEAL), ("Type A (IPv4)", "00 01", SAND, AMBER), ("Class IN", "00 01", SAND, AMBER)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 30 + i * 36
    f.box(6, y, 170, 28, a, fill=fl, stroke=st, size=12, r=4, color=NAVY)
    f.arrow([(176, y + 14), (196, y + 14)], color=SLATE, sw=1.4)
    f.box(196, y, 98, 28, b, fill="#ffffff", stroke=st, size=12, r=4, color=NAVY, bold=True)
f.text(150, 224, "12 + 17 + 4 = 33 bytes in all", size=12.5, color=RED, bold=True)
```

```svgfig label="6.1" caption="The DNS name tree, read right to left. The root (a dot) has the top-level domains below it: generic ones (com, org, edu, net) and country codes such as np. Under np the registry has created second-level domains (com.np, edu.np, gov.np), and below those sit organisations (tu.edu.np, moe.gov.np) and finally hosts (www). The dashed region is one zone: the part of the tree administered by a single authority, which holds the NS and A records for its names and may delegate sub-zones to others. A full name such as www.example.com is resolved by walking down from the root: com, then example, then www."
f = Fig(580, 290)
nodes = {"root": (290, 22), "com": (50, 86), "org": (130, 86), "edu": (210, 86), "net": (290, 86), "np": (453, 86), "excom": (53, 154), "comnp": (363, 154), "ednp": (453, 154), "govnp": (543, 154), "www": (59, 222), "tu": (453, 222), "moe": (539, 222)}
edges = [("root", "com"), ("root", "org"), ("root", "edu"), ("root", "net"), ("root", "np"), ("com", "excom"), ("np", "comnp"), ("np", "ednp"), ("np", "govnp"), ("excom", "www"), ("ednp", "tu"), ("govnp", "moe")]
f.box(318, 60, 260, 196, "", fill="#fffbeb", stroke=AMBER, r=10, dash=True, sw=1.3)
f.text(448, 247, "one zone, one authority (the .np registry)", size=10, color=AMBER, bold=True)
for a, b in edges:
    (x1, y1), (x2, y2) = nodes[a], nodes[b]
    f.line(x1, y1 + 14, x2, y2 - 14, color="#94a3b8", sw=1.4)
spec = {"root": ("root  .", 90, NAVY, "#dbeafe"), "com": ("com", 60, NAVY, BLUE), "org": ("org", 60, NAVY, BLUE), "edu": ("edu", 60, NAVY, BLUE), "net": ("net", 60, NAVY, BLUE), "np": ("np", 60, AMBER, SAND), "excom": ("example.com", 90, TEAL, MINT), "comnp": ("com.np", 66, AMBER, SAND), "ednp": ("edu.np", 66, AMBER, SAND), "govnp": ("gov.np", 66, AMBER, SAND), "www": ("www.example.com", 112, SLATE, SOFT), "tu": ("tu.edu.np", 90, SLATE, SOFT), "moe": ("moe.gov.np", 78, SLATE, SOFT)}
for k, (x, y) in nodes.items():
    t, w, st, fl = spec[k]
    f.box(x - w / 2, y - 14, w, 28, t, fill=fl, stroke=st, size=10, r=5, bold=True, color=NAVY)
f.text(10, 282, "level 0: root   level 1: top-level domain   level 2: second-level   level 3: host", size=10, color=SLATE, anchor="start")
```

```svgfig label="6.2" caption="Resolving www.example.com with nothing cached, using round-trip times of 2 ms to the local resolver, 25 ms to a root server, 30 ms to a .com server and 40 ms to the example.com name server. The host makes one recursive query (steps 1 and 8); the resolver does the iterative work: root (2-3) refers it to the .com servers, the .com server (4-5) refers it to example.com's name server, which gives the A record (6-7). The cold lookup takes 2 + 25 + 30 + 40 = 97 ms. If the .com referral is cached (it lasts days) the lookup takes 2 + 40 = 42 ms, and if the answer itself is cached (until its TTL runs out) only the 2 ms to the resolver remain, which is why most lookups feel instant."
f = Fig(580, 290)
rtt = {"res": 2, "root": 25, "tld": 30, "auth": 40}
f.box(8, 100, 92, 60, "host\nstub resolver", fill=BLUE, stroke=NAVY, size=10.5, bold=True, color=NAVY)
f.box(160, 24, 120, 204, "", fill=MINT, stroke=TEAL, r=8, sw=1.5)
f.text(220, 42, "local resolver", size=11, color=TEAL, bold=True)
f.text(220, 58, "(ISP or public)", size=10, color=SLATE)
f.text(220, 190, "keeps a cache:", size=10, color=SLATE)
f.text(220, 205, "answers by TTL", size=10, color=SLATE)
f.arrow([(100, 118), (160, 118)], color=NAVY, sw=2, label="1", lpos=(130, 110), lsize=11)
f.arrow([(160, 142), (100, 142)], color=TEAL, sw=2, label="8", lpos=(130, 158), lsize=11)
servers = [("root server", "root", "ask .com servers", NAVY, BLUE, 30), ("com TLD server", "tld", "ask ns of example.com", AMBER, SAND, 96), ("example.com NS", "auth", "A 93.184.216.34", TEAL, "#ffffff", 162)]
n = 2
for nm, key, reply, st, fl, y in servers:
    f.box(400, y, 170, 56, "", fill=fl, stroke=st, r=6, sw=1.5)
    f.text(485, y + 17, nm, size=10.5, color=st, bold=True)
    f.text(485, y + 34, "RTT %d ms" % rtt[key], size=10, color=SLATE)
    f.arrow([(280, y + 14), (400, y + 14)], color=NAVY, sw=1.6, label=str(n), lpos=(340, y + 7), lsize=10.5)
    f.arrow([(400, y + 44), (280, y + 44)], color=st, sw=1.6, label=str(n + 1), lpos=(340, y + 58), lsize=10.5)
    f.text(485, y + 49, reply, size=9.5, color=st, bold=True)
    n += 2
cold = rtt["res"] + rtt["root"] + rtt["tld"] + rtt["auth"]
warm = rtt["res"] + rtt["auth"]
hit = rtt["res"]
f.text(290, 252, "cold: 2 + 25 + 30 + 40 = %d ms     TLD cached: 2 + 40 = %d ms     answer cached: %d ms" % (cold, warm, hit), size=10.5, color=NAVY, bold=True)
f.text(290, 274, "the host's query is recursive; the resolver's queries are iterative", size=10, color=SLATE)
```

```svgfig label="6.3" caption="The DNS query for www.example.com as real bytes, built in the figure code with Python's struct rules. The 12-byte header holds the ID (abcd), the flags (0100: a standard query with recursion desired) and four counts (one question, no other records). The name is a list of labels, each with a length byte in front (03 www, 07 example, 03 com) and a zero byte at the end: 17 bytes. The type (0001, A) and class (0001, IN) make 4 more: 12 + 17 + 4 = 33 bytes. A reply repeats the question and adds one answer of 16 bytes (a 2-byte pointer c0 0c to the name at offset 12, type, class, a 4-byte TTL, a 2-byte length 0004 and the 4-byte address), so it is 12 + 21 + 16 = 49 bytes."
f = Fig(580, 262)
hdr = [0xab, 0xcd, 0x01, 0x00, 0, 1, 0, 0, 0, 0, 0, 0]
name = []
for lab in "www.example.com".split("."):
    name += [len(lab)] + [ord(c) for c in lab]
name += [0]
tail = [0, 1, 0, 1]
data = hdr + name + tail
kind = ["h"] * 12 + ["n"] * len(name) + ["t"] * 4
assert len(name) == 17 and len(data) == 33
cols = {"h": ("#dbeafe", NAVY), "n": (MINT, TEAL), "t": (SAND, AMBER)}
f.text(290, 16, "standard query: %d + %d + %d = %d bytes" % (12, len(name), 4, len(data)), size=11, color=NAVY, bold=True)
for i, b in enumerate(data):
    r, c = divmod(i, 12)
    x, y = 14 + c * 46, 30 + r * 56
    fl, st = cols[kind[i]]
    lenbyte = kind[i] == "n" and (i - 12) in (0, 4, 12, 16)
    if lenbyte:
        fl, st = "#fde68a", AMBER
    f.box(x, y, 44, 28, "%02x" % b, fill=fl, stroke=st, size=11, r=3, bold=True, color=NAVY)
    ch = chr(b) if (kind[i] == "n" and 32 < b < 127) else ""
    if ch:
        f.text(x + 22, y + 42, ch, size=10, color=TEAL, bold=True)
lx = [("header: ID, flags, counts", "#dbeafe", NAVY), ("name label bytes", MINT, TEAL), ("length byte", "#fde68a", AMBER), ("type A, class IN", SAND, AMBER)]
xx = 14
for t, fl, st in lx:
    f.box(xx, 202, 16, 14, "", fill=fl, stroke=st, r=2)
    f.text(xx + 22, 210, t, size=9.5, color=SLATE, anchor="start", vmid=True)
    xx += 28 + len(t) * 5.6
ans = 2 + 2 + 2 + 4 + 2 + 4
f.text(290, 238, "reply: 12 + 21 + %d = %d bytes (answer uses pointer c0 0c back to the name)" % (ans, 12 + 21 + ans), size=10.5, color=NAVY, bold=True)
```

```svgfig label="6.4" caption="The anatomy of an HTTP exchange. The request (left) has a request line (method, target, version), header lines, a blank line that ends the headers, and an optional body (a GET has none). The response (right) has a status line (version, code, reason phrase), headers such as the type and length of the body and a Set-Cookie header that gives the stateless protocol some memory, the blank line and then the body. Below, the five status-code families: 1xx information, 2xx success, 3xx redirection, 4xx client error and 5xx server error. Codes that students must know: 200 OK, 301 Moved Permanently, 304 Not Modified, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error and 503 Service Unavailable."
f = Fig(580, 318)
f.text(145, 14, "request (client to server)", size=11, color=NAVY, bold=True)
f.text(435, 14, "response (server to client)", size=11, color=TEAL, bold=True)
req = [("GET /index.html HTTP/1.1", "request line", BLUE, NAVY), ("Host: www.example.com", "header", MINT, TEAL), ("Accept: text/html", "header", MINT, TEAL), ("Connection: close", "header", MINT, TEAL), ("(blank line)", "ends headers", SAND, AMBER), ("(no body for GET)", "body", ROSE, RED)]
res = [("HTTP/1.1 200 OK", "status line", BLUE, NAVY), ("Content-Type: text/html", "header", MINT, TEAL), ("Content-Length: 1256", "header", MINT, TEAL), ("Set-Cookie: sid=abc123", "header", MINT, TEAL), ("(blank line)", "ends headers", SAND, AMBER), ("the page: 1256 bytes", "body", ROSE, RED)]
for i in range(6):
    y = 24 + i * 34
    for x0, items in ((6, req), (296, res)):
        t, role, fl, st = items[i]
        f.box(x0, y, 170, 28, t, fill=fl, stroke=st, size=10, r=3, color=NAVY, bold=(i == 0))
        f.text(x0 + 176, y + 14, role, size=9.5, color=st, bold=True, anchor="start", vmid=True)
fam = [("1xx", "information", "#e0e7ff", NAVY), ("2xx", "success", MINT, TEAL), ("3xx", "redirect", SAND, AMBER), ("4xx", "client error", "#fee2e2", RED), ("5xx", "server error", "#fce7f3", "#9d174d")]
for i, (c, m, fl, st) in enumerate(fam):
    f.box(6 + i * 115, 240, 108, 40, c + "\n" + m, fill=fl, stroke=st, size=10.5, r=4, bold=True, color=NAVY)
f.text(290, 296, "200 OK  |  301 Moved  |  304 Not Modified  |  400 Bad Request  |  401, 403, 404  |  500, 503", size=10, color=SLATE, bold=True)
f.text(290, 311, "each TCP segment carries these lines as plain text, so Wireshark can show them", size=9.5, color=SLATE)
```

```svgfig label="6.5" caption="Page-load time for a base file plus 4 small objects with a round-trip time of 50 ms (transmission times ignored), computed from the segments. Each TCP handshake costs one round trip (amber) and each request-and-response costs another (blue). (a) Non-persistent and serial: 5 objects x (50 + 50) = 500 ms. (b) Non-persistent with 4 parallel connections for the objects: the base takes 100 ms and the four objects together another 100 ms, so 200 ms. (c) Persistent without pipelining: one handshake (50), the base (50) and 4 x 50 for the objects = 300 ms. (d) Persistent with pipelining, which is also how HTTP/2 multiplexing behaves: 50 + 50 + 50 = 150 ms. Persistence and parallelism, not faster links, cut the waiting."
f = Fig(580, 300)
H, R = ("hs", 50), ("rr", 50)
modes = [("Non-persistent\nserial", [H, R] * 5), ("Non-persistent,\n4 parallel", [H, R, H, R]), ("Persistent,\nno pipelining", [H, R] + [R] * 4), ("Persistent,\npipelined / HTTP/2", [H, R, R])]
sc = 0.7
for i, (nm, segs) in enumerate(modes):
    y = 30 + i * 52
    tot = sum(d for _, d in segs)
    f.text(8, y + 14, nm, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    x = 150
    for k, d in segs:
        fl, st = (SAND, AMBER) if k == "hs" else (BLUE, NAVY)
        f.box(x, y, d * sc - 1, 28, "", fill=fl, stroke=st, r=2, sw=1)
        x += d * sc
    f.text(x + 6, y + 14, "%d ms" % tot, size=11, color=RED, bold=True, anchor="start", vmid=True)
for t in range(0, 501, 100):
    f.line(150 + t * sc, 232, 150 + t * sc, 238, color=SLATE, sw=1.2)
    f.text(150 + t * sc, 252, str(t), size=9.5, color=SLATE)
f.line(150, 232, 500, 232, color=SLATE, sw=1.2)
f.text(325, 268, "time in ms", size=10, color=SLATE, italic=True)
f.box(150, 280, 14, 12, "", fill=SAND, stroke=AMBER, r=2)
f.text(170, 286, "TCP handshake (1 RTT)", size=9.5, color=SLATE, anchor="start", vmid=True)
f.box(330, 280, 14, 12, "", fill=BLUE, stroke=NAVY, r=2)
f.text(350, 286, "request + response (1 RTT)", size=9.5, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="6.6" caption="Caching, in two views. Left: a conditional GET. The browser has a copy of logo.png with the validator ETag abc and asks 'send it only if it changed' (If-None-Match: abc). The server answers 304 Not Modified with no body, a few hundred bytes instead of the 48 kB image, so the object is reused from the cache. Right: average delay = h x 10 ms + (1 - h) x 200 ms for a cache that answers in 10 ms and an origin server that takes 200 ms, computed for hit ratios h of 0, 50, 80 and 95 percent: 200, 105, 48 and 29.5 ms. A hit ratio of 80 percent cuts the delay by three quarters, and the origin server's load by the same 80 percent, which is the idea behind browser caches, proxy caches and CDNs."
f = Fig(580, 280)
f.box(10, 30, 90, 50, "browser\n(has copy)", fill=BLUE, stroke=NAVY, size=10.5, bold=True, color=NAVY)
f.box(190, 30, 80, 50, "server", fill=MINT, stroke=TEAL, size=10.5, bold=True, color=NAVY)
f.line(55, 80, 55, 250, color="#94a3b8", sw=1.2, dash=True)
f.line(230, 80, 230, 250, color="#94a3b8", sw=1.2, dash=True)
f.arrow([(55, 112), (230, 112)], color=NAVY, sw=1.8)
f.text(142, 100, "GET /logo.png", size=10, color=NAVY, bold=True)
f.text(142, 126, "If-None-Match: abc", size=9.5, color=SLATE)
f.arrow([(230, 170), (55, 170)], color=TEAL, sw=1.8)
f.text(142, 158, "304 Not Modified", size=10, color=TEAL, bold=True)
f.text(142, 184, "no body (about 200 bytes)", size=9.5, color=SLATE)
f.text(142, 216, "else: 200 OK + 48 kB", size=10, color=RED, bold=True)
f.text(142, 236, "reuse copy: saves 48 kB", size=10, color=NAVY, bold=True)
f.text(400, 24, "average delay (ms)", size=10.5, color=NAVY, bold=True)
for i, hr in enumerate([0, 0.5, 0.8, 0.95]):
    d = hr * 10 + (1 - hr) * 200
    y = 44 + i * 52
    f.text(310, y + 16, "h = %d%%" % round(hr * 100), size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(366, y, d * 0.95, 30, "", fill=SAND if i < 3 else MINT, stroke=AMBER if i < 3 else TEAL, r=3)
    f.text(366 + d * 0.95 + 5, y + 16, ("%g ms" % d), size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.text(440, 262, "cache 10 ms, origin 200 ms", size=9.5, color=SLATE)
```

```svgfig label="6.7" caption="FTP uses two connections. The control connection (navy) goes from a client port (51200) to server port 21 and carries commands such as USER, PASS, LIST and RETR and replies such as 230 and 226; it stays open for the whole session. Top, active mode: the client sends PORT with its own port 51201 and the server opens the data connection from port 20 to the client; a firewall or NAT on the client side usually blocks that incoming connection. Bottom, passive mode: the client sends PASV, the server replies 227 with a port (the pair 156,64 means 156 x 256 + 64 = 40000) and the client opens the data connection to it, so every connection is outgoing from the client and passes through NAT."
f = Fig(580, 300)
ports = 156 * 256 + 64
assert ports == 40000
for top, title in ((8, "Active mode"), (158, "Passive mode (PASV)")):
    f.text(290, top + 8, title, size=11, color=NAVY, bold=True)
    f.box(8, top + 20, 96, 100, "client\n(behind NAT)", fill=BLUE, stroke=NAVY, size=10.5, bold=True, color=NAVY)
    f.box(476, top + 20, 96, 100, "FTP server", fill=MINT, stroke=TEAL, size=10.5, bold=True, color=NAVY)
    f.arrow([(104, top + 42), (476, top + 42)], color=NAVY, sw=2.2, both=True)
    f.text(290, top + 36, "control connection: client 51200 <-> server port 21 (USER, PASS, LIST, RETR)", size=9.5, color=NAVY, bold=True)
f.text(290, 100, "PORT 51201 (client tells the server where to connect)", size=9.5, color=SLATE)
f.arrow([(476, 118), (104, 118)], color=AMBER, sw=2.2, dash=True)
f.text(290, 134, "data: server port 20 to client 51201 (incoming: often blocked)", size=9.5, color=AMBER, bold=True)
f.text(290, 250, "227 Entering Passive Mode (...,156,64): port = 156 x 256 + 64 = %d" % ports, size=9.5, color=SLATE)
f.arrow([(104, 268), (476, 268)], color=TEAL, sw=2.2, dash=True)
f.text(290, 284, "data: client 51202 to server port %d (outgoing: passes NAT)" % ports, size=9.5, color=TEAL, bold=True)
```

```svgfig label="6.8" caption="The path of an e-mail and the Base64 that carries attachments. Top: the sender's mail program submits the message to its own mail server over SMTP (port 587, authenticated); that server looks up the MX record of the recipient's domain (dashed, here 10 mail.example.com) and relays the message by SMTP on port 25 to the recipient's mail server, which stores it in a mailbox; the recipient then pulls it with POP3 (110) or IMAP (143). SMTP pushes and the other two pull. Bottom: MIME turns binary into text with Base64. The three bytes 'Man' are 24 bits, regrouped as four 6-bit values (19, 22, 5, 46) that index the 64-letter alphabet to give TWFu, so every 3 bytes become 4 characters and a 300-byte attachment becomes 400 characters, one third larger."
f = Fig(580, 304)
bx = [("sender's\nmail program", 6, 84, BLUE, NAVY), ("sender's\nmail server", 130, 90, MINT, TEAL), ("recipient's\nmail server", 296, 96, SAND, AMBER), ("recipient's\nmail program", 480, 94, BLUE, NAVY)]
for t, x, w, fl, st in bx:
    f.box(x, 30, w, 48, t, fill=fl, stroke=st, size=10, bold=True, color=NAVY)
f.arrow([(90, 54), (130, 54)], color=NAVY, sw=2, label="SMTP 587", lpos=(110, 22), lsize=9.5)
f.arrow([(220, 54), (296, 54)], color=NAVY, sw=2, label="SMTP 25", lpos=(258, 22), lsize=9.5)
f.arrow([(480, 62), (392, 62)], color=AMBER, sw=2, label="POP3 110 / IMAP 143", lpos=(436, 92), lsize=9.5)
f.arrow([(392, 46), (480, 46)], color=AMBER, sw=1.5, dash=True)
f.text(436, 36, "pull", size=9.5, color=AMBER, bold=True)
f.box(110, 108, 300, 30, "DNS: MX example.com = 10 mail.example.com", fill="#ffffff", stroke=SLATE, size=9.5, r=4, dash=True, color=SLATE)
f.arrow([(175, 78), (190, 108)], color=SLATE, sw=1.3, dash=True)
base64 = __import__("base64")
b64 = base64.b64encode(b"Man").decode()
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
bits = "".join(format(c, "08b") for c in b"Man")
vals = [int(bits[i:i + 6], 2) for i in range(0, 24, 6)]
assert b64 == "TWFu" and "".join(alpha[v] for v in vals) == "TWFu"
f.text(290, 168, "Base64: 3 bytes (24 bits) become 4 characters of 6 bits each", size=11, color=NAVY, bold=True)
for i, c in enumerate(b"Man"):
    f.box(60 + i * 96, 182, 90, 26, "%s  %s" % (chr(c), format(c, "08b")), fill=BLUE, stroke=NAVY, size=10, r=3, color=NAVY)
for i, v in enumerate(vals):
    f.box(60 + i * 72, 226, 66, 26, "%s = %d" % (format(v, "06b"), v), fill=SAND, stroke=AMBER, size=9.5, r=3, color=NAVY)
    f.box(60 + i * 72, 258, 66, 24, alpha[v], fill=MINT, stroke=TEAL, size=12, r=3, bold=True, color=NAVY)
f.arrow([(350, 195), (350, 226)], color=SLATE, sw=1.4)
f.text(420, 244, "300 bytes -> %d characters" % (300 // 3 * 4), size=10.5, color=RED, bold=True, anchor="start")
f.text(420, 262, "= +33 percent", size=10.5, color=RED, bold=True, anchor="start")
f.text(420, 280, "Content-Transfer-", size=9.5, color=SLATE, anchor="start")
f.text(420, 293, "Encoding: base64", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="6.9" caption="Why peer-to-peer scales, computed. A file of F = 8000 Mbit (1 GB) is sent to N users; the server uploads at u_s = 20 Mbps, each peer uploads at u = 1 Mbps and downloads at d = 10 Mbps. Client-server needs N F / u_s = 400 N seconds, which grows without limit: 12 000 s (3.3 h) for N = 30 and 40 000 s (11.1 h) for N = 100. Peer-to-peer needs at least max(F / u_s, F / d, N F / (u_s + N u)): 800 s for N = 1 (limited by the download rate), 4 800 s (1.3 h) for N = 30 and 6 667 s (1.85 h) for N = 100, and it levels off near F / u = 8 000 s however many peers join, because every new peer brings its own upload capacity."
f = Fig(580, 280)
F, us, up, dm = 8000.0, 20.0, 1.0, 10.0
cs = lambda n: n * F / us / 3600
pp = lambda n: max(F / us, F / dm, n * F / (us + n * up)) / 3600
ax = Axes(f, 56, 24, 330, 206, (0, 100), (0, 12))
ax.grid(20, 2)
ax.axes("N peers", "hours")
ax.curve(cs, 1, 100, color=RED, sw=2.4, label="client-server", lx=62, ly=60, lsize=10.5)
ax.curve(pp, 1, 100, color=TEAL, sw=2.4)
f.text(250, 178, "peer-to-peer", size=10.5, color=TEAL, bold=True)
f.text(416, 34, "N = 1", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(416, 50, "N = 30", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(416, 66, "N = 100", size=10.5, color=NAVY, bold=True, anchor="start")
for i, n in enumerate((1, 30, 100)):
    c, p = n * F / us, max(F / us, F / dm, n * F / (us + n * up))
    f.text(478, 34 + 16 * i, "%d s" % round(c), size=10, color=RED, bold=True, anchor="start")
    f.text(530, 34 + 16 * i, "%d s" % round(p), size=10, color=TEAL, bold=True, anchor="start")
f.text(478, 22, "C-S", size=10, color=RED, bold=True, anchor="start")
f.text(530, 22, "P2P", size=10, color=TEAL, bold=True, anchor="start")
f.text(416, 108, "limit as N grows:", size=10, color=SLATE, anchor="start")
f.text(416, 124, "P2P -> F / u = %d s" % round(F / up), size=10, color=TEAL, bold=True, anchor="start")
f.text(416, 140, "each peer adds capacity", size=10, color=SLATE, anchor="start")
f.text(290, 268, "F = 8000 Mbit, server 20 Mbps, peer upload 1 Mbps, download 10 Mbps", size=10, color=SLATE)
```

```svgfig label="6.10" caption="How SNMP reads a counter and what MRTG and PRTG do with it. Top: the object identifier of ifInOctets (octets received on an interface) is a path through the MIB tree, 1.3.6.1.2.1.2.2.1.10, followed by the interface number. Bottom: the manager polls the counter twice, 300 seconds apart. In the example the counter wrapped past its 32-bit limit (4 294 967 296) between polls, so the difference is 5 000 000 + 4 294 967 296 - 3 900 000 000 = 399 967 296 octets, and utilisation = 399 967 296 x 8 / (300 x 100 Mbps) = 10.67 percent. A 32-bit counter wraps in 343.6 s at 100 Mbps, 34.4 s at 1 Gbps and 3.4 s at 10 Gbps, which is why fast links need the 64-bit ifHCInOctets counter."
f = Fig(580, 304)
oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 10]
nm = ["iso", "org", "dod", "internet", "mgmt", "mib-2", "interfaces", "ifTable", "ifEntry", "ifInOctets"]
f.text(290, 14, "MIB path to ifInOctets: " + ".".join(str(v) for v in oid), size=10.5, color=NAVY, bold=True)
for i, (v, t) in enumerate(zip(oid, nm)):
    x = 28 + i * 58
    if i:
        f.line(x - 40, 44, x - 18, 44, color="#94a3b8", sw=1.4)
    f.circle(x, 44, 15, fill=SAND if i == 9 else BLUE, stroke=AMBER if i == 9 else NAVY, label=str(v), size=11)
    f.text(x, 74, t, size=9.5, color=SLATE, bold=(i == 9))
M = 2 ** 32
c0, c1, dt, speed = 3900000000, 5000000, 300, 100e6
d = c1 + M - c0
util = d * 8 / (dt * speed) * 100
f.box(10, 96, 270, 120, "", fill=SOFT, stroke="#94a3b8", r=8)
f.text(145, 114, "two polls, 300 s apart", size=10.5, color=NAVY, bold=True)
f.text(22, 136, "t = 0 s    counter = %s" % format(c0, ","), size=10, color=SLATE, anchor="start")
f.text(22, 154, "t = 300 s  counter = %s (wrapped)" % format(c1, ","), size=10, color=SLATE, anchor="start")
f.text(22, 176, "difference = %s octets" % format(d, ","), size=10, color=NAVY, bold=True, anchor="start")
f.text(22, 196, "utilisation = %.2f percent of 100 Mbps" % util, size=10.5, color=RED, bold=True, anchor="start")
f.text(430, 106, "time to wrap a 32-bit counter", size=10.5, color=NAVY, bold=True)
for i, (lab, sp) in enumerate((("100 Mbps", 100e6), ("1 Gbps", 1e9), ("10 Gbps", 10e9))):
    t = M * 8 / sp
    y = 124 + i * 30
    f.text(300, y + 10, lab, size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(366, y, max(6, t * 0.5), 20, "", fill=SAND if t > 100 else "#fee2e2", stroke=AMBER if t > 100 else RED, r=3)
    f.text(366 + max(6, t * 0.5) + 5, y + 10, "%.1f s" % t, size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.box(10, 228, 560, 66, "SNMP operations: GET (read one variable), GETNEXT (walk the tree),\nSET (change a value), TRAP (the agent raises an alarm)\nUDP 161 for requests, 162 for traps; v1 and v2c: plaintext community string; v3: encryption", fill=BLUE, stroke=NAVY, size=9.5, r=6, color=NAVY)
```

```svgfig label="6.11" caption="The troubleshooting ladder: when a page will not open, test the layers in order and stop at the first failure. (1) Do I have an address? ip addr or ipconfig shows whether DHCP gave one; none means a Wi-Fi or DHCP problem. (2) Can I reach the gateway? ping the default gateway; no reply means a cable, access point or gateway fault. (3) Does the name resolve? nslookup returns the address or an error such as NXDOMAIN or a timeout, which points to DNS. (4) Does the port answer? curl -v shows the TCP connection and TLS handshake; a timeout means a firewall or a stopped server. (5) What does the application say? An HTTP status of 4xx or 5xx and the server log identify the application fault."
f = Fig(580, 250)
steps = [("1 Address", "ip addr", "no address:\nDHCP or Wi-Fi", BLUE, NAVY), ("2 Gateway", "ping\n192.168.1.1", "no reply:\ncable, AP, router", MINT, TEAL), ("3 Name", "nslookup\nwww.example.com", "NXDOMAIN or\ntimeout: DNS", SAND, AMBER), ("4 Port", "curl -v\nhttps://site", "timeout:\nfirewall, server", "#fce7f3", "#9d174d"), ("5 Application", "status code,\nserver log", "4xx or 5xx:\napplication", "#e0e7ff", NAVY)]
for i, (h, cmd, bad, fl, st) in enumerate(steps):
    x = 6 + i * 115
    f.box(x, 20, 104, 26, h, fill=st, stroke=st, size=10.5, r=4, bold=True, color="#ffffff")
    f.box(x, 52, 104, 58, cmd, fill=fl, stroke=st, size=10, r=4, color=NAVY, bold=True)
    f.arrow([(x + 52, 110), (x + 52, 138)], color=RED, sw=1.6)
    f.box(x, 140, 104, 54, bad, fill="#fee2e2", stroke=RED, size=9.5, r=4, color=RED)
    if i < 4:
        f.arrow([(x + 104, 81), (x + 115, 81)], color=TEAL, sw=1.8)
f.text(290, 214, "pass -> go to the next rung      fail -> the red box is the first place to look", size=10.5, color=NAVY, bold=True)
f.text(290, 234, "DHCP, ARP, DNS, TCP and HTTP all run in this order every time a page opens", size=10, color=SLATE)
```

### 6.9.1 Eight uses of application-layer protocols in Nepal

1. **Domain names for Nepali services.** Addresses such as moe.gov.np, tu.edu.np and the banks' .com.np names are resolved by DNS through the zone tree of Fig. 6.1. A student only types a name, and the resolver walks root, np and the organisation's own name server in a few milliseconds (Fig. 6.2). Caching explains why the same site opens instantly the second time, and why a changed address can take hours to reach everyone: the old record lives until its TTL ends.
2. **Secure websites and payments.** ConnectIPS, Fonepay, eSewa and internet banking all use HTTPS, which is HTTP inside TLS on port 443. The request and response have the shape of Fig. 6.4, and the Set-Cookie header keeps you logged in between pages. If the certificate or the connection fails, the browser stops with a warning instead of sending your password, which is the server authentication that plain HTTP lacks.
3. **Government portals and result sites.** Pages such as exam results, the Nagarik App services and the Public Service Commission notices are web applications behind HTTP. On result day thousands of students ask for the same page, so caches and CDNs (Fig. 6.6) serve most requests without touching the origin server. A hit ratio of 80 percent cuts both the delay and the server load by about four fifths.
4. **E-mail in offices and colleges.** Colleges and offices use mail servers or Google and Microsoft mail with their own domain. A message goes from the mail program to the sender's server by SMTP, is relayed to the server found by the MX record, and is collected with IMAP so that the phone and the laptop show the same folders (Fig. 6.8). Attachments are sent as Base64, which is why a 3 MB photo makes a 4 MB e-mail.
5. **Remote administration and file transfer.** A web developer in Kathmandu manages a hosting server with SSH and uploads files with SFTP or FTPS. Old plain FTP and Telnet are avoided because passwords cross the network readable. Passive mode (Fig. 6.7) is the setting that makes an FTP client work from behind a home router, because every connection is opened outward by the client.
6. **Video, software and content delivery.** Large video services and software-update providers keep cache servers inside many internet providers and use DNS to send each user to a nearby copy. The page or video then comes from a short path with a small round-trip time instead of from overseas. This is the same idea as the cache in Fig. 6.6 and is why popular videos start quickly even on a modest link.
7. **Monitoring an ISP or campus network.** A network operations team polls router and switch counters with SNMP every five minutes and draws the graphs with MRTG or PRTG. From two readings they compute utilisation, as in Fig. 6.10, and set alarms when a link stays above about 80 percent. Packet Tracer is used in teaching labs to build the same network before touching real equipment.
8. **Fault finding and sharing files.** When a page does not open, the ladder of Fig. 6.11 (address, gateway, name, port, application) finds the broken layer in a few minutes with ip addr, ping, nslookup and curl. Wireshark (Plate 6.4) shows the actual DNS and HTTP messages when the commands are not enough. Peer-to-peer tools such as BitTorrent spread large files, for example Linux images, over many students' computers (Fig. 6.9) so that no single server is overloaded.

## Formula and fact sheet

- Ports: HTTP 80, HTTPS 443, DNS 53, SMTP 25 (587), POP3 110, IMAP 143, FTP 21 (data 20), SSH 22, Telnet 23, DHCP 67/68, SNMP 161/162, BGP 179.
- DNS records: A, AAAA, NS, CNAME, MX, TXT, PTR, SOA. Name encoding: length-prefixed labels, 0 terminator.
- HTTP codes: 2xx success, 3xx redirect, 4xx client error, 5xx server error.
- Page load (RTT 50 ms, base plus 4 objects): non-persistent 500 ms, persistent 300 ms.
- Base64: 3 bytes → 4 characters (+33 %).
- Link utilisation from SNMP counters = Δ octets × 8 / (Δ t × speed).

## Chapter summary

- Application protocols are agreements over sockets: client–server or peer-to-peer, over TCP or UDP.
- DNS maps names to addresses with a distributed hierarchy of servers, caching by TTL and typed records.
- HTTP is a stateless text protocol; cookies add state, caching and persistent connections reduce load time; HTTPS adds TLS.
- FTP separates control and data connections; SMTP pushes mail, POP3 and IMAP pull it; MIME carries binary content as Base64.
- SNMP, MRTG, PRTG, Packet Tracer and Wireshark are the tools to monitor, simulate and analyse.

## Practice

1. Explain how a resolver finds www.example.com when nothing is cached.
2. Encode the DNS name www.example.com as it appears in a query and give the size of the query message.
3. List five DNS record types with their meaning.
4. For a page of a base file and 4 objects with RTT = 50 ms, compute the load time for non-persistent serial and persistent HTTP.
5. Differentiate GET and POST; give the meaning of 301, 304, 404 and 503.
6. What is a cookie and how does it give HTTP state?
7. Why does FTP use two connections? Compare active and passive mode.
8. Compare POP3 and IMAP.
9. What does MIME add to SMTP and why does Base64 enlarge the data by one third?
10. What are SNMP, a MIB and a trap?
11. What would you check, in order, if a page does not open?

::: note Answers and worked solutions
**1.** The host asks its recursive resolver; the resolver asks a root server, which refers it to the .com servers; those refer it to the example.com name server, which returns the A record; the resolver caches it for its TTL and replies to the host.
**2.** 03 77 77 77 07 65 78 61 6d 70 6c 65 03 63 6f 6d 00, 17 bytes; the query is 12 header + 17 name + 4 (type and class) = 33 bytes.
**3.** A (IPv4 address), AAAA (IPv6), NS (authoritative server), CNAME (alias), MX (mail exchanger), also TXT, PTR, SOA.
**4.** Non-persistent serial: 5 × (50 + 50) = 500 ms. Persistent without pipelining: 50 (handshake) + 50 (base) + 4 × 50 = 300 ms.
**5.** GET retrieves and has no body, with parameters in the URL; POST sends data in the body. 301 permanent redirect, 304 not modified (use cache), 404 not found, 503 service unavailable.
**6.** A cookie is a small value set by the server and returned by the browser on each request; the server uses it as a key to its stored session data.
**7.** Control (commands) is separated from data; the control connection stays open while data connections come and go. In active mode the server connects back to the client (problems with NAT and firewalls); in passive mode the client opens both.
**8.** POP3 downloads (and normally deletes) mail to one device; IMAP keeps mail and folders on the server so multiple devices stay in sync.
**9.** MIME describes content type and encoding so that non-ASCII data and attachments can travel through 7-bit SMTP. Base64 turns 3 bytes (24 bits) into four 6-bit characters, so the size grows by 4/3.
**10.** SNMP is a protocol to monitor and manage devices; the MIB is the tree of named variables on an agent; a trap is an unsolicited alarm message from an agent to the manager.
**11.** (1) Link and address: `ip addr`, (2) gateway: `ping`, (3) name: `nslookup` or `dig`, (4) port: `curl -v` or telnet to the port, (5) the application: server logs.
:::

## Model answers for Unit 6

**Q1. Explain the Domain Name System: hierarchy, resource records and the resolution of a name. (10 marks)**

**Introduction.** People remember names such as www.example.com, but routers forward packets by IP address. The Domain Name System (DNS) is a distributed, hierarchical database that translates names into addresses and back. It runs over UDP port 53 (TCP for large replies and zone transfers) and is used before almost every other application protocol.

**Hierarchy.** The name space is a tree read from right to left (Fig. 6.1). The root is at the top, below it are the top-level domains (generic ones such as com, org, edu and country codes such as np), below them the second-level domains (example.com, or com.np, edu.np and gov.np under Nepal's code) and finally hosts. A zone is the part of the tree managed by one authority, and an authority can delegate sub-zones to others. Thirteen root server identities exist, each copied at hundreds of sites by anycast, so no single machine is a bottleneck.

**Resolution.** The host sends one recursive query to its local resolver. If the resolver has no cached answer it works iteratively (Fig. 6.2): it asks a root server, which refers it to the .com servers; those refer it to the name server of example.com, which returns the A record. The resolver caches every answer for its TTL and replies to the host. With round-trip times of 2, 25, 30 and 40 ms a cold lookup takes 97 ms, but with the answer cached only 2 ms.

**Resource records.** Each entry is a typed record:

| Type | Meaning | Example |
|---|---|---|
| A / AAAA | name to IPv4 / IPv6 address | www.example.com A 93.184.216.34 |
| NS | authoritative name server of a zone | example.com NS a.iana-servers.net |
| CNAME | alias to the canonical name | www CNAME web.example.com |
| MX | mail server with preference (lowest first) | example.com MX 10 mail.example.com |
| PTR | address to name (reverse lookup) | under in-addr.arpa |
| TXT, SOA | free text (SPF, DKIM); zone start of authority | serial, refresh, TTL |

**Message and security.** A query has a 12-byte header, the question and the records; names are length-prefixed labels, so www.example.com takes 17 bytes and the query 33 bytes (Fig. 6.3). Replies use a compression pointer to avoid repeating the name. Caching cuts delay and load, but forged replies can poison a cache, so DNSSEC adds digital signatures to the records.

**Conclusion.** DNS combines a hierarchy of delegated zones, typed records and TTL-based caching to give fast, scalable, fault-tolerant name lookup without any central server.

**Q2. Explain HTTP: the messages, methods, status codes, persistent connections, cookies and caching. (10 marks)**

**Introduction.** The Hypertext Transfer Protocol (HTTP) is the application protocol of the World Wide Web. It is a text-based request and response protocol over TCP port 80 (443 with TLS for HTTPS), and it is stateless: the server keeps no memory of earlier requests. A page is a base HTML file plus objects (images, scripts), each named by a URL of the form scheme://host:port/path?query#fragment.

**Messages.** A request has a request line (method, target, version), header lines, a blank line and an optional body. A response has a status line, headers, a blank line and the body (Fig. 6.4).

| Methods | Meaning | Status codes | Meaning |
|---|---|---|---|
| GET | fetch a resource (safe, idempotent) | 200 | OK |
| HEAD | headers only | 301 / 304 | moved permanently / not modified |
| POST | send data for processing | 400 / 401 / 403 / 404 | bad request / unauthorised / forbidden / not found |
| PUT / DELETE | replace / remove (idempotent) | 500 / 503 | server error / service unavailable |

**Persistent connections.** HTTP/1.0 opened a new TCP connection for every object (non-persistent); HTTP/1.1 keeps it open (persistent) and can pipeline requests. For a base file and 4 objects with RTT = 50 ms the load time is 500 ms non-persistent serial, 300 ms persistent without pipelining and 150 ms pipelined (Fig. 6.5). HTTP/2 multiplexes streams over one connection, and HTTP/3 uses QUIC over UDP to avoid head-of-line blocking.

**State and caching.** A cookie is a value sent by the server in Set-Cookie and returned by the browser in every later request, which lets the server keep a session (login, cart) but also lets sites track users. A web cache stores objects; a conditional GET with If-None-Match returns 304 Not Modified without a body when the copy is current (Fig. 6.6). A hit ratio of 80 percent cuts the average delay from 200 ms to 48 ms.

**Security.** Basic authentication only Base64-encodes user:password, which anyone can decode, so HTTPS (HTTP inside TLS) is required for encryption, integrity and server authentication.

**Conclusion.** HTTP is simple and text-based, and persistence, caching, cookies and TLS were added around it to make the Web fast, stateful and secure.

**Q3. Describe the architecture of electronic mail with SMTP, POP3, IMAP and MIME. (10 marks)**

**Introduction.** Electronic mail is an asynchronous, store-and-forward service: the sender and the receiver need not be online together. It has three parts: user agents (Outlook, Thunderbird, webmail), mail servers with mailboxes, and the protocols between them (Fig. 6.8).

**Sending.** The sender's user agent submits the message to its own mail server by SMTP (port 587 with authentication). That server finds the recipient's mail server by the MX record of the destination domain, then relays the message by SMTP on port 25. If the destination is unreachable the message waits in a queue and is retried, like the sorting racks of a post office in Plate 6.3.

**Receiving.** The recipient fetches mail from the mailbox with a pull protocol. POP3 (port 110) downloads messages and usually deletes them from the server, which is simple and works offline but ties the mail to one device. IMAP (port 143) leaves the mail on the server and synchronises folders and flags, so a phone and a laptop show the same mailbox.

**SMTP dialogue.** The client sends HELO, MAIL FROM, RCPT TO and DATA, ends the message with a line holding only a dot, and sends QUIT; the server answers each command with a code such as 220, 250, 354 and 221.

**MIME.** SMTP carries only 7-bit ASCII, so MIME adds headers (Content-Type: image/jpeg, Content-Transfer-Encoding: base64). Base64 splits 3 bytes into four 6-bit values, so "Man" becomes TWFu and a 300-byte attachment becomes 400 characters, one third larger.

| Protocol | Port | Direction | Role |
|---|---|---|---|
| SMTP | 25 / 587 | push | send and relay |
| POP3 | 110 | pull | download, usually delete |
| IMAP | 143 | pull | keep on server, sync folders |

**Spam defence.** SPF, DKIM and DMARC records in DNS let a receiver check that a message really came from the domain it claims.

**Example.** When a student at a Kathmandu college mails a report to a teacher, the message first reaches the college's mail server, which asks DNS for the MX record of the teacher's domain, relays the message to that server by SMTP and leaves it in the mailbox. The teacher's phone then reads it with IMAP, and the same message is still visible on the office computer. If the receiving server is switched off, the sending server keeps the message in its queue and retries for several days before returning an error, which is the reliability that makes e-mail suitable for official work.

**Conclusion.** SMTP pushes, POP3 and IMAP pull, MIME carries any content, and DNS finds the servers, so mail works across millions of independent systems.

**Q4. Why does FTP use two connections? Compare active and passive mode. (5 marks)**

FTP separates commands from data. The **control connection** goes from a client port to server port 21 and stays open for the whole session; it carries commands (USER, PASS, LIST, RETR, STOR) and replies (230 logged in, 226 transfer complete). A new **data connection** is opened for every file or directory listing and closed afterwards. Because control is out of band, a transfer can be aborted, the session keeps its state, and large data flows do not mix with commands.

In **active mode** the client sends PORT with its own address and port (for example 51201) and the server opens the data connection from port 20 back to the client. A firewall or NAT in front of the client normally blocks that incoming connection, so active mode often fails. In **passive mode** the client sends PASV and the server replies 227 with a port, for example 156,64 meaning 156 x 256 + 64 = 40000; the client opens the data connection to that port, so every connection is outgoing and passes through NAT (Fig. 6.7).

| Feature | Active | Passive |
|---|---|---|
| Who opens the data connection | server (from port 20) | client |
| Command | PORT | PASV |
| Works behind NAT or firewall | usually not | yes |

FTP sends passwords in plaintext, so FTPS (FTP with TLS) or SFTP (a different protocol over SSH, port 22) should be used.

**Q5. A page has a base file and 4 small objects and the round-trip time is 50 ms. Compute the load time for the HTTP modes. (5 marks)**

Ignore transmission times, so each TCP handshake costs one round trip (50 ms) and each request and response costs one more (50 ms). The result is shown in Fig. 6.5.

| Mode | Working | Time |
|---|---|---|
| Non-persistent, serial | 5 objects x (50 + 50) | 500 ms |
| Non-persistent, 4 parallel connections | base (50 + 50), then 4 objects in parallel (50 + 50) | 200 ms |
| Persistent, no pipelining | handshake 50, base 50, then 4 x 50 | 300 ms |
| Persistent, pipelined (HTTP/2 style) | handshake 50, base 50, all 4 objects together 50 | 150 ms |

Each row is just a count of round trips multiplied by 50 ms, so the working is easy to check: serial non-persistent uses 10 round trips, persistent without pipelining uses 6, and the pipelined case uses 3. Browsers open several parallel connections to the same server (usually up to six) for exactly this reason, trading extra connections for lower delay, but each connection still pays its own handshake. Non-persistent HTTP is slow because it pays a handshake for every object and the operating system must allocate resources for each connection. Persistence removes the repeated handshakes, and pipelining or multiplexing removes the waiting between requests. The speed-up comes from fewer round trips, not from a faster link, which is why a nearby cache or CDN helps so much: it reduces the RTT itself.

**Q6. Compare client-server and peer-to-peer architectures with the file-distribution time. (5 marks)**

In **client-server**, a server with a fixed address answers requests from many clients. It is easy to manage, secure and update, but the server's bandwidth and cost grow with the number of users, and it is a single point of failure unless replicated. In **peer-to-peer** every host acts as client and server, so each peer that downloads a file also uploads pieces of it. Capacity grows with the number of peers, but management, security and finding peers (a tracker or a distributed hash table) are harder.

For a file F sent to N users, client-server needs at least N F / u_s, where u_s is the server upload rate. Peer-to-peer needs at least max(F / u_s, F / d, N F / (u_s + N u)). With F = 8000 Mbit, u_s = 20 Mbps, u = 1 Mbps and d = 10 Mbps, N = 30 takes 12 000 s for client-server but 4 800 s for peer-to-peer, and N = 100 takes 40 000 s against 6 667 s (Fig. 6.9). The client-server time grows linearly while the peer-to-peer time levels off near F / u = 8 000 s.

BitTorrent works this way: a tracker lists the peers, pieces are fetched rarest first, and peers upload preferentially to those who upload to them (tit-for-tat). A CDN is the managed alternative: copies of popular content are placed on servers near users.

**Q7. Explain SNMP, the MIB, MRTG and PRTG, Packet Tracer and Wireshark. (5 marks)**

**SNMP** (Simple Network Management Protocol, UDP 161, traps on 162) lets a manager monitor and control agents running in routers, switches and servers. Its operations are GET (read), GETNEXT (walk the tree), SET (change a value) and TRAP (an alarm sent by the agent). Versions 1 and 2c authenticate with a plaintext community string; version 3 adds authentication and encryption. The variables are named in the **MIB** (Management Information Base), a tree of object identifiers: ifInOctets is 1.3.6.1.2.1.2.2.1.10, followed by the interface number (Fig. 6.10).

**MRTG** and **PRTG** poll SNMP counters on a schedule, usually every five minutes, and draw traffic graphs. From two readings, utilisation = difference in octets x 8 / (seconds x link speed); a counter that wraps past 4 294 967 296 must be corrected, as in the worked example giving 10.67 percent, and fast links need 64-bit counters.

**Packet Tracer** is a Cisco simulator for teaching: you build a topology, configure routers and switches and watch packets move, without any hardware. **Wireshark** is a packet analyser that captures frames from an interface and decodes every layer (Plate 6.4), so a DNS query, a TCP handshake or an HTTP request can be read byte by byte. The first two tools answer "how busy is the network?", the last two "how does it work and what went wrong?".

**Q8. Find the size of the DNS query for www.example.com and explain why Base64 enlarges data by one third. (5 marks)**

A DNS message starts with a fixed 12-byte header: ID, flags, and four counts. The question then holds the name, a type and a class. A name is a list of labels, each preceded by its length, and ends with a zero byte: www.example.com is 03 77 77 77 07 65 78 61 6d 70 6c 65 03 63 6f 6d 00, which is 1 + 3 + 1 + 7 + 1 + 3 + 1 = 17 bytes. The type A (0001) and class IN (0001) add 4 bytes. The query is therefore 12 + 17 + 4 = 33 bytes (Fig. 6.3). A reply repeats the question and adds one answer of 16 bytes (the 2-byte pointer c0 0c, type, class, a 4-byte TTL, a 2-byte length and the 4-byte address), so it is 12 + 21 + 16 = 49 bytes. Both fit easily in one UDP datagram.

SMTP can carry only 7-bit ASCII, so MIME turns binary data into text with Base64. Three bytes are 24 bits, which are regrouped into four 6-bit values, each of which selects one of 64 printable characters. The bytes "Man" give the values 19, 22, 5 and 46 and the text TWFu (Fig. 6.8). Every 3 bytes become 4 characters, so the size grows by 4/3: a 300-byte file becomes 400 characters, an increase of 33 percent. The price is paid for being able to send any file through a text-only system.
