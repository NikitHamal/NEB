## 4.8 Backup and restore

### 4.8.1 The purpose: restore, not backup

Nobody wants a backup; everybody wants a **restore**. A backup system is judged by one question: *can we get the right data back, quickly enough, from the date we need?* Data is lost by disk failure, deleted files, software bugs, corruption, ransomware, theft, fire and administrator error; backups are the only defence against all of them. Replication and RAID protect only against some.

### 4.8.2 Policy first

Write the backup policy before choosing tools. It states, for each class of data:

| Item | Decision |
|---|---|
| **What** | Which systems and data are backed up (and which are not, such as temporary files) |
| **How often** | Set by the **RPO**: how much work may be lost |
| **How long to keep** | **Retention**: daily copies for 2 weeks, weekly for 3 months, monthly for a year, yearly for law or audit |
| **How fast to restore** | The **RTO**: determines the media, the network and the method |
| **Where** | On-site copy for speed, off-site copy for disasters, an offline or immutable copy for ransomware |
| **Who** | Owner of the policy, operator, who may request a restore |
| **Security** | Encryption of backup data, protected keys, controlled access |
| **Verification** | Automatic checks and scheduled restore tests |

### 4.8.3 Kinds of backup

| Kind | Copies | Backup time and size | Restore |
|---|---|---|---|
| **Full** | Everything | Longest and largest | Simplest: one set |
| **Incremental** | Only changes since the **last backup of any kind** | Smallest and fastest | Slowest: last full plus **every** incremental since |
| **Differential** | Changes since the **last full** | Grows during the week | Last full plus the **latest** differential |
| **Synthetic full** | Server combines the full and incrementals into a new full | Light on clients | Simple |
| **Snapshot / continuous** | Storage-level point-in-time copies, or continuous replication | Very quick | Fast; but same system, so not a stand-alone backup |

A common rotation is the **grandfather-father-son** scheme: daily incrementals (sons), a weekly full (father), a monthly full kept long (grandfather). The **3-2-1 rule** (Section 2.3.5) gives the number and place of the copies.

```svgfig label="4.1" caption="Restoring from a weekly full with daily incrementals needs the full plus every incremental up to the chosen day; with differentials only the latest differential is needed."
f = Fig(660, 230)
days = ["Sun\nfull", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
for i, d in enumerate(days):
    x = 15 + i * 92
    f.box(x, 30, 80, 42, d, fill=SAND if i == 0 else BLUE, stroke=AMBER if i == 0 else NAVY, size=10)
f.text(330, 18, "Incremental: restore Thursday = full + Mon + Tue + Wed + Thu (5 sets)", size=10, color=NAVY, bold=True)
f.box(15, 130, 80, 42, "Sun\nfull", fill=SAND, stroke=AMBER, size=10)
for i in range(1, 7):
    x = 15 + i * 92
    f.box(x, 130, 80, 42, "%s\ndiff." % ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][i], fill=SOFT, stroke=SLATE, size=10)
f.text(330, 118, "Differential: restore Thursday = full + Thursday's differential (2 sets)", size=10, color=NAVY, bold=True)
f.text(330, 205, "Faster restore costs more backup space; faster backup costs a longer restore.", size=10, color=SLATE)
```

```python
# Compare incremental and differential schemes for a weekly cycle
full_gb, daily_change_gb = 800, 24     # new or changed data per day
# a differential repeats earlier changes; assume 40% of each later day's changes touch files already changed
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
inc = [daily_change_gb] * 6
diff = []
changed = 0
for i in range(6):
    changed += daily_change_gb * (0.6 if i else 1.0)
    diff.append(changed)
print("full backup              : %d GB" % full_gb)
print("incremental sizes (GB)   :", [round(x) for x in inc], " week total %d" % (full_gb + sum(inc)))
print("differential sizes (GB)  :", [round(x) for x in diff], " week total %d" % (full_gb + sum(diff)))
for day_no, d in enumerate(days, 1):
    sets_inc = 1 + day_no
    sets_diff = 2
    print("restore after %s: incremental needs %d sets, differential %d sets" % (d, sets_inc, sets_diff))

# backup window: how long does the full take?
rate_mb_s = 110           # about one gigabit link
print("full backup time: %.1f h" % (full_gb * 1024 / rate_mb_s / 3600))
```

### 4.8.4 Design recommendations

