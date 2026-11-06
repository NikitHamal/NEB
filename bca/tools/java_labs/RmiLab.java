import java.io.*;
import java.lang.reflect.Proxy;
import java.net.*;
import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class RmiLab {
    static AtomicLong out = new AtomicLong(), in = new AtomicLong();
    static List<Integer> ports = Collections.synchronizedList(new ArrayList<>());
    static AtomicInteger created = new AtomicInteger();
    static byte[] first = new byte[16]; static AtomicInteger firstN = new AtomicInteger();
    static class CF extends RMISocketFactory {
        public Socket createSocket(String h, int p) throws IOException {
            created.incrementAndGet(); ports.add(p);
            return new Socket(h, p) {
                OutputStream o; InputStream i;
                public synchronized OutputStream getOutputStream() throws IOException {
                    if (o == null) { final OutputStream r = super.getOutputStream(); o = new OutputStream() {
                        public void write(int b) throws IOException { cap(new byte[]{(byte)b},0,1); r.write(b); }
                        public void write(byte[] b, int off, int len) throws IOException { cap(b,off,len); r.write(b, off, len); }
                        public void flush() throws IOException { r.flush(); } }; }
                    return o; }
                public synchronized InputStream getInputStream() throws IOException {
                    if (i == null) { final InputStream r = super.getInputStream(); i = new InputStream() {
                        public int read() throws IOException { int b = r.read(); if (b >= 0) in.incrementAndGet(); return b; }
                        public int read(byte[] b, int off, int len) throws IOException { int n = r.read(b, off, len); if (n > 0) in.addAndGet(n); return n; } }; }
                    return i; }
            };
        }
        void cap(byte[] b, int off, int len) { out.addAndGet(len); synchronized (first) { for (int k = 0; k < len && firstN.get() < 16; k++) first[firstN.getAndIncrement()] = b[off + k]; } }
        public ServerSocket createServerSocket(int p) throws IOException { return new ServerSocket(p); }
    }
    public interface Calc extends Remote {
        int add(int a, int b) throws RemoteException;
        long sum(int[] a) throws RemoteException;
        int slow(int ms) throws RemoteException;
        String whoAmI() throws RemoteException;
        int bumpCopy(CopyCounter c) throws RemoteException;
        int bumpRef(RefCounter c) throws RemoteException;
        String callBack(Listener l, int n) throws RemoteException;
        int increment() throws RemoteException;
        void fail(int kind) throws RemoteException, InsufficientFunds;
        void takeObject(Object o) throws RemoteException;
    }
    public static class InsufficientFunds extends Exception { public InsufficientFunds(String m) { super(m); } }
    public interface Listener extends Remote { void ping(int i) throws RemoteException; }
    public interface RefCounter extends Remote { int bump() throws RemoteException; }
    public static class CopyCounter implements Serializable { public int n; }
    public static class Impl extends UnicastRemoteObject implements Calc {
        int counter = 0;
        public Impl() throws RemoteException { super(); }
        public int add(int a, int b) { return a + b; }
        public long sum(int[] a) { long s = 0; for (int x : a) s += x; return s; }
        public int slow(int ms) { try { Thread.sleep(ms); } catch (Exception e) {} return ms; }
        public String whoAmI() { return Thread.currentThread().getName(); }
        public int bumpCopy(CopyCounter c) { c.n += 100; return c.n; }
        public int bumpRef(RefCounter c) throws RemoteException { c.bump(); c.bump(); return c.bump(); }
        public String callBack(Listener l, int n) throws RemoteException {
            for (int i = 1; i <= n; i++) l.ping(i);
            return l.getClass().getName() + " / impl? " + (l instanceof ListenerImpl); }
        public synchronized int increment() { return ++counter; }
        public void fail(int k) throws InsufficientFunds { if (k == 1) throw new InsufficientFunds("balance 500 < 800"); if (k == 2) throw new IllegalArgumentException("bad amount"); }
        public void takeObject(Object o) {}
    }
    static class ListenerImpl extends UnicastRemoteObject implements Listener {
        List<String> log = Collections.synchronizedList(new ArrayList<>());
        ListenerImpl() throws RemoteException { super(); }
        public void ping(int i) { log.add(i + "@" + Thread.currentThread().getName().replaceAll("-\\d+\\)", ")")); }
    }
    static class RefImpl extends UnicastRemoteObject implements RefCounter {
        int n; RefImpl() throws RemoteException { super(); }
        public synchronized int bump() { return ++n; }
    }
    static int ser(Object o) throws Exception { ByteArrayOutputStream b = new ByteArrayOutputStream(); try (ObjectOutputStream s = new ObjectOutputStream(b)) { s.writeObject(o); } return b.size(); }
    static String hex(byte[] b, int n) { StringBuilder s = new StringBuilder(); for (int i = 0; i < n; i++) s.append(String.format("%02x ", b[i])); return s.toString().trim(); }
    public static void main(String[] args) throws Exception {
        System.setProperty("java.rmi.server.hostname", "127.0.0.1");
        RMISocketFactory.setSocketFactory(new CF());
        Registry reg = LocateRegistry.createRegistry(51234);
        Impl impl = new Impl();
        reg.rebind("Calc", impl);
        long o0 = out.get(), i0 = in.get(); int c0 = created.get();
        Registry cv = LocateRegistry.getRegistry("127.0.0.1", 51234);
        Calc calc = (Calc) cv.lookup("Calc");
        System.out.println("LOOKUP bytes out=" + (out.get() - o0) + " in=" + (in.get() - i0) + " sockets=" + (created.get() - c0));
        System.out.println("LOOKUP ports: " + ports);
        System.out.println("JRMP first bytes: " + hex(first, 7));
        System.out.println("stub class: " + calc.getClass().getName() + " isProxy=" + Proxy.isProxyClass(calc.getClass()));
        System.out.println("stub interfaces: " + Arrays.toString(Arrays.stream(calc.getClass().getInterfaces()).map(Class::getSimpleName).toArray()));
        System.out.println("registry stub class: " + cv.getClass().getName());
        String ref = calc.toString(); System.out.println("stub ref: " + ref);
        java.util.regex.Matcher m = java.util.regex.Pattern.compile("endpoint:\\[([\\d.]+):(\\d+)\\]").matcher(ref);
        if (m.find()) System.out.println("object export port: " + m.group(2) + " (registry port 51234)");
        o0 = out.get(); i0 = in.get(); c0 = created.get();
        System.out.println("add=" + calc.add(19, 23));
        System.out.println("CALL1 bytes out=" + (out.get() - o0) + " in=" + (in.get() - i0) + " sockets=" + (created.get() - c0));
        o0 = out.get(); i0 = in.get(); c0 = created.get(); calc.add(1, 2);
        System.out.println("CALL2 bytes out=" + (out.get() - o0) + " in=" + (in.get() - i0) + " sockets=" + (created.get() - c0));
        // timing
        for (int i = 0; i < 3000; i++) calc.add(i, 1);
        c0 = created.get(); int N = 5000; long t = System.nanoTime();
        for (int i = 0; i < N; i++) calc.add(i, 1);
        double remoteUs = (System.nanoTime() - t) / 1000.0 / N;
        System.out.println("TIME remote add: " + String.format("%.1f", remoteUs) + " us/call, new sockets in " + N + " calls=" + (created.get() - c0));
        long acc = 0; int LN = 50_000_000; t = System.nanoTime();
        for (int i = 0; i < LN; i++) acc += impl.add(i, 1);
        double localNs = (System.nanoTime() - t) / (double) LN;
        System.out.println("TIME local add: " + String.format("%.2f", localNs) + " ns/call (acc " + acc + ")");
        System.out.println("RATIO remote/local: " + String.format("%.0f", remoteUs * 1000 / Math.max(localNs, 0.01)));
        // payload
        int[] big = new int[1000]; for (int i = 0; i < big.length; i++) big[i] = i;
        o0 = out.get(); long s = calc.sum(big); long bo = out.get() - o0;
        System.out.println("PAYLOAD sum(int[1000])=" + s + " bytes out=" + bo);
        int[] big2 = new int[100000]; for (int i = 0; i < big2.length; i++) big2[i] = i;
        o0 = out.get(); t = System.nanoTime(); s = calc.sum(big2); double us2 = (System.nanoTime() - t) / 1000.0;
        System.out.println("PAYLOAD sum(int[100000])=" + s + " bytes out=" + (out.get() - o0) + " time us=" + String.format("%.0f", us2));
        System.out.println("SERIAL Point-like CopyCounter=" + ser(new CopyCounter()) + " int[1000]=" + ser(big) + " stub=" + ser(calc) + " ArrayList<Integer>(1000)=" + ser(new ArrayList<>(Arrays.asList(Arrays.stream(big).boxed().toArray()))));
        // copy vs ref
        CopyCounter cc = new CopyCounter(); int r1 = calc.bumpCopy(cc);
        System.out.println("COPY server returned " + r1 + ", client counter still " + cc.n);
        RefImpl rc = new RefImpl(); int r2 = calc.bumpRef(rc);
        System.out.println("REF server returned " + r2 + ", client counter now " + rc.n);
        ListenerImpl li = new ListenerImpl(); String desc = calc.callBack(li, 3);
        System.out.println("CALLBACK server saw: " + desc);
        System.out.println("CALLBACK client log: " + li.log);
        // threads
        Set<String> names = ConcurrentHashMap.newKeySet();
        ExecutorService ex = Executors.newFixedThreadPool(4); t = System.nanoTime(); List<Future<?>> fs = new ArrayList<>();
        for (int i = 0; i < 4; i++) fs.add(ex.submit(() -> { names.add(calc.whoAmI().replaceAll("-\\d+\\)", ")")); calc.slow(200); return null; }));
        for (Future<?> f : fs) f.get();
        double conc = (System.nanoTime() - t) / 1e6; ex.shutdown();
        System.out.println("CONCURRENT 4 clients x slow(200): " + String.format("%.0f", conc) + " ms; thread names: " + new TreeSet<>(names));
        t = System.nanoTime(); for (int i = 0; i < 4; i++) calc.slow(200);
        System.out.println("SEQUENTIAL 4 x slow(200): " + String.format("%.0f", (System.nanoTime() - t) / 1e6) + " ms");
        // lost reply
        int before = impl.counter; int attempts = 0; int got = -1;
        for (attempts = 1; attempts <= 2; attempts++) { int v = calc.increment(); if (attempts == 1) continue; got = v; break; }
        System.out.println("RETRY server counter before=" + before + " after=" + impl.counter + " (client thought it ran once; first reply was discarded to simulate loss)");
        // exceptions
        String[] ek = new String[8]; int k = 0;
        try { calc.fail(1); } catch (Exception e) { System.out.println("EXC declared: " + e.getClass().getName() + ": " + e.getMessage()); }
        try { calc.fail(2); } catch (Exception e) { System.out.println("EXC runtime: " + e.getClass().getName() + ": " + e.getMessage()); }
        try { calc.takeObject(new Object()); } catch (Exception e) { System.out.println("EXC marshal: " + e.getClass().getName() + " | cause " + (e.getCause() == null ? "none" : e.getCause().getClass().getName())); }
        try { reg.bind("Calc", impl); } catch (Exception e) { System.out.println("EXC bind: " + e.getClass().getName() + ": " + e.getMessage()); }
        try { cv.lookup("Nope"); } catch (Exception e) { System.out.println("EXC lookup: " + e.getClass().getName() + ": " + e.getMessage()); }
        try { LocateRegistry.getRegistry("127.0.0.1", 51999).lookup("Calc"); } catch (Exception e) { System.out.println("EXC refused: " + e.getClass().getName() + " | cause " + e.getCause().getClass().getName() + ": " + e.getCause().getMessage()); }
        UnicastRemoteObject.unexportObject(impl, true);
        try { calc.add(1, 1); } catch (Exception e) { System.out.println("EXC unexported: " + e.getClass().getName() + ": " + e.getMessage()); }
        UnicastRemoteObject.unexportObject(reg, true);
        try { LocateRegistry.getRegistry("127.0.0.1", 51234).lookup("Calc"); } catch (Exception e) { System.out.println("EXC noregistry: " + e.getClass().getName() + " | cause " + (e.getCause() == null ? "none" : e.getCause().getClass().getName() + ": " + e.getCause().getMessage())); }
        System.exit(0);
    }
}
