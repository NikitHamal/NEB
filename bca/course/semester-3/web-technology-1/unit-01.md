---
subject: Web Technology I
grade: BCA Semester 3
unit: 1
title: Internet and the World Wide Web
area: BCA 203 · Web Technology I · Unit 1
---

The **Internet** is the global network of networks; the **World Wide Web** is one service that runs on it: linked documents fetched over HTTP. This unit explains how a page travels from a server to your browser.

::: key What this unit gives you
- Internet, WWW, client–server model; history and Web 1.0 to 3.0.
- IP addresses, domain names and DNS; the anatomy of a URL.
- HTTP requests, responses, methods, status codes, headers, cookies.
- Web servers, browsers, hosting and related protocols (FTP, SMTP, POP3, IMAP).
:::

## 1.1 Internet versus Web

| | Internet | World Wide Web |
|---|---|---|
| What | the physical and logical network infrastructure (cables, routers, TCP/IP) | a service of linked hypertext documents and resources |
| Born | ARPANET 1969; TCP/IP adopted 1983 | proposed by Tim Berners-Lee at CERN, 1989; first site 1991 |
| Others on the Internet | email, FTP, VoIP, online games, SSH | |

The Web has had phases: **Web 1.0** (static read-only pages), **Web 2.0** (user-generated content, social media, dynamic apps with AJAX), **Web 3.0 / semantic web** (machine-readable meaning, decentralised data; the term is used loosely).

**Client–server model.** A **client** (browser) sends a request; a **server** (a program, not just a machine) listens and responds. Three-tier web apps split into presentation (browser), application logic (server code) and data (database). An **intranet** is a private network using the same technology; an **extranet** shares part of it with partners.

## 1.2 Addresses: IP, domain, DNS

- **IP address** identifies a host: IPv4 has 32 bits written as four decimal bytes (`192.168.1.10`, about 4.3 billion addresses), IPv6 has 128 bits (`2001:db8::1`). **Private ranges** (`10.x.x.x`, `172.16–31.x.x`, `192.168.x.x`) are not routable on the Internet; routers use NAT.
- **Domain name** is the human-readable name: `www.example.com.np` reads right to left: country code TLD `np`, second level `com`, domain `example`, host `www`.
- **DNS** (Domain Name System) is the distributed phone book that translates names into IP addresses: browser cache → operating system → recursive resolver (ISP) → root server → TLD server → the domain's **authoritative** server. Results are cached for a time set by the **TTL**. Record types: `A` (IPv4), `AAAA` (IPv6), `CNAME` (alias), `MX` (mail), `NS` (name server), `TXT`.
- **Port** numbers pick the service on a host: HTTP 80, HTTPS 443, FTP 21, SMTP 25, SSH 22, DNS 53.

## 1.3 URL anatomy

```text
https://www.example.com:8080/courses/web/index.html?lang=en&page=2#unit3
\___/   \_____________/ \__/\____________________/ \___________/ \____/
scheme       host       port         path               query    fragment
```

The **scheme** names the protocol; **host** locates the server; **path** names the resource; **query string** carries `name=value` pairs separated by `&`; the **fragment** is used only by the browser to scroll to an element. A URL is a kind of **URI**. **Absolute** URLs include the scheme and host; **relative** ones (`../img/a.png`) are resolved against the current page.

## 1.4 HTTP

**HTTP** (Hypertext Transfer Protocol) is a text-based, **stateless** request–response protocol over TCP; **HTTPS** wraps it in TLS encryption. Each request is independent; the server remembers nothing unless cookies or sessions are used.

```text
GET /courses/web/index.html HTTP/1.1          <- request line: method, path, version
Host: www.example.com                          <- headers
Accept: text/html
User-Agent: Mozilla/5.0

HTTP/1.1 200 OK                                <- status line
Content-Type: text/html; charset=UTF-8
Content-Length: 1256

<!DOCTYPE html> ...                            <- body
```

| Method | Use | Safe/idempotent |
|---|---|---|
| `GET` | read a resource; parameters in the URL | yes |
| `POST` | send data to create/process; data in the body | no |
| `PUT` / `PATCH` | replace / partially update | PUT idempotent |
| `DELETE` | remove | idempotent |
| `HEAD` | headers only | yes |

| Status class | Meaning | Examples |
|---|---|---|
| 1xx | informational | 101 Switching Protocols |
| 2xx | success | 200 OK, 201 Created, 204 No Content |
| 3xx | redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | client error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | server error | 500 Internal Server Error, 503 Service Unavailable |

