# Database Management System — BCA 202 (Semester III, 3 credits)

Old code CACS202 (2074 curriculum; CACS255 in Semester IV there). Nine units, 45 teaching hours.

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to DBMS | 3 |
| 2 | Database Design, Architecture and Model (E-R) | 6 |
| 3 | Relational Database Model (keys, relational algebra) | 4 |
| 4 | Database Normalization (1NF–4NF) | 4 |
| 5 | Creating and Altering Database and Tables (SQL DDL) | 6 |
| 6 | Manipulating and Querying Data (SQL DML, joins, views) | 8 |
| 7 | Stored Procedures, DML Triggers and Indexing | 5 |
| 8 | Query Processing and Security | 5 |
| 9 | Transaction and Concurrency Control | 4 |

## Verification

Every `sql` block in Units 5, 6, 7 and 9 was **executed on PostgreSQL 15** by `bca/tools/fill_sql_outputs.py` (fresh schema per unit); the `output` blocks are the real results, including the real constraint-violation and trigger error messages. Blocks marked `text` (Oracle `CREATE USER`, `GRANT` examples, `CREATE DATABASE`) are dialect illustrations and were not executed. Join-cost, sparse/dense-index and sorting numbers in Units 7 and 8 are computed from the stated formulas; the closure/key example in Unit 4 was worked by hand.

## Source and honesty

Unit list and hours are the TU **BCA 202 / CACS255-style** syllabus as reproduced on bcapoint.com (9 units, 45 hours; see `bca/SOURCES.md`). The revised-curriculum PDF itself was not retrievable. The syllabus names Oracle and SQL Server constructs (T-SQL-style stored procedures, `DISABLE TRIGGER`); the executable examples use PostgreSQL's PL/pgSQL, with an Oracle/SQL Server/MySQL comparison table at each place the dialects differ. Practice in your own lab with Oracle XE or MySQL by adapting those lines.

## Layout notes from the PDF QA

56 pages, 0 hard failures. Three near-empty-page warnings are all natural: p3 is the overflow of the table of contents; p26 and p50 are the last one or two answers of Units 5 and 8 spilling onto a new page before the next chapter starts.
