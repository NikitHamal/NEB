---
subject: Operating Systems
grade: BCA Semester 4
unit: 7
title: File System Interface Management
hours: 2
area: BCA 251 · Operating Systems · Unit 7
---

Disks store blocks of bits; people store *files* in *folders*. The file system is the part of the OS that turns blocks into named, protected, persistent data. This unit covers the interface: what a file is, how files are named and organised in directories, how programs access them, and how access is controlled.

::: key What this unit gives you
- File concept: naming, structure, types, attributes, operations, descriptors.
- Directory structures and path names.
- Sequential and direct access; protection with access-control lists and matrices.
- Real output of the Unix commands that show these ideas at work.
:::

## 7.1 File concept

A **file** is a named collection of related information stored on secondary storage; to the user it is the smallest unit of logical storage. The OS maps files onto physical devices.

### Naming

Names let a file survive the process that created it. Rules differ: MS-DOS allowed 8.3 names; modern systems allow 255 characters. UNIX is case-sensitive (`Notes.txt` ≠ `notes.txt`); Windows is case-insensitive but case-preserving. Many systems use an **extension** (`.c`, `.pdf`); Windows uses it to choose the program, UNIX treats it as a convention only.

### Structure

| Structure | Description | Example |
|---|---|---|
| **Unstructured byte sequence** | the OS sees only bytes; programs impose meaning | UNIX, Windows (most general, flexible) |
| **Record sequence** | fixed-length records read or written as a unit | old mainframes, punched-card systems |
| **Tree of records** | records with keys, found by key | mainframe ISAM / database-style files |

### Types

- **Regular files**: user data, either ASCII text or binary.
- **Directories**: system files that keep the structure of the file system.
- **Character special files**: model serial I/O devices (terminals, printers).
- **Block special files**: model disks.
- Executables have an internal layout (header, text, data, relocation, symbol table) that the loader understands.

### Attributes (metadata)

Name, type, location on disk, size, protection (permissions), owner, creation / last-access / last-modification times, flags (hidden, read-only, archive), and the link count. These are kept in the directory entry or an **inode**.

### Operations and file descriptors

The basic operations are create, delete, open, close, read, write, append, seek, get attributes, set attributes and rename. `open` searches the directory once and stores the file's attributes in a **per-process open-file table**, returning a small integer, the **file descriptor** (handle). Later `read` and `write` calls name the descriptor, so no searching is repeated. By UNIX convention descriptors 0, 1 and 2 are standard input, output and error. The OS also keeps a **system-wide open-file table** with a count of how many processes have each file open.

## 7.2 Directories

A **directory** is a file that maps names to files. Organisations:

| Scheme | Description | Problems |
|---|---|---|
| **Single-level** | one directory for all files | name collisions; no grouping |
| **Two-level** | a directory per user | users cannot share easily, no sub-grouping |
| **Hierarchical (tree)** | directories contain files and sub-directories, arbitrary depth | the standard design |
| **Acyclic graph** | hierarchical plus **links**: one file reachable by several names | deletion and dangling links |
| **General graph** | cycles allowed | needs garbage collection or cycle checks |

### Path names

An **absolute path** starts at the root (`/home/user/docs/notes.txt`, or `C:\Users\Sita\notes.txt`). A **relative path** starts at the **working directory** (`docs/notes.txt`; `..` is the parent, `.` is the current directory). Directory operations: create, delete, opendir, readdir, rename, link, unlink.

### Links

A **hard link** is another directory entry for the *same* inode: both names are equally "real", and the data is deleted only when the **link count** reaches zero. A **symbolic (soft) link** is a small file containing a path; it breaks if the target is removed. Real output of the Unix commands follows (inode numbers and the user name will differ on your machine):

