---
subject: Cloud Computing
grade: BCA Semester 8
unit: 6
title: Cloud Security, IAM Evaluation and Envelope Encryption
hours: 6
area: BCA 451 · Cloud Computing · Unit 6
---

Moving to the cloud moves the data centre's locks and guards to the provider, but it does not move the responsibility for who is allowed in. Most real cloud incidents are not failures of the provider's hardware; they are misconfigurations on the customer's side: a storage bucket left open, an access key with far too many permissions, a database without encryption. This unit sets out who is responsible for what, how access decisions are made, how data keys are protected, and the Zero Trust mindset that ties them together.

::: key What this unit gives you
- The shared responsibility model for IaaS, PaaS and SaaS.
- Identity and Access Management: principals, policies, roles and the policy evaluation logic (explicit deny, allow, implicit deny).
- Encryption at rest and in transit, key management, and envelope encryption with DEKs and KEKs.
- Zero Trust architecture and defensive monitoring.
:::

## 6.1 Shared responsibility

The provider is responsible for the security **of** the cloud: facilities, hardware, the hypervisor and the foundational services. The customer is responsible for security **in** the cloud: identities, data, configuration and, depending on the service model, the operating system and application. The line moves as you climb the stack:

| Responsibility | IaaS | PaaS | SaaS |
|---|---|---|---|
| Physical data centre, hardware, network fabric | Provider | Provider | Provider |
| Hypervisor and virtualization | Provider | Provider | Provider |
| Operating system patching | **Customer** | Provider | Provider |
| Runtime and middleware | **Customer** | Provider | Provider |
| Application code and its security | **Customer** | **Customer** | Provider |
| Network controls (firewall rules, subnets) | **Customer** | **Customer** (limited) | Provider |
| Identity and access management, MFA | **Customer** | **Customer** | **Customer** |
| Data classification, encryption choices, backups | **Customer** | **Customer** | **Customer** |

::: caution
Two rows never move to the provider: **identity** and **data**. Even in SaaS the customer decides who has accounts, enforces multi-factor authentication and chooses what data to put there.
:::

## 6.2 Identity and Access Management

**IAM** controls *who* (a principal) can do *what* (an action) on *which* resource, under *which* conditions. Principals are users, groups, services and **roles**, which are identities assumed temporarily with short-lived credentials instead of long-lived keys. Good practice: the **principle of least privilege**, MFA for every human, no shared root-account use, short-lived credentials for workloads, and periodic access review.

A **policy** is a set of statements, each with an effect (Allow or Deny), a list of actions, a list of resources and optional conditions (source network, time, MFA present). When a request arrives, the cloud's policy engine evaluates all applicable statements in a fixed logic:

::: key Policy evaluation logic
1. By default every request is **denied** (implicit deny).
2. An applicable **Allow** overrides the default.
3. An applicable **explicit Deny** overrides every Allow, no matter where the Allow comes from.

On major platforms further layers (organisation-wide guardrails, permission boundaries, session policies) can only *restrict* what identity policies grant; they never add permissions.
:::

The evaluator below implements this logic with wildcard matching for a small policy: allow reading and writing objects under `reports/`, but explicitly deny everything under `reports/secret/`.

```python
import fnmatch
policy = [("Allow", "s3:GetObject", "arn:bucket/reports/*"),
          ("Allow", "s3:PutObject", "arn:bucket/reports/*"),
          ("Deny", "s3:*", "arn:bucket/reports/secret/*")]

def evaluate(action, resource):
    effects = [e for e, a, r in policy
               if fnmatch.fnmatchcase(action, a) and fnmatch.fnmatchcase(resource, r)]
    if "Deny" in effects:
        return "DENY (explicit)"
    if "Allow" in effects:
        return "ALLOW"
    return "DENY (implicit)"

requests = [("s3:GetObject", "arn:bucket/reports/q1.csv"),
            ("s3:GetObject", "arn:bucket/reports/secret/key.txt"),
            ("s3:DeleteObject", "arn:bucket/reports/q1.csv"),
            ("s3:PutObject", "arn:bucket/other/x.txt")]
for action, resource in requests:
    print(f"{action} {resource} -> {evaluate(action, resource)}")
```
```output
s3:GetObject arn:bucket/reports/q1.csv -> ALLOW
s3:GetObject arn:bucket/reports/secret/key.txt -> DENY (explicit)
s3:DeleteObject arn:bucket/reports/q1.csv -> DENY (implicit)
s3:PutObject arn:bucket/other/x.txt -> DENY (implicit)
```
The second request matches *both* an Allow (`reports/*`) and the Deny (`reports/secret/*`), and the explicit deny wins. The third and fourth requests match no statement and are refused by default. The order of statements never matters: the engine collects every match and applies precedence.

