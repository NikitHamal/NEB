---
subject: Software Project Management
grade: BCA Semester 7
unit: 7
title: Software Configuration Management
hours: 7
area: BCA 402 · Software Project Management · Unit 7
---

Two developers edit the same file on the same evening. One fixes a login bug, the other adds a new field. The next morning, one set of changes has vanished, and nobody can say which version was sent to the client last week. **Software configuration management (SCM)** exists to stop this kind of chaos. It controls *what* is in the software, *who* changed *what*, *when* and *why*, and makes any past version reproducible.

::: key What this unit gives you
- The concept of SCM, why it is needed, and its elements: configuration items, baselines, repository.
- Versioning and version control: centralised and distributed systems, branching, merging, version numbering.
- The SCM process and the change control process, with the Change Control Board.
- Configuration audit and status reporting.
- Case study of version-control tools: Git, CVS and SVN, with commands; laboratory guidance.
:::

## 7.1 Concept and need for SCM

**Software configuration management** is the discipline of identifying, organising and controlling modifications to software during development and maintenance, so that the integrity and traceability of the product are maintained. (IEEE 828 defines it as "a discipline applying technical and administrative direction and surveillance to identify and document the functional and physical characteristics of a configuration item, control changes, record and report change processing, and verify compliance with requirements.")

Software **changes constantly**: requirements, designs, code, tests and documents all evolve. Studies show that uncontrolled change is one of the biggest causes of lost work and unreleasable builds.

### Requirements of SCM (why it is needed)

| Problem without SCM | SCM solution |
|---|---|
| Two people overwrite each other's changes | check-in and check-out, merging |
| "Which version is in production?" | identified versions and baselines |
| A new release breaks an old feature | ability to compare and roll back versions |
| Fixes in version 1.0 are missing from version 2.0 | branches and merges |
| Nobody knows who changed the file and why | history, commit messages, change records |
| Documents and code are out of step | all items under one control |
| Customers on different versions need support | maintain several releases in parallel |
| Audit or regulator asks for evidence | status accounting and audit trail |

SCM supports **teams** (parallel work), **releases** (reproducible builds), **quality** (controlled change) and **maintenance** (traceability from a defect report to the code that fixed it).

## 7.2 Elements of SCM

### Configuration items (CI)

A **configuration item** is any work product placed under configuration control: source code, executables, libraries, requirement specification, design documents, test plans and test data, build scripts, user manual, database schema, project plan. Each CI has a unique **identifier**, a **version**, an **owner** and a **status** (draft, reviewed, approved, released).

### Baselines

A **baseline** is a specification or product that has been formally reviewed and agreed, and thereafter serves as the basis for further development; it can be changed only through the formal change control procedure. Typical baselines are the **requirements baseline** (approved SRS), **design baseline**, **code or product baseline** (tested build) and **release baseline** (delivered to the customer). Baselines are named, frozen, and recorded in the repository, often marked with a **tag** (for example `v1.0`).

```svgfig label="7.1" caption="Baselines along the life cycle. Each baseline is frozen; later changes (arrows below) are made only through change control and produce a new version."
f = Fig(640, 230)
f.line(30, 70, 610, 70, color=SLATE, sw=2)
bl = [(80, "Requirements\nbaseline"), (230, "Design\nbaseline"), (380, "Product\nbaseline"), (530, "Release\nbaseline")]
for x, t in bl:
    f.circle(x, 70, 14, fill="#fde68a", stroke=AMBER, sw=2)
    f.text(x, 108, t.split("\n")[0], size=11, color=NAVY, bold=True)
    f.text(x, 122, t.split("\n")[1], size=11, color=NAVY, bold=True)
f.text(155, 52, "analysis", size=10.5, color=SLATE)
f.text(305, 52, "design and code", size=10.5, color=SLATE)
f.text(455, 52, "test", size=10.5, color=SLATE)
for x in (230, 380, 530):
    f.arrow([(x, 150), (x, 188)], color=RED, sw=1.8)
    f.text(x, 205, "change request", size=10.5, color=RED)
f.box(30, 150, 140, 36, "Approved items are frozen", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=10.5, bold=True)
```

### The SCM repository

The **repository** (also called the project database or library) is the central, controlled store of all configuration items and their history. It provides:

- **Storage and retrieval** of every version of every item.
- **Access control** (who may read, change or approve).
- **Version history** with author, date and message.
- **Dependency tracking** (which versions of which items make up a build).
- **Change and defect links** (issue numbers referenced in commits).
- **Backup and security.**

Typical software libraries are the **development (working) area** where developers change items, the **controlled (integration) library** holding baselined items, and the **release (static) library** with delivered versions.

### Other elements

**Version control**, **change control**, **configuration auditing** and **status reporting** are the four control activities discussed below; **build and release management** assembles items into a deliverable product and distributes it.

## 7.3 Versioning and version control

### Versions, revisions, variants and releases

| Term | Meaning |
|---|---|
| **Version** | a particular state of a configuration item at a point in time |
| **Revision** | a new version that replaces its predecessor (bug fix or small update) |
| **Variant** | a version that exists in parallel for a different platform or customer (for example Android and iOS) |
| **Release** | a version made available to users |
| **Branch** | a line of development separate from the main line (trunk/main) |
| **Merge** | combining the changes of one branch into another |
| **Tag** | a label on a particular version, such as a baseline |

### Version numbering

A common convention is **semantic versioning MAJOR.MINOR.PATCH**: increase MAJOR for incompatible changes, MINOR for new backward-compatible features, PATCH for bug fixes (for example 2.4.1 to 2.4.2 is a fix; 2.4.2 to 2.5.0 adds a feature; 2.5.0 to 3.0.0 breaks compatibility). Older systems use sequential revision numbers (1.1, 1.2, 1.2.1.1 for branches).

### Version control systems (VCS)

A **version control system** records changes to files over time so that specific versions can be recalled, compared and merged. Three generations:

| Type | Idea | Examples | Weakness |
|---|---|---|---|
| **Local** | revisions of files kept on one machine | RCS | no collaboration |
| **Centralised (CVCS)** | a single server holds the repository; clients check out a working copy | CVS, Subversion (SVN), Perforce | server is a single point of failure; needs network for history and commits |
| **Distributed (DVCS)** | every user has a full copy of the repository and history | Git, Mercurial | more concepts to learn; large binaries need extra tools |

### Working models

- **Lock-modify-unlock (pessimistic):** a file is locked while one user edits it. It is safe but blocks others (used for binary files).
- **Copy-modify-merge (optimistic):** everyone edits their own copy and the system **merges** the changes; conflicting edits to the same lines must be resolved by hand. This is the model used by CVS, SVN and Git.

### Branching and merging strategies

Typical strategies are **trunk-based development** (short-lived branches merged to the main line daily), **feature branching** (one branch per feature or issue, merged through a review), and **Git Flow** (main, develop, feature, release and hotfix branches). Branches allow parallel work and stable releases, but long-lived branches make merging painful; the rule is **merge early, merge often**.

## 7.4 The SCM process

The SCM process has five connected activities.

1. **Identification.** Decide which items are configuration items and give each a unique name and version number; define the structure of the repository and baselines.
2. **Version control.** Manage versions and parallel development with check-in, check-out, branches and merges.
3. **Change control.** Evaluate, approve and track each proposed change (section 7.5).
4. **Configuration auditing.** Check that the product matches its requirements and that baselines are correct (section 7.6).
5. **Status accounting (reporting).** Record and report the state of every item and the changes made (section 7.6).

Surrounding these are **SCM planning** (a configuration management plan saying who, what tools, which naming and branching rules), **build management** (reproducible builds from tagged versions, ideally automated by continuous integration) and **release management** (packaging, release notes, deployment, rollback plan).

### Roles

The **configuration manager** (or librarian) maintains the repository and procedures. The **Change Control Board (CCB)** approves changes. **Developers** make changes under control. **Quality assurance** audits compliance. In small student teams one person often plays several roles.

## 7.5 Change control process

Changes are inevitable: bugs are found, users ask for new features, laws change. The aim of change control is **not to prevent change but to make it deliberate, assessed and recorded**.

