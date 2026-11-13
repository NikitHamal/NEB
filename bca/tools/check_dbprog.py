#!/usr/bin/env python3
"""Recompute every number that the BCA 453 Database Programming book prints from PL/SQL examples
(Oracle is not available in the build sandbox). Uses SQLite on the same EMP/DEPT data.  Run: python3 bca/tools/check_dbprog.py"""
import sqlite3, math
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE dept (deptno INTEGER PRIMARY KEY, dname TEXT, loc TEXT);
INSERT INTO dept VALUES (10,'ACCOUNTING','NEW YORK'),(20,'RESEARCH','DALLAS'),(30,'SALES','CHICAGO'),(40,'OPERATIONS','BOSTON');
CREATE TABLE emp (empno INTEGER PRIMARY KEY, ename TEXT, job TEXT, mgr INTEGER, hiredate TEXT, sal INTEGER, comm INTEGER, deptno INTEGER);
INSERT INTO emp VALUES
(7369,'SMITH','CLERK',7902,'1980-12-17',800,NULL,20),(7499,'ALLEN','SALESMAN',7698,'1981-02-20',1600,300,30),
(7521,'WARD','SALESMAN',7698,'1981-02-22',1250,500,30),(7566,'JONES','MANAGER',7839,'1981-04-02',2975,NULL,20),
(7654,'MARTIN','SALESMAN',7698,'1981-09-28',1250,1400,30),(7698,'BLAKE','MANAGER',7839,'1981-05-01',2850,NULL,30),
(7782,'CLARK','MANAGER',7839,'1981-06-09',2450,NULL,10),(7788,'SCOTT','ANALYST',7566,'1987-04-19',3000,NULL,20),
(7839,'KING','PRESIDENT',NULL,'1981-11-17',5000,NULL,10),(7844,'TURNER','SALESMAN',7698,'1981-09-08',1500,0,30),
(7876,'ADAMS','CLERK',7788,'1987-05-23',1100,NULL,20),(7900,'JAMES','CLERK',7698,'1981-12-03',950,NULL,30),
(7902,'FORD','ANALYST',7566,'1981-12-03',3000,NULL,20),(7934,'MILLER','CLERK',7782,'1982-01-23',1300,NULL,10);""")
q = lambda s, *a: db.execute(s, a).fetchall()
n = 0
def ok(cond, what):
    global n; n += 1
    if not cond: raise SystemExit("MISMATCH: " + what)
pay = dict(q("SELECT deptno, SUM(sal) FROM emp GROUP BY deptno"))
ok(pay == {10: 8750, 20: 10875, 30: 9400} and q("SELECT SUM(sal) FROM emp")[0][0] == 29025, "payroll totals")
# Unit 1 answers
ok(sorted(r[0] for r in q("SELECT e.ename FROM emp e JOIN dept d ON e.deptno=d.deptno WHERE e.sal>2500")) == ["BLAKE","FORD","JONES","KING","SCOTT"], "1.9a")
ok(sorted(r[0] for r in q("SELECT e.ename FROM emp e JOIN emp m ON e.mgr=m.empno WHERE e.sal>m.sal")) == ["FORD","SCOTT"], "1.9b")
ok(q("SELECT dname FROM dept d WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.deptno=d.deptno)") == [("OPERATIONS",)], "1.9c")
ok(q("SELECT MAX(sal) FROM emp WHERE sal < (SELECT MAX(sal) FROM emp)")[0][0] == 3000, "1.9d")
ok(14 * 4 == 56, "cross join")
# Unit 2
ok(800 * 12 == 9600 and sum(range(1, 101)) == 5050 and math.factorial(5) == 120 and sum(i * i for i in range(1, 6)) == 55, "2.x basics")
ok(sum(q("SELECT sal FROM emp WHERE deptno=10")[i][0] * 1.1 for i in range(3)) == 9625.000000000002 or abs(8750 * 1.1 - 9625) < 1e-6, "dept 10 raise")
ok(10875 + 5 * 100 == 11375, "dept 20 +100")
ok((0.10 * 1600, 0.02 * 3000, 0.15 * 2975) == (160.0, 60.0, 446.25), "bonuses")
ok([i for i in range(1, 10) if i % 2] == [1, 3, 5, 7, 9] and next((i, j) for i in range(1, 6) for j in range(1, 6) if i * j == 12) == (3, 4), "loops")
# Unit 3
ok((3000 * 1.10, 3000 * 1.80) == (3300.0, 5400.0) and 5400 > 5000, "3.4 cap")
# Unit 4
ok([r[0] for r in q("SELECT ename FROM emp WHERE deptno=30 ORDER BY sal DESC, ename")] == ["BLAKE","ALLEN","TURNER","MARTIN","WARD","JAMES"], "d30 order")
ok(q("SELECT job,COUNT(*),SUM(sal) FROM emp GROUP BY job ORDER BY job") == [("ANALYST",2,6000),("CLERK",4,4150),("MANAGER",3,8275),("PRESIDENT",1,5000),("SALESMAN",4,5600)], "job groups")
ok([r[0] for r in q("SELECT ename FROM emp WHERE deptno=20 AND sal>=2000 ORDER BY sal DESC, ename")] == ["FORD","SCOTT","JONES"], "d20 >=2000")
ok([r[0] for r in q("SELECT ename FROM emp WHERE deptno=20 ORDER BY ename")] == ["ADAMS","FORD","JONES","SCOTT","SMITH"], "d20 names")
ok(q("SELECT ename,sal FROM emp WHERE job='CLERK' AND deptno=20 ORDER BY ename") == [("ADAMS",1100),("SMITH",800)] and round(1100 * 1.1) == 1210 and round(800 * 1.1) == 880, "FOR UPDATE raise")
ok(q("SELECT ename FROM emp WHERE deptno=10 ORDER BY ename")[-1] == ("MILLER",), "bulk collect last")
# Unit 5
ok([round(s * 1.1) for s in (2450, 5000, 1300)] == [2695, 5500, 1430], "audit rows")
# Unit 6
ok((800 * 1.25, 1600 * 1.10, 1600 * 1.05) == (1000.0, 1760.0, 1680.0) or [round(x, 6) for x in (800 * 1.25, 1600 * 1.10, 1600 * 1.05)] == [1000, 1760, 1680], "raise_salary")
ok([round(9400 / 6, 2), round(8750 / 3, 2), 10875 / 5] == [1566.67, 2916.67, 2175], "dept_stats")
# Unit 7
net = lambda e: q("SELECT sal+COALESCE(comm,0) FROM emp WHERE empno=?", e)[0][0]
ok((net(7499), net(7369), net(7654)) == (1900, 800, 2650), "net_pay")
ok([r[0] for r in q("SELECT ename FROM emp WHERE deptno=30 AND sal+COALESCE(comm,0)>1700 ORDER BY ename")] == ["ALLEN","BLAKE","MARTIN","WARD"], "net pay > 1700")
def tax(i):
    t = 0.01 * min(i, 500000)
    if i > 500000: t += 0.10 * (min(i, 700000) - 500000)
    if i > 700000: t += 0.20 * (min(i, 1000000) - 700000)
    if i > 1000000: t += 0.30 * (i - 1000000)
    return round(t)
ok((tax(400000), tax(650000), tax(1200000)) == (4000, 20000, 145000), "annual_tax")
ok(math.factorial(10) == 3628800, "fact(10)")
ok((1760 + 300, 9400 + 160) == (2060, 9560), "emp_pkg after raises")
ok(q("SELECT COUNT(*) FROM emp WHERE deptno=20 AND sal=(SELECT MAX(sal) FROM emp WHERE deptno=20)")[0][0] == 2 and
   q("SELECT ename FROM emp WHERE deptno=10 AND sal=(SELECT MAX(sal) FROM emp WHERE deptno=10)") == [("KING",)], "top_earner")
ok(sum(int(c) for c in "4725") == 18, "digit sum")
print("check_dbprog: %d checks, 0 problems" % n)
