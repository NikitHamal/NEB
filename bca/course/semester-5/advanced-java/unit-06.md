---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 6
title: Servlets and JavaServer Pages
hours: 9
area: BCA 303 · Advanced Java Programming · Unit 6
---

A web server that only serves files cannot log you in, search a catalogue or record an order. **Servlets** are Java classes that run *inside* a web server (a **servlet container** such as Apache Tomcat or Jetty) and generate responses dynamically: the container parses the HTTP request, calls your method, and sends back what you wrote. **JavaServer Pages (JSP)** let you write the response as HTML with Java embedded; the container translates the page into a servlet. Together with JDBC (Unit 3) they are the classic Java web stack, and the base on which Spring MVC and Jakarta Faces are built.

The program in this unit exercises a real servlet: it is compiled against the servlet API 4.0 and its lifecycle methods are called by a small test harness that plays the role of the container, using proxy objects for the request, response and session. Everything the servlet prints below is real output.

::: key What this unit gives you
- The web application model: containers, WAR layout, `web.xml` and annotations.
- The servlet lifecycle (`init`, `service`, `destroy`), `HttpServlet`, request and response objects.
- Sessions: cookies, URL rewriting, `HttpSession`; filters and listeners.
- JSP: elements, implicit objects, EL and JSTL, the MVC pattern with a servlet controller.
- Security basics: output escaping, session handling.
:::

## 6.1 Web applications and containers

A Java web application is a directory (or a **WAR** file, Web ARchive) with a fixed layout:

```text
college/
  index.html, css/, images/          public static files
  WEB-INF/                           never served directly
    web.xml                          deployment descriptor (optional with annotations)
    classes/                         compiled servlets and other classes
    lib/                             JAR libraries (JDBC driver, JSTL)
  pages/result.jsp                   JSP pages
```

The container (**Tomcat**, Jetty, GlassFish, WildFly) listens for HTTP, maps URLs to servlets, manages their lifecycle and threads, and provides sessions, security and resource pools. Deployment: copy `college.war` to Tomcat's `webapps` folder, and the application is served at `http://localhost:8080/college/`. A servlet is mapped to a URL either with the annotation `@WebServlet("/hello")` (Servlet 3.0+) or in `web.xml`:

```text
<servlet>
  <servlet-name>hello</servlet-name>
  <servlet-class>edu.nebians.HelloServlet</servlet-class>
</servlet>
<servlet-mapping>
  <servlet-name>hello</servlet-name>
  <url-pattern>/hello</url-pattern>
</servlet-mapping>
```

## 6.2 The servlet lifecycle

The container manages a servlet through three methods of the `javax.servlet.Servlet` interface:

1. **`init(ServletConfig)`**: called **once**, when the servlet is first loaded (or at start-up with `load-on-startup`); open resources and read initialisation parameters here.
2. **`service(request, response)`**: called **for every request**, each in a *separate thread* of the same single servlet instance; `HttpServlet.service` looks at the HTTP method and calls `doGet`, `doPost`, `doPut`, `doDelete`, `doHead`, `doOptions` or `doTrace`.
3. **`destroy()`**: called **once** before the servlet is removed (shutdown or redeploy); release resources.

Because one instance serves many threads, **never keep per-request data in instance fields**: they would be shared between users. Use local variables, the request, or the session. If you must share state, synchronise it (or use thread-safe classes). Unhandled methods return `405 Method Not Allowed` from the default implementation.

### The request and response objects

`HttpServletRequest` gives the **method**, URL parts (`getRequestURI`, `getContextPath`), **parameters** (`getParameter("name")` for query string and form fields, `getParameterValues`), **headers** (`getHeader`), cookies, the **session** (`getSession()`), the input stream and, for forwarding, a `RequestDispatcher`. Attributes (`setAttribute`/`getAttribute`) carry objects from a servlet to a JSP in the same request. `HttpServletResponse` sets the **status** (`setStatus`, `sendError`), **headers**, **content type**, cookies, and provides the **writer** (`getWriter()`) or output stream for the body; `sendRedirect(url)` tells the browser to request another URL (a 302). The difference to remember: **forward** is internal to the server (one request, URL unchanged), **redirect** is a new browser request (URL changes; use it after a POST so a page refresh does not re-submit the form).

```java
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.lang.reflect.*;
import java.util.*;
public class ServletDemo {
    public static class HelloServlet extends HttpServlet {
        @Override public void init() { System.out.println("[container] init() called once"); }
        @Override protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
            String name = req.getParameter("name");
            if (name == null || name.isBlank()) name = "guest";
            HttpSession session = req.getSession();
            Integer visits = (Integer) session.getAttribute("visits");
            visits = (visits == null) ? 1 : visits + 1;
            session.setAttribute("visits", visits);
            resp.setContentType("text/html;charset=UTF-8");
            PrintWriter out = resp.getWriter();
            out.println("<h1>Hello, " + escape(name) + "</h1>");
            out.println("<p>visit number " + visits + "</p>");
        }
        @Override protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
            resp.setStatus(HttpServletResponse.SC_CREATED);
            resp.getWriter().println("created " + req.getParameter("item"));
        }
        @Override public void destroy() { System.out.println("[container] destroy() called once"); }
        static String escape(String s) { return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;"); }
    }
    static class Reply { int status = 200; String type = "-"; StringWriter body = new StringWriter(); }
    static <T> T mock(Class<T> type, InvocationHandler h) { return type.cast(Proxy.newProxyInstance(ServletDemo.class.getClassLoader(), new Class<?>[]{type}, h)); }
    static HttpServletRequest request(String method, Map<String, String> params, Map<String, Object> sessionData) {
        HttpSession hs = mock(HttpSession.class, (p, m, a) -> switch (m.getName()) {
            case "getAttribute" -> sessionData.get((String) a[0]);
            case "setAttribute" -> { sessionData.put((String) a[0], a[1]); yield null; }
            default -> null; });
        return mock(HttpServletRequest.class, (p, m, a) -> switch (m.getName()) {
            case "getMethod" -> method;
            case "getProtocol" -> "HTTP/1.1";
            case "getParameter" -> params.get((String) a[0]);
            case "getSession" -> hs;
            default -> null; });
    }
    static HttpServletResponse response(Reply r) {
        return mock(HttpServletResponse.class, (p, m, a) -> switch (m.getName()) {
            case "setContentType" -> { r.type = (String) a[0]; yield null; }
            case "setStatus", "sendError" -> { r.status = (Integer) a[0]; yield null; }
            case "getWriter" -> new PrintWriter(r.body, true);
            default -> null; });
    }
    static void call(HelloServlet s, String method, Map<String, String> params, Map<String, Object> session) throws Exception {
        Reply r = new Reply();
        s.service((ServletRequest) request(method, params, session), (ServletResponse) response(r));
        System.out.println(method + " " + params + " -> status " + r.status + ", type " + r.type + ", body: " + r.body.toString().trim().replace("\n", " | "));
    }
    public static void main(String[] args) throws Exception {
        HelloServlet servlet = new HelloServlet();
        servlet.init(mock(ServletConfig.class, (p, m, a) -> null));
        Map<String, Object> session = new HashMap<>();
        call(servlet, "GET", Map.of("name", "Sita"), session);
        call(servlet, "GET", Map.of(), session);
        call(servlet, "GET", Map.of("name", "<script>alert(1)</script>"), session);
        call(servlet, "POST", Map.of("item", "notebook"), session);
        call(servlet, "DELETE", Map.of(), session);
        servlet.destroy();
    }
}
```
```output
[container] init() called once
GET {name=Sita} -> status 200, type text/html;charset=UTF-8, body: <h1>Hello, Sita</h1> | <p>visit number 1</p>
GET {} -> status 200, type text/html;charset=UTF-8, body: <h1>Hello, guest</h1> | <p>visit number 2</p>
GET {name=<script>alert(1)</script>} -> status 200, type text/html;charset=UTF-8, body: <h1>Hello, &lt;script&gt;alert(1)&lt;/script&gt;</h1> | <p>visit number 3</p>
POST {item=notebook} -> status 201, type -, body: created notebook
DELETE {} -> status 405, type -, body: 
[container] destroy() called once
```
The same session map is passed to every request, as a browser's session cookie would make the container do, so the visit counter goes 1, 2, 3. The `<script>` parameter is escaped to harmless text (see 6.6); `POST` produces status 201; `DELETE` is not implemented so the default `doDelete` answers with status 405. `init` and `destroy` each run once, however many requests are served.