```svgfig label="7.2" caption="The change control process. A change request is evaluated by the Change Control Board; approved changes are implemented, tested, reviewed and then baselined again."
f = Fig(640, 250)
f.box(10, 90, 100, 46, "Change request raised", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(140, 90, 100, 46, "Impact analysis", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(270, 90, 100, 46, "CCB decision", fill="#fde68a", stroke=AMBER, color=NAVY, size=11.5, bold=True)
f.box(400, 90, 100, 46, "Implement change", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(530, 90, 100, 46, "Test and review", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
for x in (110, 240, 370, 500):
    f.arrow([(x, 113), (x + 30, 113)], color=NAVY, sw=1.8)
f.box(270, 8, 100, 40, "Rejected or deferred", fill="#fecaca", stroke=RED, color=NAVY, size=10.5, bold=True)
f.arrow([(320, 90), (320, 48)], color=RED, sw=1.6)
f.box(400, 190, 230, 44, "Update baseline, tag new version, record in status report", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.arrow([(580, 136), (580, 190)], color=NAVY, sw=1.8)
```

**Steps.**

1. **Change request (CR).** Anyone (user, tester, developer) submits a request describing the problem or enhancement, its priority and its source. It is logged with a unique ID.
2. **Impact analysis.** The technical team assesses which configuration items are affected, the effort, cost, schedule and risks, and the effect on quality and on other requirements.
3. **CCB review and decision.** The **Change Control Board**, with representatives of the customer, management, development, testing and quality assurance, approves, rejects or defers the request, sets its priority and assigns it.
4. **Implementation.** The developer checks out the affected items (often on a **branch**), makes the change and unit-tests it.
5. **Verification.** Review and regression testing confirm that the change works and has not broken anything.
6. **Baseline and release.** The CI is checked in, the baseline updated, the version tagged, and the CR closed. Records and release notes are updated.

An **emergency change** (a critical production defect) follows a shortened path, with after-the-event review.

::: example A change request record
**CR-0142.** *Raised by:* admissions officer, 12 Magh. *Description:* receipt should show the applicant's photo. *Items affected:* receipt template, `print_receipt()`, user manual section 4. *Effort:* 1.5 person-days; low risk. *CCB decision:* approved, priority medium, assigned to Sita for version 1.3. *Status:* implemented on branch `cr-0142`, merged to `main`, tagged `v1.3.0`.
:::

## 7.6 Configuration audit and status reporting

### Configuration audit

A **configuration audit** independently checks that the configuration items and baselines are correct and complete. Two types:

| Audit | Question | Checks |
|---|---|---|
| **Functional configuration audit (FCA)** | Does the product do what the requirements say? | test results against requirements; all approved changes implemented |
| **Physical configuration audit (PCA)** | Does the delivered package match its documentation? | each item in the baseline present, correctly versioned and consistent with design and user documents; build reproducible |

Audits are done before a release or at a baseline, and ask whether the change procedure was followed, whether each change was approved, and whether documents match code.

### Configuration status accounting (reporting)

**Status reporting** answers: *What is the current state of each item? What changed since the last report? Which changes are pending?* Typical reports are the list of baselines and their items, version history of an item, open, approved and closed change requests, and the number of changes per module (a signal of instability). Reports go to management, the CCB and the team, and provide the audit trail that regulators or customers may need.

## 7.7 Case study: version control tools (Git, CVS, SVN)

### Concurrent Versions System (CVS)

CVS (1986, later 1990s) was the first widely used open-source centralised VCS. It tracks files individually (no atomic multi-file commits), has weak support for renaming, and branching is cumbersome. It is now largely obsolete but important historically.

### Apache Subversion (SVN)

SVN (2000) was designed as a "better CVS." It is centralised, with **atomic commits** (a commit affects all files or none), directories and renames under version control, global revision numbers (r1, r2, ...), cheap copies for branches and tags, and good support for binary files. Typical layout: `trunk/`, `branches/`, `tags/`. Basic commands: `svn checkout`, `svn update`, `svn add`, `svn commit -m "msg"`, `svn diff`, `svn log`, `svn merge`, `svn copy` (branch or tag).

### Git

Git (created by Linus Torvalds in 2005 for the Linux kernel) is the dominant **distributed** VCS. Each clone is a full repository; commits are local and instant; branching and merging are cheap, so workflows with many short-lived branches are routine. Hosting services (GitHub, GitLab, Bitbucket) add pull requests, code review, issue tracking and CI. Git stores content as snapshots identified by a SHA-1 hash, which makes history tamper-evident.

