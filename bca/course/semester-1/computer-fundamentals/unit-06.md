---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 6
title: Internet and the World Wide Web
hours: 6
area: BCA 101 · Computer Fundamentals and Applications · Unit 6
---

The **Internet** is the global network of networks; the **World Wide Web** is one service that runs on it. People often use the words interchangeably, but the difference matters: email, video calls and online games use the Internet without using the Web. This unit explains how the Internet is organised, how a web page reaches your screen, and how to use and protect yourself on it.

::: key What this unit gives you
- History, structure and ISPs; the Internet versus the Web.
- URLs, DNS and HTTP: exactly what happens when you open a page.
- Browsers, search engines, email and other services.
- Web generations, intranet/extranet, and how a web page is built.
- Security threats, safe practices, and Nepal's legal context.
:::

## 6.1 The Internet: history and structure

| Year | Milestone |
|---|---|
| 1969 | ARPANET connects four US universities (packet switching) |
| 1971 | first email (Ray Tomlinson, the `@` sign) |
| 1983 | ARPANET switches to TCP/IP, the birth of "the Internet" |
| 1989–91 | Tim Berners-Lee at CERN proposes and builds the World Wide Web: HTML, HTTP, URL, first browser |
| 1993 | Mosaic, the first widely used graphical browser |
| 1998 | Google founded |
| 2004–2007 | social media (Facebook), smartphones (iPhone, 2007): Web 2.0 on mobile |

Nepal's first public email and Internet services appeared in the mid-1990s, and today broadband (fibre and wireless) and mobile data are the main access methods.

**Structure.** The Internet has no owner. It is a hierarchy: **Tier-1** carriers own global backbones and exchange traffic freely; **Tier-2/3 ISPs** buy transit and connect homes, colleges and businesses; **IXPs** (Internet exchange points) let networks swap traffic locally. An **ISP** (Internet service provider) gives you access: dial-up (obsolete), ADSL, cable, FTTH (fibre to the home), wireless/WiMAX, mobile 4G/5G, VSAT satellite.

| Access technology | Typical speed | Note |
|---|---|---|
| Dial-up | ≤ 56 kbps | obsolete, blocks the phone line |
| ADSL | a few Mbps | over copper telephone line |
| FTTH | 50 Mbps to 1 Gbps | optical fibre to the building |
| 4G LTE / 5G | tens to hundreds of Mbps | mobile |
| VSAT | few Mbps, ~600 ms round trip | remote areas |

```photogrid label="6.1" cols="2" ratio="1.45" caption="The Internet is physical. (a) An Interface Message Processor (IMP), the router of the ARPANET, at the Computer History Museum. (b) Samples of undersea fibre cable, from lightweight to double-armoured, with the layers named. (c) A cold aisle between server racks in a data centre. (d) A Nepal Telecom mobile tower in Achham district."
@ photo id="bca101/imp" cap="IMP: the 1969 ARPANET router, one per university"
fit 1.45
@ photo id="bca101/subcable" cap="Undersea cable: fibre, copper power conductor, steel armour"
fit 1.45
@ photo id="bca101/datacenter" cap="Data centre: racks of web, mail and database servers"
fit 1.45
@ photo id="bca101/nttower" cap="Mobile tower: radio access for 4G data in the hills"
fit 1.45
focus 0.5 0.80
```

### 6.1.1 Eight features of the Internet

1. **Global reach.** The Internet connects billions of devices in almost every country, so a student in Biratnagar can open the same website as a student in Boston. Distance changes only the delay, not the access. Nepali families abroad use it every day to talk to relatives in Nepal at almost no cost.
2. **Decentralised and ownerless.** No single company or government runs the whole Internet; thousands of independent networks agree to exchange traffic. If one network fails, others carry on. In Nepal this shows in the many ISPs and mobile operators that interconnect at local exchange points.
3. **Packet switching.** Data is cut into small packets that travel separately and are put back together at the destination. Links are shared by many users, which makes the network cheap and efficient. A video call from Pokhara to Kathmandu is therefore thousands of small packets, not one reserved circuit.
4. **Common open protocols.** TCP/IP, DNS, HTTP and SMTP are public standards, so a phone, a laptop and a bank server from different makers can understand each other. Anyone may build a new service on them without asking permission. This openness is why ConnectIPS and Fonepay apps work on any Android or iPhone.
5. **Scalability.** The same design has grown from four computers in 1969 to billions of devices, and IPv6 provides about 3.4 x 10^38 addresses for future growth. New users and networks simply plug in. Nepal's mobile data users grew from almost none to millions in about fifteen years on this principle.
6. **Reliability through redundancy.** Routers choose another path when a link breaks, and big sites keep copies in several data centres. Nepal links to the world through more than one border route, so a cut on one route does not stop all Internet traffic. A good design hides failures from the user.
7. **Many services in one network.** Web, email, voice, video, file transfer, online games and the Internet of Things all use the same infrastructure. One broadband line can carry a Google Classroom lesson, a Viber call and a Netflix film at the same time. Multimedia makes the Internet useful for study, work and entertainment.
8. **Low cost and resource sharing.** Information, software and storage are shared instead of being duplicated, and messages cost almost nothing compared with letters or phone calls. A college can serve notices, results and library books to thousands of students from one server. Cloud services such as Google Drive remove the need to buy expensive hardware.

## 6.2 Names, addresses and the journey of a web page

