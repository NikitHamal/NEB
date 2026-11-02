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

## 6.6 Summary and exercises

Security in the cloud is shared, with identity and data always the customer's; IAM decisions follow implicit deny, allow, explicit deny precedence; envelope encryption separates fast data keys from guarded master keys so rotation is cheap; Zero Trust replaces location-based trust with continuous verification.

1. Draw the responsibility split for an IaaS virtual machine and a SaaS email service.
2. State the IAM evaluation order and explain why order of statements does not matter.
3. Add a statement to the policy in this unit that allows `s3:ListBucket` on the bucket only, and predict the result for listing `reports/secret/`.
4. Explain DEK, KEK, wrapping and why rotation is cheap under envelope encryption.
5. Why does AES-GCM tamper detection matter for stored backups?
6. List four Zero Trust principles and one way to implement each.