```svgfig label="7.3" caption="Git areas and commands. A change moves from the working directory to the staging area (add), to the local repository (commit), and to the remote repository (push)."
f = Fig(640, 210)
areas = [(20, "Working directory"), (180, "Staging area (index)"), (340, "Local repository"), (500, "Remote repository")]
for x, t in areas:
    f.box(x, 40, 120, 60, t, fill=BLUE if x < 340 else "#bbf7d0", stroke=NAVY if x < 340 else TEAL, color=NAVY, size=11, bold=True)
for x, t in [(140, "git add"), (300, "git commit"), (460, "git push")]:
    f.arrow([(x, 62), (x + 40, 62)], color=NAVY, sw=1.8, label=t, lpos=(x + 20, 52), lsize=10.5)
for x, t in [(460, "git fetch / pull"), (140, "git restore")]:
    f.arrow([(x + 40, 88), (x, 88)], color=SLATE, sw=1.5, dash=True)
f.text(480, 116, "git fetch / pull", size=10.5, color=SLATE)
f.text(160, 116, "git restore", size=10.5, color=SLATE)
f.box(20, 150, 600, 40, "git clone copies the whole remote repository, history included, to the local machine", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=11, bold=True)
```

| Task | Git command |
|---|---|
| Create a repository / copy one | `git init` / `git clone <url>` |
| See changes and status | `git status`, `git diff` |
| Stage and commit | `git add file`, `git commit -m "message"` |
| History | `git log --oneline --graph` |
| Create and switch branch | `git branch feature-x`, `git switch feature-x` |
| Merge a branch | `git switch main`, `git merge feature-x` |
| Tag a baseline | `git tag -a v1.0 -m "release 1.0"` |
| Share changes | `git push origin main`, `git pull` |
| Undo a commit safely | `git revert <commit>` |
| Temporarily shelve work | `git stash`, `git stash pop` |

### Comparison of the three tools

| Feature | CVS | SVN | Git |
|---|---|---|---|
| Architecture | centralised | centralised | distributed |
| Commits | per file, not atomic | atomic | atomic, local |
| Revision identifier | per-file numbers (1.4) | global number (r120) | commit hash |
| Branching | costly, error-prone | cheap copies | very cheap, central to workflow |
| Offline work | almost none | limited | full (commit, log, branch offline) |
| Renames and moves | poor | supported | tracked by content |
| Typical use today | legacy | enterprise, large binaries | most software projects |

::: example Resolving a merge conflict in Git
Two developers change line 12 of `fees.py`. After `git merge feature-x`, Git reports *CONFLICT*. The file contains markers `<<<<<<<` (current branch), `=======`, `>>>>>>>` (incoming branch). The developer edits the file to the intended result, removes the markers, runs `git add fees.py` and `git commit`. Good practice: pull often, keep branches short, and review before merging.
:::

### Other tools

SCM also uses **issue trackers** (Jira, Bugzilla, GitHub Issues) for change requests, **build tools** (Maven, Gradle, npm) and **CI servers** (Jenkins, GitHub Actions) for reproducible builds, and **artifact repositories** (Nexus) for binaries.

## Laboratory guide (project management tools)

The TU syllabus asks for laboratory work covering every unit, done in groups with a project-management tool such as MS Project, OpenProj, dotProject, Trello, Asana or ClickUp. A suitable set:

1. **Unit 1:** write the scope statement and project charter for a small system (for example library or hostel management).
2. **Unit 2:** build the WBS, enter activities and dependencies in the tool, find the critical path and print the Gantt chart.
3. **Unit 3:** estimate the project by bottom-up, by function points and by COCOMO, and compare.
4. **Unit 4:** prepare a cash-flow forecast; compute NPV, IRR and payback in a spreadsheet.
5. **Unit 5:** create a risk register with probability, impact, exposure and responses; draw the matrix.
6. **Unit 6:** write a quality plan; compute defect density and DRE from test records.
7. **Unit 7:** put the project in Git; create branches, merge, resolve a conflict and tag a release; write a change request.

## Formula and fact sheet

- SCM elements: configuration items, baselines, repository, version control, change control, audit, status reporting.
- Semantic version: MAJOR.MINOR.PATCH. Branch to work in parallel; merge early and often; tag baselines.
- Change control: request, impact analysis, CCB decision, implementation, verification, baseline update.
- Audits: functional (does it meet requirements?) and physical (does the package match the documents?).
- Git areas: working directory, staging area, local repository, remote repository.