- **IP address**: the numeric address of a host (`142.250.77.46`). Machines use it; people do not remember it.
- **Domain name**: a readable name arranged right to left from the **top-level domain** (TLD): `www.tu.edu.np` → `.np` (country TLD) → `edu.np` (education) → `tu` (organisation) → `www` (host). Generic TLDs: `.com`, `.org`, `.net`; Nepal's: `.com.np`, `.edu.np`, `.gov.np`, `.org.np`.
- **DNS (Domain Name System)** is a distributed directory that translates names to IP addresses.
- **URL** = protocol + host + path + query + fragment:

```text
https://www.example.com:443/notes/unit6.html?lang=en#dns
\___/   \_____________/ \_/ \______________/ \_____/ \_/
scheme      host       port      path        query  fragment
```

**What happens when you type a URL and press Enter**

1. The browser checks its cache, then asks the OS resolver, then your ISP's **recursive DNS server**.
2. If unknown, that server asks a **root server** → the **TLD server** (`.com`) → the site's **authoritative server**, which returns the IP address. The answer is cached for its time-to-live.
3. The browser opens a **TCP connection** to the IP on port 443 (three-way handshake), then a **TLS handshake** to encrypt it (for HTTPS).
4. It sends an **HTTP request**: `GET /notes/unit6.html HTTP/1.1` plus headers (Host, cookies, User-Agent).
5. The **web server** returns a response: a status line, headers, and the HTML body.
6. The browser parses the HTML, requests the CSS, JavaScript and images it refers to, lays out the page and shows it.

**HTTP methods:** GET (read), POST (send/create), PUT (replace), DELETE (remove). **Status codes:** 200 OK, 301 moved permanently, 304 not modified, 400 bad request, 401 unauthorised, 403 forbidden, 404 not found, 500 server error. HTTP is **stateless**: the server does not remember you between requests, which is why **cookies** (small pieces of data the browser sends back) and sessions exist.

**HTTPS** is HTTP over **TLS**: it encrypts traffic and uses a **certificate** to prove the site's identity. The padlock means the connection is encrypted, *not* that the site is honest.

```svgfig label="6.1" caption="DNS resolution of www.example.com.np: the resolver asks root, TLD and authoritative servers in turn (steps 2-4), the answer returns (5), then the browser connects to the IP address (6)."
f = Fig(760, 320)
for i, t in enumerate(["1  Browser and OS check their cache", "2  Resolver asks a root server: who runs .np?", "3  Resolver asks the .np TLD server: who runs example.com.np?", "4  Resolver asks the authoritative server: IP of www?", "5  IP address 203.0.113.10 returns to the browser", "6  Browser opens a TCP/TLS connection to that IP"]):
    f.text(10, 14 + i * 14, t, size=9.5, color=SLATE, anchor="start")
f.box(10, 130, 110, 56, "Browser +\nOS cache", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(170, 130, 120, 56, "Recursive\nresolver (ISP)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(400, 110, 120, 44, "Root server ( . )", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(400, 170, 120, 44, "TLD server ( .np )", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(400, 230, 120, 44, "Authoritative\nexample.com.np", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(630, 130, 110, 56, "Web server\n203.0.113.10", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(120, 150), (170, 150)], color=NAVY, label="1", lpos=(145, 142))
f.arrow([(290, 140), (340, 140), (340, 132), (400, 132)], color=AMBER, label="2", lpos=(370, 124))
f.arrow([(290, 158), (345, 158), (345, 192), (400, 192)], color=AMBER, label="3", lpos=(372, 184))
f.arrow([(290, 176), (320, 176), (320, 252), (400, 252)], color=AMBER, label="4", lpos=(360, 244))
f.arrow([(520, 262), (580, 262), (580, 300), (230, 300), (230, 186)], color=TEAL, label="5", lpos=(400, 293))
f.arrow([(65, 186), (65, 312), (685, 312), (685, 186)], color=RED, label="6", lpos=(560, 305))
```

```svgfig label="6.2" caption="HTTPS request-response cycle between a browser (client) and a web server: TCP handshake, TLS handshake, then HTTP."
f = Fig(760, 330)
f.box(60, 10, 140, 40, "Browser (client)", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(560, 10, 140, 40, "Web server", fill=MINT, stroke=TEAL, size=12, bold=True)
f.line(130, 50, 130, 320, color=NAVY, dash=True); f.line(630, 50, 630, 320, color=TEAL, dash=True)
steps = [("SYN", 1, "TCP: connection request"), ("SYN-ACK", -1, "TCP: server agrees"), ("ACK", 1, "TCP: connection open"), ("ClientHello", 1, "TLS: supported ciphers"), ("ServerHello + certificate", -1, "TLS: proof of identity"), ("Key exchange, Finished", 1, "TLS: shared session key"), ("GET /index.html", 1, "HTTP request (encrypted)"), ("200 OK + HTML", -1, "HTTP response (encrypted)")]
for i, (t, d, n) in enumerate(steps):
    y = 76 + i * 33
    col = AMBER if i < 3 else (TEAL if i < 6 else RED)
    f.arrow([(130, y), (630, y)] if d == 1 else [(630, y), (130, y)], color=col, label=t, lpos=(380, y - 6), lsize=9)
    f.text(695 if False else 735, y, "", size=8)
    f.text(30, y, str(i + 1), size=9, color=col, bold=True)
f.text(690, 160, "1-3 TCP", size=9, color=AMBER, bold=True); f.text(690, 190, "4-6 TLS", size=9, color=TEAL, bold=True); f.text(690, 270, "7-8 HTTP", size=9, color=RED, bold=True)
```

