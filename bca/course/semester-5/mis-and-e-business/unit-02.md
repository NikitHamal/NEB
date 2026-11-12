---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 2
title: The Network Infrastructure for E-Commerce
hours: 8
area: BCA 304 · MIS and e-Business · Unit 2
---

Every online order travels through cables, radio links, routers and servers before a seller sees it. E-commerce looks like a website but is, underneath, a network service, and its speed, reach and security are set by that network. This unit describes the information superhighway (I-Way), the Internet as the infrastructure that carries e-commerce, the Wireless Application Protocol (WAP), the wireless technologies that connect shoppers (ADSL, Wi-Fi, WiMAX, 3G, 4G and 5G) and the security issues that follow from sending business data through the air.

::: key What this unit gives you
- The I-Way idea and its components: access equipment, on-ramps, backbone and content.
- How the Internet works as an e-commerce platform: packets, TCP/IP, DNS, ISPs and exchange points.
- WAP: architecture, the protocol stack, step-by-step working and why it faded.
- ADSL, WLAN/Wi-Fi, WMAN/WiMAX, UMTS, LTE and 5G NR compared, with a download-time calculation.
- Wireless threats (eavesdropping, evil twin, SIM swap, the WAP gap) and the controls against them.
:::

## 2.1 The information superhighway (I-Way)

The **information superhighway** (I-Way) is the name given in the early 1990s to the idea of a single, high-capacity national and global network that carries voice, data, video and commerce to every home and office. The phrase became popular when the United States government proposed a National Information Infrastructure (NII), a plan to link businesses, schools, libraries and homes by fibre and wireless links. Roads move goods and people; the I-Way moves information and, with it, orders, payments and services. E-commerce is the commercial traffic on that road.

An I-Way needs more than cables. It needs four layers working together, and a weakness in one limits the rest. The usual teaching model names **three physical components** and then adds the content and the rules.

| Component | What it is | Examples in Nepal |
|---|---|---|
| Consumer access equipment | The device and connection hardware at the user's end | Smartphone, laptop, set-top box, modem, router, ONT (fibre terminal) |
| Local on-ramps | The service that connects the user to the wider network | Fibre-to-home from an ISP, ADSL line, cable broadband, mobile data from Nepal Telecom or Ncell, community Wi-Fi |
| Global information distribution networks | The long-distance carriers and backbones that move traffic between cities and countries | National fibre backbone, links to India and China, international gateways and Internet exchange points |

Two further elements make the road useful. **Content and service providers** (online shops, banks, video sites, government portals) supply the destinations. **Policy and law** (telecommunication licences, the Electronic Transactions Act, data and consumer protection) decide who may build and use the network and how disputes are settled. A shopper in Pokhara who orders a book touches every element: a phone (access equipment), a fibre connection (on-ramp), the backbone between Pokhara, Kathmandu and the exchange point (distribution network), the seller's server (content provider) and the licence rules that govern all of it.

```svgfig label="2.1" caption="The I-Way as a chain. The shopper's device (consumer access equipment) connects through a local on-ramp such as fibre, ADSL or mobile data to an ISP. The ISP joins the national and international backbone (the global information distribution networks), which reaches the seller's data centre. Content and service providers sit at the far end, and policy and law surround the whole chain."
f = Fig(580, 190)
xs = [10, 128, 246, 364, 482]
labs = [("Device", "phone, laptop", SOFT, SLATE), ("On-ramp", "fibre, ADSL, 4G", MINT, TEAL), ("ISP", "regional network", BLUE, NAVY), ("Backbone", "national and\nintl. links", SAND, AMBER), ("Content", "shop, bank,\nportal", ROSE, RED)]
for x, (a, b, fl, st) in zip(xs, labs):
    f.box(x, 40, 88, 78, "", fill=fl, stroke=st, r=6)
    f.text(x + 44, 62, a, size=11.5, color=st, bold=True)
    for k, line in enumerate(b.split("\n")):
        f.text(x + 44, 84 + k * 14, line, size=10, color=SLATE, bold=True)
for i in range(4):
    f.arrow([(xs[i] + 88, 79), (xs[i + 1], 79)], color=SLATE)
f.box(10, 140, 560, 34, "Policy and law: licences, Electronic Transactions Act, consumer and data protection", fill=SOFT, stroke=SLATE, size=10.5, bold=True, color=SLATE, r=4)
f.text(290, 22, "Consumer access, local on-ramp, distribution network, content", size=11, color=NAVY, bold=True)
```

## 2.2 The Internet as the network infrastructure for e-commerce

