import java.io.*;
import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.apache.catalina.*;
import org.apache.catalina.startup.Tomcat;
import org.apache.tomcat.util.descriptor.web.*;

public class ServLab {
    static List<String> LOG = Collections.synchronizedList(new ArrayList<>());
    static Set<Integer> instances = ConcurrentHashMap.newKeySet();
    static Set<String> threads = ConcurrentHashMap.newKeySet();
    static AtomicInteger inits = new AtomicInteger(), services = new AtomicInteger(), newHits = new AtomicInteger();
    public static class Hello extends HttpServlet {
        public void init() { inits.incrementAndGet(); LOG.add("servlet init"); }
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException {
            services.incrementAndGet(); instances.add(System.identityHashCode(this)); threads.add(Thread.currentThread().getName().replaceAll("\\d+$", "N"));
            LOG.add("servlet doGet");
            HttpSession s = q.getSession();
            Integer v = (Integer) s.getAttribute("visits"); v = v == null ? 1 : v + 1; s.setAttribute("visits", v);
            r.setContentType("text/html;charset=UTF-8");
            r.getWriter().println("visit " + v + " sid " + s.getId().length() + " new " + s.isNew());
        }
        protected void doPost(HttpServletRequest q, HttpServletResponse r) throws IOException { r.setStatus(201); r.getWriter().println("created " + q.getParameter("item")); }
        public void destroy() { LOG.add("servlet destroy"); }
    }
    public static class Unsafe extends HttpServlet {
        String current;
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException {
            current = q.getParameter("n"); try { Thread.sleep(150); } catch (Exception e) {}
            r.getWriter().print("hello " + current);
        }
    }
    public static class Safe extends HttpServlet {
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException {
            String me = q.getParameter("n"); try { Thread.sleep(150); } catch (Exception e) {}
            r.getWriter().print("hello " + me);
        }
    }
    public static class Slow extends HttpServlet {
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException {
            try { Thread.sleep(200); } catch (Exception e) {}
            r.getWriter().print(Thread.currentThread().getName().replaceAll("\\d+$", "N"));
        }
    }
    public static class Old extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException { r.sendRedirect(q.getContextPath() + "/new"); } }
    public static class Fwd extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException, ServletException { q.getRequestDispatcher("/new").forward(q, r); } }
    public static class New extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException { newHits.incrementAndGet(); r.getWriter().print("new page"); } }
    public static class Boom extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) { throw new IllegalStateException("database is down"); } }
    public static class Link extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException { q.getSession(); r.getWriter().print(r.encodeURL("/hello")); } }
    public static class Logout extends HttpServlet { protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException { q.getSession().invalidate(); r.getWriter().print("bye"); } }
    public static class Utf extends HttpServlet {
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException { r.setContentType("text/plain;charset=UTF-8"); r.getWriter().print("नमस्ते"); }
        protected void doPost(HttpServletRequest q, HttpServletResponse r) throws IOException {
            if ("1".equals(q.getParameter("fix")) || "1".equals(q.getQueryString() == null ? "" : q.getQueryString().replace("fix=", ""))) q.setCharacterEncoding("UTF-8");
            String n = q.getParameter("name"); r.setContentType("text/plain;charset=UTF-8"); r.getWriter().print(n.length() + ":" + n);
        }
    }
    public static class Utf2 extends HttpServlet {
        protected void doPost(HttpServletRequest q, HttpServletResponse r) throws IOException {
            q.setCharacterEncoding("UTF-8"); String n = q.getParameter("name"); r.setContentType("text/plain;charset=UTF-8"); r.getWriter().print(n.length() + ":" + n);
        }
    }
    public static class Utf1 extends HttpServlet {
        protected void doPost(HttpServletRequest q, HttpServletResponse r) throws IOException {
            String n = q.getParameter("name"); r.setContentType("text/plain;charset=UTF-8"); r.getWriter().print(n.length() + ":" + n);
        }
    }
    public static class Student { String name; int marks; Student(String n, int m) { name = n; marks = m; } public String getName() { return name; } public int getMarks() { return marks; } }
    public static class Students extends HttpServlet {
        protected void doGet(HttpServletRequest q, HttpServletResponse r) throws IOException, ServletException {
            List<Student> l = List.of(new Student("Sita", 78), new Student("Ram", 64), new Student("Gita", 91));
            double avg = l.stream().mapToInt(Student::getMarks).average().orElse(0);
            q.setAttribute("students", l); q.setAttribute("average", Math.round(avg * 100) / 100.0);
            q.getRequestDispatcher("/WEB-INF/views/list.jsp").forward(q, r);
        }
    }
    public static class FA implements Filter {
        String n; FA(String n) { this.n = n; }
        public void init(FilterConfig c) {} public void destroy() {}
        public void doFilter(ServletRequest q, ServletResponse r, FilterChain c) throws IOException, ServletException { LOG.add("filter " + n + " before"); c.doFilter(q, r); LOG.add("filter " + n + " after"); }
    }
    public static class CtxL implements ServletContextListener {
        public void contextInitialized(ServletContextEvent e) { LOG.add("context initialized"); }
        public void contextDestroyed(ServletContextEvent e) { LOG.add("context destroyed"); }
    }
    public static class SesL implements HttpSessionListener {
        public void sessionCreated(HttpSessionEvent e) { LOG.add("session created"); }
        public void sessionDestroyed(HttpSessionEvent e) { LOG.add("session destroyed"); }
    }
    static void add(Context c, String name, HttpServlet s, String... pats) { Tomcat.addServlet(c, name, s); for (String p : pats) c.addServletMappingDecoded(p, name); }
    static HttpClient hc = HttpClient.newBuilder().version(HttpClient.Version.HTTP_1_1).followRedirects(HttpClient.Redirect.NEVER).build();
    static HttpResponse<String> send(String m, String path, String body, String cookie) throws Exception {
        HttpRequest.Builder b = HttpRequest.newBuilder(URI.create("http://127.0.0.1:18080" + path));
        if (cookie != null) b.header("Cookie", cookie);
        if (body != null) b.header("Content-Type", "application/x-www-form-urlencoded");
        b.method(m, body == null ? HttpRequest.BodyPublishers.noBody() : HttpRequest.BodyPublishers.ofString(body));
        return hc.send(b.build(), HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    static String flat(String s) { return s.trim().replace("\n", " | ").replace("\r", ""); }
    public static void main(String[] a) throws Exception {
        Tomcat t = new Tomcat(); t.setBaseDir("/tmp/j/tc"); t.setPort(18080); t.setHostname("127.0.0.1"); t.getConnector();
        Context c = t.addWebapp("", new File("/tmp/j/web").getAbsolutePath());
        c.addApplicationListener(CtxL.class.getName()); c.addApplicationListener(SesL.class.getName());
        add(c, "hello", new Hello(), "/hello"); add(c, "unsafe", new Unsafe(), "/unsafe"); add(c, "safe", new Safe(), "/safe"); add(c, "slow", new Slow(), "/slow");
        add(c, "old", new Old(), "/old"); add(c, "fwd", new Fwd(), "/fwd"); add(c, "new", new New(), "/new"); add(c, "boom", new Boom(), "/boom");
        add(c, "link", new Link(), "/link"); add(c, "logout", new Logout(), "/logout"); add(c, "utf", new Utf(), "/utf"); add(c, "utf1", new Utf1(), "/utf1"); add(c, "utf2", new Utf2(), "/utf2");
        add(c, "students", new Students(), "/students");
        for (String n : new String[]{"A", "B"}) { FilterDef fd = new FilterDef(); fd.setFilterName("f" + n); fd.setFilter(new FA(n)); c.addFilterDef(fd); FilterMap fm = new FilterMap(); fm.setFilterName("f" + n); fm.addURLPattern("/hello"); c.addFilterMap(fm); }
        long t0 = System.nanoTime(); t.start(); System.out.println("START ms " + (System.nanoTime() - t0) / 1000000);
        // lifecycle + session + filters
        HttpResponse<String> r1 = send("GET", "/hello", null, null);
        System.out.println("R1 " + r1.statusCode() + " " + flat(r1.body()));
        System.out.println("R1 headers " + new TreeMap<>(r1.headers().map()).keySet());
        String sc = r1.headers().firstValue("Set-Cookie").orElse("");
        System.out.println("R1 Set-Cookie attrs: " + sc.replaceAll("JSESSIONID=[0-9A-F]+", "JSESSIONID=<id>"));
        String ck = sc.split(";")[0];
        System.out.println("R1 content-type " + r1.headers().firstValue("Content-Type").orElse("-") + " | content-length " + r1.headers().firstValue("Content-Length").orElse("-") + " | transfer-encoding " + r1.headers().firstValue("Transfer-Encoding").orElse("-"));
        for (int i = 0; i < 3; i++) { HttpResponse<String> r = send("GET", "/hello", null, ck); System.out.println("R" + (i + 2) + " " + flat(r.body()) + " setcookie? " + r.headers().firstValue("Set-Cookie").isPresent()); }
        HttpResponse<String> rn = send("GET", "/hello", null, null);
        System.out.println("NOCOOKIE " + flat(rn.body()) + " different id? " + !rn.headers().firstValue("Set-Cookie").orElse("").split(";")[0].equals(ck));
        System.out.println("LIFE inits=" + inits + " services=" + services + " instances=" + instances.size() + " threads=" + threads);
        System.out.println("LOG " + LOG);
        // methods and statuses
        HttpResponse<String> rp = send("POST", "/hello", "item=notebook", null); System.out.println("POST " + rp.statusCode() + " " + flat(rp.body()));
        HttpResponse<String> rd = send("DELETE", "/hello", null, null); System.out.println("DELETE " + rd.statusCode() + " allow=" + rd.headers().firstValue("Allow").orElse("-"));
        System.out.println("MISSING " + send("GET", "/missing", null, null).statusCode());
        System.out.println("BOOM " + send("GET", "/boom", null, null).statusCode());
        // redirect vs forward
        int h0 = newHits.get(); HttpResponse<String> ro = send("GET", "/old", null, null);
        System.out.println("REDIRECT status " + ro.statusCode() + " Location " + ro.headers().firstValue("Location").orElse("-") + " newHits " + (newHits.get() - h0));
        h0 = newHits.get(); HttpResponse<String> rf = send("GET", "/fwd", null, null);
        System.out.println("FORWARD status " + rf.statusCode() + " body " + rf.body() + " newHits " + (newHits.get() - h0));
        // URL rewriting
        System.out.println("REWRITE " + send("GET", "/link", null, null).body().replaceAll("[0-9A-F]{32}", "<32 hex>"));
        // logout
        HttpResponse<String> rs = send("GET", "/hello", null, null); String ck2 = rs.headers().firstValue("Set-Cookie").get().split(";")[0];
        send("GET", "/logout", null, ck2); HttpResponse<String> after = send("GET", "/hello", null, ck2); System.out.println("AFTER LOGOUT " + flat(after.body()));
        // unsafe vs safe
        for (String p : new String[]{"unsafe", "safe"}) {
            ExecutorService ex = Executors.newFixedThreadPool(2); Future<String> f1 = ex.submit(() -> send("GET", "/" + p + "?n=Sita", null, null).body());
            Thread.sleep(50); Future<String> f2 = ex.submit(() -> send("GET", "/" + p + "?n=Ram", null, null).body());
            System.out.println(p.toUpperCase() + " Sita sees [" + f1.get() + "] Ram sees [" + f2.get() + "]"); ex.shutdown();
        }
        // concurrency
        Set<String> names = ConcurrentHashMap.newKeySet(); long s0 = System.nanoTime();
        ExecutorService ex = Executors.newFixedThreadPool(4); List<Future<String>> fs = new ArrayList<>();
        for (int i = 0; i < 4; i++) fs.add(ex.submit(() -> send("GET", "/slow", null, null).body()));
        for (Future<String> f : fs) names.add(f.get()); ex.shutdown();
        System.out.println("CONC 4x200ms = " + (System.nanoTime() - s0) / 1000000 + " ms; thread names " + names);
        s0 = System.nanoTime(); for (int i = 0; i < 4; i++) send("GET", "/slow", null, null);
        System.out.println("SEQ 4x200ms = " + (System.nanoTime() - s0) / 1000000 + " ms");
        // throughput
        for (int i = 0; i < 500; i++) send("GET", "/new", null, null);
        s0 = System.nanoTime(); int N = 2000; for (int i = 0; i < N; i++) send("GET", "/new", null, null);
        System.out.println("LATENCY /new " + String.format("%.0f", (System.nanoTime() - s0) / 1000.0 / N) + " us per request");
        // UTF-8
        HttpResponse<String> ru = send("GET", "/utf", null, null);
        System.out.println("UTF get body chars=" + ru.body().length() + " content-type=" + ru.headers().firstValue("Content-Type").orElse("-") + " content-length=" + ru.headers().firstValue("Content-Length").orElse("-"));
        String enc = java.net.URLEncoder.encode("नमस्ते", "UTF-8");
        System.out.println("UTF encoded form " + enc);
        System.out.println("UTF post default  " + send("POST", "/utf1", "name=" + enc, null).body().replace("\n", ""));
        System.out.println("UTF post fixed    " + send("POST", "/utf2", "name=" + enc, null).body());
        // jsp
        long j0 = System.nanoTime(); HttpResponse<String> j1 = send("GET", "/demo.jsp?q=" + java.net.URLEncoder.encode("<b>x</b>", "UTF-8"), null, null); long jt1 = (System.nanoTime() - j0) / 1000000;
        j0 = System.nanoTime(); send("GET", "/demo.jsp?q=1", null, null); long jt2 = (System.nanoTime() - j0) / 1000000;
        System.out.println("JSP status " + j1.statusCode() + " first " + jt1 + " ms second " + jt2 + " ms");
        System.out.println("JSP body " + flat(j1.body()).replaceAll("\\s+", " "));
        System.out.println("JSP generated: " + new File("/tmp/j/tc").getAbsolutePath());
        HttpResponse<String> st = send("GET", "/students", null, null); System.out.println("MVC " + st.statusCode() + " " + flat(st.body()).replaceAll("\\s+", " "));
        System.out.println("DIRECT /WEB-INF " + send("GET", "/WEB-INF/views/list.jsp", null, null).statusCode());
        t.stop(); t.destroy(); System.out.println("LOG2 " + LOG.subList(LOG.size() - 4, LOG.size()));
        System.exit(0);
    }
}
