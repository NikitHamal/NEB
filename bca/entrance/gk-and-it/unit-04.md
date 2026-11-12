---
subject: General Knowledge and IT
grade: BCA
unit: 4
title: Internet, E-mail, HTML, Programming and Full Forms
hours: 2
area: General IT
---

The second IT chapter covers the Internet, e-mail, HTML tags, programming terms and the abbreviations that examiners love. Two questions of the ten come from here, and the published syllabus names HTML, hardware and software, full forms, internet and email, inventions and programming. Everything below is stable knowledge.

::: key What the paper asks from this chapter
- **Internet**: WWW (Tim Berners-Lee), protocols, IP addresses, DNS, URLs, domains (.np).
- **E-mail**: SMTP sends, POP3/IMAP receive; To, Cc, Bcc.
- **HTML**: full form, common tags, HTML is *not* a programming language.
- **Programming**: language creators, translators, algorithm, flowchart.
- **Full forms**: the standard list.
:::

## 4.1 Internet, WWW, e-mail and common protocols

- The **Internet** began as ARPANET (1969). The **World Wide Web** was invented by **Tim Berners-Lee** at CERN (1989). The Web is a service on the Internet.
- **Protocols**: HTTP/HTTPS (web; the S is *secure*), FTP (files), SMTP (sending mail), POP3/IMAP (receiving mail), TCP/IP (the basic suite), DNS (domain name → IP address).
- **IPv4** is 32 bits (e.g. 192.168.1.1); **IPv6** is 128 bits. **URL** = Uniform Resource Locator. Nepal's country domain is **.np**; others: .com, .org, .edu, .gov.
- **E-mail**: To (main recipient), **Cc** (carbon copy), **Bcc** (blind carbon copy: hidden recipients). Format `name@domain`. Browsers (Chrome, Firefox, Edge, Safari) are not search engines (Google, Bing).
- Networks: LAN (building), MAN (city), WAN (wide area; the Internet).

```photogrid label="4.1" cols="4" ratio="1.1" caption="From ARPANET to the Web: (a) an ARPANET interface message processor (IMP), 1969; (b) Vint Cerf, co-designer of TCP/IP; (c) Tim Berners-Lee, who invented the World Wide Web at CERN; (d) the NeXT computer that ran the first web server at CERN, 1990."
@ photo id="bca301/bbnimp" cap="ARPANET IMP (1969)"
@ photo id="bca301/cerf" cap="Vint Cerf: TCP/IP"
@ photo id="bca301/berners" cap="Tim Berners-Lee: WWW"
@ photo id="bcagk/nextcube" cap="First web server, CERN"
```

```svgfig label="4.1" caption="Internet milestones to scale (tick = 5 years). The Web arrived in 1989, exactly 20 years after ARPANET (1969): the Internet existed long before the Web, which is why the two words are not interchangeable."
ev = [(1969, "ARPANET\nfirst link", "up", 1), (1971, "First e-mail\n(Tomlinson)", "dn", 1), (1983, "TCP/IP adopted\n(1 January)", "up", 2), (1989, "WWW proposed\n(Berners-Lee)", "dn", 2), (1991, "Web opens to\nthe public", "up", 1), (2026, "Today: billions\nof users", "dn", 1)]
assert 1989 - 1969 == 20 and [e[0] for e in ev] == sorted(e[0] for e in ev)
f = Fig(780, 260); X0, X1, A0, A1 = 50, 730, 1965, 2030; ax = lambda y: X0 + (y - A0) * (X1 - X0) / (A1 - A0); Y = 130
f.line(X0, Y, X1, Y, color=NAVY, sw=3)
for y in range(1965, 2031, 5):
    f.line(ax(y), Y - 4, ax(y), Y + 4, color=SLATE)
    if y % 10 == 0: f.text(ax(y), Y + 22, str(y), size=10, color=SLATE)
for yr, lab, d, lv in ev:
    x = ax(yr); s = -1 if d == "up" else 1; yy = Y + s * (16 + lv * 26)
    f.line(x, Y, x, yy, color=TEAL, sw=1.1); f.circle(x, Y, 4.5, fill=TEAL, stroke=TEAL)
    t = f"{yr}\n{lab}"; nl = t.count("\n") + 1
    an = "end" if x > 690 else ("start" if x < 90 else "middle")
    f.text(x, yy + (-(nl * 6 + 4) if d == "up" else (nl * 6 + 8)), t, size=10, color=NAVY, bold=True, anchor=an)
f.arrow([(ax(1969), 240), (ax(1989), 240)], color=AMBER, both=True, label="20 years", lpos=(ax(1979), 232))
```