Today the **Internet** is the practical form of the I-Way. It is a network of networks: thousands of independent networks (ISPs, universities, companies, governments) that agree to exchange traffic using one common set of rules, the **TCP/IP protocol suite**. No single body owns it, which is why it grew so fast and why it is hard to control or secure from one place.

Four ideas explain how an order reaches a shop:

1. **Packet switching.** A message such as an order form is cut into small packets, each with source and destination addresses and a sequence number. The packets may take different routes and are reassembled at the destination. This shares the lines among many users and lets traffic go around a failed link.
2. **IP addressing and routing.** Every device has an IP address. Routers read the destination address of each packet and forward it one step closer. IPv4 uses 32-bit addresses (about 4.3 billion); IPv6 uses 128 bits and removes the shortage.
3. **TCP and the application protocols.** TCP gives reliable, ordered delivery (lost packets are re-sent). On top of it HTTP carries web pages, HTTPS adds encryption, SMTP carries email and FTP moves files.
4. **DNS.** The Domain Name System turns a name such as `daraz.com.np` into the IP address of the server, so customers remember names and not numbers.

Behind these ideas are **Internet service providers** (ISPs). A local ISP sells access to customers and buys transit from larger providers. Providers meet at **Internet exchange points (IXPs)**, where they hand traffic to each other directly. Where a local exchange exists, traffic between two Nepali networks need not travel abroad and back, which lowers delay and cost. Nepal reaches the global Internet mainly through terrestrial links through India and, more recently, China.

The same technology is used in three scopes that matter for business:

| Network | Who can use it | Typical e-business use |
|---|---|---|
| **Internet** | Anyone | Online shop, public web site, email, social media |
| **Intranet** | Only the organisation's staff | Internal portal, HR system, shared documents |
| **Extranet** | The organisation plus chosen partners | Supplier ordering portal, dealer stock view, banking links |

For e-commerce the Internet gives five advantages over older private networks (EDI over leased lines): low cost, global reach, open standards, the same network for text, image and video, and quick set-up. It also brings the main weaknesses: variable quality of service, no built-in security and congestion at peak times. Good e-commerce design therefore adds a **content delivery network (CDN)** to place copies of pages near users, **load balancers** to share traffic across servers, **redundant links** to survive a cable cut, and **encryption** (TLS) for every sensitive page.

## 2.3 Wireless Application Protocol (WAP)

In the late 1990s mobile phones had small monochrome screens, slow circuit-switched data (about 9.6 kbit/s on GSM) and little memory. An ordinary web page was far too heavy. The **Wireless Application Protocol (WAP)** was designed in 1997 by the WAP Forum (Ericsson, Nokia, Motorola and Unwired Planet) as an open standard to bring web-like services to such handsets. WAP 1.0 appeared in 1998 and WAP 2.0 in 2002, after which the Forum's work passed to the Open Mobile Alliance. Even if WAP browsing has disappeared, it explains how mobile e-commerce (m-commerce) began, and the TU syllabus still asks for its architecture and working.

### Architecture of WAP

WAP uses a three-part, client-gateway-server model:

- **WAP client:** the handset with a **microbrowser**, a very small browser that shows pages written in **WML (Wireless Markup Language)**. A WML document is a **deck** of small **cards**; one card is shown at a time, which suits a small screen.
- **WAP gateway (proxy):** a server operated by the mobile operator. It translates between the compact WAP protocols used over the air and ordinary HTTP used on the Internet, and it compresses WML into a binary form so that less data crosses the slow link.
- **Origin (web) server:** the shop's own server holding WML pages, or HTML pages that a filter converts to WML.

```svgfig label="2.2" caption="WAP architecture. The handset's microbrowser sends a compact WAP request over the wireless bearer to the WAP gateway. The gateway converts it to an HTTP request for the origin web server on the Internet. The server replies with WML or HTML, and the gateway encodes the answer in compact binary form before sending it back to the phone. The gateway is the one place where data are briefly in plain form, known as the WAP gap."
f = Fig(580, 170)
f.box(10, 45, 120, 70, "", fill=MINT, stroke=TEAL, r=6); f.text(70, 68, "WAP client", size=11.5, color=TEAL, bold=True); f.text(70, 88, "microbrowser", size=10.5, color=SLATE, bold=True); f.text(70, 104, "(WML deck)", size=10.5, color=SLATE, bold=True)
f.box(230, 45, 120, 70, "", fill=SAND, stroke=AMBER, r=6); f.text(290, 68, "WAP gateway", size=11.5, color=AMBER, bold=True); f.text(290, 88, "protocol and", size=10.5, color=SLATE, bold=True); f.text(290, 104, "content converter", size=10.5, color=SLATE, bold=True)
f.box(450, 45, 120, 70, "", fill=BLUE, stroke=NAVY, r=6); f.text(510, 68, "Web server", size=11.5, color=NAVY, bold=True); f.text(510, 88, "WML or HTML", size=10.5, color=SLATE, bold=True); f.text(510, 104, "e-shop content", size=10.5, color=SLATE, bold=True)
f.arrow([(130, 70), (230, 70)], color=TEAL, label="WAP request", lpos=(180, 58))
f.arrow([(230, 98), (130, 98)], color=TEAL, label="binary WML", lpos=(180, 114))
f.arrow([(350, 70), (450, 70)], color=NAVY, label="HTTP request", lpos=(400, 58))
f.arrow([(450, 98), (350, 98)], color=NAVY, label="WML / HTML", lpos=(400, 114))
f.text(70, 140, "wireless network", size=10.5, color=TEAL, bold=True); f.text(290, 140, "operator network", size=10.5, color=AMBER, bold=True); f.text(510, 140, "the Internet", size=10.5, color=NAVY, bold=True)
```

