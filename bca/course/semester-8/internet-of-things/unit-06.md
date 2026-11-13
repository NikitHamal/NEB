---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 6
title: Securing IoT Systems
hours: 3
area: BCA 454 · Internet of Things · Unit 6
---

On 21 October 2016 many well-known websites became unreachable for hours. The attack came largely from home devices such as cameras and video recorders, taken over because they still used the username and password they had when they left the factory. That botnet, **Mirai**, shows the whole subject of this unit in one story: IoT devices are many, cheap, left unattended and rarely updated, and an attacker needs only one weakness repeated a hundred thousand times. This unit covers the two topics of the outline: **IoT security challenges** and **IoT security practices**.

::: key What this unit gives you
- Why IoT security is harder than ordinary IT security, and the attack surface at each layer.
- Real incidents (Stuxnet, the Target breach, the Jeep Cherokee hack, Mirai) and what they teach.
- The practices: identity, encryption, secure boot, updates, network design, privacy and lifecycle, with standards and a checklist.
- Executable examples: default-password audit, message authentication with replay protection, and signed firmware.
:::

## 6.1 IoT security challenges

**Why IoT is different.**

| Challenge | Explanation | Consequence |
|---|---|---|
| **Constrained resources** | Little memory, CPU and battery; strong cryptography and long keys cost energy | Weak or no encryption; shortcuts |
| **Scale** | Thousands to millions of devices | One flaw is repeated everywhere; manual management is impossible |
| **Heterogeneity** | Many vendors, protocols and operating systems | No single security product; gaps at the joints |
| **Physical exposure** | Devices sit in streets, farms and homes | Theft, tampering, reading keys from the flash chip, debug ports |
| **Long life and no updates** | Meters and machines last 10 to 20 years; vendors may stop support | Known vulnerabilities stay open for years |
| **Weak defaults** | Shared default passwords, open services, hard-coded keys | Mass compromise |
| **Insecure development** | Time-to-market pressure, no security testing | Bugs such as buffer overflows and injection in firmware |
| **Privacy** | Devices record behaviour, voice, video and location | Surveillance and data misuse |
| **Safety link** | Actuators affect the physical world (valves, locks, cars, pumps) | Attacks can injure people or damage plants |
| **Supply chain** | Chips, modules and software come from many sources | Hidden backdoors or vulnerable libraries inherited from suppliers |

**Security goals.** The **CIA triad**: **confidentiality** (only authorised parties read the data), **integrity** (data and commands are not altered), **availability** (the service works when needed). IoT adds **authenticity** (is this really device 7?), **non-repudiation** and **privacy**. In many IoT systems **integrity and availability matter more than confidentiality**: a forged "valve open" command is worse than a leaked temperature.

**The attack surface by layer.**

| Layer | Typical attacks |
|---|---|
| **Device (hardware and firmware)** | Physical tampering, debug-port (UART, JTAG) access, firmware extraction, side channels, fault injection, buffer overflows, hard-coded credentials |
| **Network and communication** | Eavesdropping, man-in-the-middle, replay, spoofing, jamming (radio), rogue gateway, denial of service |
| **Cloud and services** | Weak API authentication, misconfigured storage buckets, injection, account takeover, insecure broker access |
| **Application and user** | Phishing, weak passwords, insecure mobile apps, over-broad permissions |
| **Lifecycle** | Insecure update channel, no revocation of lost devices, no secure disposal of data at end of life |

```svgfig label="6.1" caption="IoT attack surface by layer. Each layer has its own attacks, and an attacker needs to break only one; defence must therefore cover every layer, which is the idea of defence in depth."
f = Fig(640, 270)
layers = [("Application and user", "phishing, weak passwords, app flaws", BLUE, NAVY),
          ("Cloud and services", "API abuse, open buckets, broker access", MINT, TEAL),
          ("Network and communication", "sniffing, replay, spoofing, DoS, jamming", SAND, AMBER),
          ("Device: firmware and hardware", "default passwords, debug ports, extraction", ROSE, RED)]
for i, (name, att, fill, stroke) in enumerate(layers):
    y = 15 + i * 62
    f.box(20, y, 210, 50, name, fill=fill, stroke=stroke, size=11, bold=True)
    f.box(250, y, 370, 50, att, fill=SOFT, stroke=stroke, size=10.5)
    f.arrow([(230, y + 25), (250, y + 25)], color=stroke)
```