```svgfig label="4.2" caption="Internet and Web are not the same thing. The Internet is the global network of networks running TCP/IP; the World Wide Web (HTTP and HTML pages), e-mail (SMTP, POP3, IMAP), file transfer (FTP) and the DNS are services that run on top of it. A browser is the client of the Web, a search engine is a website."
f = Fig(780, 270)
f.box(10, 10, 760, 250, "", fill="#eff6ff", stroke=NAVY, r=12, sw=2)
f.text(390, 32, "THE INTERNET: network of networks, TCP/IP, IPv4 / IPv6 addresses", size=12, color=NAVY, bold=True)
sv = [("World Wide Web", "HTTP / HTTPS\nHTML pages", "#bbf7d0", TEAL), ("E-mail", "send: SMTP\nreceive: POP3, IMAP", "#fed7aa", AMBER), ("File transfer", "FTP", "#e9d5ff", NAVY), ("Name service", "DNS: name -> IP", "#fef9c3", AMBER)]
for i, (n, p, col, ec) in enumerate(sv):
    x = 30 + i * 185
    f.box(x, 56, 170, 56, n, fill=col, stroke=ec, size=12, bold=True); f.text(x + 85, 132, p, size=10.5, color=SLATE, bold=True)
f.box(30, 175, 170, 38, "Browser: Chrome, Edge,\nFirefox, Safari", fill="#ffffff", stroke=TEAL, size=9.5, bold=True)
f.box(215, 175, 170, 38, "Search engine: Google,\nBing (a website)", fill="#ffffff", stroke=TEAL, size=9.5, bold=True)
f.box(400, 175, 170, 38, "Mail apps: Gmail,\nOutlook", fill="#ffffff", stroke=AMBER, size=9.5, bold=True)
f.box(585, 175, 170, 38, "ISP: gives you the\nconnection", fill="#ffffff", stroke=NAVY, size=9.5, bold=True)
f.text(390, 238, "Clients and companies on the right and bottom are not the Internet itself", size=10, color=SLATE, italic=True)
```

```svgfig label="4.3" caption="Anatomy of a URL, split by a program: https://www.tu.edu.np/bca/results.html. The scheme is the protocol, the host is www.tu.edu.np, .np is Nepal's country-code top-level domain, .edu marks education, and the path names the page. Reading right to left through the host goes from the most general part to the most specific."
import urllib.parse as up
u = up.urlparse("https://www.tu.edu.np/bca/results.html")
assert (u.scheme, u.netloc, u.path) == ("https", "www.tu.edu.np", "/bca/results.html")
lab = u.netloc.split("."); assert lab == ["www", "tu", "edu", "np"]
f = Fig(780, 220)
parts = [("https", "scheme\n(protocol)", "#fed7aa", AMBER), ("://", "", "#ffffff", SLATE), ("www", "subdomain\n(host name)", "#bbf7d0", TEAL), (".tu", "organisation\n(Tribhuvan Univ.)", "#bfdbfe", NAVY),
         (".edu", "category\n(education)", "#e9d5ff", NAVY), (".np", "country code\n(Nepal)", "#fecaca", RED), ("/bca/results.html", "path to the page", "#fef9c3", AMBER)]
wd = [90, 50, 80, 80, 90, 80, 230]; x = 20
for (t, d, col, ec), w in zip(parts, wd):
    f.box(x, 50, w, 44, t, fill=col, stroke=ec, size=13, bold=True, r=4)
    if d: f.text(x + w / 2, 124, d, size=10, color=ec, bold=True)
    x += w
f.line(20 + 90 + 50, 100, 20 + 90 + 50 + 330, 100, color=SLATE, sw=1.6); f.text(20 + 90 + 50 + 165, 160, "host name: www.tu.edu.np (read right to left: np > edu > tu > www)", size=10.5, color=NAVY, bold=True)
f.text(390, 195, "DNS turns the host name into an IP address; the path is then asked from that computer", size=10, color=SLATE, italic=True)
```