### The WAP protocol stack

WAP mirrors the Internet stack with lighter layers:

| WAP layer | Role | Internet counterpart |
|---|---|---|
| Wireless Application Environment (WAE) | WML, WMLScript, microbrowser, telephony interfaces | HTML, JavaScript, browser |
| Wireless Session Protocol (WSP) | Request and reply sessions that can be suspended and resumed | HTTP |
| Wireless Transaction Protocol (WTP) | Reliable request-response transactions with low overhead | TCP (lighter) |
| Wireless Transport Layer Security (WTLS) | Encryption, integrity and authentication | SSL/TLS |
| Wireless Datagram Protocol (WDP) | Datagram transport over any bearer | UDP |
| Bearers | SMS, circuit-switched data, GPRS and other carriers | Physical and link layers |

### How WAP works, step by step

1. The user selects a bookmark or types a URL in the microbrowser.
2. The microbrowser encodes the request and sends it through the bearer to the WAP gateway (WSP over WTP, protected by WTLS).
3. The gateway decodes it and issues a normal HTTP request to the origin server.
4. The server returns a WML deck, or an HTML page that a converter turns into WML.
5. The gateway compiles the WML into a compact binary format and returns it to the handset.
6. The microbrowser shows the first card; choosing a link moves to another card in the same deck without another request.

**Why WAP faded.** Data were slow, screens small, pages poorly designed and pricing by the minute. Smartphones with full browsers and faster 3G/4G networks replaced it, and WAP 2.0 itself moved to XHTML Mobile Profile, close to ordinary HTML. A remnant, **WAP billing**, still lets mobile operators charge subscriptions to a phone account.

## 2.4 Wireless technologies for e-commerce

A shopper's last link to the network is often wireless. Wireless networks are grouped by range:

- **WPAN** (personal): a few metres, for example Bluetooth.
- **WLAN** (local): a building or campus, for example Wi-Fi (IEEE 802.11).
- **WMAN** (metropolitan): a city, for example WiMAX (IEEE 802.16).
- **WWAN** (wide area): a country, for example cellular 3G, 4G and 5G.

| Technology | Type and standard | Typical theoretical speed | Range | Typical e-commerce role |
|---|---|---|---|---|
| **ADSL** | Wired, over copper telephone line; asymmetric, so the download speed is higher than upload | Up to 8 Mbps (ADSL), 24 Mbps (ADSL2+) down; about 1 Mbps up | Within about 5 km of the exchange | Home and small-shop broadband |
| **Wi-Fi (WLAN)** | IEEE 802.11 b/g/n/ac/ax | 11 Mbps (b), 54 Mbps (g), 600 Mbps (n), several Gbps (ac, ax) | 30 to 100 m indoors | Shops, cafes, offices, in-store customer Wi-Fi |
| **WiMAX (WMAN)** | IEEE 802.16 (fixed 16d, mobile 16e) | About 70 Mbps | Up to tens of km in line of sight; a few km in practice | Rural and city wireless broadband, ISP backhaul |
| **UMTS (3G)** | Cellular, WCDMA | 384 kbps, then 14 to 42 Mbps with HSPA and HSPA+ | Cell radius of a few km | First mass mobile web and m-commerce |
| **LTE (4G)** | Cellular, OFDMA downlink | 100 Mbps (LTE) to 1 Gbps (LTE-Advanced); latency near 10 ms | Several km per cell | Mobile apps, wallets, video, delivery tracking |
| **5G NR** | Cellular, 3GPP New Radio | Up to 20 Gbps peak target; latency target 1 ms; very dense device support | Small cells, sub-6 GHz and millimetre-wave | AR shopping, live commerce, IoT stock sensors |