```svgfig label="6.3" caption="Bandwidth and distance are different limits. (A) Time to download 100 MB at five access speeds, computed from size divided by speed. (B) Round-trip delay caused only by distance: a geostationary satellite link (four trips of 35,786 km at the speed of light) against 5,000 km of fibre (light travels at about two thirds of its vacuum speed in glass)."
import math
f = Fig(760, 330)
# left: 100 MB download time at five access speeds (log-length bars)
sizeMB = 100; bits = sizeMB * 8e6
rows = [("Dial-up 56 kbps", 56e3), ("ADSL 4 Mbps", 4e6), ("4G 30 Mbps", 30e6), ("FTTH 100 Mbps", 100e6), ("FTTH 1 Gbps", 1e9)]
def fmt(t):
    if t >= 3600: return f"{t/3600:.1f} h"
    if t >= 60: return f"{t/60:.1f} min"
    return f"{t:.1f} s"
ts = [bits / r for _, r in rows]
print([round(t, 2) for t in ts], [fmt(t) for t in ts])
assert abs(ts[0] - 14285.7) < 0.1 and abs(ts[1] - 200) < 1e-9 and abs(ts[3] - 8) < 1e-9 and abs(ts[4] - 0.8) < 1e-9
f.text(10, 20, "A. Time to download a 100 MB file (bar length is logarithmic)", size=11.5, color=NAVY, bold=True, anchor="start")
cols = [ROSE, SAND, MINT, BLUE, BLUE]; strokes = [RED, AMBER, TEAL, NAVY, NAVY]
for i, ((name, r), t) in enumerate(zip(rows, ts)):
    y = 44 + i * 52
    L = (math.log10(t) + 1.2) * 52          # 0.8 s -> ~58 px, 3.97 h -> ~300 px
    f.text(10, y + 15, name, size=10.5, color=SLATE, anchor="start")
    f.box(150, y, L, 28, "", fill=cols[i], stroke=strokes[i])
    f.text(150 + L + 8, y + 15, fmt(t), size=11, color=strokes[i], bold=True, anchor="start", vmid=True)
f.text(10, 312, "time = (100 x 8 000 000 bits) / speed; real speeds are lower (overheads, sharing)", size=10.5, color=SLATE, anchor="start")
# right: round-trip propagation delay only
c = 299792.458
geo = 4 * 35786 / c * 1000          # up+down for request, up+down for reply
fib = 2 * 5000 / 200000 * 1000      # 5 000 km of fibre, light at 2/3 c
print(round(geo, 1), round(fib, 1), round(geo / fib, 1))
assert 476 < geo < 479 and abs(fib - 50) < 1e-9
f.text(520, 20, "B. Round-trip delay from distance alone", size=11.5, color=NAVY, bold=True, anchor="start")
bx = 540
f.box(bx + 110, 70, 40, 200, "", fill=ROSE, stroke=RED)
f.box(bx, 70 + 200 - 200 * fib / geo, 40, 200 * fib / geo, "", fill=BLUE, stroke=NAVY)
f.text(bx + 20, 70 + 200 - 200 * fib / geo - 9, f"{fib:.0f} ms", size=11, color=NAVY, bold=True)
f.text(bx + 130, 62, f"{geo:.0f} ms", size=11, color=RED, bold=True)
f.text(bx + 20, 288, "Fibre", size=10.5, color=SLATE); f.text(bx + 20, 302, "5 000 km", size=10.5, color=SLATE)
f.text(bx + 130, 288, "VSAT", size=10.5, color=SLATE); f.text(bx + 130, 302, "geostationary", size=10.5, color=SLATE)
f.text(bx + 75, 322, f"satellite is {geo/fib:.1f} times slower", size=10.5, color=RED, bold=True)
```

## 6.3 The World Wide Web

The Web is a system of linked **hypertext** documents. Its three pillars: **HTML** (structure), **HTTP** (transfer), **URL** (naming). A **web page** is one document; a **website** is a collection; a **web server** (Apache, Nginx) serves them; a **browser** (Chrome, Firefox, Edge, Safari) fetches and renders them.

A minimal HTML page:

```html
<!DOCTYPE html>
<html>
  <head><title>My first page</title></head>
  <body>
    <h1>Namaste</h1>
    <p>Read the <a href="https://www.tu.edu.np">TU site</a>.</p>
  </body>
</html>
```

- **Static** pages are the same for every visitor; **dynamic** pages are generated by server code (PHP, Node.js, Python) from a database. **CSS** styles pages; **JavaScript** adds behaviour in the browser.
- **Web 1.0** (read-only pages), **Web 2.0** (user-generated content, social media, interactive apps), **Web 3.0** (semantic web and decentralised/blockchain ideas; still emerging and debated).
- **Search engines** (Google, Bing) work in three steps: **crawl** (bots follow links), **index** (store words per page) and **rank** (order results by relevance and link authority). Good queries use quotes for exact phrases, `site:tu.edu.np` to limit a domain, and `-word` to exclude.
- **Intranet**: a private network inside an organisation using web technology; **extranet**: part of it opened to partners; the **deep web** is content not indexed (your email inbox); the **dark web** needs special software (Tor) and is a tiny part of it.

## 6.4 Internet services

| Service | Protocol | Notes |
|---|---|---|
| Email | SMTP sends, POP3 downloads, IMAP syncs | address `user@domain`; fields To, Cc, Bcc, Subject, attachments |
| File transfer | FTP / SFTP | bulk upload and download |
| Remote login | SSH (Telnet is obsolete) | control a distant computer securely |
| VoIP and video calls | SIP, WebRTC | Zoom, Meet, Messenger |
| Streaming | HTTP adaptive streaming | YouTube, Netflix |
| Messaging and social media | proprietary | WhatsApp, Viber, Facebook |
| Cloud storage and apps | HTTPS | Google Drive, OneDrive |
| Online learning (e-learning) | HTTPS | Moodle, Google Classroom |