## 6.3 GET and POST, forms and parameters

A form `<form action="login" method="post">` sends its fields in the **request body** with POST (or in the URL with GET). Use **GET** for safe, repeatable retrieval (searches, page views): parameters appear in the URL, can be bookmarked and cached, and must never carry passwords. Use **POST** for actions that change state and for sensitive or large data. In both cases the servlet reads `request.getParameter("field")`. Set `request.setCharacterEncoding("UTF-8")` before reading parameters so Nepali text in a form is decoded correctly.

## 6.4 Session management

HTTP is stateless (Computer Networking, Unit 6), so the server needs a way to recognise a returning browser. The four techniques:

| Technique | How | Remark |
|---|---|---|
| **Cookies** | server sends `Set-Cookie`, browser returns `Cookie` on each request; `new Cookie(name, value)`, `response.addCookie(c)`, `request.getCookies()` | stored in the browser, size-limited, user can disable |
| **URL rewriting** | session ID appended to every URL (`;jsessionid=...`); `response.encodeURL(url)` | works without cookies; ID is visible in the URL |
| **Hidden form fields** | the state is carried in `<input type="hidden">` | only for form flows |
| **`HttpSession`** | container keeps a server-side map per user, identified by the `JSESSIONID` cookie (falling back to URL rewriting) | the standard answer |

`request.getSession()` returns the current session, creating one if needed (`getSession(false)` returns null instead). Use `setAttribute`/`getAttribute` for per-user data (the logged-in user, a shopping cart), `setMaxInactiveInterval(seconds)` for the time-out and **`invalidate()`** to end the session at logout. After login, create a **new** session ID (`request.changeSessionId()`) to prevent session fixation.

## 6.5 Filters, listeners and the request dispatcher

- A **filter** (`javax.servlet.Filter`) intercepts requests before and after servlets: authentication checks, logging, compression, character-encoding setup. Its `doFilter(req, res, chain)` does its work and calls `chain.doFilter(req, res)` to continue (or stops the chain, for example to redirect to the login page).
- **Listeners** react to lifecycle events: `ServletContextListener` (application start and stop: open the connection pool), `HttpSessionListener` (session created or destroyed: count online users), `ServletRequestListener`, and attribute listeners.
- A **`RequestDispatcher`** (`request.getRequestDispatcher("/result.jsp").forward(request, response)`) passes control to another resource inside the server, the key operation of MVC below.
- The **`ServletContext`** is shared by the whole application (`getServletContext()`): application-wide attributes and initialisation parameters. `ServletConfig` is per servlet.

## 6.6 Security basics for servlets

- **Escape output.** Writing user input into HTML without escaping lets an attacker inject a `<script>` (**cross-site scripting**, XSS). The `escape` method above turns `<` and `>` into entities; JSTL's `<c:out>` does it automatically.
- **Use `PreparedStatement`** for SQL (Unit 3).
- **Never trust hidden fields or cookies**; verify on the server.
- Use HTTPS, mark session cookies `HttpOnly` and `Secure`, regenerate the session ID on login, and add a CSRF token to state-changing forms.
- Declare **security constraints** in `web.xml` or use a framework for authentication and role checks.

## 6.7 JavaServer Pages (JSP)

A servlet that prints HTML with `out.println` is tedious for designers. A **JSP** is an HTML file containing special tags; on the first request the container **translates** it into a servlet class (`_result_jsp.java`), compiles it, and from then on runs the servlet (so JSP and servlet have the same lifecycle: translation, compilation, `jspInit`, `_jspService` per request, `jspDestroy`).

```text
<%@ page contentType="text/html;charset=UTF-8" import="java.util.*" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html><body>
<%! int hits = 0; %>
<% hits++; String name = request.getParameter("name"); %>
<h1>Hello, <%= name == null ? "guest" : name %></h1>
<p>Page views since start: <%= hits %></p>
<c:forEach var="s" items="${students}">
  <li><c:out value="${s.name}"/>: ${s.marks}</li>
</c:forEach>
</body></html>
```

| Element | Syntax | Meaning |
|---|---|---|
| Directive | `<%@ page ... %>`, `<%@ include file="..." %>`, `<%@ taglib ... %>` | page settings, static include, tag libraries (processed at translation time) |
| Scriptlet | `<% java code %>` | code placed inside `_jspService` |
| Expression | `<%= expr %>` | value printed into the output |
| Declaration | `<%! int hits = 0; %>` | field or method of the generated class (shared by all requests) |
| Comment | `<%-- hidden --%>` | not sent to the browser |
| Action | `<jsp:include page="..."/>`, `<jsp:forward>`, `<jsp:useBean>`, `<jsp:getProperty>` | run-time actions |
| EL | `${student.name}` | expression language: reads attributes and bean properties |
| JSTL | `<c:if>`, `<c:forEach>`, `<c:out>`, `<fmt:formatNumber>`, `<sql:query>` | standard tag library replacing most scriptlets |

**Implicit objects** available in a JSP without declaration: `request`, `response`, `out`, `session`, `application` (the `ServletContext`), `config`, `pageContext`, `page`, `exception` (on error pages). **Scopes** for attributes: page, request, session, application; EL searches them in that order.

Modern practice is **no Java in JSP**: scriptlets mix logic with markup, are hard to test and are a security risk, so JSPs use EL and JSTL only and a servlet does the work.

## 6.8 The MVC pattern with servlets and JSP

**Model 2 (MVC)**: a **controller servlet** receives the request, validates input and calls the **model** (plain Java classes and DAOs, Unit 3); it puts the result in the request as an attribute and **forwards** to a **view** (a JSP) that only displays it.

```text
Browser ──GET /students──▶ StudentServlet (controller)
                              │ calls StudentDao.findAll()          (model)
                              │ request.setAttribute("students", list)
                              ▼ forward
                           students.jsp (view) ──HTML──▶ Browser
```

The benefits: designers edit the JSP, programmers the servlet and DAO; logic is testable; one model serves many views. Frameworks (Spring MVC, Struts, Jakarta Faces) are elaborations of this idea. A complete small application therefore needs: a table and DAO (Unit 3), a controller servlet mapped with `@WebServlet`, a JSP with `<c:forEach>` and a `web.xml` (or annotations) – all packaged in a WAR.

## 6.9 Seeing the ideas: containers, sessions, filters and JSP

Server-side Java is easier to learn when you can see what the container does between the browser and your code. Plate 6.1 gives four pictures for the mechanisms of this unit: railway points for the request dispatcher, a security checkpoint for a filter chain, a lettering template for a JSP page and a paper form for a POST request. Plate 6.2 shows four everyday session tokens: a bus ticket, a luggage tag, a hotel key card and a cookie. Plate 6.3 shows the switchboard of the container, the inventor of MVC and the inventor of the web. Figures 6.1 to 6.13 then use numbers from one real run of Apache Tomcat 9.0.89, embedded in a Java 17 program, with servlets, two filters, two listeners, JSP pages with JSTL and a client that sent real HTTP requests and counted what came back.

```photogrid label="6.1" cols="4" ratio="1.0" caption="Four pictures for the container's machinery. (a) Railway points (CC BY-SA 3.0): a switch blade sends the same train down one of two tracks, as a RequestDispatcher forwards a request to a servlet or a JSP. (b) Passengers queueing at an airport security checkpoint (CC BY 2.0): every person passes the same checks in order before reaching the gate, like a filter chain before a servlet. (c) A set of plastic lettering templates (public domain, CIA): fixed holes with shapes to fill, like a JSP page of fixed markup with places for dynamic values. (d) Paper voter-registration forms on a clipboard (CC BY-SA 4.0): the fields are the form, and handing it over is a POST request with the data in the body."
@ photo id="bca303/points" cap="Railway points: the dispatcher"
fit 1.0
focus 0.5 0.55
call 0.5 0.55 0.8 0.2 "switch"
@ photo id="bca303/security" cap="Security checkpoint: filters"
fit 1.0
focus 0.5 0.6
@ photo id="bca303/lettering" cap="Lettering templates: JSP"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/voterform" cap="Paper form: POST"
fit 1.0
focus 0.5 0.8
```

