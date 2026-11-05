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
