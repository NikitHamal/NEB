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