```photogrid label="6.2" cols="4" ratio="1.0" caption="Four session tokens from daily life. (a) Paper bus tickets (CC BY 4.0): the ticket proves a payment without the conductor remembering your face, as the session id proves a visit. (b) A railway-hotel luggage label (public domain): a short mark on the bag leads the porter to the right owner, as the id leads the server to the right data. (c) A hotel key card (CC BY 2.0): the card holds only a code and opens only the room that the hotel's computer has linked to it, so the data stays in the hotel. (d) A chocolate-chip cookie (public domain): a small piece handed to you and brought back next time, the pun behind the name of the browser cookie."
@ photo id="bca303/busticket" cap="Bus tickets: an id as proof"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/luggagetag" cap="Luggage tag: an id on the bag"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/hotelkey" cap="Key card: a code, data elsewhere"
fit 1.0
focus 0.6 0.4
@ photo id="bca303/cookie" cap="A cookie: a token to bring back"
fit 1.0
focus 0.5 0.5
```

```photogrid label="6.3" cols="3" ratio="1.0" caption="The container, the pattern and the protocol. (a) A telephone switchboard (CC BY-SA 4.0): the operator listens, then connects each caller to the right line, as the container accepts every request and maps its URL to a servlet. (b) Trygve Reenskaug (CC BY-SA 3.0), who described the model-view-controller idea at Xerox PARC in 1979, the pattern behind Section 6.8. (c) Tim Berners-Lee (CC BY-SA 4.0), who proposed HTTP and the web at CERN in 1989, the protocol that every servlet speaks."
@ photo id="bca303/switchboard" cap="Switchboard: URL to servlet"
fit 1.0
focus 0.3 0.6
@ photo id="bca303/reenskaug" cap="Trygve Reenskaug: MVC"
fit 1.0
focus 0.5 0.4
@ photo id="bca301/berners" cap="Tim Berners-Lee: HTTP"
fit 1.0
focus 0.5 0.6
```

```svgfig label="6.1" caption="A web application inside a container, from a real embedded Tomcat 9.0.89 run. Left: the folder layout. Everything outside WEB-INF is public; WEB-INF holds web.xml, the compiled classes, the libraries and the views, and is never served: a request for /WEB-INF/views/list.jsp returned status 404. Right: how the container reads a URL, with the context path (the application, empty here) and the servlet path /hello that was mapped to the Hello servlet. The container started in 722 ms in the run, including the JSP engine."
f = Fig(580, 262)
f.text(150, 14, "folder layout of the web application", size=11, color=NAVY, bold=True)
f.box(10, 24, 280, 226, "", fill=SOFT, stroke="#cbd5e1")
rows = [("college/", 0, NAVY), ("index.html, css/, images/", 1, TEAL), ("pages/result.jsp", 1, TEAL), ("WEB-INF/", 1, RED), ("web.xml", 2, RED), ("classes/  compiled servlets", 2, RED), ("lib/  JSTL, JDBC driver", 2, RED), ("views/list.jsp", 2, RED)]
for i, (t, d, c) in enumerate(rows):
    f.text(22 + d * 18, 42 + i * 24, t, size=10, color=c, anchor="start", bold=(d == 0))
f.text(150, 238, "teal: public     red: never served (404)", size=9.5, color=SLATE, bold=True)
f.text(435, 14, "reading a URL", size=11, color=NAVY, bold=True)
f.box(300, 28, 270, 26, "http://127.0.0.1:18080/hello?name=Sita", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
parts = [("host and port", "127.0.0.1:18080: the connector", AMBER, SAND), ("context path", "empty: the application root", TEAL, MINT), ("servlet path", "/hello -> Hello servlet", NAVY, BLUE), ("query string", "name=Sita -> getParameter", RED, ROSE)]
for i, (a, b, st, fl) in enumerate(parts):
    y = 70 + i * 36
    f.box(300, y, 88, 28, a, fill=fl, stroke=st, size=9, bold=True)
    f.box(392, y, 178, 28, b, fill="#ffffff", stroke=st, size=9, color=SLATE)
f.box(300, 216, 270, 34, "GET /WEB-INF/views/list.jsp -> 404\nthe container hides WEB-INF", fill=ROSE, stroke=RED, size=9.5, bold=True)
```

```svgfig label="6.2" caption="The servlet lifecycle, read from the log of a real run. The container reported context initialized, then the servlet's init() ran once, at the first request; five requests followed and all five went through doGet() of one single servlet instance (the identity hash codes gave a set of size 1), on pool threads named http-nio-18080-exec-n. At shutdown destroy() ran once and then the context was destroyed. Two filters wrapped each request, as shown in Figure 6.10."
f = Fig(580, 214)
seq = [("context\ninitialized", SAND, AMBER, 96), ("init()\nonce", MINT, TEAL, 80), ("doGet() x 5\nrequests 1 to 5", BLUE, NAVY, 150), ("destroy()\nonce", ROSE, RED, 90), ("context\ndestroyed", SAND, AMBER, 96)]
gap = (560 - sum(q[3] for q in seq)) / (len(seq) - 1)
x = 10
for i, (t, fl, st, w) in enumerate(seq):
    f.box(x, 34, w, 40, t, fill=fl, stroke=st, size=9.5, bold=True)
    if i < len(seq) - 1:
        f.arrow([(x + w, 54), (x + w + gap, 54)], color=SLATE, sw=1.2)
    x += w + gap
f.text(290, 18, "events in the order of the log", size=11, color=NAVY, bold=True)
inits, services, inst = 1, 5, 1
f.box(10, 100, 170, 50, "init() calls: %d\nservice calls: %d" % (inits, services), fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(205, 100, 170, 50, "servlet instances: %d\nfor all requests" % inst, fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(400, 100, 170, 50, "threads: http-nio-\n18080-exec-n (pool)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(290, 176, "one instance, many threads: instance fields are shared by every user", size=10, color=RED, bold=True)
f.text(290, 196, "init() runs lazily at the first request unless load-on-startup is set", size=9.5, color=SLATE)
```

```svgfig label="6.3" caption="One real HTTP exchange with the servlet. The request GET /hello carried no cookie. The reply was status 200 with four headers: content-length 24, content-type text/html;charset=UTF-8, date and set-cookie, whose value was JSESSIONID=id; Path=/; HttpOnly. The body was visit 1 sid 32 new true: the container created a session, whose identifier has 32 characters. The length 24 is the byte count of that body line, so no chunked transfer-encoding was needed."
f = Fig(580, 246)
f.text(145, 14, "request", size=11, color=NAVY, bold=True)
f.box(10, 24, 270, 62, "", fill=BLUE, stroke=NAVY)
for i, t in enumerate(["GET /hello HTTP/1.1", "Host: 127.0.0.1:18080", "(no Cookie header)", "(blank line ends the headers)"]):
    f.text(20, 38 + i * 14, t, size=9.5, color=NAVY if i < 2 else SLATE, anchor="start", bold=(i == 0))
f.text(435, 14, "response", size=11, color=TEAL, bold=True)
f.box(300, 24, 270, 130, "", fill=MINT, stroke=TEAL)
body = "visit 1 sid 32 new true"
assert len(body) + 1 == 24
for i, (t, c, b) in enumerate([("HTTP/1.1 200", TEAL, True), ("Content-Type: text/html;charset=UTF-8", SLATE, False), ("Content-Length: 24", SLATE, False), ("Date: (server time)", SLATE, False), ("Set-Cookie: JSESSIONID=<32 chars>;", RED, True), ("      Path=/; HttpOnly", RED, True), ("", SLATE, False), (body, NAVY, True)]):
    f.text(308, 38 + i * 14, t, size=9, color=c, anchor="start", bold=b)
f.arrow([(280, 60), (300, 60)], color=AMBER)
f.box(10, 110, 270, 44, "24 = 23 characters + 1 newline\nso Content-Length is known, not chunked", fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(10, 170, 560, 66, "", fill=SOFT, stroke="#cbd5e1")
for i, t in enumerate(["HttpOnly: JavaScript in the page cannot read the cookie, which limits session theft by XSS.", "Path=/: the browser returns the cookie for every URL of the site.", "The session id is 32 hex characters = 128 bits; the server keeps the data, the browser keeps only the id."]):
    f.text(20, 186 + i * 18, t, size=9, color=SLATE, anchor="start")
```