1. **Automate** schedules and **monitor** results; a backup that fails silently for three months is the usual story. Alert on failure *and* on missing success reports.
2. **Verify**: check integrity after every run and **test a restore** regularly, a file, a mailbox and a whole server, with the time taken written down and compared with the RTO.
3. **Protect the backups**: encrypt them, keep the keys apart, use an account that production systems cannot delete from, and keep an **offline or immutable** copy so that ransomware cannot encrypt the backups with the data.
4. **Back up consistently**: databases need a dump or a snapshot-aware agent (copying files of a running database yields garbage); applications may need quiescing.
5. **Network**: back up over a dedicated network or at night; use deduplication and compression; for remote sites send the first full on disk and increments over the WAN.
6. **Capacity**: plan from the data size, change rate and retention (the program below).
7. **Document** the restore procedure, including how to rebuild the backup system itself.
8. **Do not forget** laptops, SaaS data (hosted mail and documents are still your responsibility), configuration of network devices and the DNS zone files.

Tools: `rsync` and `tar` for simple jobs; `restic`, `borg` and `duplicity` (encrypted, deduplicated); Bacula, Amanda and Veeam for enterprise; Windows Server Backup and VSS on Windows; storage and cloud snapshots.

```bash
# restic example (not run in the build sandbox)
export RESTIC_REPOSITORY=sftp:backup@10.20.60.5:/srv/restic RESTIC_PASSWORD_FILE=/root/.restic-pass
restic init
restic backup /srv/shares /etc --exclude '*.tmp'
restic forget --keep-daily 14 --keep-weekly 12 --keep-monthly 12 --prune
restic check
restic restore latest --target /tmp/restore-test --include /srv/shares/staff/budget.xlsx
```

```python
# Capacity for retention: 2 TB data, 2% daily change, weekly full, 4 weekly + 12 monthly kept
data_tb, change = 2.0, 0.02
weekly_fulls_kept, monthly_kept = 4, 12
daily_inc_per_week = 6 * data_tb * change
week_set = data_tb + daily_inc_per_week
total = week_set * weekly_fulls_kept + data_tb * monthly_kept
print("one week of sets (full + 6 incrementals): %.2f TB" % week_set)
print("4 weeks + 12 monthly fulls               : %.1f TB (before deduplication)" % total)
dedup = 0.35
print("with 3:1-ish deduplication and compression (35%% of raw): %.1f TB" % (total * dedup))
```

## 4.9 Software repository

### 4.9.1 What it is and why have one

A **software repository (software depot)** is the organisation's own, controlled source of software: operating-system packages, updates, applications, licences and in-house tools. Users and machines install from it instead of from random websites. Reasons: **consistency** (everyone gets the tested version), **security** (patches are tested and signed, and nothing unknown is installed), **bandwidth** (a package is downloaded once from the internet, then distributed on the LAN), **licence control**, **reproducibility** and the ability to **work offline** or on restricted networks.

### 4.9.2 Kinds of repository

| Kind | Examples |
|---|---|
| **OS package mirror or cache** | Local mirror of Ubuntu or Rocky repositories (`apt-mirror`, `reposync`), a caching proxy (`apt-cacher-ng`) |
| **Update server** | WSUS or Windows Update for Business, Red Hat Satellite, Landscape |
| **Application deployment** | Microsoft Intune or Configuration Manager, Chocolatey/Winget private source, Ansible |
| **Language and artefact repositories** | Nexus, Artifactory or Gitea packages for pip, npm, Maven, container images (Harbor) |
| **Installers and licence store** | A file share with checksums, documented licence keys and keys server |

### 4.9.3 Design recommendations

1. **Mirror or cache** the repositories your systems use; machines point to the internal name (`repo.college.edu.np`) by configuration management.
2. **Stage updates**: *testing* group, then *pilot*, then everyone, as for any change; keep the previous package versions to roll back.
3. **Sign and verify** packages (GPG keys, hash lists); never disable signature checking to make an installation work.
4. **Keep an inventory** of what is installed where and which licences are in use, to prove compliance and to find vulnerable versions fast.
5. **Control who may publish** to the internal repository; automate builds from version control.
6. **Plan capacity**: a full mirror of one Linux release is hundreds of gigabytes, so mirror only the repositories and architectures you need.
7. **Make it reliable**: it is a dependency of installation and patching, so back it up and serve it from two hosts if it matters.
8. **Respect licences**: free software has licences too; commercial software must be bought for each use; unlicensed copies are a legal and security risk.

```bash
# Ubuntu client using an internal mirror, and a caching proxy (not run in the build sandbox)
# /etc/apt/sources.list.d/internal.sources
#   Types: deb
#   URIs: http://repo.college.edu.np/ubuntu
#   Suites: jammy jammy-updates jammy-security
#   Components: main universe
# Cache proxy on the server:
sudo apt install apt-cacher-ng            # clients: echo 'Acquire::http::Proxy "http://repo:3142";' > /etc/apt/apt.conf.d/01proxy
# Rocky/Alma mirror with dnf
sudo dnf install dnf-utils createrepo_c
sudo reposync --repoid=baseos --download-metadata -p /srv/repo/rocky9
```