```svgfig label="4.4" caption="IPv4 versus IPv6. An IPv4 address such as 192.168.1.1 has four octets of 8 bits (0 to 255 each), 32 bits in all, so there are 2^32 = 4,294,967,296 addresses; IPv6 uses 128 bits, 2^128 = 340,282,366,920,938,463,463,374,607,431,768,211,456 addresses. 192.168.x.x is a private range used on home and college LANs."
ip = "192.168.1.1"; oc = [int(x) for x in ip.split(".")]; bits = [format(o, "08b") for o in oc]
assert bits == ["11000000", "10101000", "00000001", "00000001"] and 2 ** 32 == 4294967296 and 2 ** 128 == 340282366920938463463374607431768211456
f = Fig(780, 270)
f.text(390, 18, "IPv4 address 192.168.1.1 = 4 octets x 8 bits = 32 bits", size=11.5, color=NAVY, bold=True)
for i, (o, b) in enumerate(zip(oc, bits)):
    x = 40 + i * 180
    f.box(x, 34, 160, 34, str(o), fill="#fed7aa", stroke=AMBER, size=16, bold=True)
    for k, ch in enumerate(b):
        f.box(x + k * 20, 82, 19, 26, ch, fill=("#bbf7d0" if ch == "1" else "#ffffff"), stroke=SLATE, size=10, bold=True, r=2)
    f.text(x + 80, 126, f"octet {i + 1}: 0-255", size=9.5, color=SLATE)
f.box(40, 150, 340, 50, "IPv4: 32 bits\n2^32 = 4,294,967,296 addresses", fill="#dbeafe", stroke=NAVY, size=11, bold=True)
f.box(400, 150, 340, 50, "IPv6: 128 bits, written in hex, e.g. 2001:db8::1\n2^128 = about 3.4 x 10^38 addresses", fill="#e9d5ff", stroke=NAVY, size=10.5, bold=True)
f.text(390, 225, "Invalid IPv4: any octet above 255, e.g. 192.168.1.256", size=10.5, color=RED, bold=True)
f.text(390, 247, "Special: 127.0.0.1 = localhost;  192.168.x.x, 10.x.x.x = private", size=10, color=SLATE, bold=True)
```

```photogrid label="4.2" cols="3" ratio="1.25" caption="Pieces of the Web: (a) a screenshot of the first web page, the World Wide Web project page; (b) an analogue dial-up modem of the 1990s, which let a phone line carry data; (c) a K-root DNS server rack, one of the root name servers that start every domain lookup."
@ photo id="bcagk/wwwbrowser" cap="First web page (WWW project)"
focus 0.5 0.4
@ photo id="bcagk/modem" cap="56k dial-up modem"
focus 0.5 0.5
@ photo id="bca301/rootk" cap="K-root DNS server rack"
```

```svgfig label="4.5" caption="What happens when you type tu.edu.np: the browser asks DNS to turn the name into an IP address, then sends an HTTPS request to that address and receives the page. The address 203.0.113.10 is from the documentation range reserved for examples."
f = Fig(780, 270)
steps = [("1  Browser", "you type\ntu.edu.np", "#bbf7d0", TEAL, 20), ("2  DNS resolver\n(your ISP)", "who is\ntu.edu.np?", "#fef9c3", AMBER, 215), ("3  Root -> .np ->\nedu.np servers", "asks down the\nname tree", "#e9d5ff", NAVY, 410), ("4  Web server", "IP 203.0.113.10\nsends the page", "#bfdbfe", NAVY, 600)]
for t, d, col, ec, x in steps:
    f.box(x, 40, 160, 56, t, fill=col, stroke=ec, size=10.5, bold=True); f.text(x + 80, 116, d, size=10, color=ec, bold=True)
f.arrow([(180, 60), (215, 60)], color=SLATE); f.arrow([(375, 60), (410, 60)], color=SLATE); f.arrow([(570, 60), (600, 60)], color=SLATE)
f.arrow([(80, 160), (680, 160)], color=TEAL, sw=2, label="5  HTTPS request to 203.0.113.10 (port 443)", lpos=(380, 150))
f.arrow([(680, 190), (80, 190)], color=NAVY, sw=2, label="6  HTML page comes back; browser draws it", lpos=(380, 207))
f.text(390, 245, "DNS: name -> IP (like a phone book); HTTP/HTTPS: fetch the page", size=10.5, color=SLATE, bold=True)
```

```photogrid label="4.3" cols="2" ratio="1.4" caption="E-mail and its traffic: (a) the sign marking the place where Ray Tomlinson sent the first network e-mail in 1971 and chose the @ symbol; (b) a packet capture (Wireshark) of the name lookups that happen before mail or a page is fetched."
@ photo id="bca301/tomlinson" cap="Ray Tomlinson's e-mail sign: user@host"
@ photo id="bca301/wireshark" cap="Packet capture of DNS traffic"
```