```svgfig label="6.4" caption="Status codes of the real run. GET /hello gave 200; POST /hello with item=notebook gave 201 and the body created notebook (the servlet called setStatus(201)); DELETE /hello gave 405 because the servlet does not override doDelete; GET /missing gave 404; GET /boom gave 500 because the servlet threw IllegalStateException: database is down, and the container wrote the stack trace to its log, not to the visitor; /old gave 302 with a Location header; /fwd gave 200."
f = Fig(580, 280)
for t, x, w in [("request", 10, 170), ("status", 184, 60), ("what happened", 248, 322)]:
    f.box(x, 6, w, 22, t, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=3)
rows = [("GET /hello", "200", "doGet ran; session created", TEAL, MINT), ("POST /hello item=notebook", "201", "doPost: setStatus(201), body created notebook", TEAL, MINT), ("DELETE /hello", "405", "no doDelete: HttpServlet answers Method Not Allowed", AMBER, SAND), ("GET /missing", "404", "no servlet or file for this URL", AMBER, SAND), ("GET /boom", "500", "IllegalStateException: stack trace in the log only", RED, ROSE), ("GET /old", "302", "sendRedirect: Location /new, the browser asks again", NAVY, BLUE), ("GET /fwd", "200", "forward: handled inside the server, one request", NAVY, BLUE)]
for i, (a, b, c, st, fl) in enumerate(rows):
    y = 34 + i * 32
    f.box(10, y, 170, 28, a, fill="#ffffff", stroke="#cbd5e1", color=SLATE, size=9, r=3)
    f.box(184, y, 60, 28, b, fill=fl, stroke=st, size=11, bold=True, r=3)
    f.box(248, y, 322, 28, c, fill="#ffffff", stroke="#cbd5e1", color=SLATE, size=9, r=3)
f.text(290, 270, "2xx success   3xx redirect   4xx client error   5xx server error", size=9, color=SLATE)
```

```svgfig label="6.5" caption="Redirect against forward, counted in the real run. For GET /old the servlet called sendRedirect: the reply was status 302 with Location /new and the target servlet had not run (hit count 0); the browser must send a second request, and its address bar changes. For GET /fwd the servlet called getRequestDispatcher(/new).forward: the client saw one request, status 200 and the body new page, the target servlet ran once (hit count 1) and the address stays /fwd. Use forward inside the application (MVC) and redirect after a POST so that a refresh does not repeat it."
f = Fig(580, 262)
f.text(145, 14, "redirect: two requests", size=11, color=RED, bold=True)
f.text(435, 14, "forward: one request", size=11, color=TEAL, bold=True)
f.line(290, 22, 290, 250, color="#cbd5e1", sw=2)
for x0, c in [(0, RED), (290, TEAL)]:
    f.text(x0 + 60, 36, "browser", size=10, color=NAVY, bold=True)
    f.text(x0 + 230, 36, "server", size=10, color=c, bold=True)
    f.line(x0 + 60, 44, x0 + 60, 200, color="#e2e8f0", sw=2)
    f.line(x0 + 230, 44, x0 + 230, 200, color="#e2e8f0", sw=2)
f.arrow([(64, 62), (226, 62)], color=NAVY, label="GET /old", lpos=(145, 56), lsize=9)
f.arrow([(226, 92), (64, 92)], color=RED, label="302 Location /new", lpos=(145, 86), lsize=9)
f.arrow([(64, 124), (226, 124)], color=NAVY, label="GET /new", lpos=(145, 118), lsize=9)
f.arrow([(226, 154), (64, 154)], color=TEAL, label="200 new page", lpos=(145, 148), lsize=9)
f.arrow([(354, 62), (516, 62)], color=NAVY, label="GET /fwd", lpos=(435, 56), lsize=9)
f.box(380, 78, 140, 34, "inside the server:\nforward to /new", fill=MINT, stroke=TEAL, size=9, bold=True)
f.arrow([(516, 134), (354, 134)], color=TEAL, label="200 new page", lpos=(435, 128), lsize=9)
f.box(10, 208, 270, 44, "address bar becomes /new\nmeasured: first reply 302, /new ran 0 times", fill=ROSE, stroke=RED, size=9, bold=True)
f.box(300, 208, 270, 44, "address bar stays /fwd\nmeasured: status 200, /new ran 1 time", fill=MINT, stroke=TEAL, size=9, bold=True)
```

```svgfig label="6.6" caption="Why instance fields are dangerous, shown with a real pair of requests. The Unsafe servlet stored the parameter n in a field, slept 150 ms and printed the field. Sita's request started at time 0 and Ram's at 50 ms; Ram's request overwrote the field, so Sita's page said hello Ram, a privacy bug. The Safe servlet kept n in a local variable and each visitor saw their own name. A servlet is one object shared by all threads, so per-request data belongs in local variables, the request or the session."
f = Fig(580, 262)
f.text(290, 14, "time in ms (to scale), one servlet instance", size=11, color=NAVY, bold=True)
sc = 2.2
def X(t): return 90 + t * sc
f.text(10, 60, "Sita", size=10, color=NAVY, anchor="start", bold=True)
f.text(10, 100, "Ram", size=10, color=TEAL, anchor="start", bold=True)
f.text(10, 140, "field", size=10, color=RED, anchor="start", bold=True)
f.box(X(0), 44, 150 * sc, 28, "Sita: sleeps 150 ms", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.box(X(50), 86, 150 * sc, 28, "Ram: sleeps 150 ms", fill=MINT, stroke=TEAL, size=9, bold=True)
f.box(X(0), 126, 50 * sc, 28, "Sita", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.box(X(50), 126, 150 * sc, 28, "Ram (overwritten)", fill=ROSE, stroke=RED, size=9, bold=True)
f.arrow([(X(150), 72), (X(150), 124)], color=RED, dash=True)
f.text(X(150) + 6, 98, "Sita reads Ram", size=9, color=RED, bold=True, anchor="start")
for t in (0, 50, 150, 200):
    f.line(X(t), 160, X(t), 168, color=SLATE)
    f.text(X(t), 180, str(t), size=9, color=SLATE)
f.box(10, 196, 275, 56, "Unsafe: field current\nSita sees [hello Ram]\nRam sees [hello Ram]", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(295, 196, 275, 56, "Safe: local variable me\nSita sees [hello Sita]\nRam sees [hello Ram]", fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

```svgfig label="6.7" caption="Concurrency and speed of the container, measured. Four clients each asked for a page that sleeps 200 ms: the container served them in parallel threads and finished in 205 ms, while four requests one after another took 811 ms, a speed-up of 3.96 (computed). For a trivial page, 2,000 sequential requests from the Java HttpClient took 456 microseconds each on the loopback interface, which is about 2,190 requests per second for one client thread."
f = Fig(580, 200)
seq, con, lat = 811, 205, 456
sp = seq / con
assert 3.9 < sp < 4.0
rate = 1e6 / lat
assert 2190 < rate < 2195
sc = 380 / 811
f.text(290, 14, "4 requests of 200 ms (to scale, ms)", size=11, color=NAVY, bold=True)
f.text(10, 42, "one by one", size=10, color=SLATE, anchor="start", bold=True)
for i in range(4):
    f.box(110 + i * 200 * sc, 28, 200 * sc - 2, 24, "200", fill=SAND, stroke=AMBER, size=9, bold=True)