## 6.2 Incidents that shaped IoT security

| Incident | What happened | Lesson |
|---|---|---|
| **Stuxnet (discovered 2010)** | Malware aimed at industrial controllers used several unknown vulnerabilities and USB spread to reach a physically isolated plant and damage centrifuges | A network "air gap" is not security; industrial IoT is a target for states |
| **Target breach (2013)** | Attackers stole credentials of a heating and cooling contractor, entered the retailer's network and reached payment systems; tens of millions of card records were stolen | Third-party and building-system devices must be separated from critical networks |
| **Jeep Cherokee (2015)** | Researchers Miller and Valasek took control of a car's brakes, steering and engine remotely through its internet-connected entertainment unit; the maker recalled about 1.4 million vehicles | Connected components need isolation from safety-critical systems and a way to patch |
| **Mirai (2016)** | Malware scanned the Internet for devices with open Telnet and a list of about 60 factory-default username and password pairs, enrolled them in a botnet and launched record denial-of-service attacks, including one against the DNS provider Dyn on 21 October 2016 | Default credentials and exposed services are fatal at scale; the source code was published, producing many copies |
| **Medical devices (various)** | Researchers and regulators have shown flaws in insulin pumps and pacemakers; manufacturers have issued firmware updates and recalls | Safety, regulation and updateability must be planned from the start |

::: note Check dates and figures
The incidents are widely documented; exact counts (cards, vehicles, devices) differ between sources and years, so quote them as "about". Read the original reports for coursework.
:::

## 6.3 Threats in a worked threat model

A **threat model** lists assets, attackers, entry points and counter-measures **before** building. The STRIDE categories help: **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial of service, **E**levation of privilege.

| Asset or flow | STRIDE example | Counter-measure |
|---|---|---|
| Sensor reading on the way to the cloud | **T**ampering: an attacker changes 28 to 8 degrees | Message authentication (HMAC) or TLS |
| Device identity | **S**poofing: a fake node sends data as `ktm-07` | Per-device key or certificate |
| Valve command | **S**poofing and replay: an old "open" is sent again | Authentication plus nonce or timestamp |
| Camera stream | **I**nformation disclosure: stream is open on the network | Encryption, authentication, no default password |
| Gateway | **D**enial of service: flood of connections | Rate limits, firewall, redundancy |
| Firmware update | **E**levation of privilege: malicious update installed | Signed firmware and secure boot |
| Action log | **R**epudiation: operator denies sending the command | Signed, append-only logs |

```python
# Default-credential audit: the first line of defence against Mirai-style attacks
FACTORY_DEFAULTS = {("admin", "admin"), ("admin", "1234"), ("root", "root"), ("root", "12345"),
                    ("admin", "password"), ("user", "user"), ("admin", ""), ("support", "support")}
inventory = [("cam-01", "admin", "admin"), ("cam-02", "admin", "T7!pQ2x9vLm"), ("plug-07", "root", "12345"),
             ("hub-03", "admin", "password"), ("meter-11", "operator", "n3p@l-2082-Kx")]
weak = []
for device, user, pw in inventory:
    problems = []
    if (user, pw) in FACTORY_DEFAULTS: problems.append("factory default")
    if len(pw) < 10: problems.append("shorter than 10 characters")
    if problems: weak.append(device)
    print("%-9s %-8s %s" % (device, user, "; ".join(problems) if problems else "ok"))
print("devices to fix today:", weak)
space = 62 ** 8
print("8 random characters (62 symbols): %.2e guesses; at 10^9 guesses/s: %.1f hours" % (space, space / 1e9 / 3600))
```
```output
cam-01    admin    factory default; shorter than 10 characters
cam-02    admin    ok
plug-07   root     factory default; shorter than 10 characters
hub-03    admin    factory default; shorter than 10 characters
meter-11  operator ok
devices to fix today: ['cam-01', 'plug-07', 'hub-03']
8 random characters (62 symbols): 2.18e+14 guesses; at 10^9 guesses/s: 60.7 hours
```

## 6.4 IoT security practices

**1. Device identity and authentication.** Give **every device a unique identity and credential**: a random per-device secret or, better, an **X.509 certificate** with its private key stored in a **secure element** or trusted platform module (a small tamper-resistant chip) so that it cannot be copied. Authenticate both ways: the device checks the server (certificate) and the server checks the device. Use **no shared or default passwords**; force a change at first use or ship a unique random password on the label.