```svgfig label="4.6" caption="How an e-mail travels. The sender's mail client hands the message to its mail server by SMTP, SMTP carries it to the recipient's server, and the recipient reads it with POP3 or IMAP. SMTP sends, POP3 and IMAP receive. Cc recipients are visible to all; Bcc recipients are hidden from everyone else."
f = Fig(780, 300)
nodes = [("Sender\n(mail client)", 20, "#bbf7d0", TEAL), ("Sender's\nmail server", 215, "#fef9c3", AMBER), ("Recipient's\nmail server", 410, "#fef9c3", AMBER), ("Recipient\n(mail client)", 600, "#bbf7d0", TEAL)]
for t, x, col, ec in nodes: f.box(x, 40, 150, 56, t, fill=col, stroke=ec, size=11, bold=True)
f.arrow([(170, 68), (215, 68)], color=AMBER, label="SMTP", lpos=(192, 58)); f.arrow([(365, 68), (410, 68)], color=AMBER, label="SMTP", lpos=(388, 58)); f.arrow([(560, 68), (600, 68)], color=NAVY, label="POP3/IMAP", lpos=(580, 58))
f.text(390, 130, "Address format: name@domain, e.g. ram@example.com.np", size=10.5, color=NAVY, bold=True)
f.box(40, 160, 700, 125, "", fill="#f8fafc", stroke=SLATE, r=8)
f.text(390, 180, "Example: Ram writes To: Sita, Cc: Hari, Bcc: Gita", size=11, color=NAVY, bold=True)
rows = [("Sita (To)", "sees: Sita, Hari; not Gita", "#bbf7d0"), ("Hari (Cc)", "sees: Sita, Hari; not Gita", "#fef9c3"), ("Gita (Bcc)", "sees: Sita, Hari and her own copy", "#fecaca")]
for i, (a, b, col) in enumerate(rows):
    f.box(70, 192 + i * 30, 130, 24, a, fill=col, stroke=SLATE, size=10.5, bold=True, r=3); f.text(215, 204 + i * 30, b, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
```

## 4.2 HTML basics

**HTML** = HyperText Markup Language: a markup language, **not** a programming language. Tags come in pairs `<tag>…</tag>`.

| Tag | Use |
|---|---|
| `<html>`, `<head>`, `<title>`, `<body>` | page structure |
| `<h1>` … `<h6>` | headings (h1 largest) |
| `<p>` | paragraph |
| `<br>` | line break |
| `<a href="…">` | hyperlink |
| `<img src="…" alt="…">` | image |
| `<ul>`, `<ol>`, `<li>` | unordered list, ordered list, item |
| `<table>`, `<tr>`, `<td>` | table, row, cell |

CSS styles pages; JavaScript makes them interactive.

```svgfig label="4.7" caption="HTML structure: a page is a tree of paired tags. <html> holds <head> (with <title>) and <body>; the body holds headings (h1 largest to h6 smallest), paragraphs, links (a href), images (img src alt), lists (ul, ol, li) and tables. <br> and <img> have no closing tag. HTML is a markup language, not a programming language."
f = Fig(780, 330)
def nd(x, y, t, col="#dbeafe", ec=NAVY, w=100): f.box(x, y, w, 28, t, fill=col, stroke=ec, size=11, bold=True, r=4)
nd(330, 10, "<html>", "#e9d5ff"); nd(160, 70, "<head>", "#fef9c3", AMBER); nd(500, 70, "<body>", "#bbf7d0", TEAL); nd(160, 130, "<title>", "#fef9c3", AMBER)
f.arrow([(380, 38), (210, 70)], color=SLATE); f.arrow([(380, 38), (550, 70)], color=SLATE); f.arrow([(210, 98), (210, 130)], color=SLATE)
kids = ["<h1> heading", "<p> paragraph", "<a href> link", "<img src alt>", "<ul><li> list", "<table><tr><td>"]
for i, k in enumerate(kids):
    x = 250 + (i % 3) * 170; y = 140 + (i // 3) * 40
    f.box(x, y, 160, 28, k, fill="#ecfdf5", stroke=TEAL, size=10, bold=True, r=4)
    f.arrow([(550, 98), (x + 80, y)], color=SLATE, sw=1)
f.box(20, 230, 740, 90, "", fill="#f8fafc", stroke=SLATE, r=8)
f.text(390, 250, "Rules to remember", size=11, color=NAVY, bold=True)
f.text(40, 272, "Tags come in pairs <tag> ... </tag>; <br> and <img> are single.", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(40, 292, "<h1> is the largest heading, <h6> the smallest.   <a href=...> is a link; <img src=... alt=...> is a picture.", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(40, 312, "CSS styles pages; JavaScript makes them interactive; HTML only gives them structure.", size=10.5, color=SLATE, bold=True, anchor="start")
```

## 4.3 Programming languages and concepts

| Language | Creator |
|---|---|
| C (1972, Bell Labs) | Dennis Ritchie |
| C++ | Bjarne Stroustrup |
| Java | James Gosling |
| Python | Guido van Rossum |
| FORTRAN (1957) | the first widely used high-level language |

- **Algorithm**: a step-by-step procedure to solve a problem; **flowchart**: its diagram (oval start/end, rectangle process, parallelogram input/output, diamond decision).
- **Compiler** translates the whole program; **interpreter** line by line; **assembler** assembly → machine code.
- **Syntax error**: breaks the language's rules. **Logic error**: runs but gives wrong results. SQL is the language of databases.