f.text(110 + seq * sc + 6, 40, "811 ms", size=10, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(10, 100, "together", size=10, color=SLATE, anchor="start", bold=True)
for i in range(4):
    f.box(110, 66 + i * 22, con * sc, 18, "thread %d" % (i + 1), fill=MINT, stroke=TEAL, size=9, bold=True, r=3)
f.text(110 + con * sc + 6, 108, "205 ms", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(290, 168, "speed-up = 811 / 205 = %.2f" % sp, size=10.5, color=NAVY, bold=True)
f.text(290, 186, "trivial page: 456 us per request = %s requests per second per client" % format(round(rate), ","), size=9.5, color=SLATE, bold=True)
```

```svgfig label="6.8" caption="Session tracking, step by step, from the real run. The first request had no cookie: the container created a session and sent Set-Cookie, and the page said visit 1. The next three requests sent that cookie back and said visit 2, 3 and 4, with no Set-Cookie in the replies. A request without the cookie got visit 1 and a different id. After /logout called invalidate(), the old cookie was useless and the next request said visit 1, new true. The data lives in the server; the browser holds only the 32-character id."
f = Fig(580, 332)
for t, x, c in [("browser", 100, NAVY), ("server (session table)", 440, TEAL)]:
    f.text(x, 14, t, size=11, color=c, bold=True)
    f.line(x, 22, x, 290, color="#cbd5e1", sw=2)
steps = [(40, "GET /hello  (no cookie)", "visit 1, Set-Cookie: JSESSIONID", NAVY, TEAL), (88, "GET /hello  Cookie: id", "visit 2 (no Set-Cookie)", NAVY, TEAL), (136, "GET /hello  Cookie: id", "visit 3", NAVY, TEAL), (184, "GET /hello  Cookie: id", "visit 4", NAVY, TEAL), (232, "GET /hello  (cookie dropped)", "visit 1, a new id", AMBER, AMBER), (280, "GET /logout, then old cookie", "invalidate(): visit 1, new true", RED, RED)]
for y, a, b, c1, c2 in steps:
    f.arrow([(104, y), (436, y)], color=c1, label=a, lpos=(270, y - 5), lsize=8.5)
    f.arrow([(436, y + 20), (104, y + 20)], color=c2, label=b, lpos=(270, y + 15), lsize=8.5)
f.text(290, 322, "ids differ: 16^32 = 2^128 = %s possible ids, so guessing one is hopeless" % format(16 ** 32, ",").split(",")[0] + "e+" + str(len(str(16 ** 32)) - 1) if False else "128-bit id: 16^32 = 2^128, about 3.4 x 10^38 possible values", size=9.5, color=SLATE, bold=True)
assert 3.4e38 < 16 ** 32 < 3.5e38
```

```svgfig label="6.9" caption="Three ways the session id can travel. A cookie (Set-Cookie and Cookie headers) keeps the id out of the address; URL rewriting, produced by response.encodeURL, gave /hello;jsessionid= followed by the 32 hex characters, a 50-character path (computed); a hidden form field carries state only inside a form. The URL form is the weakest because the id is visible in the address bar, history, server logs and the Referer header, so a cookie with HttpOnly (and Secure over HTTPS) is the standard choice."
f = Fig(580, 206)
u = "/hello;jsessionid=" + "A" * 32
assert len(u) == 50
cols = [("Cookie", "Set-Cookie / Cookie headers", "not in the URL;\nHttpOnly, Secure possible", "best: the standard", TEAL, MINT), ("URL rewriting", "/hello;jsessionid=<32 hex>", "50 characters; visible in\nhistory, logs, Referer", "fallback only", RED, ROSE), ("Hidden field", "<input type=hidden ...>", "only inside a\nform flow", "for wizards", AMBER, SAND)]
for i, (t, a, b, c, st, fl) in enumerate(cols):
    x = 10 + i * 190
    f.box(x, 8, 180, 26, t, fill=st, stroke=st, color="#ffffff", size=10.5, bold=True, r=4)
    f.box(x, 40, 180, 40, a, fill=fl, stroke=st, size=8.5, bold=True)
    f.box(x, 86, 180, 52, b, fill="#ffffff", stroke=st, size=8.5, color=SLATE)
    f.box(x, 144, 180, 26, c, fill=fl, stroke=st, size=9.5, bold=True)
f.text(290, 192, "encodeURL(url) adds the id only when the browser has not returned a cookie", size=9.5, color=SLATE, bold=True)
```

```svgfig label="6.10" caption="A filter chain, shown with the real log of a request to /hello with two filters A and B registered in that order: filter A before, filter B before, servlet doGet, filter B after, filter A after. Each filter calls chain.doFilter to pass the request inward, and the code after that call runs on the way out, like layers of an onion; a filter that does not call it stops the request (for example a login check). Typical filters log, compress, set UTF-8 or check the session."
f = Fig(580, 210)
f.box(10, 10, 260, 190, "", fill=SAND, stroke=AMBER)
f.text(140, 24, "Filter A", size=10.5, color=AMBER, bold=True)
f.box(34, 36, 212, 150, "", fill=BLUE, stroke=NAVY)
f.text(140, 50, "Filter B", size=10.5, color=NAVY, bold=True)
f.box(64, 66, 152, 100, "", fill=MINT, stroke=TEAL)
f.text(140, 116, "servlet doGet", size=10.5, color=TEAL, bold=True)
f.arrow([(0, 100), (62, 100)], color=SLATE)
log = ["1  filter A before", "2  filter B before", "3  servlet doGet", "4  filter B after", "5  filter A after"]
f.text(430, 18, "order in the real log", size=11, color=NAVY, bold=True)
for i, t in enumerate(log):
    fl, st = [(SAND, AMBER), (BLUE, NAVY), (MINT, TEAL), (BLUE, NAVY), (SAND, AMBER)][i]
    f.box(320, 30 + i * 32, 220, 26, t, fill=fl, stroke=st, size=10, bold=True, anchor="start")
f.text(430, 198, "no chain.doFilter(): the request stops here", size=9.5, color=RED, bold=True)
```

```svgfig label="6.11" caption="What happens to a JSP, with real measurements. The first request for demo.jsp took 474 ms because the container translated the page to a servlet (class org.apache.jsp.demo_jsp), compiled it and loaded it; the second request took 1 ms, a ratio of 474 (computed). The page printed scriptlet=10 (the sum 1+2+3+4), sum=5 from the expression language form of 2+3, loop=[1][2][3] from the JSTL forEach tag, and method GET from an implicit object. A JSP is therefore a servlet written the other way round: HTML with Java inside."
f = Fig(580, 250)
steps = [("demo.jsp\nHTML + tags", SAND, AMBER), ("translate", BLUE, NAVY), ("demo_jsp.java\na servlet", BLUE, NAVY), ("compile", BLUE, NAVY), ("demo_jsp.class\nloaded once", MINT, TEAL), ("service()\neach request", MINT, TEAL)]
for i, (t, fl, st) in enumerate(steps):
    x = 8 + i * 96
    f.box(x, 24, 84, 44, t, fill=fl, stroke=st, size=8.5, bold=True)
    if i < 5:
        f.arrow([(x + 84, 46), (x + 96, 46)], color=SLATE, sw=1.2)
f.text(145, 14, "translated once, then the class is reused", size=10.5, color=NAVY, bold=True)
first, second = 474, 1
f.box(10, 90, 270, 26, "first request  474 ms (translate + compile)", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(10, 122, 270 * 6 / 474 + 2, 26, "", fill=MINT, stroke=TEAL, r=2)
f.text(10 + 270 * 6 / 474 + 12, 135, "second request  1 ms", size=9.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(145, 168, "ratio = %d (computed)" % (first / second), size=10, color=NAVY, bold=True)
rows = [("<%= n %> after a scriptlet", "scriptlet=10", AMBER), ("${2+3}", "sum=5", NAVY), ("<c:forEach begin=1 end=3>", "loop=[1][2][3]", TEAL), ("${pageContext.\nrequest.method}", "method=GET", RED)]
n = sum(range(1, 5)); assert n == 10
for i, (a, b, c) in enumerate(rows):
    y = 90 + i * 38
    f.box(300, y, 150, 30, a, fill="#ffffff", stroke=c, color=SLATE, size=9, r=3)
    f.arrow([(450, y + 15), (462, y + 15)], color=SLATE, sw=1.2)
    f.box(462, y, 108, 30, b, fill=SOFT, stroke=c, size=9, bold=True, r=3)
f.box(10, 190, 270, 50, "class name printed by the page:\norg.apache.jsp.demo_jsp", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.text(435, 244, "four kinds of JSP element, real output", size=9, color=SLATE, bold=True)
```

```svgfig label="6.12" caption="Two output bugs, reproduced. Left: with q equal to <b>x</b>, the expression param.q in dollar-brace form wrote the text unchanged, so a browser would run it as HTML (and as a script if q held a script tag), while the JSTL tag c:out wrote &lt;b&gt;x&lt;/b&gt;, which shows as plain text. Right: a POST body with the Devanagari word for namaste, 6 characters and 18 UTF-8 bytes, was decoded by default as ISO-8859-1 and gave 18 garbled characters; after request.setCharacterEncoding(UTF-8) it gave 6 correct characters."
f = Fig(580, 250)
f.text(145, 14, "escaping: q = <b>x</b>", size=11, color=NAVY, bold=True)
f.box(10, 28, 270, 54, "${param.q}\nwrites  <b>x</b>  unchanged", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.text(145, 98, "the browser runs it as HTML", size=9.5, color=RED, bold=True)
f.box(10, 112, 270, 54, "<c:out value=\"${param.q}\"/>\nwrites  &lt;b&gt;x&lt;/b&gt;", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.text(145, 182, "the browser shows the text", size=9.5, color=TEAL, bold=True)
f.box(10, 196, 270, 44, "rule: escape every value from a user,\nin servlets and in JSP", fill=SAND, stroke=AMBER, size=9, bold=True)
word = "\u0928\u092e\u0938\u094d\u0924\u0947"
b = len(word.encode("utf-8"))
assert len(word) == 6 and b == 18
f.text(435, 14, "POST body decoding", size=11, color=NAVY, bold=True)
f.box(300, 28, 270, 40, "the word has %d characters, %d UTF-8 bytes\nsent as 18 percent-groups %%E0%%A4..." % (len(word), b), fill=BLUE, stroke=NAVY, size=9, bold=True)
f.arrow([(435, 68), (435, 84)], color=SLATE)
f.box(300, 84, 130, 50, "default decoding\n18 characters\nmojibake", fill=ROSE, stroke=RED, size=9, bold=True)
f.box(440, 84, 130, 50, "setCharacterEncoding\n(UTF-8) first\n6 characters", fill=MINT, stroke=TEAL, size=9, bold=True)
f.text(435, 154, "call it before the first getParameter,", size=9.5, color=SLATE, bold=True)
f.text(435, 170, "best in a filter for every request", size=9.5, color=SLATE, bold=True)
f.box(300, 190, 270, 50, "GET reply: Content-Type text/plain;\ncharset=UTF-8, Content-Length 18", fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9)
```

```svgfig label="6.13" caption="The MVC pattern in the real run. A request for /students reached the controller servlet, which built the model (three Student objects, marks 78, 64 and 91, with the average computed as 77.67), stored it as request attributes and forwarded to /WEB-INF/views/list.jsp, the view, which printed a table row for each student and the average. The view lives under WEB-INF, so a direct request for it gave 404: the only way in is through the controller."
f = Fig(580, 236)
marks = [78, 64, 91]
avg = round(sum(marks) / 3, 2)
assert avg == 77.67
f.box(10, 80, 100, 50, "browser\nGET /students", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(150, 80, 120, 50, "Controller\nStudents servlet", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(150, 10, 120, 44, "Model\n3 Student objects", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(310, 80, 140, 50, "View\nWEB-INF/views/list.jsp", fill=ROSE, stroke=RED, size=9, bold=True)
f.box(480, 80, 90, 50, "HTML table\nand average", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.arrow([(110, 105), (150, 105)], color=NAVY, label="1", lpos=(130, 98))
f.arrow([(210, 80), (210, 54)], color=AMBER, label="2", lpos=(222, 70))
f.arrow([(270, 105), (310, 105)], color=AMBER, label="3 forward", lpos=(290, 98), lsize=8.5)
f.arrow([(450, 105), (480, 105)], color=RED, label="4", lpos=(465, 98))
f.text(290, 160, "model: Sita 78, Ram 64, Gita 91; average = (78 + 64 + 91) / 3 = %.2f" % avg, size=10, color=NAVY, bold=True)
f.box(10, 178, 270, 46, "GET /WEB-INF/views/list.jsp\n-> 404: the view is not public", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(300, 178, 270, 46, "controller: logic and routing\nview: markup only, no business code", fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

### 6.9.1 Eight uses of servlets and JSP in Nepal

Servlets and JSP are the older generation of Java web technology, and frameworks such as Spring MVC and Jakarta Faces are built on them, so every point below describes work that a BCA graduate may meet in a Nepali company or a college project.

1. **Result and admission portals.** On result day thousands of students send a GET request with a roll number or symbol number. The container serves each request in its own pool thread (Figure 6.7), so a slow request does not block the others. The servlet must escape the roll number before printing it and must keep it in a local variable, not in a field (Figures 6.6 and 6.12).
2. **Internet and mobile banking back ends.** After login, the server keeps the customer's data in an HttpSession and gives the browser only a 32-character id in a cookie with HttpOnly (Figures 6.3 and 6.8). A logout must call invalidate(), because the old cookie then leads to a fresh, empty session. A short inactivity time-out ends forgotten sessions at a cyber cafe.
3. **Government service portals.** A form for a passport, licence or tax service sends a long POST with names, dates and Nepali text. The servlet should call setCharacterEncoding(UTF-8) before reading the parameters, or a Nepali name arrives as 18 garbled characters instead of 6 (Figure 6.12). After saving, the servlet redirects to a thank-you page, so a refresh does not submit the form twice (Figure 6.5).
4. **Online shops and a shopping cart.** A shop keeps the items of each visitor in the session, so the cart survives from page to page although HTTP forgets every request (Figure 6.8). If a visitor blocks cookies, URL rewriting can carry the id, but it exposes the id in the address (Figure 6.9). Large shops store sessions in a shared cache so that several servers can serve the same visitor.
5. **College management systems.** Attendance, fee and exam systems are often built as MVC: a controller servlet reads the request, a model class fetches the data with JDBC (Unit 3), and a JSP in WEB-INF shows the table (Figure 6.13). Because the view is under WEB-INF, nobody can open it directly, and a change in design touches only the JSP.
6. **Hospital and clinic portals.** A filter checks, for every URL under /patient, that the session holds a logged-in user, and another filter writes an audit line with the time and the user (Figure 6.10). The servlets stay short because the repeated checks live in the filters. A filter that does not call chain.doFilter stops the request, which is how an unauthorised visitor is turned away.
7. **Utility bill payment pages.** A page that shows the dues of a customer and takes a payment must behave well when something fails. An uncaught exception produced status 500 with the stack trace written to the server log, not shown to the visitor (Figure 6.4). A payment form should be protected from double submission, using a redirect after POST and a unique request number.
8. **BCA projects and internships.** A common final-year project is a WAR deployed to Tomcat, with servlets for logic and JSP for pages. The first request for a JSP took 474 ms while the next took 1 ms (Figure 6.11), so a student should open every page once before a demonstration. Testing on the loopback address with the container embedded in the program, as this unit does, needs no installation of a server.

## Formula and fact sheet

- Lifecycle: `init()` once → `service()` per request (separate threads, one instance) → `destroy()` once.
- `HttpServlet.service` dispatches to `doGet`, `doPost`, …; unimplemented methods give 405.
- Per-request data in local variables, never in instance fields.
- Forward = server-side, same request, URL unchanged; redirect = new browser request (302).
- Session: `getSession()`, `setAttribute`, `invalidate()`; cookie `JSESSIONID`; URL rewriting `encodeURL`.
- JSP translated to a servlet; elements: directive, scriptlet, expression, declaration, action; EL `${}`, JSTL `c:`; implicit objects request, response, out, session, application, config, pageContext, page, exception.
- Escape output to stop XSS; `javax.servlet` (Tomcat 9 and below) became `jakarta.servlet` (Tomcat 10+).

## Chapter summary

- A servlet container runs Java servlets that turn HTTP requests into responses; one instance handles all requests concurrently, so state must not be kept in fields.
- The lifecycle is init once, service per request, destroy once; `HttpServlet` routes to doGet and doPost.
- Sessions overcome HTTP's statelessness with cookies, URL rewriting or `HttpSession`; filters and listeners add cross-cutting behaviour.
- JSP pages are translated into servlets; EL and JSTL keep Java out of the page; MVC separates controller servlet, model classes and JSP views.
- Escaping output, prepared statements, HTTPS and careful session handling are the basic defences.

## Practice

1. Explain the servlet lifecycle and say how many times each method is called.
2. Why must a servlet not store request-specific data in instance variables?
3. Write a servlet that reads the parameter `roll` and prints it with the escaping shown above.
4. Differentiate GET and POST; when would you use each?
5. Differentiate forward and redirect.
6. List the four session-tracking techniques and explain `HttpSession`.
7. What is a filter? Give two uses.
8. Describe the JSP life cycle and name five JSP elements.
9. What are the implicit objects of JSP and the four attribute scopes?
10. Draw the MVC flow of a student-list page using a servlet, a DAO and a JSP.
11. What is cross-site scripting and how do you prevent it?

::: note Answers and worked solutions
**1.** `init()` once after loading; `service()` for every request (calls `doGet` or `doPost`); `destroy()` once before unloading. In the demo run, five requests called `service` five times while `init` and `destroy` each printed once.
**2.** One servlet instance serves many requests in parallel threads, so an instance field is shared between users and causes data races and leaks of one user's data to another. Use local variables, the request or the session.
**3.** `protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException { String roll = req.getParameter("roll"); resp.setContentType("text/html;charset=UTF-8"); resp.getWriter().println("Roll: " + escape(roll)); }`
**4.** GET: parameters in the URL, safe and idempotent, cacheable and bookmarkable (search, view). POST: data in the body, for changes and sensitive or large data (login, order).
**5.** Forward: server-internal handover to another resource within the same request; the browser URL does not change. Redirect: the server answers 302 and the browser makes a new request to a new URL; used after POST to avoid resubmission.
**6.** Cookies, URL rewriting, hidden form fields, `HttpSession`. `HttpSession` stores per-user data on the server and gives the browser a session ID (`JSESSIONID`) by cookie or URL.
**7.** An object that intercepts requests and responses in a chain. Uses: authentication or authorisation checks, logging, compression, setting the character encoding.
**8.** Translated into a servlet, compiled, `jspInit()`, `_jspService()` per request, `jspDestroy()`. Elements: directive, scriptlet, expression, declaration, action (also EL and JSTL tags).
**9.** request, response, out, session, application, config, pageContext, page, exception. Scopes: page, request, session, application.
**10.** Browser → controller servlet; servlet calls `StudentDao.findAll()`; stores the list with `request.setAttribute("students", list)`; forwards to `students.jsp`, which loops with `<c:forEach>` and writes the HTML.
**11.** Injecting a script into a page through unescaped input, so that it runs in other users' browsers. Prevent by escaping output (`<c:out>` or an escape function), validating input and setting a content security policy and HttpOnly cookies.
:::

## Model answers for Unit 6

**Q1. Explain the servlet lifecycle and the structure of a Java web application. (10 marks)**

**Introduction.** A servlet is a Java class that runs inside a servlet container such as Apache Tomcat and answers HTTP requests. The container, not the programmer, creates the servlet, calls its methods and manages its threads (Fig. 6.1).

**Structure of the application.** A web application is a folder or a WAR file. Files outside `WEB-INF` (HTML, CSS, images, JSP) are public. `WEB-INF` holds `web.xml`, `classes`, `lib` and private views, and is never served: in the real run a request for `/WEB-INF/views/list.jsp` returned 404. A URL is read as host and port, context path and servlet path, so `/hello` was mapped to the `Hello` servlet.

**The lifecycle.**

1. **Loading and `init()`.** The container creates one instance and calls `init()` once, at the first request or at start-up if `load-on-startup` is set. Resources such as a database pool are opened here.
2. **`service()`.** For every request the container calls `service()` in a pool thread, and `HttpServlet` passes the call to `doGet`, `doPost` and similar methods. In the run, five requests used `doGet` of one instance (Fig. 6.2).
3. **`destroy()`.** The container calls it once before removing the servlet, and resources are closed.

**Rules that follow.** One instance serves many threads, so instance fields are shared by all visitors. In the experiment, a servlet that kept the parameter in a field made Sita's page say `hello Ram` (Fig. 6.6). Per-request data belongs in local variables, the request or the session.

| Method | Called | Times |
|---|---|---|
| `init()` | at first request or start-up | once |
| `service()` and `doXxx()` | each request | many |
| `destroy()` | at shutdown or redeploy | once |

**Example from the run.** A visitor opens `/hello?name=Sita`. The connector accepts the TCP connection and parses the request line, and the container finds the context and the servlet mapped to `/hello`. It then creates the request and response objects, runs the filters, and calls `doGet` in a pool thread. The servlet reads the parameter, uses the session, and writes the page, and the container sends status 200 with headers such as `Content-Type` and `Content-Length` (Fig. 6.3). Starting the whole container took 722 ms in the run, and a request for a trivial page took 456 microseconds on the loopback interface, so the container adds little cost to each request.

**Conclusion.** The container controls the lifecycle, and the programmer fills in the three hooks. A servlet that is thread-safe, short and free of per-user fields is the basis of every Java web application.

**Q2. Distinguish `doGet` and `doPost`, with the status codes seen in the real run. (5 marks)**

`HttpServlet.service()` reads the HTTP method of the request and calls the matching method. `doGet` handles GET, which asks for a page and must not change data. Its parameters appear in the URL after `?`, so the page can be bookmarked and cached, but a password must never be sent this way because it stays in history and server logs. `doPost` handles POST, which sends data such as a form in the request body. It is not cached or bookmarked, it is not shown in the address, and it is used to create or change something.

In the run, `GET /hello` returned 200 and the page `visit 1`. `POST /hello` with `item=notebook` returned status 201 and the body `created notebook`, because `doPost` called `setStatus(201)`. `DELETE /hello` returned 405, because the servlet did not override `doDelete`, and `GET /missing` returned 404 (Fig. 6.4). A servlet that throws an exception gives status 500, and the stack trace goes to the log, not to the visitor. After a successful POST the servlet should redirect, so that a refresh does not send the form again. In a form that carries Nepali text, `request.setCharacterEncoding("UTF-8")` must be called before the first `getParameter` (Fig. 6.12).

**Q3. Explain the techniques of session management in servlets, with the behaviour seen in a real run. (10 marks)**

**Introduction.** HTTP is stateless: each request is independent, so the server must recognise a returning browser by itself. A session ties several requests of one visitor to data kept on the server (Fig. 6.8).

**The four techniques.**

1. **Cookies.** The server sends `Set-Cookie`, and the browser returns `Cookie` with each request. In the run the first reply carried `JSESSIONID=...; Path=/; HttpOnly` (Fig. 6.3).
2. **`HttpSession`.** `request.getSession()` finds the session of the id in the cookie, or creates one. The data is stored with `setAttribute` and read with `getAttribute`. The id had 32 hex characters, which is 128 bits, about 3.4 x 10^38 values.
3. **URL rewriting.** If cookies are blocked, `response.encodeURL(url)` appends `;jsessionid=` and the id, giving a 50-character path in the run. The id is visible in history, logs and the Referer header, so this is a fallback (Fig. 6.9).
4. **Hidden form fields.** State travels inside `input type=hidden` fields, which suits only a multi-step form.

**Behaviour measured.** The first request had no cookie, created a session and printed `visit 1`. Three requests with the cookie printed visit 2, 3 and 4 and received no new `Set-Cookie`. A request without the cookie printed `visit 1` and got a different id. After `/logout` called `invalidate()`, the old cookie gave `visit 1`, `new true`.

| Technique | Where the data is | Weakness |
|---|---|---|
| Cookie | id in the browser | user can disable it |
| URL rewriting | id in the address | id leaks |
| Hidden field | in the page | form flows only |
| HttpSession | on the server | uses server memory |

**Good practice.** Use HttpOnly and Secure cookies, call `invalidate()` at logout, set `setMaxInactiveInterval`, and create a new session after login to prevent fixation.

**Session lifetime.** A session ends in three ways: `invalidate()` at logout, a time-out set with `setMaxInactiveInterval`, or the shutdown of the application. The listener `HttpSessionListener` reports `sessionCreated` and `sessionDestroyed`, which is useful for counting online users. In the run the listener logged a creation at the first request of each new visitor and a destruction at logout. Servers with several machines must share sessions through a common cache or sticky routing, otherwise the next request may reach a server that has never seen the id.

**Security of the id.** The id must be long and random, so that nobody can guess it; 32 hex characters give 2^128 values. The server should issue a new id after login, to prevent session fixation, and should send the cookie only over HTTPS with the `Secure` flag.

**Conclusion.** The browser keeps only an identifier, and the server keeps the data, which is why a logout must destroy the server-side session.

**Q4. Differentiate forward and redirect with an example. (5 marks)**

Both pass control to another resource, but they work differently (Fig. 6.5).

**Forward.** `request.getRequestDispatcher("/new").forward(req, resp)` is handled inside the server. The browser sends one request, the address bar stays the same, and the request and its attributes are shared with the target. In the run, `GET /fwd` returned status 200 with the body `new page`, and the target servlet ran once.

**Redirect.** `response.sendRedirect("/new")` sends status 302 with a `Location` header. The browser then sends a second request to the new address, and the address bar changes. In the run, `GET /old` returned 302 with `Location /new`, and the target had not run yet. The request attributes are lost, because the second request is new.

| Point | Forward | Redirect |
|---|---|---|
| Requests | 1 | 2 |
| Address bar | unchanged | changes |
| Scope | same application | any site |
| Request attributes | kept | lost |

Use forward inside the application, for example from a controller to a JSP in MVC. Use redirect after a successful POST, so that a refresh repeats only the harmless GET, and for moving to another site.

**Q5. What is a servlet filter? Explain how a chain works. (5 marks)**

A filter is an object that sits in front of servlets and can examine or change the request before it arrives and the response before it leaves. It implements `javax.servlet.Filter`, with `init`, `doFilter` and `destroy`, and is mapped to URL patterns with `@WebFilter` or in `web.xml`. The same filter can serve many servlets, which avoids repeated code.

A filter calls `chain.doFilter(request, response)` to pass control to the next filter or, at the end, to the servlet. The code before that call runs on the way in, and the code after it runs on the way out. In the real run two filters A and B were mapped in that order, and the log read: filter A before, filter B before, servlet `doGet`, filter B after, filter A after (Fig. 6.10). If a filter does not call `doFilter`, the request stops there; a login check does this and redirects to the login page.

Common uses are authentication and authorisation, logging and audit, setting `UTF-8` encoding on every request, compression, and adding security headers. A filter works on whole requests and so differs from a listener, which reacts to events such as the start of the application or the creation of a session. In the run, the listeners logged `context initialized` at start-up and `context destroyed` at shutdown.

**Q6. Explain JavaServer Pages: elements, life cycle, and the difference from a servlet. (10 marks)**

**Introduction.** A JavaServer Page (JSP) is a text file of HTML with Java and special tags inside. The container turns it into a servlet, so a JSP is a servlet written the other way round: markup first, code in the gaps (Fig. 6.11).

**Life cycle.**

1. **Translation.** On the first request the container translates `demo.jsp` into a Java servlet, in the run the class `org.apache.jsp.demo_jsp`.
2. **Compilation and loading.** The generated source is compiled and loaded once.
3. **Execution.** `service()` runs for each request. The first request took 474 ms and the second 1 ms, so page compilation costs a visible delay once.
4. **Destruction.** The class is unloaded at shutdown or when the page changes.

**Elements.**

1. **Directives**, such as `page` and `taglib`.
2. **Scriptlets** `<% ... %>` and **expressions** `<%= ... %>`: in the run the loop gave `scriptlet=10`.
3. **Expression Language (EL)**: `${2+3}` printed 5 and `${pageContext.request.method}` printed GET.
4. **JSTL tags**, such as `c:forEach` (printed `[1][2][3]`) and `c:out`.
5. **Implicit objects**: `request`, `response`, `session`, `application`, `out`, `param`.

**Escaping.** With `q` equal to `<b>x</b>`, the plain EL expression wrote the text unchanged, which a browser runs as HTML, while `c:out` wrote `&lt;b&gt;x&lt;/b&gt;` (Fig. 6.12).

| Point | Servlet | JSP |
|---|---|---|
| Main content | Java code | HTML with tags |
| Best for | logic, control | presentation |
| Compiled | by the programmer | by the container, at first request |

**Example.** The page `demo.jsp` of the run contains one scriptlet `<% int n = 0; for (int i = 1; i <= 4; i++) n += i; %>` and the expression `<%= n %>`, which printed 10. The same page uses `<c:forEach var="i" begin="1" end="3">[${i}]</c:forEach>` to print `[1][2][3]` without any Java, which is the style that modern JSP prefers. Tag libraries are declared with the `taglib` directive and a prefix, here `c` for the core library of JSTL.

**Implicit objects and scopes.** Data lives in four scopes: page, request, session and application. The attribute set by a controller with `request.setAttribute` is found by `${name}` in the request scope, and `${param.q}` reads a request parameter. This lets a JSP show data without a single line of Java, so a web designer can edit it safely.

**Include and error pages.** A common header is added with the `include` directive or the `jsp:include` action, and an error page is named in the `page` directive, so the visitor sees a friendly message and not a stack trace.

**Conclusion.** Servlets suit control and JSP suits display. Modern JSP avoids scriptlets and uses EL and JSTL, leaving Java code to controllers.

**Q7. Explain the MVC pattern with servlets and JSP, using the example of the unit. (10 marks)**

**Introduction.** Model-View-Controller separates an application into three parts: the data and rules, the display, and the coordination between them. Trygve Reenskaug described it in 1979, and Java web applications use a servlet as controller, classes as model and a JSP as view (Fig. 6.13).

**The three parts.**

1. **Model.** Plain Java classes, with JDBC for storage, hold the data and the business rules. In the example, three `Student` objects with marks 78, 64 and 91 were created, and the average was computed as 77.67.
2. **View.** A JSP shows the model. It contains markup, EL and JSTL, and no business code. The example printed one table row per student with `c:forEach` and the average with `${average}`.
3. **Controller.** A servlet reads the request, calls the model, stores the result as a request attribute, and forwards to the view.

**Flow of one request.** The browser sends `GET /students`. The controller builds the list, calls `request.setAttribute("students", list)` and `getRequestDispatcher("/WEB-INF/views/list.jsp").forward(req, resp)`. The JSP reads the attribute and writes HTML, which the browser receives with status 200.

**Why the view sits in `WEB-INF`.** A page under `WEB-INF` cannot be requested directly: a direct `GET` returned 404, so every visitor must pass through the controller, where login checks and validation live.

| Part | Contains | Must not contain |
|---|---|---|
| Model | data, rules, JDBC | HTML |
| View | markup, EL, JSTL | business logic |
| Controller | routing, validation | HTML printing |

**Advantages.** The design can change without touching the logic, several views can share one model, teams can work in parallel, and testing is easier. **Example of the code.** The controller has about five lines: it builds `List<Student>`, computes the average, calls `setAttribute` twice and forwards. The JSP has a table with one `c:forEach` over `${students}` and two expressions per row, `${s.name}` and `${s.marks}`, which call the getters `getName` and `getMarks` of the model class. Because the JSP never calls the database, the same view works with a list from a file, a test or JDBC.

**Testing and teamwork.** The model has no HTML and no servlet types, so it can be tested with plain JUnit code. A designer can change `list.jsp` while a programmer changes the controller, and a second view, such as a CSV or JSON writer, can reuse the same model.

**Conclusion.** MVC with servlets and JSP is the basis of larger frameworks such as Spring MVC.

**Q8. Why are servlets multithreaded, and how is thread safety achieved? (5 marks)**

The container creates one instance of each servlet and runs every request in a separate thread from a pool. This is efficient, because no object is created per request and many visitors are served at once. In the run, four requests that each needed 200 ms finished in 205 ms, against 811 ms one after another, a speed-up of 3.96 (Fig. 6.7). Pool threads were named `http-nio-18080-exec-n`.

The price is shared state. Instance fields, static fields and the application scope are visible to all threads. In the experiment, Sita's request stored her name in a field and slept for 150 ms; Ram's request arrived at 50 ms and overwrote it, so Sita's page said `hello Ram` (Fig. 6.6). The servlet with a local variable gave each visitor the correct name.

Thread safety is achieved by five habits: keep per-request data in local variables; keep per-user data in the session; make shared fields `final` or immutable; protect unavoidable shared state with `synchronized` or atomic classes; and use a connection pool, not one shared `Connection`. The old `SingleThreadModel` interface is deprecated and should not be used.

**Q9. Discuss the security basics every servlet programmer must follow. (5 marks)**

Most web attacks use input that the programmer trusted. Six basic rules protect an application.

1. **Escape output.** Any value from a user, printed into a page, must be escaped. The plain expression wrote `<b>x</b>` unchanged, but `c:out` wrote `&lt;b&gt;x&lt;/b&gt;` (Fig. 6.12). This stops cross-site scripting (XSS).
2. **Use prepared statements** in JDBC, never concatenated SQL, to stop SQL injection (Unit 3).
3. **Protect sessions.** Use an HttpOnly and Secure cookie, avoid URL rewriting because it exposes the id (Fig. 6.9), call `invalidate()` at logout and set a time-out.
4. **Use HTTPS** for login and payment pages, so passwords and ids are not readable on the network.
5. **Hide internals.** Keep views and configuration in `WEB-INF`, which returned 404 when requested directly, and show a friendly error page for status 500, with the stack trace only in the log (Fig. 6.4).
6. **Validate on the server.** Browser checks can be bypassed, so each parameter's type, length and range is checked again, and a POST that changes data is protected by a token against forged requests.