**2. Encrypt data in transit.** Use **TLS** (for TCP: HTTPS, MQTT on port 8883) or **DTLS** (for UDP: CoAP over DTLS) with current versions (TLS 1.2 or 1.3), check the server certificate, and never disable verification "to make it work". For links with very small payloads, use **message-level authentication** (HMAC or authenticated encryption such as AES-GCM or ChaCha20-Poly1305). Wireless protocols have their own security (Wi-Fi WPA2 or WPA3, BLE pairing, Zigbee network keys, LoRaWAN session keys); enable it and do not leave test keys. Encrypt **data at rest** where sensitive.

**3. Protect integrity and prevent replay.** An attacker who records "open valve" and sends it later should fail. Add a **timestamp** or **counter** and a **nonce** (number used once), and authenticate the whole message with an **HMAC**: $\text{tag}=\text{HMAC}_K(\text{message})$. The receiver recomputes the tag, compares in constant time, and rejects old or repeated counters.

**4. Secure boot and signed firmware.** At power-up the ROM code verifies the **digital signature** of the bootloader, which verifies the firmware, so only code signed by the manufacturer runs (a chain of trust). Updates are delivered **over the air (OTA)** as signed images; the device checks the signature and a **version number** (to refuse **rollback** to an old, vulnerable version) before installing, and keeps the previous image so that a failed update can **roll back safely**. Without a safe update path every other practice decays over time.

**5. Harden the device.** Disable unused services and ports (especially Telnet and debug interfaces), close or lock UART and JTAG on production units, remove default accounts, use the **principle of least privilege** for software, use memory-safe practices and update third-party libraries, and store secrets in protected storage, never in the source code.

**6. Secure the network.** **Segment** IoT devices from business and payment networks (VLANs, a separate Wi-Fi network at home), use a firewall that allows only the destinations a device needs (**deny by default**), monitor flows for deviations (Section 4.5), and put brokers behind authentication with **per-device topic permissions** (device 7 may publish only to `farm/7/#`). Do not expose devices directly to the Internet; use outbound connections to a broker or a VPN for remote access.

**7. Secure the cloud and the application.** Strong authentication for users (**multi-factor**), role-based access, API keys that can be revoked, input validation, rate limiting, private storage buckets, audit logs and backups. Rotate and revoke credentials: a lost or stolen device must be removable from the registry at once.

**8. Privacy by design.** Collect only the data needed (**data minimisation**), process locally when possible (send "3 people" not the video), tell users what is collected, let them delete it, keep it only as long as necessary, and comply with the privacy law that applies, such as Nepal's Privacy Act 2075 (2018) and, for foreign users, the EU GDPR.

**9. Manage the whole lifecycle.** Secure design and testing (threat model, code review, penetration test), secure manufacturing and provisioning of keys, an update commitment and a **vulnerability disclosure policy**, monitoring in operation, and at end of life wipe the data and revoke the identity.

| Practice | Threats it answers |
|---|---|
| Unique identity and certificates | Spoofing, unauthorised devices |
| TLS/DTLS and HMAC | Eavesdropping, tampering, man-in-the-middle |
| Nonce, timestamp, counter | Replay |
| Secure boot, signed OTA updates | Malicious firmware, long-lived vulnerabilities |
| Hardening, closed debug ports | Physical and local attacks |
| Segmentation, deny-by-default, flow monitoring | Lateral movement, botnet scanning, DoS |
| MFA, RBAC, revocation in the cloud | Account takeover, stolen devices |
| Minimisation and local processing | Privacy loss |

**Standards and guidance.** **OWASP IoT Top 10** (2018 edition: weak or hard-coded passwords is number 1, followed by insecure network services, insecure ecosystem interfaces, no secure update mechanism, outdated components, insufficient privacy, insecure data transfer and storage, poor device management, insecure default settings, lack of physical hardening). **ETSI EN 303 645** (a baseline for consumer IoT: no universal default passwords, a vulnerability disclosure policy, keep software updated, store credentials securely, communicate securely, minimise attack surfaces, protect personal data). **NIST IR 8259** (device cybersecurity capabilities for manufacturers) and **IEC 62443** (industrial control systems). Some countries have turned such baselines into law, for example the UK's product security regime in force since April 2024 bans universal default passwords; check the current text of any law you cite.

