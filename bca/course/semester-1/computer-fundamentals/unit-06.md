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