```photogrid label="4.4" cols="4" ratio="1.0" caption="Creators of languages named in the exam: (a) Dennis Ritchie, C (1972); (b) Bjarne Stroustrup, C++; (c) James Gosling, Java; (d) Guido van Rossum, Python."
@ photo id="bca102/ritchie" cap="Dennis Ritchie: C"
focus 0.5 0.4
@ photo id="bcagk/stroustrup" cap="Bjarne Stroustrup: C++"
focus 0.5 0.4
@ photo id="bca303/gosling" cap="James Gosling: Java"
focus 0.5 0.4
@ photo id="bcagk/guido" cap="Guido van Rossum: Python"
focus 0.5 0.35
```

```photogrid label="4.5" cols="4" ratio="1.0" caption="Where programming started and how it looks: (a) an IBM 704 installation, the machine FORTRAN (1957) was first written for; (b) punched cards that carried programs; (c) the cover of The C Programming Language (Kernighan and Ritchie); (d) a UNIX V5 terminal screen."
@ photo id="bcagk/ibm704" cap="IBM 704 'data processing machine'"
focus 0.4 0.5
@ photo id="bca101/punchcard" cap="Punched card: program storage"
@ photo id="bca102/kr-cover" cap="K&R: the C book"
@ photo id="bca102/unix-v5" cap="UNIX V5 terminal"
```

```svgfig label="4.8" caption="Language birth years to scale: FORTRAN 1957, C 1972, C++ 1985, Python 1991, Java 1995 (tick = 5 years). C came 15 years after FORTRAN and Java is 38 years younger than FORTRAN; Python and Java are only 4 years apart."
L = [(1957, "FORTRAN", "first widely used\nhigh-level language"), (1972, "C", "Dennis Ritchie,\nBell Labs"), (1985, "C++", "Bjarne\nStroustrup"), (1991, "Python", "Guido van\nRossum"), (1995, "Java", "James\nGosling")]
assert 1972 - 1957 == 15 and 1995 - 1957 == 38 and 1995 - 1991 == 4
f = Fig(780, 250); X0, X1, A0, A1 = 50, 730, 1955, 2000; ax = lambda y: X0 + (y - A0) * (X1 - X0) / (A1 - A0); Y = 120
f.line(X0, Y, X1, Y, color=NAVY, sw=3)
for y in range(1955, 2001, 5):
    f.line(ax(y), Y - 4, ax(y), Y + 4, color=SLATE); f.text(ax(y), Y + 20, str(y), size=10, color=SLATE)
for i, (yr, n, d) in enumerate(L):
    x = ax(yr); up = i % 2 == 0; yy = Y + (-62 if up else 62)
    f.line(x, Y, x, yy, color=TEAL, sw=1.1); f.circle(x, Y, 4.5, fill=TEAL, stroke=TEAL)
    f.box(x - 65, yy - (50 if up else 0), 130, 50, f"{n} ({yr})\n{d}", fill=("#fef9c3" if up else "#dbeafe"), stroke=(AMBER if up else NAVY), size=9.5, bold=True, r=4)
```

```svgfig label="4.9" caption="Flowchart symbols and a worked flowchart: read A and B, test A > B, print the larger. Oval = start/end, parallelogram = input/output, rectangle = process, diamond = decision. A flowchart is the diagram of an algorithm; the algorithm is the step-by-step procedure itself."
f = Fig(780, 330)
f.text(80, 18, "Symbols", size=11, color=NAVY, bold=True)
f.box(20, 30, 120, 30, "Start / End", fill="#fecaca", stroke=RED, size=10, bold=True, r=15)
f.poly([(35, 110), (145, 110), (125, 78), (15, 78)], fill="#dbeafe", stroke=NAVY, label="Input / Output", lx=80, ly=94, size=9)
f.box(20, 126, 120, 30, "Process", fill="#bbf7d0", stroke=TEAL, size=10, bold=True, r=2)
f.poly([(80, 166), (140, 196), (80, 226), (20, 196)], fill="#fef9c3", stroke=AMBER, label="Decision", lx=80, ly=196, size=9)
cx = 470
f.box(cx - 55, 14, 110, 28, "Start", fill="#fecaca", stroke=RED, size=10.5, bold=True, r=14)
f.arrow([(cx, 42), (cx, 62)], color=SLATE)
f.poly([(cx - 70, 100), (cx + 80, 100), (cx + 60, 62), (cx - 90, 62)], fill="#dbeafe", stroke=NAVY, label="Read A, B", lx=cx - 5, ly=81, size=10.5)
f.arrow([(cx, 100), (cx, 122)], color=SLATE)
f.poly([(cx, 122), (cx + 70, 156), (cx, 190), (cx - 70, 156)], fill="#fef9c3", stroke=AMBER, label="A > B ?", lx=cx, ly=156, size=11)
f.arrow([(cx - 70, 156), (cx - 150, 156), (cx - 150, 214)], color=TEAL, label="Yes", lpos=(cx - 110, 148))
f.arrow([(cx + 70, 156), (cx + 150, 156), (cx + 150, 214)], color=RED, label="No", lpos=(cx + 110, 148))
f.poly([(cx - 90, 252), (cx - 210, 252), (cx - 195, 214), (cx - 105 - 45, 214)], fill="#dbeafe", stroke=NAVY, label="Print A", lx=cx - 150, ly=233, size=10.5)
f.poly([(cx + 210, 252), (cx + 90, 252), (cx + 105, 214), (cx + 195, 214)], fill="#dbeafe", stroke=NAVY, label="Print B", lx=cx + 150, ly=233, size=10.5)
f.arrow([(cx - 150, 252), (cx - 150, 280), (cx - 40, 280)], color=SLATE); f.arrow([(cx + 150, 252), (cx + 150, 280), (cx + 40, 280)], color=SLATE)
f.box(cx - 40, 266, 80, 28, "End", fill="#fecaca", stroke=RED, size=10.5, bold=True, r=14)
```