```python
import hmac, hashlib, json, time
SECRET = b"per-device-secret-ktm-07"                 # in a real device this lives in a secure element

def make_message(counter, reading, key=SECRET):
    body = json.dumps({"node": "ktm-07", "counter": counter, "ts": 1_700_000_000 + counter, "temp": reading}, sort_keys=True)
    tag = hmac.new(key, body.encode(), hashlib.sha256).hexdigest()
    return body, tag

class Receiver:
    def __init__(self, key): self.key, self.last_counter = key, 0
    def accept(self, body, tag):
        expected = hmac.new(self.key, body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, tag): return "REJECT: bad tag (tampered or wrong key)"
        counter = json.loads(body)["counter"]
        if counter <= self.last_counter: return "REJECT: replay (counter %d <= %d)" % (counter, self.last_counter)
        self.last_counter = counter
        return "accept counter %d" % counter

rx = Receiver(SECRET)
body, tag = make_message(1, 18.4)
print("1:", rx.accept(body, tag))
print("2 replay of the same message:", rx.accept(body, tag))
forged = body.replace("18.4", "-8.0")
print("3 tampered reading:", rx.accept(forged, tag))
body2, tag2 = make_message(2, 18.9)
print("4 next genuine message:", rx.accept(body2, tag2))
print("5 attacker without the key:", rx.accept(*make_message(3, 99.0, key=b"guess")))
print("tag length: %d hex characters = %d bits" % (len(tag), 4 * len(tag)))
```
```output
1: accept counter 1
2 replay of the same message: REJECT: replay (counter 1 <= 1)
3 tampered reading: REJECT: bad tag (tampered or wrong key)
4 next genuine message: accept counter 2
5 attacker without the key: REJECT: bad tag (tampered or wrong key)
tag length: 64 hex characters = 256 bits
```
```svgfig label="6.2" caption="Secure over-the-air update. The device downloads an image and its signature, checks the signature and that the version is newer, installs into the spare slot, reboots into it and confirms; if the check or the boot fails it keeps the old image."
f = Fig(640, 232)
f.box(10, 80, 100, 50, "Update server\nsigned image\n+ version", fill=SAND, stroke=AMBER, size=9.5)
f.box(150, 80, 100, 50, "Download over\nTLS", fill=BLUE, stroke=NAVY, size=10)
f.box(290, 20, 120, 50, "Signature valid?\nversion newer?", fill=ROSE, stroke=RED, size=10)
f.box(290, 140, 120, 50, "Write to spare\nslot B", fill=BLUE, stroke=NAVY, size=10)
f.box(450, 140, 90, 50, "Reboot into B\nself-test", fill=BLUE, stroke=NAVY, size=10)
f.box(560, 80, 70, 50, "Confirm\nB is active", fill=MINT, stroke=TEAL, size=10)
f.box(450, 20, 180, 40, "Reject: keep running slot A", fill=ROSE, stroke=RED, size=10)
f.arrow([(110, 105), (150, 105)], color=NAVY)
f.arrow([(250, 100), (290, 55)], color=NAVY)
f.arrow([(350, 70), (350, 140)], color=TEAL, label="yes", lpos=(370, 105))
f.arrow([(410, 40), (450, 40)], color=RED, label="no", lpos=(430, 32))
f.arrow([(410, 165), (450, 165)], color=NAVY)
f.arrow([(540, 160), (590, 130)], color=TEAL, label="ok", lpos=(575, 158))
f.arrow([(495, 190), (495, 222), (60, 222), (60, 130)], color=RED, dash=True, label="boot fails: roll back to A", lpos=(280, 212))
```

## 6.5 Verifying firmware before installing it

A signed update has two checks: the **hash** (is the image the one that was signed?) and the **signature** (did the manufacturer sign that hash?). Real devices verify an asymmetric signature (RSA or Ed25519) with a public key burned into the device, so the key cannot be used to forge updates. The program uses the standard library only, so it stands in for the signature with an HMAC; the logic of version and hash checks, rollback protection and the spare slot is the same.