::: note
Wildcards like `s3:*` on `*` are convenient in a lab and dangerous in production. Review tools that analyse policies for unintended public or cross-account access are a standard control.
:::

## 6.3 Data protection and key management

**Encryption in transit** uses TLS (covered in the Cryptography and Network Security course); **encryption at rest** protects stored data, typically AES-256. Encryption only moves the problem to the key, so keys need their own protection and lifecycle. A **Key Management Service (KMS)** creates and stores master keys in hardware security modules (HSMs), never exposes them in plaintext and logs every use. Customers choose provider-managed keys, customer-managed keys (CMK) with their own rotation and access policy, or customer-supplied keys.

### Envelope encryption

Encrypting large data directly with a master key would mean sending it to the KMS and would make key rotation a massive re-encryption. **Envelope encryption** uses two layers:

1. A **data encryption key (DEK)** is generated locally for each object or volume and encrypts the data with an authenticated cipher such as AES-GCM.
2. A **key encryption key (KEK)**, held in the KMS, encrypts (*wraps*) the DEK. The wrapped DEK is stored beside the ciphertext.

To read, the application sends the wrapped DEK to the KMS, which unwraps it only if the caller's IAM policy allows, and then decrypts the data locally. Rotating the KEK needs only the small wrapped DEKs to be re-wrapped, not the data.

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

kek = AESGCM.generate_key(bit_length=256)
dek = AESGCM.generate_key(bit_length=256)
message = b"patient record: confidential"
nonce = os.urandom(12)
ciphertext = nonce + AESGCM(dek).encrypt(nonce, message, b"obj-1")
wrap_nonce = os.urandom(12)
wrapped = wrap_nonce + AESGCM(kek).encrypt(wrap_nonce, dek, b"dek")

dek_again = AESGCM(kek).decrypt(wrapped[:12], wrapped[12:], b"dek")
plain = AESGCM(dek_again).decrypt(ciphertext[:12], ciphertext[12:], b"obj-1")
print(f"round trip ok: {plain == message}")
damaged = bytearray(ciphertext)
damaged[-1] ^= 1
try:
    AESGCM(dek_again).decrypt(bytes(damaged[:12]), bytes(damaged[12:]), b"obj-1")
    rejected = False
except InvalidTag:
    rejected = True