Real speeds are far lower than the theoretical figures because of distance, interference, the number of users sharing the cell and the quality of the backhaul. WiMAX has largely been replaced by LTE, but is still examined.

::: example How long does a 100 MB product catalogue take to download?
Size in bits: 100 MB × 8 = 800 megabits. Time = size ÷ speed.
- ADSL2+ at a realistic 16 Mbps: 800 ÷ 16 = **50 seconds**.
- 4G at a realistic 40 Mbps: 800 ÷ 40 = **20 seconds**.
- 5G at a realistic 400 Mbps: 800 ÷ 400 = **2 seconds**.
The same catalogue is 25 times faster on 5G than on ADSL, which is why app-based shopping with video and 3D previews becomes practical only on the faster links.
:::

```svgfig label="2.3" caption="Realistic download time for a 100 MB file (800 megabits). ADSL2+ at 16 Mbps takes 50 seconds, 4G at 40 Mbps takes 20 seconds and 5G at 400 Mbps takes 2 seconds. Time = size in bits divided by speed in bits per second, so a tenfold faster link is tenfold quicker."
f = Fig(580, 150)
dt = [("ADSL2+ 16 Mbps", 50, RED, ROSE), ("4G 40 Mbps", 20, AMBER, SAND), ("5G 400 Mbps", 2, TEAL, MINT)]
for i, (n, t, c, fl) in enumerate(dt):
    y = 12 + i * 44
    f.text(10, y + 18, n, size=11, color=SLATE, bold=True, anchor="start")
    f.box(150, y, max(t * 7.6, 6), 30, f"{t} s" if t > 5 else "", fill=fl, stroke=c, color=c, size=11, bold=True, r=3)
    if t <= 5:
        f.text(150 + t * 7.6 + 8, y + 18, f"{t} s", size=11, color=c, bold=True, anchor="start")
```

## 2.5 Security issues related to wireless communication

Radio waves pass through walls and can be received by anyone nearby, so wireless links face threats that a cable does not. For an e-business the loss is not only a stolen password: customers lose trust in the whole service.

| Threat | How it works | Main control |
|---|---|---|
| **Eavesdropping (sniffing)** | An attacker captures traffic on an open Wi-Fi or a weakly encrypted link | HTTPS everywhere, WPA2 or WPA3 on Wi-Fi, a VPN on public networks |
| **Rogue access point and evil twin** | A fake hotspot copies a real name ("Cafe_Free_WiFi") and the user connects to it; the attacker sees or alters traffic | Verify the network name, disable auto-connect, use HTTPS and a VPN |
| **Weak Wi-Fi encryption** | WEP can be broken in minutes; WPA2 passphrases can be guessed offline if short; the KRACK attack (2017) showed a protocol flaw | WPA3 or WPA2 with a long random passphrase, firmware updates |
| **Man-in-the-middle** | An attacker sits between user and server and relays or changes messages | TLS with certificate checking, certificate pinning in apps |
| **Denial of service by jamming or flooding** | Noise on the frequency or floods of requests make the link or site unusable | Spectrum monitoring, rate limiting, redundant links |
| **SIM swap and SS7 abuse** | Fraudsters persuade an operator to move a victim's number to a new SIM and then read OTP messages | Operator identity checks, app-based authentication, alerts on SIM change |
| **Lost or stolen device** | A phone with logged-in banking or shop apps | Screen lock, encryption, remote wipe |
| **The WAP gap** | In WAP 1.x the gateway decrypts WTLS and re-encrypts with SSL, so data are plain inside the gateway | End-to-end TLS (WAP 2.0), trusted operators |

Practical rules for a business that accepts mobile and wireless orders:

1. Put payment pages on HTTPS only and never send card data or OTPs by SMS, email or chat.
2. Use WPA3 or WPA2 with a strong passphrase on the shop's own Wi-Fi, and keep customer Wi-Fi on a separate network from the payment terminals.
3. Change default router passwords and update firmware.
4. Give staff and customers clear advice on public Wi-Fi: use the mobile data connection for banking when in doubt.
5. Log and monitor access points, and remove unknown devices.

## 2.6 Seeing the network: I-Way, WAP and wireless speeds

Figure 2.1 shows the chain from device to content, Figure 2.2 how a WAP request passes through the gateway, and Figure 2.3 how a faster wireless link shortens the same download. Notice the pattern: each layer adds capacity or protection and also a place where something can fail or be attacked.

## Chapter summary