```python
import hashlib, hmac
VENDOR_KEY = b"vendor-signing-key (stand-in for a private key; devices would hold only a public key)"

def sign(image: bytes, version: int):
    digest = hashlib.sha256(image).digest()
    return {"version": version, "sha256": digest.hex(), "sig": hmac.new(VENDOR_KEY, digest + bytes([version]), hashlib.sha256).hexdigest()}

class Device:
    def __init__(self): self.slot, self.version = "A", 3
    def install(self, image, manifest):
        digest = hashlib.sha256(image).digest()
        if digest.hex() != manifest["sha256"]: return "REJECT: image does not match its hash (corrupted or altered)"
        good = hmac.new(VENDOR_KEY, digest + bytes([manifest["version"]]), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(good, manifest["sig"]): return "REJECT: bad signature"
        if manifest["version"] <= self.version: return "REJECT: rollback (version %d is not newer than %d)" % (manifest["version"], self.version)
        self.slot, self.version = ("B" if self.slot == "A" else "A"), manifest["version"]
        return "installed version %d into the spare slot, now running slot %s" % (self.version, self.slot)

image4 = b"firmware v4: fix telnet service" * 20
dev = Device()
print("genuine v4       :", dev.install(image4, sign(image4, 4)))
print("altered image    :", Device().install(image4 + b"backdoor", sign(image4, 4)))
forged = dict(sign(image4, 4)); forged["sig"] = "00" * 32
print("forged signature :", Device().install(image4, forged))
old = b"firmware v2 (has a known flaw)" * 20
print("old version      :", dev.install(old, sign(old, 2)))
```
```output
genuine v4       : installed version 4 into the spare slot, now running slot B
altered image    : REJECT: image does not match its hash (corrupted or altered)
forged signature : REJECT: bad signature
old version      : REJECT: rollback (version 2 is not newer than 4)
```
## 6.6 Case study: securing a smart-farm system

Take the level 2 irrigation system of Unit 1 (soil probes, a gateway with a pump relay, cloud history and a phone app) and apply the unit.

| Step | Finding | Action |
|---|---|---|
| Assets | Pump control, farm data, owner's phone number | Rank the pump first: wrong actions cause crop loss and flooding |
| Entry points | Wi-Fi to the gateway, cloud API, phone app, USB and serial ports, firmware updates | List each; remove what is not needed |
| Identity | One shared password for all gateways | One certificate per gateway, stored in a secure element; revoke on loss |
| Transport | Plain HTTP between gateway and cloud | MQTT over TLS on port 8883, certificate checked |
| Commands | Pump command is a plain message | HMAC plus counter; the gateway also enforces a safe local limit (never more than 2 hours a day) whatever the cloud says |
| Updates | USB stick by hand | Signed OTA with rollback protection |
| Network | Gateway and the owner's laptop on the same Wi-Fi | Separate IoT network; firewall allows only the broker address |
| Privacy | Location of the farm and the phone number are stored | Minimise, encrypt, allow deletion |
| Operations | No logs | Signed log of every pump command; alert if the gateway goes offline (last will) |

The fail-safe rule in the commands row is a general **safety principle**: the device should keep a local limit that no remote message can exceed, so that a compromised cloud account cannot flood the field.

## 6.7 Summary and exercises

IoT is hard to secure because devices are constrained, numerous, diverse, exposed, long-lived and often shipped with weak defaults, while their actions affect the physical world. Attacks occur at the device, network, cloud, application and lifecycle layers (Stuxnet, Target, Jeep and Mirai illustrate this). The practices are unique identity, encryption (TLS, DTLS, HMAC), replay protection, secure boot and signed OTA updates, hardening, segmentation and monitoring, strong cloud access control, privacy by design and lifecycle management; standards (OWASP IoT Top 10, ETSI EN 303 645, NIST IR 8259) give checklists.

1. List six reasons why IoT security is harder than ordinary IT security.
2. Explain the CIA triad and why integrity and availability can matter more than confidentiality in IoT.
3. Describe the attack surface of an IoT system layer by layer.
4. Explain how the Mirai botnet worked and which three practices would have stopped it.
5. What is STRIDE? Apply it to a smart door lock.
6. Explain replay attacks and how a nonce, a counter or a timestamp with an HMAC prevents them.
7. Explain secure boot and signed OTA updates. Why is rollback protection needed?
8. Why is TLS verification of the server certificate essential? What goes wrong if it is disabled?
9. Explain network segmentation and deny-by-default for IoT. Give an example rule set for a camera.
10. State five principles of privacy by design for IoT with an example each.
11. An 8-character password uses 62 symbols. How many combinations are there? How long at $10^{9}$ guesses per second? What changes with 12 characters?
12. Prepare a security checklist for a smart-home hub, using the OWASP IoT Top 10 as a guide.