**Email etiquette (also asked in Professional Communication):** meaningful subject line, polite greeting, short paragraphs, check attachments before sending, use Cc only for people who need to know and Bcc to protect addresses, never send passwords.

## 6.5 Security and safe use

| Threat | What it is | Defence |
|---|---|---|
| **Malware** (virus, worm, trojan, ransomware, spyware) | harmful software; ransomware encrypts files for payment | updates, antivirus, no cracked software |
| **Phishing** | fake email or site that steals passwords | check the sender and URL, never click unexpected links |
| **Spam** | unsolicited bulk email | filters |
| **Hacking / brute force** | breaking into accounts | strong unique passwords, two-factor authentication |
| **Man-in-the-middle** | eavesdropping on traffic, e.g. on open Wi-Fi | HTTPS, VPN |
| **DoS / DDoS** | flooding a service so it fails | filtering, CDNs |
| **Identity theft, cyberbullying, online fraud** | misuse of personal data | share less, report quickly |

**Good habits:** a long passphrase per account (a password manager helps), 2FA on email and banking, installing updates, backups (the **3-2-1 rule**: 3 copies, 2 media types, 1 off-site), checking the real URL before login.

**Firewall**: a filter between networks that allows or blocks traffic by rule. **Encryption**: scrambling data so only the key holder can read it. **Digital signature**: proves who sent a message and that it was not altered.

**Legal and ethical context in Nepal.** The **Electronic Transactions Act, 2063 (BS)** recognises electronic records and digital signatures and defines computer-related offences such as hacking, publishing illegal material and unauthorised access; the **Cyber Bureau** of Nepal Police investigates cybercrime. Copyright law protects software and online content. Treat these as the starting point; your *Professional Communication and Ethics* and *Cyber Security* subjects return to them.

### 6.5.1 Eight habits that stop most attacks

1. **Use a long, unique passphrase for every account.** A passphrase of four or five random words is easy to remember and very hard to guess. If one site is hacked, the same password must not unlock your email or bank. A password manager can store them safely.
2. **Switch on two-factor authentication (2FA).** After the password, the service asks for a one-time code or an app approval. Even a thief who knows your password cannot enter without your phone. Use it on email, eSewa, Khalti and mobile banking first.
3. **Install updates quickly.** Updates close security holes that attackers already know about. Many ransomware attacks succeed only on computers that missed an update for months. Turn on automatic updates for the operating system, browser and phone apps.
4. **Run antivirus and avoid cracked software.** Pirated games and "free" activators are the commonest way for trojans to enter a PC. Install programs only from the official site or app store. A good antivirus scans downloads and warns before you open a dangerous file.
5. **Check the real address before you log in.** Read the host part of the link and type the bank address yourself or use a saved bookmark. The padlock only means the connection is encrypted, not that the owner is honest. Fig 6.4 shows how a fake host is spotted.
6. **Be careful on public Wi-Fi.** Anyone on an open network may try to watch or change your traffic. Use HTTPS sites only, avoid banking on open Wi-Fi, and use a VPN when you must. Your own mobile data is safer in a cafe or bus park.
7. **Keep backups using the 3-2-1 rule.** Keep three copies of important files, on two kinds of media, with one copy off-site, such as cloud storage. Ransomware then cannot hold your project or thesis hostage. Test a restore once, because an untested backup may be useless.
8. **Think before you share, and report quickly.** Do not post citizenship numbers, OTPs or photos of cards; they help criminals. If you are cheated or harassed online, keep screenshots, change passwords and report to the Cyber Bureau of Nepal Police. Fast reporting helps to block money transfers and stop the spread.

```photogrid label="6.2" cols="2" ratio="1.5" caption="Phishing in practice. (a) A real phishing e-mail (German bank, 2005) with its warning signs numbered. (b) How one fake message turns into a stolen account. The tricks are the same in Nepali and English messages."
@ photo id="bca101/phish" cap="A genuine phishing sample, pretending to be a bank"
mark 0.27 0.76 "1"
mark 0.93 0.56 "2"
mark 0.68 0.37 "3"
mark 0.90 0.30 "4"
mark 0.52 0.205 "5"
key 1 Generic greeting: "Dear customer", not your name
key 2 Vague reason and pressure: a "new security system" needs action now
key 3 A button hides the real web address: hover to check it
key 4 False comfort: "for your protection"
key 5 Signed "Administration", with no person or phone number
@ svg cap="One fake message, five steps to a stolen account"
f = Fig(400, 300)
steps = ["Attacker sends thousands of copies", "Victim reads: urgent, official-looking", "Link opens a copy of the bank login page", "Victim types username, password, OTP", "Attacker logs in to the real account"]
cols = [ROSE, SAND, SAND, ROSE, ROSE]; sts = [RED, AMBER, AMBER, RED, RED]
for i, t in enumerate(steps):
    y = 10 + i * 56
    f.box(30, y, 340, 38, t, fill=cols[i], stroke=sts[i], size=10.5, bold=True, color=sts[i])
    if i < 4: f.arrow([(200, y + 38), (200, y + 56)], color=SLATE)
```

