# Advanced Java Programming — BCA 303 (Semester V, 3 credits)

Old code CACS354 (2074 curriculum, Semester VI; the revised list moves it to Semester V as BCA 303). 45 teaching hours.

| Unit | Title | Hours |
|---|---|---|
| 1 | Foundations for Advanced Java: Threads, I/O and Serialization | 6 |
| 2 | GUI Programming: Swing, Layouts and Event Handling (JavaFX in outline) | 10 |
| 3 | Database Programming with JDBC | 9 |
| 4 | Network Programming with Sockets and HTTP | 7 |
| 5 | Remote Method Invocation and CORBA | 6 |
| 6 | Servlets and JavaServer Pages | 9 |
| 7 | JavaBeans and the Enterprise Java Landscape | 5 |

## Verification

`bca/tools/fill_java_outputs.py` compiles every ```java block with a real JDK (OpenJDK 17) against the Xerial SQLite JDBC driver, H2, slf4j and the servlet API 4.0 from the Debian packages, runs each program headless (`-Djava.awt.headless=true`) and inserts its real output after the listing. Result for this book: **19 compiled, 18 executed, 0 failures** (the one program not run is the Swing window `TempConverter`, which opens a frame, so it is compile-checked only). What was really executed: threads and executors, file and serialization round trips, headless Swing components (button clicks through `doClick`, combo and check boxes, list and table models, grid and border layout bounds), JDBC against a live SQLite database (prepared statements, generated keys, metadata, batch of 1000 inserts, transaction commit and rollback, a `CachedRowSet`, a DAO), TCP echo with a thread pool, a UDP exchange, an `HttpServer` and `HttpClient`, a real RMI registry with a remote object, the servlet lifecycle through the real servlet API with proxy objects for request, response and session, and a bean with bound and constrained properties and introspection. Not executed (listed in the text as such): the JavaFX listing (OpenJFX not installed), the CORBA IDL (CORBA was removed from the JDK in Java 11), JSP pages and `web.xml` (no servlet container was run), and the `CallableStatement` syntax (SQLite has no stored procedures).

**What the verification caught while writing:** (1) the textbook SQL-injection example `' OR '1'='1` typed only in the name field **does not** work against `... name='' OR '1'='1' AND pw='x'` (AND binds tighter than OR, 0 rows); the book now demonstrates the two injections that do work (`admin' --` and the tautology in both fields) and shows the prepared statement blocking both; (2) a first draft of the bean caution claimed that serialising a bean with registered listeners fails; the program showed that `PropertyChangeSupport` is serializable and simply skips non-serializable listeners, so the text was corrected; (3) calling the protected `HttpServlet.service(HttpServletRequest, HttpServletResponse)` from outside the class does not compile, so the harness calls the public `service(ServletRequest, ServletResponse)` as the container does; (4) the default `doDelete` needs `getProtocol()` from the request (a null protocol raised a NullPointerException in a first harness), which is why the mock returns HTTP/1.1.

## Source and honesty

**No TU unit list for BCA 303 / CACS354 was retrieved in this session.** The unit order and the 45-hour split are a reconstruction from the topics named in the course brief for this task (Swing/JavaFX GUI and event handling, JDBC, servlets and JSP, JavaBeans, RMI, CORBA and network sockets), arranged in the usual teaching order of the Advanced Java textbooks (Horstmann *Core Java vol. 2*, Deitel, the Oracle Java tutorials, the Jakarta EE tutorial). The revised-syllabus PDF was not retrieved; see `bca/SOURCES.md`. All text and code are original. API facts (Java 9 deprecation and Java 11 removal of CORBA, the javax-to-jakarta rename in Jakarta EE 9, default RMI registry port 1099) are standard published facts.