```svgfig label="4.10" caption="Full forms grouped by family so that they stick: hardware, interface and file formats, Internet, input recognition and data. Learn them as sets, not as a 25-item list."
fam = [("Hardware", "#fed7aa", AMBER, ["CPU: Central Processing Unit", "RAM: Random Access Memory", "ROM: Read Only Memory", "USB: Universal Serial Bus"]),
       ("Interface and files", "#e9d5ff", NAVY, ["GUI: Graphical User Interface", "PDF: Portable Document Format", "ASCII: American Standard Code for Information Interchange"]),
       ("Internet", "#bbf7d0", TEAL, ["URL: Uniform Resource Locator", "ISP: Internet Service Provider", "HTML: HyperText Markup Language"]),
       ("Input recognition", "#fecaca", RED, ["OCR: Optical Character Recognition", "OMR: Optical Mark Recognition", "MICR: Magnetic Ink Character Recognition"]),
       ("Data and course", "#bfdbfe", NAVY, ["SQL: Structured Query Language", "BCA: Bachelor of Computer Application"])]
f = Fig(780, 330)
for i, (t, col, ec, items) in enumerate(fam):
    x = 8 + i * 154
    f.box(x, 10, 146, 32, t, fill=col, stroke=ec, size=10.5, bold=True)
    for j, it in enumerate(items):
        a, b = it.split(": ")
        y = 54 + j * 70
        f.box(x, y, 146, 62, "", fill="#ffffff", stroke=ec, r=5)
        f.text(x + 73, y + 16, a, size=13, color=ec, bold=True)
        words = b.split(); lines = []; cur = ""
        for w in words:
            if len(cur) + len(w) > 22: lines.append(cur.strip()); cur = ""
            cur += w + " "
        lines.append(cur.strip())
        f.text(x + 73, y + 36 + (len(lines) - 1) * 5.2, "\n".join(lines), size=8.5, color=SLATE, bold=True)
```

## 4.4 Important full forms and inventors

| Abbr. | Full form |
|---|---|
| CPU | Central Processing Unit |
| RAM / ROM | Random Access Memory / Read Only Memory |
| USB | Universal Serial Bus |
| GUI | Graphical User Interface |
| URL | Uniform Resource Locator |
| ISP | Internet Service Provider |
| SQL | Structured Query Language |
| ASCII | American Standard Code for Information Interchange |
| PDF | Portable Document Format |
| OCR / OMR / MICR | Optical Character / Optical Mark / Magnetic Ink Character Recognition |
| BCA | Bachelor of Computer Application |

## 4.5 Eight traps in Internet, HTML and programming questions

These eight traps appear in almost every set of entrance questions on this chapter. Each one is a pair of ideas that sound similar.

1. **Internet is not the Web.** The Internet is the worldwide network of networks (ARPANET began in 1969), while the World Wide Web is one service on it, invented by Tim Berners-Lee at CERN in 1989 (Fig 4.1). E-mail and FTP also use the Internet but are not the Web. A question "who invented the Internet" has a different answer from "who invented the WWW".
2. **Browser is not a search engine.** Chrome, Firefox, Edge and Safari are browsers, the programs you use to open pages. Google and Bing are search engines, which are websites that find pages. Students lose marks by writing Google as a browser, so say it aloud: "I open Google *in* Chrome".
3. **Which protocol does what.** HTTP fetches web pages and HTTPS is the secure version, FTP moves files, SMTP *sends* mail and POP3 or IMAP *receive* mail (Fig 4.6). TCP/IP is the base suite, and DNS converts a domain name into an IP address. Remember the arrow: S in SMTP is for *sending* ("Simple Mail Transfer").
4. **Cc and Bcc.** Cc (carbon copy) recipients are visible to everyone, while Bcc (blind carbon copy) recipients are hidden from all the others. The main recipient goes in To. If a manager wants to send a notice to 200 students without showing their addresses to each other, Bcc is the correct choice.
5. **IPv4 is 32 bits and IPv6 is 128 bits.** An IPv4 address has four octets, each from 0 to 255, so 192.168.1.256 is not valid (Fig 4.4). IPv4 gives about 4.3 billion addresses, which is why IPv6 was created. Nepal's country domain is .np, and tu.edu.np is read from the right: Nepal, education, Tribhuvan University.
6. **HTML is a markup language, not a programming language.** It describes structure with tags such as `<h1>`, `<p>`, `<a>` and `<img>`; it has no loops or decisions. `<h1>` is the largest heading and `<h6>` the smallest, and `<br>` needs no closing tag. If an option says "HTML is a programming language", it is wrong.
7. **Match language to creator.** C is by Dennis Ritchie (1972, Bell Labs), C++ by Bjarne Stroustrup, Java by James Gosling and Python by Guido van Rossum (Plate 4.4). FORTRAN (1957) was the first widely used high-level language. The order of birth is FORTRAN, C, C++, Python, Java (Fig 4.8).
8. **Syntax error or logic error?** A syntax error breaks the rules of the language, so the program will not compile or run. A logic error lets the program run but gives the wrong answer, such as using + instead of -. Also remember the flowchart symbols: oval for start and end, parallelogram for input and output, rectangle for a process and diamond for a decision (Fig 4.9).