- The I-Way is the high-capacity network idea whose practical form is the Internet; its components are access equipment, on-ramps and distribution networks, plus content and the rules.
- The Internet carries e-commerce by packet switching, IP, TCP, HTTP and DNS; intranets and extranets use the same technology for staff and partners.
- WAP (client, gateway, server) brought the web to early phones using WML and a lightweight stack; the gateway created the WAP gap, and smartphones replaced it.
- ADSL, Wi-Fi, WiMAX, UMTS, LTE and 5G differ in range, speed and cost; real speeds are well below the theoretical ones.
- Wireless links face eavesdropping, evil twins, jamming and SIM-swap fraud; encryption (HTTPS, WPA3), VPNs and strong authentication are the main controls.

## Practice

1. Define the information superhighway. Name its three components.
2. Differentiate the Internet, an intranet and an extranet, with one e-business use of each.
3. Why is packet switching suited to e-commerce traffic?
4. State the roles of DNS and an IXP.
5. Draw and label the WAP architecture.
6. List the layers of the WAP stack and give the Internet counterpart of WTLS and WDP.
7. What is the WAP gap and how did WAP 2.0 reduce it?
8. Compare ADSL, WiMAX, 4G and 5G in a table (speed, range, use).
9. How long does a 250 MB file take at 20 Mbps?
10. Describe an evil twin attack and two defences.
11. Why is SIM swap dangerous for online banking?

::: note Answers and worked solutions
**1.** The I-Way is a high-capacity national and global network that carries voice, data and video to homes and businesses. Components: consumer access equipment, local on-ramps, global information distribution networks.
**2.** Internet: open to all (online shop). Intranet: staff only (HR portal). Extranet: organisation plus chosen partners (supplier ordering portal).
**3.** Packets share lines among many users, take alternative routes around failures and carry many small order and payment messages efficiently.
**4.** DNS maps names to IP addresses; an IXP is where ISPs exchange traffic directly, reducing delay and cost.
**5.** Client (microbrowser) to WAP gateway to web server, with WAP request and binary WML on the wireless side and HTTP and HTML or WML on the Internet side.
**6.** WAE, WSP, WTP, WTLS, WDP over bearers. WTLS corresponds to SSL/TLS and WDP to UDP.
**7.** The gateway decrypts WTLS and re-encrypts with SSL, so data are readable inside it. WAP 2.0 allows end-to-end TLS between phone and server.
**8.** ADSL: up to 24 Mbps, a few km, home broadband. WiMAX: about 70 Mbps, many km, wireless broadband. 4G: 100 Mbps to 1 Gbps, several km per cell, mobile apps. 5G: up to 20 Gbps, small cells, AR and IoT.
**9.** 250 MB = 2,000 megabits; 2,000 ÷ 20 = **100 seconds**.
**10.** A fake hotspot imitates a real name; users connect and the attacker reads or alters traffic. Defences: HTTPS and a VPN, and checking the network name or using mobile data.
**11.** The attacker receives SMS OTPs and can reset passwords; defence is app-based authentication and operator alerts.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q. Explain the architecture and working of WAP. (5 marks)**

WAP is a client-gateway-server model. The client is a handset with a microbrowser that displays WML decks of cards. The WAP gateway translates between WAP protocols over the wireless link and HTTP on the Internet, and encodes content in compact binary form. The origin server holds the WML or HTML pages. Working: the user requests a page; the microbrowser sends an encoded request to the gateway; the gateway sends an HTTP request to the server; the server returns WML or HTML; the gateway encodes it and sends it to the handset, which displays the first card. The stack is WAE, WSP, WTP, WTLS and WDP over bearers such as SMS or GPRS. Its weakness, the WAP gap, is that the gateway decrypts and re-encrypts data.

**Q. Compare the wireless technologies used in e-commerce and discuss their security issues. (10 marks)**

Begin with the classification by range (WPAN, WLAN, WMAN, WWAN). Give the table of ADSL, Wi-Fi, WiMAX, UMTS, LTE and 5G NR with standard, speed, range and role. Note that real speed is below the theoretical rate. Add the 100 MB download calculation (50 s on 16 Mbps ADSL2+, 20 s on 40 Mbps 4G, 2 s on 400 Mbps 5G) to show the effect of speed on m-commerce. Then discuss threats: eavesdropping, evil twin, weak encryption (WEP, KRACK), man-in-the-middle, jamming and SIM swap, and the WAP gap. Conclude with controls: HTTPS, WPA3, VPN, strong passphrases, separate customer and payment networks, app-based authentication and device protection. A balanced conclusion says that faster wireless networks expand e-commerce but enlarge the attack surface, so every new link needs encryption and authentication from the start.
