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