### 4.5.1 Worked checks

**Q. Which of the following is a valid IPv4 address? (a) 192.168.1.256 (b) 172.16.0.1 (c) 10.300.4.1 (d) 192.168.1**

**Answer: (b).** An IPv4 address must have exactly four octets and each must be between 0 and 255. Option (a) has 256, option (c) has 300 and option (d) has only three octets, so only 172.16.0.1 is valid. It also belongs to a private range, which is common on college LANs.

**Q. Ram sends a mail To: Sita, Cc: Hari, Bcc: Gita. Who can see Gita's address?** (a) Sita (b) Hari (c) Everyone (d) Only Ram

**Answer: (d).** A Bcc address is hidden from every other recipient, so Sita and Hari cannot see Gita; Ram wrote it himself so he knows it. Gita sees the To and Cc lists, so she knows who else received the mail (Fig 4.6).

## Formula and fact sheet

| Quick facts | |
|---|---|
| WWW | Tim Berners-Lee, 1989 |
| IPv4 / IPv6 | 32 / 128 bits |
| Send mail / receive mail | SMTP / POP3, IMAP |
| C / Python / Java | Ritchie / van Rossum / Gosling |

## Chapter summary

- HTML is a markup language; `<h1>` is the largest heading.
- SMTP sends, POP3 and IMAP receive.
- Bcc hides recipients from each other.
- HTTPS means HTTP over a secure connection.
- Learn the creator of each language and the full forms above.

## Practice questions

**Set A — Recall (20 questions)**

1. HTML stands for
   (a) Hyper Text Making Language (b) High Text Markup Language (c) HyperText Markup Language (d) Hyperlink Text Mode Language
2. The World Wide Web was invented by
   (a) Tim Berners-Lee (b) Dennis Ritchie (c) Bill Gates (d) Linus Torvalds
3. The tag for the largest heading in HTML is
   (a) `<head>` (b) `<h6>` (c) `<title>` (d) `<h1>`
4. The HTML tag for a hyperlink is
   (a) `<link>` (b) `<a>` (c) `<href>` (d) `<url>`
5. URL stands for
   (a) Uniform Resource Locator (b) Universal Record Locator (c) Uniform Record Link (d) United Resource Locator
6. The protocol used to send e-mail is
   (a) HTTP (b) FTP (c) SMTP (d) DNS
7. The country-code domain of Nepal is
   (a) .nl (b) .ne (c) .nep (d) .np
8. The C language was created by
   (a) James Gosling (b) Dennis Ritchie (c) Guido van Rossum (d) Bjarne Stroustrup
9. Python was created by
   (a) James Gosling (b) Bjarne Stroustrup (c) Guido van Rossum (d) Dennis Ritchie
10. Java was created by
    (a) James Gosling (b) Dennis Ritchie (c) Linus Torvalds (d) Tim Berners-Lee
11. Bcc in e-mail stands for
    (a) Black copy (b) Basic carbon copy (c) Blind computer copy (d) Blind carbon copy
12. An IPv4 address is how many bits long?
    (a) 16 (b) 32 (c) 64 (d) 128
13. In HTTPS the letter S means
    (a) simple (b) speed (c) secure (d) server
14. The HTML tag that inserts an image is
    (a) `<img>` (b) `<image>` (c) `<pic>` (d) `<src>`
15. A translator that converts a program line by line is a
    (a) compiler (b) assembler (c) linker (d) interpreter
16. SQL is used to work with
    (a) graphics (b) databases (c) networks (d) printers
17. Which of these is NOT a programming language?
    (a) C (b) Java (c) HTML (d) Python
