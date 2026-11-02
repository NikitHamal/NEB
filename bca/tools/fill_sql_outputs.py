#!/usr/bin/env python3
"""Execute every ```sql fence of a markdown unit on PostgreSQL (fresh schema per file, blocks run in order in
one schema) and insert whatever the block prints (query results, RAISE NOTICE lines, real ERROR messages) as an
```output fence right after it. Blocks that print nothing get no output fence. Use ```text for dialect-only code
(Oracle, SQL Server, MySQL) that must not be executed.
    python3 bca/tools/fill_sql_outputs.py bca/course/semester-3/dbms/unit-0[5-9].md
Connection: DATABASE_URL or postgresql://postgres:postgres@127.0.0.1:5432/app_db."""
import os, re, subprocess, sys, tempfile
URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/app_db")
pat = re.compile(r"(```sql\n(.*?)```\n)(?:\s*```output\n.*?```\n)?", re.S)
def psql(args, sql_file=None, schema=None):
    env = dict(os.environ, PGOPTIONS=f"-c search_path={schema}" if schema else "")
    cmd = ["psql", "-X", "-q", URL] + args
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, timeout=60)
for path in sys.argv[1:]:
    schema = "u_" + re.sub(r"\W", "_", os.path.basename(os.path.dirname(os.path.abspath(path))) + "_" + os.path.basename(path)[:-3])
    psql(["-c", f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"])
    text = open(path, encoding="utf-8").read()
    def repl(m):
        f = tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False); f.write(m.group(2)); f.close()
        r = psql(["-f", f.name], schema=schema)
        out = r.stdout.replace(f.name + ":", "")
        out = re.sub(r"psql:\d+: ", "", out)
        out = re.sub(r"^psql:.*?:(\d+): ", "", out, flags=re.M)
        out = "\n".join(l for l in out.split("\n") if not l.startswith(("CONTEXT:", "PL/pgSQL function"))).strip("\n")
        os.unlink(f.name)
        return m.group(1) + (f"```output\n{out}\n```\n" if out else "")
    new = pat.sub(repl, text)
    psql(["-c", f"DROP SCHEMA IF EXISTS {schema} CASCADE;"])
    if new != text: open(path, "w", encoding="utf-8").write(new)
    print(path, "sql blocks:", len(pat.findall(text)), "errors in output:", len(re.findall(r"^ERROR:", new, re.M)))