```python
# Bandwidth saved by a local cache
machines, update_mb = 150, 900
without = machines * update_mb / 1024            # every machine downloads from the internet
with_cache = update_mb / 1024                    # only the cache downloads; the LAN carries the rest
print("internet traffic without cache: %.1f GB" % without)
print("internet traffic with cache   : %.2f GB" % with_cache)
print("download time on a 10 Mbit/s link: %.1f h without, %.2f h with" % (without * 8192 / 10 / 3600, with_cache * 8192 / 10 / 3600))
```

## 4.10 Web services

### 4.10.1 Anatomy of a web service

A web service answers HTTP(S) requests with pages or data. A production design has layers, and each layer is a choice:

```svgfig label="4.2" caption="A recommended web-service architecture: the load balancer and reverse proxy terminate TLS, application servers are replaceable, state lives in the database."
f = Fig(680, 230)
f.box(10, 90, 90, 50, "Users\nbrowsers", fill=SAND, stroke=AMBER, size=10)
f.box(130, 90, 110, 50, "Firewall +\nCDN / DNS", fill=SOFT, stroke=SLATE, size=10)
f.box(270, 90, 110, 50, "Load balancer\nTLS, reverse proxy", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 30, 110, 45, "Web / app\nserver 1", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 105, 110, 45, "Web / app\nserver 2", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 180, 110, 40, "Static files /\ncache", fill=SOFT, stroke=SLATE, size=9)
f.box(570, 70, 100, 70, "Database\n(primary +\nreplica)", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(100, 115), (130, 115)], color=NAVY)
f.arrow([(240, 115), (270, 115)], color=NAVY)
f.arrow([(380, 105), (420, 55)], color=NAVY)
f.arrow([(380, 125), (420, 127)], color=NAVY)
f.arrow([(380, 135), (420, 195)], color=SLATE, dash=True)
f.arrow([(530, 55), (570, 90)], color=NAVY)
f.arrow([(530, 127), (570, 115)], color=NAVY)
```

### 4.10.2 Recommendations

1. **Web server**: Nginx or Apache httpd (or IIS on Windows); use **virtual hosts** so one server hosts several sites by name; keep the document root away from system files.
2. **TLS everywhere**: certificates from a trusted CA (**Let's Encrypt** is free, automated by ACME with `certbot`); redirect HTTP to HTTPS; enable HSTS; monitor **certificate expiry**; disable old protocols (SSLv3, TLS 1.0 and 1.1).
3. **Reverse proxy and load balancer**: one public front (Nginx, HAProxy, a cloud load balancer) that spreads load, checks the health of back ends and takes a failed server out of service; this also enables rolling upgrades with no downtime.
4. **Stateless application servers**: keep sessions and files in a shared store so any server can answer any request, and a server can be replaced at any time.
5. **Caching and CDN**: cache static content and use a content-delivery network for global or heavy sites; set sensible cache headers.
6. **Separate environments** (development, test, production) and deploy by an automated pipeline.
7. **Security**: keep software patched; hide version banners; a **web application firewall (WAF)**; run the server under an unprivileged account; least privilege for the database user; rate limiting; protection against DoS at the edge; regular scanning.
8. **Logging and monitoring**: access and error logs sent to the central log server; probes for the home page, login and payment; track the golden signals (Section 4.3.1).
9. **Backup and DR**: site files and database in the backup policy, with a rebuild procedure, and a test of recovery on another host.
10. **Capacity**: load-test before launch and before peak times (admission results, examination registration); scale horizontally by adding servers.

```ini
# /etc/nginx/sites-available/college  (not run in the build sandbox)
server {
    listen 80;
    server_name www.college.edu.np college.edu.np;
    return 301 https://www.college.edu.np$request_uri;
}
upstream app { server 10.20.40.11:8000; server 10.20.40.12:8000; }
server {
    listen 443 ssl http2;
    server_name www.college.edu.np;
    ssl_certificate     /etc/letsencrypt/live/www.college.edu.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.college.edu.np/privkey.pem;
    add_header Strict-Transport-Security "max-age=31536000" always;
    location /static/ { root /srv/www; expires 7d; }
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```

```python
# Sizing the web tier for admission-result day (illustrative)
peak_users = 6000                # at the busiest minute
requests_per_user_min = 6
rps = peak_users * requests_per_user_min / 60
per_server_rps = 150             # measured in a load test
import math
servers = math.ceil(rps / (per_server_rps * 0.65))   # keep 65% utilisation
print("peak load %.0f requests/s" % rps)
print("servers needed at 65%% utilisation: %d, plus 1 spare = %d" % (servers, servers + 1))
print("bandwidth for 120 KB average response: %.0f Mbit/s" % (rps * 120 * 8 / 1000))
```