18. Google Chrome is a
    (a) web browser (b) operating system (c) programming language (d) search engine
19. Which of these is a search engine?
    (a) Chrome (b) Firefox (c) Edge (d) Google Search
20. ISP stands for
    (a) Internal Service Protocol (b) Internet Service Provider (c) Internet System Program (d) Internal Site Provider

::: note Answers and explanations — Set A
**1.** (c) — HyperText Markup Language.
**2.** (a) — Tim Berners-Lee, 1989.
**3.** (d) — `<h1>` is the largest; `<h6>` the smallest.
**4.** (b) — the anchor tag with an href.
**5.** (a) — Uniform Resource Locator.
**6.** (c) — SMTP sends mail.
**7.** (d) — .np.
**8.** (b) — Dennis Ritchie, 1972.
**9.** (c) — Guido van Rossum.
**10.** (a) — James Gosling.
**11.** (d) — blind carbon copy.
**12.** (b) — 32 bits; IPv6 is 128.
**13.** (c) — secure.
**14.** (a) — `<img src="…">`.
**15.** (d) — an interpreter; a compiler works on the whole program.
**16.** (b) — Structured Query Language.
**17.** (c) — HTML is a markup language.
**18.** (a) — Chrome is a browser.
**19.** (d) — Google Search; the others are browsers.
**20.** (b) — Internet Service Provider.
:::

**Set B — Understanding (12 questions)**

1. ARPANET, the forerunner of the Internet, began in
   (a) 1949 (b) 1959 (c) 1979 (d) 1969
2. An IPv6 address is how many bits long?
   (a) 64 (b) 128 (c) 32 (d) 256
3. Which protocol is used to receive e-mail?
   (a) POP3 (b) SMTP (c) FTP (d) HTML
4. The HTML tag `<br>` produces
   (a) bold text (b) italic text (c) a line break (d) a new page
5. The HTML tag `<p>` defines a
   (a) picture (b) page (c) program (d) paragraph
6. DNS translates
   (a) domain names into IP addresses (b) IP addresses into MAC addresses (c) files into folders (d) text into speech
7. A web browser displays pages written in
   (a) C (b) HTML (c) SQL (d) binary only
8. The first widely used high-level programming language (1957) was
   (a) COBOL (b) BASIC (c) FORTRAN (d) Pascal
9. In an e-mail, Cc stands for
   (a) carbon copy (b) closed copy (c) central copy (d) cancelled copy
10. CSS is used for
    (a) databases (b) networking (c) hardware (d) styling web pages
11. USB stands for
    (a) Universal Standard Bus (b) United Serial Bus (c) Universal Serial Bus (d) Unique Serial Block
12. GUI stands for
    (a) General User Interface (b) Graphical User Interface (c) Group User Input (d) Global User Interface

::: note Answers and explanations — Set B
**1.** (d) — 1969.
**2.** (b) — 128 bits.
**3.** (a) — POP3 (or IMAP) receives mail.
**4.** (c) — a line break.
**5.** (d) — paragraph.
**6.** (a) — names to numeric addresses.
**7.** (b) — HTML.
**8.** (c) — FORTRAN, 1957.
**9.** (a) — carbon copy.
**10.** (d) — Cascading Style Sheets style pages.
**11.** (c) — Universal Serial Bus.
**12.** (b) — Graphical User Interface.
:::

**Set C — Application (8 questions)**

1. The HTML tag for an ordered list is
   (a) `<ul>` (b) `<ol>` (c) `<li>` (d) `<list>`
2. The Internet is an example of a
   (a) LAN (b) PAN (c) MAN (d) WAN
3. The attribute that gives the destination of a link is
   (a) href (b) src (c) alt (d) link
4. Which is a valid e-mail address?
   (a) ram@@gmail.com (b) ram.gmail.com (c) ram@gmail.com (d) @ram gmail.com
5. ASCII stands for
   (a) American System Code for Information Interchange (b) American Standard Code for Information Interchange (c) Applied Standard Code for Internet Interchange (d) Automatic Standard Code for Information Input
6. A step-by-step procedure to solve a problem is called
   (a) syntax (b) a compiler (c) a bug (d) an algorithm
7. In a flowchart a decision is shown by a
   (a) rectangle (b) oval (c) diamond (d) parallelogram
8. A syntax error is
   (a) a violation of the rules of the language (b) a wrong answer from a correct program (c) a hardware fault (d) a slow program

::: note Answers and explanations — Set C
**1.** (b) — `<ol>`; `<ul>` is unordered.
**2.** (d) — a wide area network of networks.
**3.** (a) — href holds the link target; src is for images.
**4.** (c) — one @ and a domain.
**5.** (b) — American Standard Code for Information Interchange.
**6.** (d) — an algorithm.
**7.** (c) — the diamond.
**8.** (a) — the code breaks the language's grammar rules.
:::