**Cookies** are small name–value pairs the server sets with `Set-Cookie` and the browser returns with every later request; they implement **sessions** (login state), preferences and tracking. Flags: `HttpOnly` (not readable by JavaScript), `Secure` (HTTPS only), `SameSite`, `Max-Age`.

**GET versus POST:** GET data is visible in the URL, bookmarkable, cached, length-limited; POST is for forms that change data or carry secrets such as passwords (still needs HTTPS to be private).

## 1.5 Web server, browser, search engine and hosting

- A **web server** (Apache, Nginx, IIS, Node.js) receives HTTP requests and returns **static** files or output of **dynamic** programs (PHP, Node, Python, Java).
- A **browser** (Chrome, Firefox, Safari, Edge) requests resources, parses HTML into the **DOM**, applies CSS, runs JavaScript and renders. Engines: Blink, Gecko, WebKit.
- A **search engine** has a **crawler** (follows links), an **index** (word → pages) and a **ranking** algorithm (relevance, links such as PageRank, quality).
- **Hosting:** shared, VPS, dedicated, cloud, or static hosting. To publish: register a domain, point its DNS `A`/`CNAME` record to the host, upload files (FTP/SFTP or Git), enable HTTPS (certificate).
- **Web design strategies:** know the audience, plan the structure (site map), keep navigation consistent, design for mobile first, load fast, be accessible.

## 1.6 Other Internet protocols and services

| Protocol | Port | Purpose |
|---|---|---|
| **FTP / SFTP** | 21 / 22 | transfer files |
| **SMTP** | 25, 587 | **send** mail between servers |
| **POP3** | 110 | download mail and (usually) delete from the server |
| **IMAP** | 143 | read mail kept on the server, synchronised across devices |
| **Telnet / SSH** | 23 / 22 | remote terminal (Telnet unencrypted; use SSH) |
| **DHCP** | 67/68 | automatically give hosts IP addresses |

**Email path:** your client → your SMTP server → recipient's SMTP server (found by MX record) → recipient's mailbox → read by POP3 or IMAP.

## Formula and fact sheet

- IPv4 = 32 bits (2³² ≈ 4.29 × 10⁹); IPv6 = 128 bits.
- URL = scheme://host:port/path?query#fragment.
- HTTP is stateless; cookies add state. 2xx ok, 3xx redirect, 4xx client error, 5xx server error.
- Ports: HTTP 80, HTTPS 443, FTP 21, SSH 22, SMTP 25, DNS 53, POP3 110, IMAP 143.
- DNS: name → IP; A, AAAA, CNAME, MX, NS.

## Chapter summary

- The Web is a service on the Internet built from URLs, HTTP and HTML; clients request and servers respond.
- DNS turns names into IP addresses; HTTP is stateless and uses methods and status codes; cookies carry sessions.
- Browsers render; servers serve static or dynamic content; mail uses SMTP, POP3 and IMAP.

## Practice

1. Differentiate the Internet and the World Wide Web.
2. Identify the parts of `https://shop.example.com.np:8443/items/list.php?cat=5&sort=price#top`.
3. Explain how DNS resolves `www.example.com`.
4. State the difference between GET and POST; when would you use each?
5. What do status codes 200, 301, 403, 404 and 500 mean?
6. Why is HTTP called stateless and how do cookies address this?
7. Compare POP3 and IMAP.
8. List the steps needed to publish a website on its own domain.

::: note Answers and worked solutions
**1.** The Internet is the global network infrastructure; the Web is a service of linked documents (HTTP/HTML) running on it; email and FTP are other services.
**2.** Scheme `https`; host `shop.example.com.np`; port `8443`; path `/items/list.php`; query `cat=5&sort=price`; fragment `top`.
**3.** Check the browser/OS cache; ask the recursive resolver; it asks a root server, then the `.com` TLD server, then the domain's authoritative server, which returns the IP; the answer is cached for its TTL.
**4.** GET reads and puts parameters in the URL (searches, bookmarks); POST sends data in the body (login, registration, uploads).
**5.** 200 success; 301 permanent redirect; 403 forbidden (authenticated but not allowed); 404 not found; 500 server error.
**6.** Each request is independent and carries no memory of earlier ones. A cookie set by the server is sent back on each request, letting the server recognise the session.
**7.** POP3 downloads mail to one device, usually removing it from the server; IMAP leaves mail on the server and synchronises folders across devices.
**8.** Choose hosting; register a domain; set the DNS A/CNAME record to the host; upload files; install an HTTPS certificate; test.
:::