```svgfig label="6.4" caption="Reading a link before clicking. For each address the host is computed with the urlparse function of Python; only the host decides where the browser goes. The bank name examplebank.com is made up for this exercise."
from urllib.parse import urlparse
GENUINE = "examplebank.com"
cases = [
 "https://www.examplebank.com/login",
 "https://examplebank.com.secure-login.xyz/login",
 "https://www.examp1ebank.com/login",
 "http://www.examplebank.com/login",
 "https://examplebank.com@evil.example/login",
]
def verdict(u):
    p = urlparse(u); host = p.hostname
    ok_host = host == GENUINE or host.endswith("." + GENUINE)
    if not ok_host: return "FAKE", host
    if p.scheme != "https": return "WARN", host
    return "OK", host
res = [verdict(u) for u in cases]
print(res)
assert [r[0] for r in res] == ["OK", "FAKE", "FAKE", "WARN", "FAKE"]
assert res[1][1] == "examplebank.com.secure-login.xyz" and res[4][1] == "evil.example"
f = Fig(760, 328)
f.text(10, 18, "Which host will the browser really contact? (host computed with urlparse)", size=11.5, color=NAVY, bold=True, anchor="start")
f.text(10, 44, "URL shown in the message", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(430, 44, "Real host", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(690, 44, "Verdict", size=10.5, color=SLATE, bold=True, anchor="start")
why = ["", "looks like the bank, but the host ends in .xyz", "digit 1 instead of the letter l", "right host, but no HTTPS", "text before @ is only a login name; host is after it"]
colmap = {"OK": (MINT, TEAL), "FAKE": (ROSE, RED), "WARN": (SAND, AMBER)}
for i, (u, (v, h)) in enumerate(zip(cases, res)):
    y = 56 + i * 54
    fl, st = colmap[v]
    f.box(10, y, 410, 34, "", fill=BLUE, stroke=NAVY)
    f.text(18, y + 17, u, size=10.5, color=NAVY, anchor="start", vmid=True)
    f.text(430, y + 17, h, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.box(690, y, 62, 34, v, fill=fl, stroke=st, size=11, bold=True, color=st)
    if why[i]: f.text(18, y + 47, why[i], size=10.5, color=st, anchor="start")
```

## 6.6 Eight uses of the Internet in Nepal

```photogrid label="6.3" cols="3" ratio="0.9" caption="Internet-connected devices around you. (a) An ESP8266 Wi-Fi module on a development board, a few-dollar chip that lets a sensor report over the Internet (IoT). (b) A handheld GPS receiver (Garmin) that finds its position from satellites. (c) A card terminal showing a QR code for digital payment."
@ photo id="bca101/esp8266" cap="IoT: ESP8266 Wi-Fi board for sensors"
fit 0.9
@ photo id="bca101/garmin" cap="GIS and GPS: handheld satellite navigation"
fit 0.9
focus 0.5 0.62
@ photo id="bca101/qrpay" cap="E-payment: QR code on a card terminal"
fit 0.9
focus 0.5 0.62
```

1. **Communication.** E-mail, Viber, Messenger and video calls let people talk across the world for the price of data. Families of Nepali workers in the Gulf, Malaysia and Korea depend on them. Colleges and offices also use e-mail and group chats for notices.
2. **Education.** Students use Google Classroom, Zoom, YouTube lessons and online libraries, and campuses publish results and notices on websites. During the COVID-19 lockdown, schools and Tribhuvan University campuses moved many classes online. The Internet also gives rural students access to books that their library does not hold.
3. **Digital payments and banking.** ConnectIPS, Fonepay QR, eSewa, Khalti and mobile banking allow bill payment, transfers and shopping without cash. A shopkeeper in a small town can accept a QR payment with just a phone. Every transaction travels over HTTPS and needs a PIN or OTP.
4. **E-governance.** Citizens use the Nagarik App, online tax filing with the Inland Revenue Department, and online forms for passport and driving-licence services. This saves travel and reduces queues and middlemen. Government sites also publish budgets, notices and tender information.
5. **E-commerce and online services.** Daraz, Foodmandu, Pathao and many Facebook shops sell goods and services online. Buyers compare prices and read reviews before paying, and sellers reach customers beyond their own city. Cash on delivery and QR payment both help trust.
6. **Health.** Hospitals post timetables, book appointments and deliver reports online, and telemedicine links a village health post with a specialist in the city. Patients read reliable advice from the Ministry of Health and WHO sites. Wrong medical advice online is also a risk, so sources must be checked.
7. **Maps, GIS and navigation.** Google Maps and OpenStreetMap guide drivers and delivery riders, and volunteers mapped damaged areas of Kathmandu Valley after the 2015 earthquake. GIS layers of rivers, roads and land use help planners. A GPS receiver such as Fig 6.3(b) needs the Internet only for map data, not for the satellite signal.
8. **Internet of Things and monitoring.** Small Wi-Fi or mobile boards, like the one in Fig 6.3(a), read sensors and send the data to a server. Examples include rainfall and river-level gauges, smart meters, cold-storage temperature and school attendance. The Department of Hydrology and Meteorology publishes weather and flood information online for the public.

## Formula and fact sheet

- Internet = network of networks; Web = a service (HTML + HTTP + URL).
- DNS: root → TLD → authoritative; cached by TTL.
- URL = scheme://host:port/path?query#fragment.
- HTTP 200 OK, 301 moved, 403 forbidden, 404 not found, 500 server error. HTTP is stateless; cookies add state.
- HTTPS = HTTP + TLS (encryption + identity).
- Email: SMTP out, POP3/IMAP in. Search engine: crawl → index → rank.
- 3-2-1 backup; two-factor authentication.

## Chapter summary