```text
$ ls -l docs/notes.txt hard.txt soft.txt
-rw-r----- 2 user user 10  docs/notes.txt
-rw-r----- 2 user user 10  hard.txt
lrwxrwxrwx 1 user user 14  soft.txt -> docs/notes.txt
$ stat -c "%i %h %A %s %n" docs/notes.txt hard.txt soft.txt
1070623 2 -rw-r----- 10 docs/notes.txt
1070623 2 -rw-r----- 10 hard.txt
1070624 1 lrwxrwxrwx 14 soft.txt
$ rm docs/notes.txt; cat hard.txt; cat soft.txt
BCA sem 4
cat: soft.txt: No such file or directory
```

`notes.txt` and `hard.txt` share inode **1070623** and link count **2**; the soft link has its own inode, count 1 and a size of 14 (the length of the string `docs/notes.txt`). After `rm`, the data survives through the hard link, but the symbolic link dangles.

## 7.3 Access methods

| Method | How | Fits |
|---|---|---|
| **Sequential** | read or write records in order; a file pointer advances; `rewind` resets | tapes, compilers, logs, text processing |
| **Direct (random)** | jump to any block by number: `read n`, `write n`, or `seek` then `read` | databases, indexes, virtual memory |
| **Indexed** | an index of keys points into the file | large records databases |

Sequential access can be simulated on direct-access files, but not the other way round efficiently. `lseek(fd, offset, whence)` positions the pointer for direct access.

## 7.4 File-system layout and allocation (what the interface hides)

A UNIX-style **inode** stores attributes and the block pointers: 12 *direct* pointers, then a *single*, *double* and *triple indirect* pointer. With 4 KB blocks and 4-byte pointers an indirect block holds 1,024 pointers.

| Pointers | Reach |
|---|---|
| 12 direct | 12 × 4 KB = **48 KB** |
| single indirect | 1,024 × 4 KB = **4 MB** |
| double indirect | 1,024² × 4 KB = **4 GB** |
| triple indirect | 1,024³ × 4 KB = **4 TB** |

Maximum file size ≈ **4.004 TiB**. A 10,000-byte file needs 3 blocks (wasting 2,288 bytes in the last), and a 100 MB file (25,600 blocks) needs the double-indirect level. Other allocation methods: **contiguous** (fast, but external fragmentation), **linked** (no fragmentation, slow random access; FAT keeps the chain in a table: a 32 GB FAT32 volume with 4 KB clusters needs 8,388,608 entries = 32 MB of table), and **indexed** (inode style).

## 7.5 Protection

Protection controls *who may do what* with a file. Types of access: read, write, execute, append, delete, list.

### UNIX permissions

Each file has an owner, a group and **nine permission bits**: read/write/execute for *user*, *group*, *others*. `rw-r-----` is octal **640**: owner read/write, group read, others nothing. The **umask** removes bits from the defaults for new files (666) and directories (777):

```text
$ chmod 600 docs/notes.txt; stat -c "%a %A" docs/notes.txt
600 -rw-------
$ (umask 022; touch a.txt; mkdir d); stat -c "%a %n" a.txt d
644 a.txt
755 d
$ (umask 077; touch b.txt); stat -c "%a %n" b.txt
600 b.txt
```

umask 022 turns file default 666 into 644 and directory default 777 into 755; umask 077 leaves the owner alone: 600. (Bitwise: 666 AND NOT 022 = 644.)

### Access-control matrix and access-control list

Conceptually, protection is a matrix with a row per **domain** (user or process) and a column per **object** (file, device):

| Domain \ Object | notes.txt | printer | grades.db |
|---|---|---|---|
| Ram (student) | read | print | — |
| Sita (teacher) | read, write | print | read, write |
| Admin | read, write | print, manage | read, write, delete |

Storing the whole matrix is wasteful, as it is mostly empty, so systems store it by column or by row:

- **Access-control list (ACL)**: for each object, a list of ⟨domain, rights⟩. Easy to see *who* can access a file and to revoke it. Windows NTFS and Linux POSIX ACLs (`setfacl`) work this way. It costs a list search per access.
- **Capability list**: for each domain, a list of ⟨object, rights⟩ tokens it holds. Natural for passing rights between processes; revocation is harder.

UNIX permissions are a compact ACL with exactly three entries. Beyond file permissions, protection includes **user authentication** (Unit 8), encryption and the principle of **least privilege**: give a process only the rights it needs.

::: example Reading an ACL decision
File `grades.db` has the ACL: Sita = rw, Admin = rwd, Ram = none. Ram runs `cat grades.db`. The kernel finds no entry granting read to Ram, so `open` fails with *Permission denied*. When Sita later gets promoted to admin, only the ACL of each file needs editing; a capability system would have to find and recall every issued token.
:::

## Formula and fact sheet

- Inode reach: 12 direct + P + P² + P³ blocks, with P = block size ÷ pointer size.
- Permissions: r = 4, w = 2, x = 1; 640 = rw-r-----. New-file mode = 666 AND NOT umask; new-directory mode = 777 AND NOT umask.
- Hard link: same inode, link count + 1. Symbolic link: separate file holding a path.
- ACL = column of the access matrix (per object); capability list = row (per domain).

## Chapter summary

- A file is a named, persistent collection of bytes with attributes; a file descriptor is the handle returned by `open`.
- Directories are organised as trees (or graphs with links); paths are absolute or relative.
- Access is sequential or direct. Inodes, linked and contiguous allocation are the implementations behind the interface.
- Protection uses permission bits, ACLs and capabilities, ideally with least privilege.

## Practice

1. Define a file. List five file attributes and five file operations.
2. What is a file descriptor and why does `open` exist as a separate call?
3. Compare single-level, two-level and tree-structured directories.
4. Differentiate absolute and relative path names with an example.
5. Explain hard and soft links; what happens to each if the original is deleted?
6. Compare sequential and direct access with a use for each.
7. A file has mode 754. Describe the rights of the owner, group and others.
8. With umask 027, what mode does a new file (default 666) get?
9. Distinguish an ACL from a capability list. Which makes revocation easier?
10. With 8 KB blocks and 4-byte pointers, what is the largest file reachable with 10 direct pointers plus one single-indirect block?

::: note Answers and worked solutions
**1.** A file is a named collection of related data on secondary storage. Attributes: name, type, size, owner, protection, timestamps, location. Operations: create, open, read, write, seek, close, delete, rename.
**2.** A descriptor is a small integer index into the process's open-file table. `open` searches the directory and checks permissions *once*; later calls use the descriptor, so the directory is not searched on every read and write.
**3.** Single-level: all files in one directory, name clashes. Two-level: separate directory per user, avoids clashes but no sub-grouping and awkward sharing. Tree: arbitrary nesting, grouping, relative paths, the modern design.
**4.** Absolute: from the root (`/home/user/docs/a.txt`). Relative: from the working directory (`docs/a.txt`, or `../x.txt` for a file in the parent).
**5.** A hard link is another name for the same inode; deleting one name leaves the data reachable via the other (count decrements). A symbolic link stores a path; deleting the target leaves a dangling link that fails to open.
**6.** Sequential: process in order, e.g. reading a log or compiling source. Direct: jump to any block, e.g. a database record lookup.
**7.** 754 = rwx r-x r--: the owner can read, write and execute; the group can read and execute; others can only read.
**8.** 666 AND NOT 027: the mask removes group write (020) and all of others (007), giving 640.
**9.** ACL: a list per object of who may access it. Capability list: per domain, the objects it may access. Revocation is easier with ACLs: edit the object's list. Capabilities are held by processes, so they must be tracked down.
**10.** Pointers per block = 8 KB / 4 B = 2,048. Blocks reachable = 10 + 2,048 = 2,058; size = 2,058 × 8 KB = **16,464 KB ≈ 16.08 MB**.
:::