**Answers to the numerical items.** (11) $62^8=2.18\times10^{14}$ combinations; $2.18\times10^{14}/10^{9}=2.18\times10^{5}$ s $=60.7$ hours (the average attacker finds it in half that time). For 12 characters, $62^{12}=3.2\times10^{21}$, which at $10^{9}$ guesses per second is about $3.2\times10^{12}$ s, more than 100,000 years: length matters more than complexity. The real risk is **default and reused** passwords, which are guessed in the first few tries, whatever their length.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the main security challenges of IoT.**

Devices are constrained in memory, CPU and battery, so strong cryptography is skipped. They are deployed at huge scale and from many vendors, so management and uniform protection are hard. They sit in exposed places, so physical tampering and debug ports are a threat. They live 10 to 20 years but are rarely updated, leaving known flaws open. Weak defaults (shared passwords, open Telnet) allow mass compromise, as Mirai showed. Devices collect personal data, so privacy is at risk, and because actuators affect the physical world, attacks can cause physical harm.

**Q2 (5 marks). Explain replay protection with an example.**

A replay attack records a valid message and sends it again later: for example a captured "open valve" command. Protection: include a **counter** or **timestamp** and a **nonce**, and authenticate the whole message with an HMAC key shared by the device and the server. The receiver recomputes the HMAC (comparing in constant time), then rejects a message whose counter is not greater than the last accepted one. In the demonstration, message 1 is accepted, the same message sent again is rejected as a replay, a message with the reading changed from 18.4 to -8.0 fails the tag check, and the next genuine message with counter 2 is accepted.

**Q3 (10 marks). Describe the IoT security practices.**

*Introduction.* Because one weakness is multiplied across many devices, security must be built into the design, the deployment and the operation.

*Practices.* (1) Unique device identity (certificate in a secure element), no default passwords. (2) Encryption in transit with TLS or DTLS, with certificate checks, and HMAC or AEAD at message level for tiny payloads. (3) Replay protection by counters and nonces. (4) Secure boot and signed OTA updates with version checks and rollback. (5) Hardening: close debug ports and unused services, least privilege. (6) Network segmentation, deny-by-default firewalls, flow monitoring and per-device broker permissions. (7) Strong user authentication, role-based access and revocation in the cloud. (8) Privacy by design: minimise, process locally, allow deletion. (9) Lifecycle: threat model, testing, vulnerability disclosure, secure disposal.

*Example.* For the smart farm, each gateway has its own certificate, uses MQTT over TLS, signs pump commands, enforces a local two-hours-a-day limit and accepts only signed updates.

*Standards.* OWASP IoT Top 10, ETSI EN 303 645 and NIST IR 8259 provide checklists.

*Conclusion.* No single measure is enough; layered defences make an attack costly and limit the damage when one layer fails.

**Q4 (10 marks). Discuss the security challenges of IoT with reference to real attacks and the counter-measures.**

*Introduction.* IoT devices combine weak resources, scale and physical consequences, so they attract attackers.

*Challenges.* Constrained resources, scale, heterogeneity, exposure, long life without updates, weak defaults, insecure development, privacy, safety link and supply chain (Section 6.1).

*Attacks.* Stuxnet showed that isolated industrial networks can be reached and physical equipment damaged; the Target breach showed that a building-systems contractor's credentials led to payment systems; the Jeep Cherokee showed remote control of a car through an entertainment unit and led to a recall of about 1.4 million vehicles; Mirai in 2016 used about 60 default credentials over Telnet to enrol devices and attacked the DNS provider Dyn.

*Counter-measures.* Unique credentials and no defaults (stops Mirai), segmentation of contractor and building systems from critical networks (Target), isolation of safety systems and the ability to patch (Jeep), secure boot and signed updates (Stuxnet-style code injection), encryption and authentication of all messages, monitoring of flows for scanning behaviour.

*Conclusion.* The same few weaknesses, default passwords, exposed services, flat networks and no updates, caused all the incidents, so basic hygiene prevents most of the harm; the standards turn this into a checklist.