- The Internet grew from ARPANET; the Web was added by Tim Berners-Lee around 1990.
- DNS turns names into IP addresses; HTTP/HTTPS carries requests and responses over TCP.
- Browsers render HTML, CSS and JavaScript; search engines crawl, index and rank.
- Email, VoIP, streaming and cloud services all ride on the Internet.
- Malware, phishing and weak passwords are the commonest threats; encryption, updates, 2FA and caution are the commonest defences.
- Bandwidth sets how fast bulk data moves; distance sets the delay (a geostationary satellite adds about 0.48 s of round trip).
- Nepal's main Internet uses: communication, education, payments, e-governance, e-commerce, health, maps and IoT.

## Practice

**A. Short questions**

1. Differentiate the Internet and the World Wide Web.
2. What is an ISP? Name four access technologies.
3. What does DNS do? Name the parts of the URL `https://www.tu.edu.np/exam?year=2082`.
4. What is the difference between HTTP and HTTPS?
5. What is a cookie? Why does HTTP need cookies?
6. Differentiate POP3 and IMAP.
7. What is phishing? How can it be recognised?
8. Differentiate intranet and extranet.

**B. Problems**

9. List the steps from typing `www.example.com` to the page appearing.
10. A page makes 1 HTML request and 20 resource requests; each needs 80 ms of latency and 6 requests run in parallel at a time. Estimate the minimum load time of the resource phase.
11. Write the HTML for a page with a heading, a paragraph and a link.

**C. Long questions**

12. Explain how a search engine works.
13. Discuss the common internet security threats and the measures against them.
14. Compare Web 1.0, 2.0 and 3.0.
15. Discuss the applications of the Internet with examples from Nepal.

::: note Answers and worked solutions
**1.** The Internet is the physical and logical network of networks; the Web is a service on it that serves linked hypertext pages. Email and VoIP use the Internet but not the Web.
**2.** An ISP provides Internet access. ADSL, FTTH, 4G/5G, VSAT (also cable, wireless).
**3.** DNS translates names to IP addresses. Scheme `https`, host `www.tu.edu.np` (TLD `.np`), path `/exam`, query `year=2082`.
**4.** HTTPS encrypts HTTP using TLS and authenticates the server with a certificate.
**5.** A small data item stored by the browser and sent with later requests; HTTP is stateless, so cookies keep login sessions and preferences.
**6.** POP3 downloads mail to one device (usually deleting it from the server); IMAP keeps mail on the server and syncs all devices.
**7.** Phishing is a fake message or site that tricks you into giving credentials. Check the sender address, mismatched or misspelt URLs, urgency, and unexpected attachments or login requests.
**8.** An intranet is private to one organisation; an extranet gives selected outsiders (partners, suppliers) access to part of it.
**9.** The six steps of §6.2.
**10.** 20 requests in groups of 6 give ⌈20 / 6⌉ = 4 rounds; 4 × 80 = **320 ms** (ideal).
**11.** See the HTML example of §6.3.
**12.** Crawl → index → rank; mention bots, inverted index, relevance and link analysis.
**13.** Table of §6.5.
**14.** Web 1.0 read-only static pages; Web 2.0 interactive, user-generated, social; Web 3.0 semantic/decentralised, with data meaning understood by machines.
**15.** The eight uses of §6.6: communication, education, payments, e-governance, e-commerce, health, GIS and IoT, each with a Nepali example.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

### Medium question (5 marks)

**Q9. List and explain the steps from typing www.example.com to the page appearing. (5 marks)**

1. **Cache check:** the browser and operating system look for a saved IP address of the name. If none is found, a request goes to the **DNS resolver** of the ISP (Figure 6.1).
2. **DNS lookup:** the resolver asks a root server, then the TLD server (`.com`), then the authoritative server, which returns the IP address. The answer is cached for its time-to-live.
3. **TCP connection:** the browser opens a connection to port 443 using a three-way handshake (SYN, SYN-ACK, ACK) (Figure 6.2).
4. **TLS handshake:** the server sends its certificate; the browser checks it and both sides agree on a session key, so everything after is encrypted (HTTPS).
5. **HTTP request:** the browser sends `GET /` and the server replies with `200 OK` and the HTML.
6. **Rendering:** the browser reads the HTML, requests the CSS, images and scripts, and draws the page.

| Step | Protocol | Result |
|---|---|---|
| Name to address | DNS (UDP 53) | IP address |
| Connect | TCP | reliable channel |
| Secure | TLS | encrypted session |
| Fetch | HTTP | HTML page |

**Example.** Opening a bank's internet-banking page in Kathmandu follows exactly these steps; the padlock in the address bar shows that the TLS step succeeded.

### Long questions (10 marks)

**Q12. Explain how a search engine works. (10 marks)**

**Introduction.** A **search engine** (Google, Bing) is a web application that finds pages related to a user's words from billions of pages in a fraction of a second. It does this by preparing the answers in advance, in three main stages.

1. **Crawling:** programs called **crawlers (spiders, bots)** start from known URLs, download each page and follow its links to discover new pages. A `robots.txt` file tells them which parts to skip.
2. **Indexing:** the engine analyses each page (words, title, headings, links, language, images) and stores it in an **inverted index**: for every word, a list of the pages containing it. Looking up a word becomes as fast as looking up a book's index.
3. **Query processing:** the query is cleaned (lower case, spelling correction, stop words removed) and matched with the index to find candidate pages.
4. **Ranking:** the candidates are scored by relevance (words in the title and body), authority (the PageRank idea that links from good pages count more), freshness, speed, mobile friendliness and user location.
5. **Results page:** the top results are shown with title, URL and a snippet, plus ads, maps and images.
6. **Feedback:** clicks and time spent improve later ranking.
7. **SEO:** website owners improve titles, content and speed to rank higher; dishonest tricks are penalised.