## Chapter summary

- SCM controls change so that every version is identified, traceable and reproducible.
- Configuration items under a repository, frozen as baselines, change only through change control.
- Version control systems are local, centralised (CVS, SVN) or distributed (Git); the copy-modify-merge model dominates, with branches and tags.
- The SCM process is identification, version control, change control, audit and status accounting, with build and release management.
- Change control passes each request through impact analysis and a Change Control Board.
- FCA and PCA verify product and baseline; status reports give the audit trail.
- Git is the leading tool; SVN is centralised with atomic commits; CVS is a legacy predecessor.

## Practice

1. Define SCM. Why is it needed in a software project?
2. Define configuration item and baseline. Give examples of each.
3. What is an SCM repository? Describe its functions.
4. Differentiate centralised and distributed version control systems.
5. Explain versioning, branching and merging. How does semantic versioning work?
6. Explain the SCM process in brief.
7. Describe the change control process with a diagram. What is the role of the CCB?
8. What are configuration audits? Distinguish FCA and PCA.
9. Compare Git, SVN and CVS.
10. Write the Git commands to create a branch `login-fix`, commit a change, merge it into `main` and tag version 1.1.0.

::: note Answers and worked solutions
**1.** Controlling and recording modifications to software items; needed because change is constant, teams work in parallel, and releases must be reproducible and traceable.
**2.** CI: source file, SRS, test plan, build script. Baseline: formally agreed and frozen version such as the approved SRS or release 1.0.
**3.** A controlled store of all items and versions: storage, access control, history, dependency tracking, links to change requests, backup.
**4.** Centralised: one server holds history and clients check out copies (SVN, CVS); distributed: each user has a full repository (Git), allowing offline work and cheap branching.
**5.** Versions are states of an item; branches are parallel lines of development; merge combines them; semantic versioning increments MAJOR for breaking changes, MINOR for features, PATCH for fixes.
**6.** Identification, version control, change control, audit, status accounting, plus build and release management.
**7.** Request, impact analysis, CCB decision, implementation, verification, baseline update (figure 7.2). The CCB approves, rejects or defers requests and sets priority.
**8.** Independent checks of items and baselines. FCA checks function against requirements; PCA checks that the delivered items match the documentation.
**9.** See the comparison table in section 7.7 (architecture, atomic commits, branching, offline work).
**10.** `git switch -c login-fix`, edit, `git add .`, `git commit -m "Fix login timeout"`, `git switch main`, `git merge login-fix`, `git tag -a v1.1.0 -m "release 1.1.0"`.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is software configuration management? Explain its importance in a software project.**

*Introduction.* SCM is the discipline of identifying, controlling, auditing and reporting changes to software items throughout their life.

*Importance.*

1. **Parallel work without overwriting,** through version control.
2. **Reproducibility.** Any past release can be rebuilt from its tagged baseline.
3. **Controlled change.** Every change is assessed and approved.
4. **Traceability** from requirement to code, test and defect.
5. **Quality and audit.** FCA and PCA and status reports provide evidence.
6. **Maintenance of several releases** in parallel through branches.

*Conclusion.* Without SCM, a team of more than one person cannot reliably know what it has built.

**Q2 (10 marks). Explain the change control process and the roles of baseline, repository, audit and status reporting in SCM.**

*Introduction.* Change control is the heart of SCM: it makes sure that changes to baselined items are deliberate and recorded.

*Process.* A change request is logged; impact analysis estimates the items, effort, cost and risk; the Change Control Board approves, rejects or defers it; an approved change is implemented on a branch, tested and reviewed; the item is checked in, the baseline updated, and the version tagged.

*Supporting elements.* The **baseline** is the frozen, approved version that only change control may alter. The **repository** stores every version with history and access control. **Configuration audits** (functional and physical) check that the product meets requirements and that the delivered package matches the documentation. **Status reporting** records the state of every item and change, giving an audit trail.

| Element | Role |
|---|---|
| Baseline | agreed reference point |
| Repository | controlled store with history |
| Change control | assess and approve changes |
| Audit | verify correctness |
| Status report | record and communicate |

*Tools.* Git, SVN and CVS implement version control; Jira or GitHub Issues track change requests.

*Conclusion.* Together, these elements allow the project to change safely and to prove what was delivered.
