import edu.nebians.StudentBean;
import java.beans.*;
import java.io.*;
import java.lang.reflect.Method;
import java.net.URI;
import java.net.http.*;
import java.util.*;
import org.apache.catalina.*;
import org.apache.catalina.startup.Tomcat;

public class BeanLab {
    static class SerListener implements PropertyChangeListener, Serializable { public void propertyChange(PropertyChangeEvent e) {} }
    static int ser(Object o) throws Exception { ByteArrayOutputStream b = new ByteArrayOutputStream(); try (ObjectOutputStream s = new ObjectOutputStream(b)) { s.writeObject(o); } return b.size(); }
    static HttpClient hc = HttpClient.newBuilder().version(HttpClient.Version.HTTP_1_1).build();
    static HttpResponse<String> get(String p, String ck) throws Exception {
        HttpRequest.Builder b = HttpRequest.newBuilder(URI.create("http://127.0.0.1:18081" + p)); if (ck != null) b.header("Cookie", ck);
        return hc.send(b.build(), HttpResponse.BodyHandlers.ofString());
    }
    public static void main(String[] a) throws Exception {
        long t0 = System.nanoTime(); BeanInfo bi = Introspector.getBeanInfo(StudentBean.class); double first = (System.nanoTime() - t0) / 1e6;
        t0 = System.nanoTime(); Introspector.getBeanInfo(StudentBean.class); double second = (System.nanoTime() - t0) / 1e6;
        System.out.println("INTRO first " + String.format("%.2f", first) + " ms, second " + String.format("%.3f", second) + " ms");
        for (PropertyDescriptor pd : bi.getPropertyDescriptors()) {
            String kind = pd instanceof IndexedPropertyDescriptor ? "indexed" : "simple";
            System.out.println("PROP " + pd.getName() + " type=" + (pd.getPropertyType() == null ? "-" : pd.getPropertyType().getSimpleName()) + " get=" + (pd.getReadMethod() == null ? "-" : pd.getReadMethod().getName()) + " set=" + (pd.getWriteMethod() == null ? "-" : pd.getWriteMethod().getName()) + " " + kind + " bound=" + pd.isBound() + " constrained=" + pd.isConstrained());
        }
        System.out.println("EVENTS " + Arrays.stream(bi.getEventSetDescriptors()).map(EventSetDescriptor::getName).toList());
        System.out.println("METHODS declared " + bi.getMethodDescriptors().length);
        StudentBean s = new StudentBean(); List<String> log = new ArrayList<>();
        s.addPropertyChangeListener(e -> log.add(e.getPropertyName() + ":" + e.getOldValue() + "->" + e.getNewValue()));
        s.setName("Sita"); s.setName("Sita"); s.setMarks(72); s.setMarks(72); s.setScores(1, 9);
        System.out.println("BOUND events " + log + " (6 setter calls, " + log.size() + " events)");
        try { s.setMarks(150); } catch (PropertyVetoException e) { System.out.println("VETO " + e.getMessage() + "; marks still " + s.getMarks() + "; passed " + s.isPassed()); }
        try { s.setMarks(-5); } catch (PropertyVetoException e) { System.out.println("VETO2 " + e.getMessage()); }
        System.out.println("LISTENERS before: bound=" + s.listenerCount() + " veto=" + s.vetoCount());
        int plain = ser(s); s.addPropertyChangeListener(new SerListener()); int withL = ser(s);
        System.out.println("SERIAL bytes " + plain + " ; with one serializable listener " + withL);
        ByteArrayOutputStream bo = new ByteArrayOutputStream(); try (ObjectOutputStream o = new ObjectOutputStream(bo)) { o.writeObject(s); }
        StudentBean r = (StudentBean) new ObjectInputStream(new ByteArrayInputStream(bo.toByteArray())).readObject();
        System.out.println("RESTORED name=" + r.getName() + " marks=" + r.getMarks() + " scores1=" + r.getScores(1) + " bound=" + r.listenerCount() + " veto=" + r.vetoCount());
        r.setMarks(150); System.out.println("RESTORED setMarks(150) accepted -> marks " + r.getMarks() + " (the lambda veto rule was not serialized)");
        // reflection cost
        Method setter = new PropertyDescriptor("name", StudentBean.class).getWriteMethod(); StudentBean t = new StudentBean(); int N = 2_000_000;
        for (int i = 0; i < 200000; i++) { setter.invoke(t, "x"); t.setName("y"); }
        long q = System.nanoTime(); for (int i = 0; i < N; i++) t.setName((i & 1) == 0 ? "a" : "b"); double dir = (System.nanoTime() - q) / (double) N;
        q = System.nanoTime(); for (int i = 0; i < N; i++) setter.invoke(t, (i & 1) == 0 ? "a" : "b"); double refl = (System.nanoTime() - q) / (double) N;
        System.out.println("REFLECT direct " + String.format("%.1f", dir) + " ns, reflective " + String.format("%.1f", refl) + " ns");
        // web
        new File("/tmp/j/bweb/WEB-INF").mkdirs();
        try (PrintWriter w = new PrintWriter("/tmp/j/bweb/bean.jsp", "UTF-8")) { w.println("<%@ page contentType=\"text/html;charset=UTF-8\" %><jsp:useBean id=\"st\" class=\"edu.nebians.StudentBean\" scope=\"session\"/><jsp:setProperty name=\"st\" property=\"*\"/>name=${st.name} marks=${st.marks} passed=${st.passed}"); }
        try (PrintWriter w = new PrintWriter("/tmp/j/bweb/req.jsp", "UTF-8")) { w.println("<%@ page contentType=\"text/html;charset=UTF-8\" %><jsp:useBean id=\"st\" class=\"edu.nebians.StudentBean\" scope=\"request\"/><jsp:setProperty name=\"st\" property=\"*\"/>name=${st.name}"); }
        Tomcat tc = new Tomcat(); tc.setBaseDir("/tmp/j/tc2"); tc.setPort(18081); tc.setHostname("127.0.0.1"); tc.getConnector(); tc.addWebapp("", "/tmp/j/bweb"); tc.start();
        HttpResponse<String> w1 = get("/bean.jsp?name=Sita&marks=72", null); String ck = w1.headers().firstValue("Set-Cookie").get().split(";")[0];
        System.out.println("WEB1 " + w1.statusCode() + " " + w1.body().trim());
        System.out.println("WEB2 (same session, no params) " + get("/bean.jsp", ck).body().trim());
        System.out.println("WEB3 (no cookie) " + get("/bean.jsp", null).body().trim());
        System.out.println("WEB4 marks=150 -> " + get("/bean.jsp?marks=150", ck).statusCode());
        System.out.println("WEB5 marks=abc -> " + get("/bean.jsp?marks=abc", ck).statusCode());
        System.out.println("WEB6 request scope params then none: " + get("/req.jsp?name=Ram", null).body().trim() + " | " + get("/req.jsp", null).body().trim());
        System.out.println("WEB7 after bad marks, bean still: " + get("/bean.jsp", ck).body().trim());
        tc.stop(); System.exit(0);
    }
}