| Stage | Input | Output |
|---|---|---|
| Crawl | URL list | raw pages |
| Index | raw pages | inverted index |
| Rank | query + index | ordered list |

**Example.** Searching "BCA entrance model question" returns Nepali college and notes sites because their pages contain those words and are linked from other sites.

**Conclusion.** A search engine is fast because crawling and indexing are done before the user searches; only matching and ranking happen at query time.

**Q13. Discuss the common internet security threats and the measures against them. (10 marks)**

**Introduction.** The Internet connects strangers, so data, money and identity are targets. Threats are matched by technical and human safeguards.

1. **Malware:** viruses, worms, trojans, ransomware and spyware. *Measure:* antivirus, updates, no cracked software.
2. **Phishing:** fake emails, SMS or sites that steal passwords. *Measure:* check the URL, never share OTPs, use two-factor authentication.
3. **Identity theft and social engineering:** attackers trick people into revealing data. *Measure:* privacy settings, verify callers.
4. **Denial of service (DoS/DDoS):** a flood of requests makes a site unavailable. *Measure:* filtering, rate limits, CDN.
5. **Man-in-the-middle and eavesdropping:** data read on open Wi-Fi. *Measure:* HTTPS, VPN, WPA2/WPA3.
6. **Hacking and SQL injection:** unauthorised access through weak passwords or bugs. *Measure:* strong passwords, patches, input checks, firewalls.
7. **Cyber bullying and harmful content:** abuse on social media. *Measure:* report, block, awareness.
8. **Data breach and loss:** stolen or lost data. *Measure:* encryption, backups, access control.

| Threat | Main safeguard |
|---|---|
| Malware | antivirus and updates |
| Phishing | two-factor authentication, alertness |
| DDoS | traffic filtering |
| Eavesdropping | HTTPS and VPN |

**Legal note.** Nepal's **Electronic Transactions Act 2063** punishes hacking, data theft and online fraud; victims can report to the Cyber Bureau of Nepal Police.

**Conclusion.** No single tool is enough; safe internet use combines software protection, strong authentication, encryption and informed users.

**Q14. Compare Web 1.0, 2.0 and 3.0. (10 marks)**

**Introduction.** The Web has changed from read-only pages to social and then to intelligent, decentralised services.

| Basis | Web 1.0 (1990s) | Web 2.0 (2000s) | Web 3.0 (emerging) |
|---|---|---|---|
| Nature | read-only | read-write, social | read-write-own, semantic |
| Content by | site owners | users | users and machines |
| Technology | static HTML | AJAX, CSS, JS, mobile apps | AI, blockchain, semantic web |
| Control | website owner | large platforms | users and communities |
| Example | early static sites | Facebook, YouTube, Wikipedia | smart contracts, AI assistants |
| Data | hosted by owner | held by platforms | user-owned, decentralised |

1. **Web 1.0:** pages were static, like an online brochure, and users only read.
2. **Web 2.0:** blogs, wikis and social media let users create and share content, and sites became interactive.
3. **Web 3.0:** data gets meaning, so software understands context; blockchain gives users ownership of data and assets.
4. **Impact in Nepal:** online newspapers (Web 1.0), Facebook and YouTube creators (Web 2.0), digital wallets and AI chat tools (towards Web 3.0).

**Conclusion.** Each version adds interaction and intelligence; the trend is from owner-controlled to user-centred services.

**Q13. Discuss the common Internet security threats and the measures against them. (10 marks)**

**Introduction.** Internet security is the protection of users, devices and data from theft, damage and misuse while they are connected. As banking, study and government services move online in Nepal (ConnectIPS, Fonepay, Nagarik App), a single successful attack can cost money, privacy or reputation. Threats are of two kinds: technical attacks on machines and social attacks on people.

1. **Malware:** harmful software such as viruses, worms, trojans, spyware and ransomware. A virus attaches itself to files, a worm spreads alone through networks, a trojan pretends to be useful, and ransomware encrypts files and demands payment. Defence: updates, antivirus, and no cracked software.
2. **Phishing:** a fake e-mail, SMS or site that steals passwords and OTPs, as in the sample in Figure 6.4 and Plate 6.2. Warning signs are a generic greeting, urgency and a link whose host is not the real domain. Defence: read the host, type the address yourself, never share an OTP.
3. **Spam and scams:** unwanted bulk messages, lottery and job frauds, and fake online shops. Defence: mail filters, checking seller reviews and paying by cash on delivery when unsure.
4. **Password attacks:** guessing, brute force and reuse of leaked passwords. Defence: long unique passphrases and two-factor authentication.
5. **Man-in-the-middle:** an attacker on open Wi-Fi watches or changes traffic. Defence: HTTPS (TLS), a VPN, and no banking on public networks.
6. **Denial of service (DoS/DDoS):** a flood of requests from many infected machines makes a site unavailable. Defence: traffic filtering, content delivery networks and extra capacity.
7. **Identity theft, cyberbullying and online fraud:** misuse of personal data, photos and accounts. Defence: share less, set privacy options, keep evidence and report to the Cyber Bureau of Nepal Police.
8. **Data loss:** disks fail, devices are lost or ransomware locks files. Defence: the 3-2-1 backup rule.

| Threat | Target | Main defence |
|---|---|---|
| Malware | files, devices | updates, antivirus |
| Phishing | people | check host, 2FA |
| Man-in-the-middle | traffic | HTTPS, VPN |
| DDoS | servers | filtering, CDN |
| Ransomware | data | backups |

