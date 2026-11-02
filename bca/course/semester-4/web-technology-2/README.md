# Web Technology II — BCA 255 (Semester IV, 3 credits)

New code in the revised curriculum (2082 batch). It takes over the server-side half of the old CACS254 *Scripting Language*; client-side JavaScript and jQuery are in Web Technology I (BCA 203) in this repository.

| Unit | Title | Hours (planned, 45 total) |
|---|---|---|
| 1 | Server-Side Scripting and PHP Fundamentals | 8 |
| 2 | Forms, Files, Sessions and Cookies | 7 |
| 3 | MySQL for Web Applications | 7 |
| 4 | Connecting PHP to MySQL | 7 |
| 5 | Object-Oriented Programming in PHP | 7 |
| 6 | AJAX, JSON and Web APIs | 6 |
| 7 | Web Application Security and Authentication (addition) | 4 |
| 8 | Content Management Systems and PHP Frameworks | 4 |

## IMPORTANT: unit list is derived, not TU's

**No TU syllabus for BCA 255 was retrievable** (only code, title and 3 credits). Units 1–6 and 8 follow the server-side half of the old CACS254 outline (PHP 8 h, MySQL 7 h, object-oriented PHP, AJAX, and the CMS section: WordPress and Joomla at administrator level). Unit 7 (security and authentication) is an **addition**, because it is standard in any such course. The hours column is a planning guide, not a TU figure. Check your college's notice for the exact units; if TU's revised outline includes, for example, Laravel in depth or Node.js, those are not covered here.

## Verification

- Every ` ```php ` block was **executed** with PHP 8.2 (CLI) by `bca/tools/fill_script_outputs.py`; the ` ```output ` block is the real stdout, warnings and errors included. Web-only features (superglobals, sessions, headers) were simulated: `$_GET`/`$_POST` set by hand; sessions run with `ob_start()` and a fixed session id; Unit 6 starts PHP's built-in web server and makes **real HTTP requests** with `file_get_contents` (GET, and POST with JSON), printing status lines and bodies.
- Every ` ```sql ` block was executed on **MariaDB 10.11.19** (the MySQL-compatible server shipped by Debian), through the `mysql` client in table mode, in a freshly created database; PHP blocks in Units 3, 4 and 6 ran against the same server using mysqli and PDO (`mysql:` DSN). **Oracle MySQL 8 was not available**; MariaDB and MySQL agree on everything used here, but error wording and `EXPLAIN` output can differ, and the CHECK-constraint error number shown (4025) is MariaDB's (MySQL 8 reports 3819).
- Unit 7's injection and login demonstrations use in-memory **SQLite** (PDO) so that they can be destroyed freely; the SQL strings behave the same on MySQL.
- Not executed: code needing a browser or mail server or file-upload request (JavaScript snippets in Unit 6, `mail()`, `move_uploaded_file`, `setcookie`, the Laravel route) is shown in blocks marked `noexec`/`js`; Unit 8's CMS installation steps are descriptive. These are said to be unexecuted where they appear.
- `fill_script_outputs.py` exits non-zero if any block misbehaves; it printed no failures for the final text.

**What running the code caught:** (1) `echo @include "x.php" ? a : b` parses as `include ("x.php" ? a : b)` and crashed with *Path cannot be empty*; rewritten as `$r = @include …; var_dump($r)`; (2) `mb_strlen()` was undefined because the PHP mbstring extension was not installed (installed `php-mbstring`; note that it is a separate package on Debian/Ubuntu); (3) the `mysql` client returns exit status 0 even after an error in a sourced script, which hid failing SQL from the first run of the runner, so the runner now also scans stderr for `ERROR`; (4) the first draft of the e-mail example was going to be run and would have tried a real mail transport, so it is marked `noexec`.

## Layout notes from the PDF QA

See the build record in `bca/course/CHANGELOG_BCA_COURSE.md`.