print(f"tampered ciphertext rejected: {rejected}")
print(f"wrapped DEK length: {len(wrapped)} bytes")
objects, avg_size = 10_000_000, 10**6
print(f"rewrap {objects * len(wrapped)} bytes versus re-encrypt {objects * avg_size} bytes (ratio {avg_size / len(wrapped):.1f})")
```
```output
round trip ok: True
tampered ciphertext rejected: True
wrapped DEK length: 60 bytes
rewrap 600000000 bytes versus re-encrypt 10000000000000 bytes (ratio 16666.7)
```
The wrapped DEK is 60 bytes: a 12-byte nonce, the 32-byte key and a 16-byte authentication tag. The authentication tag also explains the third line: changing one bit of the stored ciphertext makes decryption fail instead of returning garbage. For 10 million objects of 1 MB, rotating the KEK re-wraps only 600 MB of key material rather than re-encrypting 10 TB of data, a ratio of about 16,667 to one. The program prints no key material; real systems never log keys.

## 6.4 Zero Trust

The traditional **perimeter** model trusted anything inside the corporate network. Cloud, remote work and SaaS dissolved that perimeter. **Zero Trust** (NIST SP 800-207) assumes no implicit trust from network location. Its core ideas:

- **Verify explicitly:** authenticate and authorise every request using identity, device health, location and risk signals.
- **Least privilege and just-in-time access:** narrow, time-limited rights.
- **Assume breach:** segment the network (microsegmentation), encrypt internal traffic (mutual TLS between services), and monitor everything.
- A **policy decision point** evaluates each request and a **policy enforcement point** (proxy or gateway) applies the decision.

## 6.5 Defensive monitoring and compliance

Turn on audit logging for every account (who called which API, from where), send logs to a separate, write-protected account, and alert on high-risk events such as root-user logins, policy changes and disabled logging. **Cloud Security Posture Management (CSPM)** tools continuously compare configuration against benchmarks (public storage, unencrypted volumes, open administrative ports). Compliance frameworks (ISO/IEC 27001, SOC 2, PCI DSS) require evidence of these controls. In Nepal, the Electronic Transactions Act 2063 and the Individual Privacy Act 2075 set baseline duties for handling electronic records and personal data; regulated sectors add directives from Nepal Rastra Bank and others.

## 6.6 Seeing the ideas: shared responsibility, policy evaluation and envelope encryption

Cloud security is a mix of physical protection that the provider owns and logical controls that the customer must configure. Plate 6.1 shows the two ends: a lock, the oldest access-control device, and a hardware security module that guards the keys at the root of the cloud's encryption.

```photogrid label="6.1" cols="2" ratio="1.4" caption="Two faces of access control. (a) A padlock: something that opens only for the holder of the right key, the idea behind every IAM policy. (b) An nCipher hardware security module on a PCIe card: a tamper-resistant device that generates and holds master keys and never lets them leave in plain form; cloud key-management services keep their root keys in such devices."
@ photo id="bca306/padlock" cap="Padlock: access only with the right key"
fit 1.4
focus 0.5 0.5
@ photo id="bca451/hsm" cap="Hardware security module (HSM)"
fit 1.4
focus 0.5 0.5
```

```svgfig label="6.1" caption="The shared responsibility model. The provider always secures the cloud itself (buildings, hardware, hypervisor); the customer always secures their data, identities and access. The boundary moves up the stack as you go from IaaS to PaaS to SaaS, but the customer never hands over responsibility for data and access."
f = Fig(580, 232)
rows = ["Data and access (IAM)", "Application code", "Operating system and patches", "Network configuration", "Hypervisor and hardware", "Buildings, power, network"]
cols = [("IaaS", 4), ("PaaS", 2), ("SaaS", 1)]
f.box(8, 8, 210, 22, "Layer", fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
for j, (n, k) in enumerate(cols):
    x = 226 + j * 118
    f.box(x, 8, 110, 22, n, fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
    for i in range(6):
        mine = i < k
        f.box(x, 34 + i * 28, 110, 24, "Customer" if mine else "Provider", fill=MINT if mine else "#e2e8f0", stroke=TEAL if mine else SLATE, size=9.5)
for i, t in enumerate(rows):
    f.box(8, 34 + i * 28, 210, 24, t, fill=BLUE, stroke=NAVY, size=9.5)
f.text(290, 216, "Provider: security OF the cloud | Customer: security IN the cloud", size=10.5, color=NAVY, bold=True)
```

```svgfig label="6.2" caption="IAM policy evaluation. Every request starts denied. An explicit Deny anywhere wins immediately; otherwise an applicable Allow grants access; if no statement matches, the implicit deny stands."
f = Fig(580, 150)
f.box(8, 52, 90, 44, "Request\n(who, what,\nwhich resource)", fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(130, 52, 110, 44, "Any explicit\nDeny matches?", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(280, 52, 110, 44, "Any Allow\nmatches?", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(430, 52, 140, 44, "ALLOW", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(130, 112, 110, 30, "DENY", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(280, 112, 110, 30, "DENY (implicit)", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(98, 74), (130, 74)])
f.arrow([(240, 74), (280, 74)], label="no", lpos=(260, 64))
f.arrow([(390, 74), (430, 74)], label="yes", lpos=(410, 64))
f.arrow([(185, 96), (185, 112)], color=RED, label="yes", lpos=(203, 106))
f.arrow([(335, 96), (335, 112)], color=RED, label="no", lpos=(351, 106))
f.text(495, 124, "guardrails and permission\nboundaries only restrict", size=9, color=SLATE)
```

```svgfig label="6.3" caption="Envelope encryption. Each object is encrypted with its own data key (DEK). The DEK is encrypted (wrapped) by a master key (KEK) that stays inside the key-management service or HSM. Rotating the master key means re-wrapping the small DEKs, not re-encrypting the data: 10,000,000 wrapped keys of 60 bytes (600 MB) instead of 10 TB."
f = Fig(580, 190)
f.box(10, 20, 100, 40, "Plaintext\nobject", fill=SAND, stroke=AMBER, bold=True, size=10)
f.box(160, 20, 110, 40, "Encrypt with\nDEK (AES-GCM)", fill=BLUE, stroke=NAVY, bold=True, size=10)
f.box(320, 20, 110, 40, "Ciphertext\nobject", fill=MINT, stroke=TEAL, bold=True, size=10)
f.arrow([(110, 40), (160, 40)]); f.arrow([(270, 40), (320, 40)])
f.box(160, 100, 110, 40, "DEK (random,\nper object)", fill=ROSE, stroke=RED, bold=True, size=10)
f.arrow([(215, 100), (215, 60)])
f.box(320, 100, 110, 40, "KEK in KMS / HSM\n(never leaves)", fill=SAND, stroke=AMBER, bold=True, size=9.5)
f.arrow([(270, 120), (320, 120)], label="wrap", lpos=(295, 110))
f.box(470, 100, 100, 40, "Wrapped DEK\n(60 B), stored\nbeside object", fill=MINT, stroke=TEAL, size=9, bold=True)
f.arrow([(430, 120), (470, 120)])
f.text(290, 170, "Rotate KEK: re-wrap 600 MB of keys, not re-encrypt 10 TB (ratio 16,667)", size=10.5, color=TEAL, bold=True)
```

### 6.6.1 Eight good practices for cloud security

1. **Protect the root account.** Use the root login only for setup, turn on multi-factor authentication and lock the credentials away. A single stolen root password can cost a company its whole cloud bill and data. Create named users and roles for daily work.
2. **Grant least privilege.** Give each person or service only the actions and resources it needs. A developer who reads logs does not need permission to delete databases. Review permissions regularly and remove the unused ones.
3. **Use roles and short-lived credentials.** Roles give temporary keys that expire in hours. Long-lived access keys leak into code and chat messages. A leaked temporary key stops working soon, which limits the damage.
4. **Encrypt data at rest and in transit.** Turn on disk and bucket encryption and use HTTPS everywhere. Keep keys in a key-management service and rotate them. Encrypted data that is stolen is useless without the key.
5. **Keep resources private by default.** Place databases in private subnets and close storage buckets to the public. Many breaches are simply public buckets with customer files. Open only what must be open and check it regularly.
6. **Log and monitor everything.** Record every API call and network flow in a protected log store and alert on unusual events, such as a login from a new country. In an incident, the logs show who did what and when. Without logs the team is blind.
7. **Patch and scan.** Update operating systems and containers, and scan images and code for known weaknesses. Most attacks use bugs that already have a fix. Automation makes patching routine instead of rare.
8. **Back up and practise recovery.** Keep copies in another account or region that cannot be deleted from the main account. Test the restore, because an untested backup is only a hope. This protects against mistakes, fire, and ransomware.

## 6.7 Summary and exercises

Security in the cloud is shared, with identity and data always the customer's; IAM decisions follow implicit deny, allow, explicit deny precedence; envelope encryption separates fast data keys from guarded master keys so rotation is cheap; Zero Trust replaces location-based trust with continuous verification.

1. Draw the responsibility split for an IaaS virtual machine and a SaaS email service.
2. State the IAM evaluation order and explain why order of statements does not matter.
3. Add a statement to the policy in this unit that allows `s3:ListBucket` on the bucket only, and predict the result for listing `reports/secret/`.
4. Explain DEK, KEK, wrapping and why rotation is cheap under envelope encryption.
5. Why does AES-GCM tamper detection matter for stored backups?
6. List four Zero Trust principles and one way to implement each.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the shared responsibility model in cloud security.**

*Introduction.* In the cloud, security is divided between the provider and the customer. The provider is responsible for **security of the cloud**; the customer for **security in the cloud** (Figure 6.1).

*Provider.* Physical data centres, power, network, hardware, the hypervisor and the managed services' own software. *Customer.* Their data, user identities and permissions, application code, and, depending on the model, the operating system and network settings.

| Model | Provider also manages | Customer still manages |
|---|---|---|
| IaaS | Hardware, hypervisor | OS, patches, firewall rules, apps, data, IAM |
| PaaS | Plus OS and runtime | Application, data, IAM |
| SaaS | Plus the application | Data, user accounts, sharing settings |

*Example.* If a Nepali firm leaves a storage bucket public, the provider is not at fault: configuration is the customer's job. *Conclusion:* moving to SaaS reduces the tasks but never removes responsibility for data and access.

**Q2 (5 marks). Explain how IAM decides whether a request is allowed. State the evaluation logic.**

**Identity and Access Management (IAM)** controls who (a principal: user, group, service or role) may do what (action) on which resource, under which conditions (source network, time, MFA). Permissions are written as **policies**, each statement having an effect (Allow or Deny), actions, resources and conditions.

*Evaluation (Figure 6.2).* (1) Every request is denied by default (implicit deny). (2) An applicable Allow overrides the default. (3) An explicit Deny overrides every Allow, whatever its source. Guardrails such as organisation policies and permission boundaries can only restrict, never add, permissions.

*Example.* A role allows s3:GetObject on a bucket but a service control policy explicitly denies access from outside Nepal; a request from abroad is denied. *Best practice:* least privilege, roles instead of permanent keys, MFA and regular review. *Conclusion:* the deny-first logic makes safe defaults and lets administrators add strict guardrails.

**Q3 (5 marks). What is envelope encryption? Why is it used in cloud key management?**

Envelope encryption uses two levels of keys (Figure 6.3). A fresh random **data encryption key (DEK)** encrypts each object with a fast cipher such as AES-GCM. The DEK is then encrypted (**wrapped**) with a **key encryption key (KEK)** that stays inside a key-management service or hardware security module (Plate 6.1) and never leaves it in plain form. The wrapped DEK is stored next to the ciphertext; to read the object, the service unwraps the DEK and decrypts.

*Why:* (1) the big master key never touches the data, so there is less exposure; (2) bulk encryption happens locally and fast, and only 60-byte keys travel to the KMS; (3) **rotation is cheap**: for 10 TB of data in 10 million objects the wrapped keys total 600 MB, so rotating the KEK re-wraps 600 MB instead of re-encrypting 10 TB (16,667 times less); (4) each object has its own key, so one leak exposes one object; (5) the KMS logs every use. *Conclusion:* envelope encryption gives strong, auditable, cheaply rotated protection at cloud scale.

**Q4 (10 marks). Discuss security in cloud computing. Explain the main threats, the shared responsibility model, identity management, data protection and the Zero Trust approach.**

*Introduction.* Cloud security protects data, applications and infrastructure that run on shared, internet-reachable services. It differs from a private data centre because resources are created in minutes through APIs, so mistakes spread quickly.

*Threats.* (1) Misconfiguration such as public buckets or open ports, the commonest cause of breaches. (2) Stolen or leaked credentials and access keys. (3) Insecure APIs. (4) Insider misuse. (5) Data loss and ransomware. (6) Denial-of-service attacks. (7) Shared-tenancy and hypervisor weaknesses. (8) Compliance and legal risks when data crosses borders.

*Shared responsibility.* The provider secures the cloud; the customer secures what they put in it, with the split of Figure 6.1.

*Identity management.* IAM policies follow default deny and explicit-deny-wins logic (Figure 6.2). Use least privilege, roles with short-lived credentials, MFA and periodic access review.

*Data protection.* Encrypt at rest and in transit. Use envelope encryption with keys in a KMS or HSM, so that rotation re-wraps small keys (Figure 6.3). Classify data, mask personal data, and keep backups in a separate account.

*Zero Trust.* The old model trusted anything inside the network perimeter. Zero Trust says "never trust, always verify": every request is authenticated and authorised using identity, device health and context, access is limited and temporary, and the network is treated as hostile. Micro-segmentation limits movement if an attacker gets in.

*Monitoring and compliance.* Central logging of API calls, alerts on unusual behaviour, regular scans and audits, and compliance with ISO 27001 and Nepal's Electronic Transactions Act 2063 and Individual Privacy Act 2075.

| Control | Reduces risk of |
|---|---|
| MFA, least privilege | Credential theft, insider misuse |
| Private subnets, closed buckets | Misconfiguration exposure |
| Encryption, KMS | Data theft |
| Logging, alerts | Late detection |
| Backups, tested restore | Ransomware, loss |

*Conclusion.* Cloud security is a shared task in which the customer's configuration decides most outcomes. Strong identity control, encryption with managed keys, Zero Trust design and continuous monitoring give security that is often better than what a small organisation can build alone.