**Legal protection.** The Electronic Transactions Act, 2063 (BS) recognises electronic records and digital signatures and punishes hacking and unauthorised access; the Cyber Bureau investigates complaints. A **firewall** filters traffic by rule, **encryption** hides content from outsiders, and a **digital signature** proves the sender and that the message was not changed.

**Conclusion.** No single tool is enough; security needs layers: technology (firewall, encryption, updates), good habits (passphrases, 2FA, backups) and law. Most successful attacks use human error, so awareness is the cheapest and strongest defence.

**Q14. Compare Web 1.0, Web 2.0 and Web 3.0. (10 marks)**

**Introduction.** The World Wide Web was proposed by Tim Berners-Lee at CERN around 1989-91. Its growth is described in three generations: the read-only web, the social and interactive web, and the emerging semantic and decentralised web. The generations overlap, and the names describe a change in how people use the Web, not a version number of software.

1. **Web 1.0 (about 1991-2004), the read-only web.** Pages were static HTML written by a few webmasters, and visitors could only read them. Examples are early university pages, online brochures and directories. Connections were slow dial-up, so pages were small and mostly text.
2. **Web 2.0 (about 2004 to today), the read-write web.** Users create content: blogs, wikis, social networks, video sharing and online reviews. Pages are dynamic, generated by server code from databases, and JavaScript makes them interactive. Smartphones and cheap broadband made it mass-market; Facebook, YouTube, Wikipedia and Daraz are examples.
3. **Web 3.0 (emerging), the semantic and decentralised web.** Two ideas are used under this name. The **semantic web** adds machine-readable meaning to data (structured data, ontologies, knowledge graphs) so that software can understand it. The **decentralised web** uses blockchains and peer-to-peer systems so that users, not one company, own their data and identity. Artificial intelligence assistants and cryptocurrencies are linked to this idea, but the term is still debated.
4. **Role of the user.** In Web 1.0 the user is a consumer, in Web 2.0 a producer and consumer, in Web 3.0 an owner and participant.
5. **Technology.** Web 1.0 used HTML and basic HTTP; Web 2.0 added CSS, JavaScript, AJAX, databases and APIs; Web 3.0 adds metadata standards, AI and distributed ledgers.
6. **Risks.** Web 2.0 brought privacy loss, fake news and phishing at scale; Web 3.0 brings scams, energy use and legal uncertainty.

| Point | Web 1.0 | Web 2.0 | Web 3.0 |
|---|---|---|---|
| Content | static pages | user-generated | machine-understood data |
| User role | reader | creator and sharer | owner and participant |
| Control | webmasters | large platforms | users and networks |
| Technology | HTML, HTTP | JavaScript, databases, APIs | semantic data, AI, blockchain |
| Examples | early campus sites | Facebook, YouTube, Daraz | smart assistants, crypto wallets |

**Conclusion.** Each generation keeps the earlier ones: today's browser still shows static pages, runs social apps and is beginning to use semantic data. For Nepal the Web 2.0 stage is dominant, with growing e-governance and payments.

**Q15. Discuss the applications of the Internet with examples from Nepal. (10 marks)**

**Introduction.** The Internet is the global network of networks that lets computers exchange data using TCP/IP. Its cheap, fast and worldwide nature has made it a basic utility, like electricity, for study, business and government. Plate 6.3 shows devices through which it reaches daily life, from a QR payment terminal to a sensor board.

1. **Communication:** e-mail, Viber, Messenger and video calls connect families of migrant workers with Nepal at the cost of data. Offices and campuses use e-mail and groups for notices.
2. **Education:** Google Classroom, Zoom, YouTube and online libraries support learning; campuses publish results online. During the COVID-19 lockdown, many Tribhuvan University campuses taught online.
3. **Digital payments and banking:** ConnectIPS, Fonepay QR, eSewa, Khalti and mobile banking allow transfers and bill payment without cash, protected by HTTPS, PINs and OTPs.
4. **E-governance:** the Nagarik App, online tax filing with the Inland Revenue Department and online forms for passports and licences save travel and reduce corruption by cutting middlemen.
5. **E-commerce:** Daraz, Foodmandu and Pathao sell goods and services; small sellers on social media reach customers beyond their town.
6. **Health:** online appointments, reports and telemedicine link rural health posts with city specialists.
7. **Maps and GIS:** Google Maps and OpenStreetMap guide travel; volunteers mapped Kathmandu Valley after the 2015 earthquake; planners use GIS layers for roads, rivers and land use.
8. **Internet of Things:** Wi-Fi boards such as the ESP8266 send sensor readings (rainfall, river level, temperature) to servers; the Department of Hydrology and Meteorology publishes weather and flood information online.

| Area | Nepali example | Benefit |
|---|---|---|
| Communication | Viber, e-mail | low-cost contact |
| Education | Google Classroom | learning anywhere |
| Payments | ConnectIPS, Fonepay | cash-free transfer |
| Governance | Nagarik App | fewer queues |
| Commerce | Daraz | wider market |
| Health | telemedicine | specialist access |
| GIS | OpenStreetMap | planning and navigation |
| IoT | river-level sensors | early warning |

**Limitations.** The same openness brings risks: phishing, fraud, misinformation and addiction, and the digital divide leaves remote villages with poor access and low skills.

**Conclusion.** The Internet has become a platform for almost every public and private service in Nepal. Its benefits grow with wider access, digital skills and safe habits, which is why Internet literacy is part of the BCA course.
