---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 5
title: Remote Method Invocation and CORBA
hours: 6
area: BCA 303 · Advanced Java Programming · Unit 5
---

With sockets you design a message format, write the parser, and send bytes. With **Remote Method Invocation (RMI)** you simply *call a method on an object that lives in another JVM*, and Java handles the connection, the marshalling of arguments, the transfer and the unmarshalling of the result. The call looks like a local call; what it hides is exactly what makes distributed programming hard: partial failure, latency and the fact that arguments are *copied* while remote objects are *referenced*. This unit runs a real RMI registry, server and client in one program and then compares RMI with CORBA, its language-neutral cousin.

::: key What this unit gives you
- The RMI architecture: remote interface, implementation, stub, registry, client.
- Parameter passing: by value (serialization) versus by remote reference.
- Writing, running and deploying an RMI application; exceptions.
- CORBA: ORB, IDL, IIOP; RMI versus CORBA.
:::

## 5.1 Distributed objects and RMI

A **distributed object** system lets a client in one JVM invoke methods of an object in another, on the same machine or across a network. RMI is Java's native technology for it (package `java.rmi`), designed around three ideas:

- the **remote interface** declares what a client may call (it extends `java.rmi.Remote`, and every method throws `RemoteException`);
- the **implementation** (the *server object*) does the work (usually extends `UnicastRemoteObject`, which exports the object so it can receive calls);
- a **stub** (a client-side proxy implementing the same interface) turns each method call into a network request, **marshalls** (serializes) the arguments, waits for the reply and **unmarshalls** the result or exception. In modern Java the stub is a dynamic proxy generated automatically; older versions required the `rmic` compiler, and the server-side *skeleton* is no longer needed.

### Architecture

| Layer | Role |
|---|---|
| Application | client and server code using the remote interface |
| Stub and skeleton (proxy layer) | intercept calls and marshal/unmarshal |
| Remote reference layer | locates the object, manages the connection semantics |
| Transport layer | TCP connections (Java Remote Method Protocol, JRMP) |

### The RMI registry

The client needs a first reference to a remote object. The **RMI registry** is a simple naming service: the server **binds** a name to the stub (`registry.rebind("Calculator", stub)`), and the client **looks it up** (`registry.lookup("Calculator")`) and receives a stub. The registry listens on **port 1099** by default and can be started inside the server with `LocateRegistry.createRegistry(port)` or as a separate program `rmiregistry`. Names can be addressed as URLs: `rmi://host:1099/Calculator`.

## 5.2 Parameters: by value or by reference

- **Primitives and serializable objects** are passed **by value**: a *copy* is made by serialization, so changes the server makes to its copy are not seen by the client, and vice versa. The class must implement `Serializable` and, if the client lacks it, the class file must be made available (a codebase), which is the reason Java now restricts remote class loading.
- **Remote objects** (those implementing `Remote`) are passed **by reference**: the receiver gets a *stub* for the original, and calls through it run on the object's home JVM.
- Non-serializable, non-remote arguments cause `java.rmi.MarshalException` (caused by `NotSerializableException`).

## 5.3 A complete RMI program

The following single file defines a remote interface, an implementation with state, starts a registry on a fixed local port, binds the object, looks it up like a client would and calls it. It demonstrates a method with primitives, a pass-by-value object (`Point`), a remote counter whose state lives on the server, and an unbound lookup.

```java
import java.io.Serializable;
import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.UnicastRemoteObject;
public class RmiDemo {
    public interface Calculator extends Remote {
        int add(int a, int b) throws RemoteException;
        Point translate(Point p, int dx, int dy) throws RemoteException;
        int increment() throws RemoteException;
    }
    public static class Point implements Serializable {
        private static final long serialVersionUID = 1L;
        public int x, y;
        public Point(int x, int y) { this.x = x; this.y = y; }
        public String toString() { return "(" + x + "," + y + ")"; }
    }
    public static class CalculatorImpl extends UnicastRemoteObject implements Calculator {
        private int counter = 0;
        public CalculatorImpl() throws RemoteException { super(); }
        public int add(int a, int b) { return a + b; }
        public Point translate(Point p, int dx, int dy) { p.x += dx; p.y += dy; return new Point(p.x, p.y); }
        public synchronized int increment() { return ++counter; }
    }
    public static void main(String[] args) throws Exception {
        System.setProperty("java.rmi.server.hostname", "127.0.0.1");
        Registry registry = LocateRegistry.createRegistry(51234);
        registry.rebind("Calculator", new CalculatorImpl());
        System.out.println("bound names: " + String.join(",", registry.list()));
        Registry clientView = LocateRegistry.getRegistry("127.0.0.1", 51234);
        Calculator calc = (Calculator) clientView.lookup("Calculator");
        System.out.println("stub is a proxy, not the implementation: " + !(calc instanceof CalculatorImpl));
        System.out.println("add(19, 23) = " + calc.add(19, 23));
        Point mine = new Point(1, 2);
        Point moved = calc.translate(mine, 10, 20);
        System.out.println("returned copy = " + moved + ", my original is still " + mine + " (passed by value)");
        System.out.println("remote counter: " + calc.increment() + ", " + calc.increment() + ", " + calc.increment());
        Calculator second = (Calculator) clientView.lookup("Calculator");
        System.out.println("a second client sees the same server object: " + second.increment());
        try { clientView.lookup("NoSuchService"); }
        catch (NotBoundException e) { System.out.println("NotBoundException: " + e.getMessage()); }
        System.exit(0);
    }
}
```
```output
bound names: Calculator
stub is a proxy, not the implementation: true
add(19, 23) = 42
returned copy = (11,22), my original is still (1,2) (passed by value)
remote counter: 1, 2, 3
a second client sees the same server object: 4
NotBoundException: NoSuchService
```
The server's `translate` method moved *its copy* of the point; the caller's object was untouched, so serialization means pass by value. The counter lives on the server: three calls give 1, 2, 3, and a second lookup returns another stub for the **same** server object, so its call returns 4.

### Writing and running RMI in practice

1. Write the remote interface (extends `Remote`, methods `throws RemoteException`).
2. Write the implementation (extends `UnicastRemoteObject`, or call `UnicastRemoteObject.exportObject`).
3. Write the server: create or locate the registry, `rebind` the object.
4. Write the client: `LocateRegistry.getRegistry(host, port)`, `lookup`, call methods.
5. Compile; start `rmiregistry` (or let the server create it); start the server, then the client. Firewalls must allow the registry port **and** the object's export port (set it explicitly with `UnicastRemoteObject.exportObject(obj, port)`), and the server's `java.rmi.server.hostname` must be an address the client can reach (the demo sets 127.0.0.1; a wrong value is the classic cause of connection hangs).

### Exceptions and failure

Every remote call can fail in ways a local call cannot, which is why every method declares `RemoteException`: `ConnectException` (server unreachable), `NoSuchObjectException` (object no longer exported), `MarshalException`/`UnmarshalException` (serialization problems), `ServerException` (the remote method itself threw). The caller must decide whether to retry, and a retry of a non-idempotent call (like `increment`) may run it twice. This is the "partial failure" problem of distributed systems.

### RMI features and limits

- **Callbacks**: a client can pass a *remote object* (its own listener) to the server, which then calls it back; each side becomes both client and server.
- **Distributed garbage collection** via leases.
- **Security**: RMI used to download code from remote codebases; since Java 8u121 (and in 17) remote class loading is disabled by default and a serialization filter (`ObjectInputFilter`) should be set to avoid deserialization attacks.
- **Java only**: both sides must be Java (the price of being native and simple).
- **Alternatives today**: REST/JSON over HTTP, gRPC, message queues.

## 5.4 CORBA

**CORBA** (Common Object Request Broker Architecture, defined by the Object Management Group in 1991) gives distributed objects *across languages and platforms*: a C++ client can call a Java object, a Python object or a COBOL object.

| CORBA concept | Meaning |
|---|---|
| **ORB** (Object Request Broker) | the middleware that locates objects and carries requests |
| **IDL** (Interface Definition Language) | language-neutral description of interfaces; a compiler generates stubs and skeletons for each language |
| **IIOP** (Internet Inter-ORB Protocol) | the standard wire protocol over TCP |
| **Stub / skeleton** | client proxy / server-side dispatcher generated from IDL |
| **Naming Service** | like the RMI registry: names → object references |
| **POA** (Portable Object Adapter) | server-side object management |

An interface in IDL looks like Java without bodies:

```text
module college {
    struct Student { string name; long marks; };
    interface Registrar {
        Student find(in long id);
        void enroll(in Student s);
        readonly attribute long count;
    };
};
```

Steps: write the IDL; compile with an IDL compiler to produce stubs and skeletons; implement the servant; register it with the ORB and the Naming Service; the client resolves the name, narrows the reference to the interface type and calls it.

::: caution Where CORBA stands today
CORBA support was **deprecated in Java 9 and removed from the JDK in Java 11**, so the IDL example above is shown but not compiled here (it needs a third-party ORB such as JacORB). CORBA is still met in older telecom, banking and defence systems and in examination syllabi, but new systems use REST, gRPC or messaging.
:::

### RMI versus CORBA

| Aspect | RMI | CORBA |
|---|---|---|
| Languages | Java only | many (C++, Java, Python, …) |
| Interface definition | a Java interface | IDL |
| Parameter passing | objects by value (serialization) or remote reference | objects by reference or by value via IDL types |
| Protocol | JRMP (and RMI-IIOP) | IIOP |
| Complexity | low | high |
| Extra services | little | naming, events, transactions, security |
| Status | still in the JDK | removed from the JDK (Java 11) |

**RMI-IIOP** let RMI code speak IIOP to interoperate with CORBA. Today the same needs are met by web services: **SOAP** (XML, WSDL) and **REST** (HTTP, JSON), and by **gRPC** (HTTP/2, Protocol Buffers, with an IDL much like CORBA's).

## 5.5 Seeing the ideas: stubs, copies, wire bytes and failures

A remote call is easier to understand when you can picture it and measure it. Plate 5.1 gives four everyday pictures: a remote control for the stub, a telephone and its directory for the registry, a card catalogue for names that lead to objects, and a pneumatic tube for the transport. Plate 5.2 shows a photocopier for pass by value, standard containers for serialization, an interpreters' booth for the ORB and the Rosetta Stone for IDL. Plate 5.3 shows why distance matters: antennas that talk to a rover on Mars. Figures 5.1 to 5.9 then use numbers from one real run of Java 17 (a registry, a server object and a client in one program, with a socket wrapper that counted every byte), and Figures 5.10 to 5.12 turn to CORBA and the choice of technology today.

```photogrid label="5.1" cols="4" ratio="1.0" caption="Four pictures for the RMI machinery. (a) A television remote control (CC BY-SA 4.0): you press a button here and the work happens somewhere else; the stub is the remote control of a remote object. (b) A rotary telephone beside a printed telephone directory (CC BY-SA 4.0): the registry is a directory in which you look up a name and get a number. (c) A card catalogue with rows of labelled drawers (CC0): a name leads to the place where the thing is kept, as lookup(Calc) leads to a stub. (d) A hospital pneumatic tube station (CC BY-SA 4.0): the item is packed in a carrier, sent through a pipe and unpacked at the other end, which is marshalling and transport."
@ photo id="bca303/remote" cap="Remote control: the stub"
fit 1.0
focus 0.5 0.35
call 0.5 0.45 0.78 0.7 "buttons"
@ photo id="bca303/phonebook" cap="Telephone and directory: the registry"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/catalog" cap="Card catalogue: name to object"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/tube" cap="Pneumatic tube: transport"
fit 1.0
focus 0.5 0.45
```

```photogrid label="5.2" cols="4" ratio="1.0" caption="Four pictures for parameters and for CORBA. (a) A large photocopier (CC BY 4.0): a copy leaves the original untouched, like an argument passed by value. (b) A container ship in port with stacked standard containers (CC BY 2.0): goods are packed in a standard box so that any port can handle them, as serialization packs objects into a standard byte stream. (c) Interpreters in glass booths marked English, Espanol and Portugues (public domain): the ORB translates between parties that do not share a language. (d) The Rosetta Stone (CC BY-SA 4.0), one text in three scripts: an IDL file is the shared description from which every language reads the same contract."
@ photo id="bca303/copier" cap="Photocopier: pass by value"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/container" cap="Containers: serialization"
fit 1.0
focus 0.6 0.5
@ photo id="bca303/interp" cap="Interpreters: the ORB"
fit 1.0
focus 0.35 0.5
call 0.3 0.78 0.2 0.45 "booth 1"
@ photo id="bca303/rosetta" cap="Rosetta Stone: IDL"
fit 1.0
focus 0.5 0.5
```

```photogrid label="5.3" cols="3" ratio="1.0" caption="Distance, delay and partial failure. (a) Antennas of the Deep Space Network at Goldstone, California (public domain, NASA): the dishes that send commands to spacecraft. (b) The Curiosity rover on Mars, photographed by itself (CC BY 2.0): the rover receives each command as a message and cannot be rebooted by hand. (c) The one-way delay of a radio signal between Earth and Mars, computed in the figure from the two extreme distances: 3.0 to 22.3 minutes, so a question and its answer need 6.1 to 44.6 minutes. A remote method call is the same idea on a small scale: the delay and the chance of silence can never be removed."
@ photo id="bca303/dsn" cap="Deep Space Network antennas"
fit 1.0
focus 0.6 0.5
@ photo id="bca303/rover" cap="Curiosity rover on Mars"
fit 1.0
focus 0.5 0.45
@ svg cap="Radio delay Earth to Mars"
f = Fig(190, 250)
c = 299792.458
near, far = 54.6e6, 401e6
tn, tf = near / c, far / c
assert 182 < tn < 183 and 1337 < tf < 1338
f.text(95, 14, "light speed 299,792 km/s", size=9.5, color=NAVY, bold=True)
for i, (nm, d, t, fl, st) in enumerate([("closest", near, tn, MINT, TEAL), ("farthest", far, tf, ROSE, RED)]):
    y = 28 + i * 106
    f.box(6, y, 178, 96, "", fill=fl, stroke=st)
    f.text(95, y + 14, nm + ": %s million km" % ("%.1f" % (d / 1e6)).rstrip("0").rstrip("."), size=9.5, color=st, bold=True)
    f.text(95, y + 36, "one way %.0f s" % t, size=11, color=SLATE, bold=True)
    f.text(95, y + 54, "= %.1f minutes" % (t / 60), size=11, color=st, bold=True)
    f.text(95, y + 74, "round trip %.1f minutes" % (2 * t / 60), size=9.5, color=SLATE, bold=True)
f.text(95, 244, "no timeout can hide this delay", size=9, color=NAVY, bold=True)
```

```svgfig label="5.1" caption="The RMI architecture, with the facts of the real run. Left, the client JVM: the client calls calc.add(19, 23) on a stub, which in Java 17 is a generated dynamic proxy class (Proxy0 in package jdk.proxy1) implementing Remote and Calc, so no rmic compiler is needed. The call passes the remote reference layer and a TCP socket. Right, the server JVM: the transport listens on the object's own port (33225 in this run, chosen by the system), the dispatch layer unmarshals the arguments and the real object computes the answer. The registry on port 51234 holds the name Calc and gives the client its first stub."
f = Fig(580, 316)
f.box(206, 8, 168, 54, "RMI registry\nport 51234\nname Calc -> stub", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(95, 76, "client JVM", size=11, color=NAVY, bold=True)
f.text(485, 76, "server JVM", size=11, color=TEAL, bold=True)
cl = [("Client code\ncalc.add(19, 23)", BLUE, NAVY), ("Stub (dynamic proxy)\njdk.proxy1.$Proxy0", BLUE, NAVY), ("Remote reference layer\nmarshal 19 and 23", BLUE, NAVY), ("Transport: TCP socket\nJRMP stream protocol", BLUE, NAVY)]
sv = [("Real object\nImpl.add(a, b) = 42", MINT, TEAL), ("Dispatch (skeleton role)\nunmarshal, call method", MINT, TEAL), ("Remote reference layer\nmarshal the result", MINT, TEAL), ("Transport: ServerSocket\nobject port 33225", MINT, TEAL)]
for i, (t, fl, st) in enumerate(cl):
    y = 88 + i * 52
    f.box(10, y, 200, 42, t, fill=fl, stroke=st, size=9.5, bold=True)
    if i < 3:
        f.arrow([(110, y + 42), (110, y + 52)], color=SLATE)
for i, (t, fl, st) in enumerate(sv):
    y = 88 + i * 52
    f.box(370, y, 200, 42, t, fill=fl, stroke=st, size=9.5, bold=True)
    if i < 3:
        f.arrow([(470, y + 52), (470, y + 42)], color=SLATE)
f.arrow([(210, 265), (370, 265)], color=AMBER, both=True, label="request 50 bytes / reply 27 bytes", lpos=(290, 255), lsize=9)
f.arrow([(110, 88), (216, 62)], color=AMBER, dash=True, label="lookup", lpos=(172, 58), lsize=9)
f.arrow([(470, 88), (364, 62)], color=AMBER, dash=True, label="rebind", lpos=(408, 58), lsize=9)
f.text(290, 304, "the program sees only a method call: everything in between is hidden", size=9.5, color=SLATE, bold=True)
```

```svgfig label="5.2" caption="From bind to the first call, with the bytes counted by a socket wrapper in a real run. The server creates a registry on port 51234 and rebinds the name Calc to the stub of its object. The client's getRegistry and lookup opened two connections, one to port 51234 and one to the object's own port 33225, and moved 559 bytes out and 624 bytes in, 1,183 bytes in all (computed). The following add(19, 23) opened no new socket: the connection was reused, and the request was 50 bytes and the reply 27 bytes."
f = Fig(580, 270)
xs = {"server": 90, "registry": 290, "client": 490}
col = {"server": TEAL, "registry": AMBER, "client": NAVY}
for k, x in xs.items():
    f.text(x, 14, k, size=12, color=col[k], bold=True)
    f.line(x, 22, x, 262, color="#cbd5e1", sw=2)
lo, li = 559, 624
tot = lo + li
assert tot == 1183
steps = [
 (40, "server", "registry", "createRegistry(51234)", AMBER),
 (68, "server", "registry", "rebind(Calc, stub)", AMBER),
 (104, "client", "registry", "lookup(Calc): 559 B out", NAVY),
 (132, "registry", "client", "stub back: 624 B in", AMBER),
 (168, "client", "server", "connection to port 33225", TEAL),
 (204, "client", "server", "add(19, 23): 50 B out", NAVY),
 (232, "server", "client", "42: 27 B in", TEAL),
]
for y, a, b, t, c in steps:
    xa, xb = xs[a], xs[b]
    d = 1 if xb > xa else -1
    f.arrow([(xa + 4 * d, y), (xb - 4 * d, y)], color=c, label=t, lpos=((xa + xb) / 2, y - 6), lsize=9)
f.text(290, 252, "lookup total %s bytes; later calls open 0 new sockets" % format(tot, ","), size=9.5, color=SLATE, bold=True)
```

```svgfig label="5.3" caption="What travels on the wire. The first seven bytes the client wrote were 4a 52 4d 49 00 02 4b, decoded in the figure as the letters J R M I, protocol version 2 and the code K for the stream protocol (the Java Remote Method Protocol, JRMP). A call add(19, 23) needed 50 bytes for only 8 bytes of arguments, so the fixed overhead is 42 bytes (computed). The cost of the payload is linear: an int array of 1,000 elements cost 4,066 bytes and one of 100,000 cost 400,066 bytes, which is 4 bytes per element plus 66 bytes in both cases."
f = Fig(580, 262)
hexs = [0x4a, 0x52, 0x4d, 0x49, 0x00, 0x02, 0x4b]
txt = "".join(chr(h) for h in hexs[:4])
assert txt == "JRMI"
f.text(290, 14, "first 7 bytes written by the client", size=11, color=NAVY, bold=True)
for i, h in enumerate(hexs):
    x = 40 + i * 70
    fl, st = (BLUE, NAVY) if i < 4 else ((SAND, AMBER) if i < 6 else (MINT, TEAL))
    f.box(x, 26, 62, 30, "%02x" % h, fill=fl, stroke=st, size=13, bold=True)
for i, ch in enumerate(txt):
    f.text(40 + i * 70 + 31, 72, ch, size=12, color=NAVY, bold=True)
f.text(40 + 4 * 70 + 66, 72, "version 2", size=10, color=AMBER, bold=True)
f.text(40 + 6 * 70 + 31, 72, "'K'", size=12, color=TEAL, bold=True)
f.text(40 + 6 * 70 + 31, 86, "stream", size=9.5, color=TEAL, bold=True)
f.text(160, 88, "magic number JRMI", size=9.5, color=NAVY, bold=True)
args, req = 8, 50
assert req - args == 42
f.text(145, 118, "one call: add(19, 23)", size=11, color=NAVY, bold=True)
f.box(10, 128, 270 * req / 400, 20, "", fill=BLUE, stroke=NAVY, r=2)
f.box(10, 128, 270 * args / 400, 20, "", fill=SAND, stroke=AMBER, r=2)
f.text(10 + 270 * req / 400 + 6, 138, "request 50 B = 8 B arguments + 42 B overhead", size=9.5, color=SLATE, anchor="start", vmid=True)
f.box(10, 154, 270 * 27 / 400, 20, "", fill=MINT, stroke=TEAL, r=2)
f.text(10 + 270 * 27 / 400 + 6, 164, "reply 27 B (the int 42 and its header)", size=9.5, color=SLATE, anchor="start", vmid=True)
f.text(145, 198, "an int array as argument", size=11, color=NAVY, bold=True)
for (n, b), y in zip([(1000, 4066), (100000, 400066)], [208, 234]):
    ov = b - 4 * n
    assert ov == 66
    w = 4 + 270 * (b / 400066) if n > 1000 else 5
    f.box(10, y, max(w, 5), 18, "", fill=ROSE, stroke=RED, r=2)
    f.text(max(w, 5) + 16, y + 9, "%s elements: %s bytes = 4 x n + %d" % (format(n, ","), format(b, ","), ov), size=9.5, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="5.4" caption="The price of crossing a JVM boundary, measured. Left: an ordinary method call add(a, b) took 1.01 nanoseconds (50 million calls, so the optimiser had inlined it), while the same method through RMI on the loopback interface took 53.0 microseconds per call (5,000 calls after a warm-up). The ratio, computed here, is about 52,000, on one machine with no real network. Right: sending an int array of 100,000 elements (400,066 bytes) took 5,712 microseconds, about 70 MB per second. A thousand fine calls would cost about 53 ms at this rate, so a good remote interface has few, coarse methods."
import math
f = Fig(580, 250)
loc, rem = 1.01, 53.0 * 1000
ratio = rem / loc
assert 52000 < ratio < 53000
f.text(145, 14, "one add(a, b) call, log scale", size=11, color=NAVY, bold=True)
def X(v):
    return 20 + (math.log10(v) - 0) / (5 - 0) * 250
for d in range(0, 6):
    f.line(X(10 ** d), 30, X(10 ** d), 150, color="#e2e8f0", sw=1)
    f.text(X(10 ** d), 164, ["1 ns", "10 ns", "100 ns", "1 us", "10 us", "100 us"][d], size=8.5, color=SLATE)
f.box(20, 40, X(loc) - 20 + 3, 28, "", fill=MINT, stroke=TEAL, r=2)
f.text(X(loc) + 12, 54, "local 1.01 ns", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.box(20, 84, X(rem) - 20, 28, "", fill=ROSE, stroke=RED)
f.text(X(rem) - 8, 98, "RMI 53.0 us", size=10, color=RED, bold=True, anchor="end", vmid=True)
f.text(145, 134, "ratio = %s x slower (computed)" % format(int(round(ratio, -3)), ","), size=10, color=NAVY, bold=True)
thr = 400066 / 5712e-6 / 1e6
assert 69 < thr < 71
f.text(430, 14, "sending a big array", size=11, color=NAVY, bold=True)
f.box(300, 34, 250, 30, "add(19, 23): 8 B in 53 us", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(300, 74, 250, 30, "sum(int[100000]): 400,066 B in 5,712 us", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.text(425, 126, "throughput = %.1f MB per second" % thr, size=10, color=NAVY, bold=True)
f.text(425, 144, "1,000 fine calls = %.0f ms" % (1000 * 53.0 / 1000), size=10, color=RED, bold=True)
f.box(10, 180, 560, 58, "", fill=SOFT, stroke="#cbd5e1")
for i, t in enumerate(["Rule 1: make few coarse calls (send a list, not 1,000 single values).", "Rule 2: never call a remote method inside a tight loop or a Swing event handler.", "Rule 3: set timeouts, because the other JVM may be slow, busy or gone."]):
    f.text(22, 196 + i * 16, t, size=9.5, color=SLATE, anchor="start", bold=(i == 0))
```

```svgfig label="5.5" caption="How big is an argument after serialization, from real ObjectOutputStream sizes. A tiny CopyCounter object with one int field is 47 bytes; the stub that stands for a remote object is 282 bytes whatever the server object holds; an int array of 1,000 elements is 4,027 bytes; and an ArrayList of 1,000 Integer objects is 10,125 bytes, about 2.5 times the array because every boxed number is an object. A remote reference is therefore cheap to pass, while a large serializable object is expensive, since it is copied each time."
f = Fig(580, 190)
rows = [("CopyCounter (1 int)", 47, SAND, AMBER), ("stub of a remote object", 282, MINT, TEAL), ("int[1000]", 4027, BLUE, NAVY), ("ArrayList of 1,000 Integer", 10125, ROSE, RED)]
f.text(290, 14, "bytes after serialization (to scale)", size=11, color=NAVY, bold=True)
for i, (t, v, fl, st) in enumerate(rows):
    y = 28 + i * 34
    f.text(10, y + 12, t, size=10, color=SLATE, anchor="start", bold=True, vmid=True)
    w = max(3, 300 * v / 10125)
    f.box(190, y, w, 24, "", fill=fl, stroke=st, r=2)
    f.text(190 + w + 8, y + 12, "%s bytes" % format(v, ","), size=10, color=st, anchor="start", bold=True, vmid=True)
r = 10125 / 4027
assert 2.5 < r < 2.6
f.text(290, 176, "the list is %.1f x the array; the stub stays 282 bytes" % r, size=10, color=NAVY, bold=True)
```

```svgfig label="5.6" caption="A copy against a reference, from one run. Left: a serializable CopyCounter was passed to the server, which added 100 to its copy and returned 100; the client's own object still held 0, so serialization means pass by value. Right: a RefCounter that implements Remote was passed instead. The server received a stub (a generated proxy class, not an instance of the real class) and called bump() three times; each call ran in the client's JVM in a thread named RMI TCP Connection, and the client's counter became 3. The same mechanism makes a callback listener work."
f = Fig(580, 266)
f.text(145, 14, "Serializable: pass by value", size=11, color=NAVY, bold=True)
f.text(435, 14, "Remote: pass by reference", size=11, color=TEAL, bold=True)
f.line(290, 24, 290, 256, color="#cbd5e1", sw=2)
f.box(14, 30, 118, 40, "client\ncc.n = 0", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(160, 30, 118, 40, "server's copy\nn = 0", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(132, 50), (160, 50)], color=AMBER)
f.text(145, 88, "serialized: 47 bytes", size=9.5, color=AMBER, bold=True)
f.box(160, 106, 118, 40, "server adds 100\nn = 100", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(160, 126), (132, 126)], color=TEAL)
f.box(14, 106, 118, 40, "client\ncc.n still 0", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.text(145, 164, "server returns 100; caller's object unchanged", size=9.5, color=SLATE, bold=True)
f.box(14, 190, 264, 56, "", fill=SOFT, stroke="#cbd5e1")
for i, t in enumerate(["bumpCopy(cc) returned 100", "client object after the call: n = 0", "rule: a copy is safe but costs its size"]):
    f.text(24, 204 + i * 16, t, size=9.5, color=SLATE, anchor="start")
f.box(300, 30, 130, 40, "client JVM\nreal RefImpl n = 0", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(446, 30, 126, 40, "server holds a stub\n$Proxy2", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(430, 50), (446, 50)], color=AMBER)
f.text(436, 88, "stub passed: 282 bytes", size=9.5, color=AMBER, bold=True)
f.text(436, 100, "server calls bump() 3 times", size=9.5, color=TEAL, bold=True)
for i in range(3):
    f.arrow([(560, 110 + i * 12), (340, 110 + i * 12)], color=TEAL, sw=1.2)
f.box(300, 150, 130, 30, "client n = 3", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(300, 190, 272, 56, "", fill=SOFT, stroke="#cbd5e1")
for i, t in enumerate(["bumpRef(rc) returned 3; client n = 3", "server saw a stub, not the impl (false)", "callbacks ran on RMI TCP Connection threads"]):
    f.text(310, 204 + i * 16, t, size=9.5, color=SLATE, anchor="start")
```

```svgfig label="5.7" caption="The server runs each remote call in its own thread. Four clients each called a method that sleeps 200 ms: the calls overlapped and all four finished in 203 ms, while the same four calls made one after another took 802 ms, a speed-up of 3.95 (computed). The server threads are named RMI TCP Connection(n). Because several calls may reach one object at the same moment, a remote object must be thread-safe: the counter in this unit uses a synchronized increment()."
f = Fig(580, 196)
seq, con = 802, 203
sp = seq / con
assert 3.9 < sp < 4.0
sc = 380 / 802
f.text(290, 14, "4 calls of 200 ms each (to scale, ms)", size=11, color=NAVY, bold=True)
f.text(10, 40, "one by one", size=10, color=SLATE, anchor="start", bold=True)
for i in range(4):
    f.box(130 + i * 200 * sc, 28, 200 * sc - 2, 24, "%d" % 200, fill=SAND, stroke=AMBER, size=9, bold=True)
f.text(130 + seq * sc + 6, 40, "802 ms", size=10, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(10, 96, "together", size=10, color=SLATE, anchor="start", bold=True)
for i in range(4):
    f.box(130, 70 + i * 22, 203 * sc, 18, "thread %d" % (i + 1), fill=MINT, stroke=TEAL, size=9, bold=True, r=3)
f.text(130 + con * sc + 6, 114, "203 ms", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(290, 172, "speed-up = 802 / 203 = %.2f" % sp, size=10.5, color=NAVY, bold=True)
f.text(290, 188, "shared state in the remote object needs synchronized or an atomic class", size=9.5, color=RED, bold=True)
```

```svgfig label="5.8" caption="Seven failures of the real run and the exception RMI raised for each (the first six in package java.rmi, the declared and runtime exceptions as thrown by the method). A second bind of the same name gave AlreadyBoundException; a lookup of an unknown name NotBoundException; a declared exception of the method (InsufficientFunds, balance 500 less than 800) and a runtime exception (IllegalArgumentException, bad amount) arrived unchanged; an argument that is neither Serializable nor Remote gave MarshalException caused by NotSerializableException; a call on an unexported object gave NoSuchObjectException (no such object in table); and a lookup at port 51999 where no registry runs gave ConnectException caused by Connection refused."
f = Fig(580, 282)
hd = [("situation", 10, 190), ("exception raised", 204, 180), ("message or cause", 388, 186)]
for t, x, w in hd:
    f.box(x, 6, w, 22, t, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=3)
rows = [
 ("bind the same name twice", "AlreadyBoundException", "Calc", AMBER),
 ("lookup of an unknown name", "NotBoundException", "Nope", AMBER),
 ("method throws InsufficientFunds", "InsufficientFunds (unchanged)", "balance 500 < 800", TEAL),
 ("method throws a runtime exception", "IllegalArgumentException", "bad amount", TEAL),
 ("argument not Serializable or Remote", "MarshalException", "cause NotSerializableException", RED),
 ("call on an unexported object", "NoSuchObjectException", "no such object in table", RED),
 ("no registry listens at port 51999", "ConnectException", "cause: Connection refused", RED),
]
for i, (a, b, c, col) in enumerate(rows):
    y = 34 + i * 32
    fl = {AMBER: SAND, TEAL: MINT, RED: ROSE}[col]
    f.box(10, y, 190, 28, a, fill="#ffffff", stroke="#cbd5e1", color=SLATE, size=9, r=3)
    f.box(204, y, 180, 28, b, fill=fl, stroke=col, size=9, bold=True, r=3)
    f.box(388, y, 186, 28, c, fill="#ffffff", stroke="#cbd5e1", color=SLATE, size=9, r=3)
f.text(290, 272, "amber: naming   teal: the method itself   red: the distribution layer", size=9, color=SLATE)
```

```svgfig label="5.9" caption="Why a blind retry is dangerous. The server executed increment() and its counter became 1, but the reply was lost (in the real run the first reply was discarded to simulate it). The client, getting no answer, called increment() again and the counter became 2, although the client believes it ran the operation once; the measured counter after both attempts was 2. The three safe habits are shown at the bottom: use idempotent operations such as setBalance(800), send a request number the server remembers, or put the work in a transaction."
f = Fig(580, 262)
lanes = [("client", 90, NAVY), ("network", 290, AMBER), ("server", 490, TEAL)]
for t, x, c in lanes:
    f.text(x, 14, t, size=12, color=c, bold=True)
    f.line(x, 22, x, 176, color="#cbd5e1", sw=2)
f.arrow([(94, 44), (486, 44)], color=NAVY, label="1 increment()", lpos=(190, 38), lsize=9)
f.box(430, 52, 120, 22, "counter 0 -> 1", fill=MINT, stroke=TEAL, size=9, bold=True)
f.arrow([(486, 92), (296, 92)], color=TEAL, dash=True)
f.text(290, 106, "X", size=18, color=RED, bold=True)
f.text(395, 86, "reply 1 lost", size=9, color=RED, bold=True)
f.text(100, 122, "timeout: no answer", size=9.5, color=NAVY, bold=True, anchor="start")
f.arrow([(94, 140), (486, 140)], color=NAVY, label="2 increment() again", lpos=(190, 134), lsize=9)
f.box(430, 146, 120, 22, "counter 1 -> 2", fill=ROSE, stroke=RED, size=9, bold=True)
f.box(10, 190, 560, 22, "Result: the client ran the operation once, the server ran it twice (counter = 2)", fill=ROSE, stroke=RED, size=10, bold=True)
for i, (t, a) in enumerate([("idempotent call:\nsetBalance(800)", "safe to repeat"), ("request number:\nserver remembers it", "repeat is ignored"), ("transaction:\ncommit or roll back", "all or nothing")]):
    x = 10 + i * 190
    f.box(x, 220, 180, 36, t, fill=MINT, stroke=TEAL, size=9, bold=True)
```

```svgfig label="5.10" caption="CORBA architecture. A single interface file, college.idl, is fed to an IDL compiler, which writes the client stub for one language (say Java) and the server skeleton for another (say C++). The client calls the stub, the stub hands the request to its Object Request Broker (ORB), the ORBs talk to each other over the standard protocol IIOP on TCP, and the server's ORB passes the call through the Portable Object Adapter (POA) to the servant. A Naming Service plays the role of the RMI registry. Because the contract is the IDL, neither side needs to know the other's language."
f = Fig(580, 308)
f.box(215, 6, 150, 34, "college.idl\nthe one contract", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(240, 40), (110, 66)], color=AMBER, label="IDL compiler", lpos=(140, 50), lsize=9)
f.arrow([(340, 40), (470, 66)], color=AMBER, label="IDL compiler", lpos=(440, 50), lsize=9)
f.text(95, 82, "client (any language)", size=10.5, color=NAVY, bold=True)
f.text(485, 82, "server (any language)", size=10.5, color=TEAL, bold=True)
cl = ["Client program\nreg.find(7)", "IDL stub\n(generated)", "ORB\nfinds the object", "IIOP over TCP"]
sv = ["Servant\nthe real code", "Skeleton and POA\n(generated)", "ORB\nroutes the request", "IIOP over TCP"]
for i in range(4):
    y = 92 + i * 48
    f.box(10, y, 190, 38, cl[i], fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    f.box(380, y, 190, 38, sv[i], fill=MINT, stroke=TEAL, size=9.5, bold=True)
    if i < 3:
        f.arrow([(105, y + 38), (105, y + 48)], color=SLATE)
        f.arrow([(475, y + 48), (475, y + 38)], color=SLATE)
f.arrow([(200, 249), (380, 249)], color=AMBER, both=True, label="GIOP messages", lpos=(290, 241), lsize=9)
f.box(240, 140, 100, 50, "Naming\nService\nname -> ref", fill=SAND, stroke=AMBER, size=9, bold=True)
f.arrow([(200, 175), (240, 168)], color=AMBER, dash=True)
f.arrow([(380, 175), (340, 168)], color=AMBER, dash=True)
f.text(290, 296, "Java stubs and C++ skeletons come from the same IDL file", size=9.5, color=SLATE, bold=True)
```

```svgfig label="5.11" caption="Two wire formats and the IDL type map. Left: a CORBA message begins with a 12-byte GIOP header (the magic letters GIOP, version 1.2, a flags byte, a message-type byte where 0 is Request and 1 is Reply, and a 4-byte size), while the RMI stream of the real run began with the 7 bytes J R M I, version 2 and K. Right: the standard IDL to Java mapping: long is int, long long is long, short is short, string is String, boolean is boolean, a struct becomes a class and a sequence becomes an array. The 4 magic bytes of GIOP are computed in the figure."
f = Fig(580, 268)
mg = [0x47, 0x49, 0x4f, 0x50]
assert "".join(chr(x) for x in mg) == "GIOP"
f.text(145, 14, "GIOP header: 12 bytes", size=11, color=NAVY, bold=True)
parts = [("GIOP", "47 49 4f 50", 4, BLUE, NAVY), ("version", "01 02", 2, SAND, AMBER), ("flags", "00", 1, MINT, TEAL), ("type", "00", 1, ROSE, RED), ("size", "4 bytes", 4, BLUE, NAVY)]
tot = sum(p[2] for p in parts)
assert tot == 12
x = 10
for n, h, w, fl, st in parts:
    pw = 270 * w / 12 - 2
    f.box(x, 26, pw, 34, "", fill=fl, stroke=st)
    if w > 1:
        f.text(x + pw / 2, 38, n, size=9.5, color=st, bold=True, vmid=True)
        f.text(x + pw / 2, 52, h, size=9, color=SLATE, vmid=True)
    else:
        f.text(x + pw / 2, 76 if n == "flags" else 88, n + " " + h, size=8.5, color=st, bold=True)
    x += pw + 2
f.text(145, 106, "type 0 = Request, 1 = Reply", size=9.5, color=SLATE)
f.text(145, 136, "RMI stream: 7 bytes", size=11, color=TEAL, bold=True)
for i, (t, w, fl, st) in enumerate([("JRMI", 4, BLUE, NAVY), ("ver 2", 2, SAND, AMBER), ("K", 1, MINT, TEAL)]):
    ws = [4, 2, 1]
    xx = 10 + sum(ws[:i]) * 38
    f.box(xx, 148, ws[i] * 38 - 2, 30, t, fill=fl, stroke=st, size=9.5, bold=True)
f.text(145, 196, "both start with a magic number", size=9.5, color=SLATE, bold=True)
f.text(145, 212, "so a server rejects a wrong protocol at once", size=9.5, color=SLATE)
f.box(10, 224, 270, 38, "GIOP is the same for every language;\nJRMP only speaks Java", fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9.5)
f.text(435, 14, "IDL type -> Java type", size=11, color=NAVY, bold=True)
mp = [("long", "int"), ("long long", "long"), ("short", "short"), ("string", "String"), ("boolean", "boolean"), ("struct Student", "class Student"), ("sequence<long>", "int[]"), ("interface Registrar", "interface, Helper, Holder")]
for i, (a, b) in enumerate(mp):
    y = 26 + i * 27
    f.box(300, y, 120, 23, a, fill=SAND, stroke=AMBER, size=9, bold=True, r=3)
    f.arrow([(420, y + 11), (432, y + 11)], color=SLATE, sw=1.2)
    f.box(432, y, 140, 23, b, fill=MINT, stroke=TEAL, size=8.5, bold=True, r=3)
```

```svgfig label="5.12" caption="Choosing a technology for a remote call today. If the other side is not Java or is a browser, use REST with JSON; if services are internal, typed and busy, gRPC (HTTP/2 and Protocol Buffers, whose .proto file plays the role of IDL) is the modern choice; if work should be decoupled in time, put a message queue between the parts. Java RMI is kept for existing Java-only systems and for teaching, and CORBA only for maintaining old ORB-based systems, usually behind a gateway."
f = Fig(580, 268)
f.box(190, 6, 200, 28, "Call a remote service", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True)
f.arrow([(290, 34), (290, 48)], color=SLATE)
f.box(190, 48, 200, 34, "Can the caller move on\nwithout waiting?", fill=SAND, stroke=AMBER, size=9, bold=True)
f.arrow([(190, 65), (85, 65), (85, 100)], color=AMBER, label="yes", lpos=(130, 59), lsize=9)
f.box(10, 100, 150, 34, "message queue\n(Kafka, RabbitMQ)", fill=MINT, stroke=TEAL, size=9, bold=True)
f.arrow([(290, 82), (290, 104)], color=SLATE, label="no", lpos=(302, 97), lsize=9)
f.box(190, 104, 200, 34, "Are all callers Java,\nin one team?", fill=SAND, stroke=AMBER, size=9, bold=True)
f.arrow([(390, 121), (485, 121), (485, 150)], color=AMBER, label="yes", lpos=(440, 115), lsize=9)
f.box(400, 150, 170, 44, "old system: keep RMI\nnew system: prefer gRPC", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.arrow([(290, 138), (290, 160)], color=SLATE, label="no", lpos=(302, 153), lsize=9)
f.box(190, 160, 200, 34, "Typed, fast,\ninternal calls?", fill=SAND, stroke=AMBER, size=9, bold=True)
f.arrow([(190, 177), (100, 177), (100, 222)], color=AMBER, label="yes", lpos=(145, 171), lsize=9)
f.box(10, 222, 180, 38, "gRPC\n(.proto, HTTP/2)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(290, 194), (290, 222)], color=SLATE, label="no", lpos=(302, 212), lsize=9)
f.box(200, 222, 180, 38, "REST and JSON\n(any language, browser)", fill=MINT, stroke=TEAL, size=9, bold=True)
f.box(392, 222, 180, 38, "CORBA: only to maintain\nan existing ORB estate", fill=ROSE, stroke=RED, size=8.5, bold=True)
```

### 5.5.1 Eight uses of remote-object ideas in Nepal

RMI itself is now mostly met in older Java systems and in examinations, but every idea in this unit (a stub, a name lookup, a copy against a reference, a thread per call, a retry) lives on in the services that Nepali students use every day. Each point below says where the idea appears.

1. **Branch banking and core banking.** A teller screen in a branch does not hold the accounts; it calls services in the bank's data centre, and each call crosses a network (Figure 5.1). A call that took 1 nanosecond locally takes tens of microseconds even on one machine (Figure 5.4), and much more over a real link. Good designs therefore send one coarse request, such as a whole deposit slip, and not many tiny calls.
2. **Payment gateways such as ConnectIPS and Fonepay.** When a payment request is sent and the answer is lost, the wallet cannot know whether the money moved. A blind retry could debit a customer twice (Figure 5.9). Real payment services avoid this with a unique request number that the server remembers, so a repeated request is recognised and answered again, not run again.
3. **The Nagarik App and government back ends.** The app talks to servers of several offices, and many of those servers are written in different languages. For this reason such services use REST and JSON over HTTPS, not Java RMI, which only speaks Java (Figure 5.12). The ideas are still the same: a name or URL is looked up, arguments are copied into a message, and every call can fail.
4. **Tribhuvan University results and EMIS portals.** On result day thousands of students ask the server at the same moment. The server runs each request in its own thread, exactly as an RMI server does (Figure 5.7), so the shared parts, such as a hit counter, must be thread-safe. A synchronized counter gave the right numbers in the unit's run; an unprotected one would lose counts, as Unit 1 showed.
5. **Electricity bill and utility counters.** A counter in a ward office asks the central billing server for the dues of a customer number. The request and the reply are copies of small objects (Figure 5.5), and the counter must show a clear error when the server is unreachable, as ConnectException does (Figure 5.8). The screen must never freeze while it waits, so the call runs in a background thread with a timeout.
6. **Hospital and laboratory systems.** A doctor's computer sends a test request and later receives the result. The request can carry a callback object, so the laboratory calls the doctor's program when the result is ready (Figure 5.6), instead of the program asking again and again. The patient record travels by value, a copy, so the lab cannot change the original by mistake.
7. **Telecom and equipment management.** Telecom companies run equipment from several makers, and older management systems describe each device in IDL and talk through CORBA and IIOP (Figures 5.10 and 5.11). A graduate who joins such a company may have to maintain this code, even though new systems choose gRPC or REST. Knowing the stub, skeleton and ORB makes the old code readable.
8. **BCA projects and college labs.** A common project is a chat or an attendance system in which clients call a server object and the server calls back each client. The client must find the server's address (Figure 5.2), and a wrong java.rmi.server.hostname is the classic reason for a connection that hangs. Testing on the loopback address with a fixed registry port makes the project easy to run in a lab without a network.

## Formula and fact sheet

- Remote interface extends `Remote`; methods `throws RemoteException`; implementation extends `UnicastRemoteObject`.
- Server: `LocateRegistry.createRegistry(port)` + `rebind(name, obj)`; client: `getRegistry(host, port)` + `lookup(name)`. Default registry port 1099.
- Parameters: serializable → by value (copy); `Remote` objects → by reference (stub).
- Every remote call can fail: handle `RemoteException`; retries may repeat non-idempotent operations.
- CORBA: ORB + IDL + IIOP; removed from the JDK in Java 11.

## Chapter summary

- RMI lets a client call methods on an object in another JVM through a stub; a registry maps names to stubs; the transport is TCP (JRMP).
- Serializable arguments are copied (so the server cannot change the caller's object), remote objects are referenced; the object's state stays on the server.
- Distribution adds failure modes, so remote methods declare `RemoteException` and callers must handle partial failure.
- CORBA offers language-neutral distributed objects with IDL, an ORB and IIOP but is obsolete in the JDK; REST and gRPC are today's choices.

## Practice

1. Explain the RMI architecture: stub, remote reference layer, transport and registry.
2. List the steps to write an RMI application.
3. What must a remote interface look like? Why does every method throw `RemoteException`?
4. Distinguish pass by value and pass by reference in RMI with an example from the program above.
5. What is the RMI registry, on which port does it listen by default, and what do `bind`, `rebind` and `lookup` do?
6. Why might a retry after a `RemoteException` be dangerous?
7. Define CORBA, ORB, IDL and IIOP.
8. Compare RMI and CORBA in five points.
9. Write the IDL for an interface with one method `add(in long a, in long b)` returning a long.
10. Name two modern alternatives to RMI/CORBA and what they use instead of IDL.

::: note Answers and worked solutions
**1.** The client calls a method on the stub; the stub marshals the arguments and sends them through the remote reference layer and the TCP transport to the server's JVM, which unmarshals them and invokes the real object; the result returns the same way. The registry gives the client its first stub by name.
**2.** Write the remote interface; write the implementation; write the server that creates or locates the registry and binds the object; write the client that looks it up; compile and run registry, server and client.
**3.** `public interface Calculator extends Remote { int add(int a, int b) throws RemoteException; }`. Network failure is always possible, so the interface forces callers to deal with `RemoteException`.
**4.** `Point` is `Serializable`: `translate(mine, 10, 20)` received a copy, changed it and returned a new object; `mine` still printed (1,2). The `Calculator` is a `Remote`: the client holds a stub, and increments change the one server object (1, 2, 3, then 4 from a second client).
**5.** A simple naming service that maps names to remote stubs; default port 1099. `bind` adds a binding (fails if it exists), `rebind` adds or replaces, `lookup` returns the stub for a name.
**6.** The first call may have executed on the server even though the reply was lost, so repeating a non-idempotent call such as `increment` or "transfer money" runs it twice.
**7.** CORBA: language-neutral distributed object standard of the OMG. ORB: the broker that routes requests. IDL: the interface description language. IIOP: the standard TCP protocol between ORBs.
**8.** RMI is Java-only, uses Java interfaces, is simpler, uses JRMP and is still in the JDK; CORBA is multi-language, uses IDL, is complex, uses IIOP, offers many services and was removed from the JDK in 11.
**9.** `interface Calculator { long add(in long a, in long b); };`
**10.** REST/JSON over HTTP (resources and URLs, description via OpenAPI) and gRPC (HTTP/2 with Protocol Buffers, whose `.proto` files play the role of IDL).
:::

## Model answers for Unit 5

**Q1. Explain the architecture of Java RMI and how a remote call travels from client to server. (10 marks)**

**Introduction.** Remote Method Invocation lets a program in one JVM call a method of an object that lives in another JVM as if it were a local object. The call looks ordinary, but a stub, a transport and a registry do the hidden work (Fig. 5.1).

**The parts.**

1. **Remote interface.** It extends `java.rmi.Remote`, and every method declares `throws RemoteException`. It is the contract the client sees.
2. **Implementation.** The server class implements the interface, usually by extending `UnicastRemoteObject`, which exports the object on a TCP port. In the run, the object was exported on port 33225, chosen by the system.
3. **Stub.** The client holds a stub, a proxy that implements the same interface. In Java 17 it is a dynamic proxy of class `jdk.proxy1.$Proxy0`, so no `rmic` is needed.
4. **Remote reference layer.** It marshals the arguments into bytes and unmarshals the result.
5. **Transport.** A TCP connection carries the Java Remote Method Protocol; the first bytes were `4a 52 4d 49 00 02 4b`, the letters JRMI, version 2 and the stream code (Fig. 5.3).
6. **Registry.** A naming service, on port 1099 by default (51234 in the run), maps a name such as `Calc` to a stub. The server calls `rebind`, and the client calls `lookup`.

**Path of one call.** The client calls `calc.add(19, 23)` on the stub. The stub and the reference layer marshal the two ints and send a 50-byte request. The server's transport receives it, the dispatch layer unmarshals the arguments and calls `Impl.add`, and the answer 42 returns in 27 bytes. The lookup before it moved 559 bytes out and 624 bytes in over two connections, and the 5,000 calls that followed opened no new socket, because connections are reused (Fig. 5.2).

| Layer | Client side | Server side |
|---|---|---|
| Application | calls the interface | real object |
| Proxy | stub | dispatch (skeleton role) |
| Reference | marshals arguments | marshals result |
| Transport | TCP socket | ServerSocket |

**Conclusion.** RMI hides the network behind a method call, but it cannot hide its cost or its failures. Even on one machine the call took 53.0 microseconds against 1 nanosecond for a local call, so a designer treats a remote call as an expensive operation that can fail (Fig. 5.4).

**Q2. Write the steps of a minimal RMI application with the key code. (5 marks)**

An RMI application needs five steps, and the same steps were used in the unit's program.

1. **Write the remote interface.** It extends `Remote`, and each method throws `RemoteException`.
2. **Write the implementation.** It extends `UnicastRemoteObject` and has a constructor that throws `RemoteException`.
3. **Write the server.** It creates or finds the registry and binds the object.
4. **Write the client.** It gets the registry, looks up the name and calls the stub.
5. **Run.** Start the registry and server first, then the client. Set `java.rmi.server.hostname` to an address the client can reach, and allow the registry port and the object's port through the firewall.

```
public interface Calculator extends Remote {
    int add(int a, int b) throws RemoteException;
}
public class CalculatorImpl extends UnicastRemoteObject implements Calculator {
    public CalculatorImpl() throws RemoteException { super(); }
    public int add(int a, int b) { return a + b; }
}
// server
Registry reg = LocateRegistry.createRegistry(51234);
reg.rebind("Calc", new CalculatorImpl());
// client
Registry r = LocateRegistry.getRegistry("127.0.0.1", 51234);
Calculator c = (Calculator) r.lookup("Calc");
System.out.println(c.add(19, 23));   // 42
```

In the real run this printed 42 after a 50-byte request and a 27-byte reply (Fig. 5.2). Notice that the client code never mentions sockets, bytes or ports of the object: the stub finds the object's port inside the reference that the registry returned. The server must also keep a reference to the registry or the object, otherwise the object may be garbage collected and later calls fail with `NoSuchObjectException`. A lookup of a name that was never bound threw `NotBoundException`, and a second `bind` of a used name threw `AlreadyBoundException`; `rebind` replaces silently, which is why servers usually use it (Fig. 5.8).

**Q3. Distinguish pass by value and pass by reference in RMI with the experiment of the unit. (5 marks)**

RMI passes an argument in one of two ways, according to its type (Fig. 5.6).

**Pass by value.** A primitive or a `Serializable` object is turned into bytes and rebuilt at the other end, so the server works on a copy. In the experiment a `CopyCounter` was sent to the server, which added 100 and returned 100, but the client's own object still held 0. The copy of this small object cost 47 bytes, but an `int[1000]` costs 4,027 bytes and an `ArrayList` of 1,000 `Integer` objects 10,125 bytes, so a big argument is expensive every time it is sent (Fig. 5.5).

**Pass by reference.** An object that implements `Remote` is not copied. The receiver gets a stub, which is only 282 bytes however large the object is. In the experiment a `RefCounter` was passed, and the server called `bump()` three times; each call ran in the client's JVM, in a thread named `RMI TCP Connection`, and the client's counter became 3. The server's argument was an instance of a proxy class, not of the real class.

| Point | By value | By reference |
|---|---|---|
| Type needed | `Serializable` | `Remote` |
| Where the work runs | at the receiver, on a copy | at the home JVM |
| Cost | size of the object | 282-byte stub, but every call crosses the network |

An argument that is neither type fails with `MarshalException`, caused by `NotSerializableException`.

**Q4. How is a remote call different from a local call? Discuss cost, concurrency and failure with a diagram reference. (10 marks)**

**Introduction.** RMI makes a remote call look like a local call, but the two differ in speed, in how arguments are passed, in concurrency and, above all, in the ways they can fail. A programmer who forgets this writes slow and fragile systems.

**Differences.**

1. **Cost.** A local `add` took 1.01 nanoseconds in the run, and the same call through RMI took 53.0 microseconds, about 52,000 times longer, on one machine with no real network (Fig. 5.4). A thousand fine calls would cost about 53 milliseconds.
2. **Payload.** A call needs 42 bytes of overhead, and each int sent costs 4 bytes more (Fig. 5.3). A 100,000-element array took 5,712 microseconds, about 70 MB per second.
3. **Parameters.** Serializable arguments are copied, and Remote arguments are passed as stubs (Fig. 5.6). A local call shares the object itself.
4. **Concurrency.** The server runs each call in its own thread. Four clients calling a 200 ms method finished in 203 ms, against 802 ms one by one (Fig. 5.7), so the remote object must be thread-safe.
5. **Failure.** A local call either runs or throws. A remote call may fail before, during or after the work, and the caller cannot tell which. The exceptions of the run were `ConnectException`, `NoSuchObjectException`, `MarshalException`, `NotBoundException` and `AlreadyBoundException` (Fig. 5.8).
6. **Retry.** If the reply is lost, repeating the call may repeat the work. In the run a lost reply and one retry made the server counter 2 although the client had asked for one increment (Fig. 5.9).

| Aspect | Local call | Remote call |
|---|---|---|
| Time | about 1 ns | about 53 us on loopback |
| Arguments | shared | copied or stubbed |
| Failure | exception only | silent loss possible |
| Retry | harmless | may repeat the work |

**Remedies.** Use few coarse methods, set timeouts, make operations idempotent (such as `setBalance(800)`), send a request number that the server remembers, or use a transaction.

**Conclusion.** A remote call is a network message in disguise. The wise rule is to design the interface around that fact: coarse, thread-safe, and safe to repeat.

**Q5. What is the RMI registry? Explain `bind`, `rebind`, `lookup` and the default port. (5 marks)**

The RMI registry is a simple naming service that stores bindings from names to remote stubs. A client needs a first stub to start with, and the registry gives it by name, like a telephone directory that gives a number for a name (Plate 5.1).

1. **Starting it.** The server calls `LocateRegistry.createRegistry(port)`, or an operator runs the `rmiregistry` tool. The default port is 1099; the run used 51234.
2. **`bind(name, stub)`.** It adds a binding and throws `AlreadyBoundException` if the name exists.
3. **`rebind(name, stub)`.** It adds a binding or replaces an old one without complaint.
4. **`lookup(name)`.** It returns the stub for the name, or throws `NotBoundException` for an unknown name (the run: `NotBoundException: Nope`).
5. **Names as URLs.** A name may be written as `rmi://host:1099/Calc`.

In the run, `getRegistry` and `lookup` moved 559 bytes out and 624 bytes in, and used two connections: one to the registry port and one to the object's own port (Fig. 5.2). If no registry listens on the port, the client gets a `ConnectException` caused by `Connection refused`. The registry stores only stubs, never the objects, so the objects remain on the server.

**Q6. Name and explain the exceptions an RMI program must handle. (5 marks)**

Every remote method declares `RemoteException` because the network can fail. The run of the unit produced seven different failures (Fig. 5.8).

1. **`ConnectException`.** The client could not reach the registry or the server. The lookup at port 51999 failed with the cause `Connection refused`.
2. **`NoSuchObjectException`.** The object is no longer exported, for instance after the server unexported it; the message was `no such object in table`.
3. **`MarshalException` and `UnmarshalException`.** An argument or result could not be turned into bytes. Passing a plain `Object` caused a `MarshalException` with the cause `NotSerializableException`.
4. **`NotBoundException` and `AlreadyBoundException`.** These are naming errors from the registry.
5. **Exceptions of the method itself.** A declared exception such as `InsufficientFunds` (balance 500 less than 800) and a runtime exception such as `IllegalArgumentException` reach the client unchanged, so business errors can be handled in the normal way.

A caller should catch `RemoteException` separately from business exceptions, and it should decide whether a retry is safe. A retry of a non-idempotent call such as `increment()` may run it twice, as the counter of 2 showed (Fig. 5.9). Timeouts and clear messages to the user complete the handling.

**Q7. Explain the architecture of CORBA and compare it with RMI. (10 marks)**

**Introduction.** The Common Object Request Broker Architecture (CORBA) was defined by the Object Management Group in 1991 to let objects written in different languages and running on different machines call each other. It was removed from the JDK in Java 11, but it is still in syllabi and in older telecom, banking and defence systems.

**Architecture** (Fig. 5.10).

1. **IDL.** The Interface Definition Language describes interfaces in a language-neutral way. An IDL compiler reads `college.idl` and writes the client stub and the server skeleton in the chosen languages.
2. **Stub and skeleton.** The client calls the stub, and the skeleton passes the request to the servant.
3. **ORB.** The Object Request Broker finds the object and carries the request and reply.
4. **IIOP.** The Internet Inter-ORB Protocol, over TCP, is the standard wire format. Its messages start with a 12-byte GIOP header (Fig. 5.11).
5. **POA.** The Portable Object Adapter manages servants on the server.
6. **Naming Service.** It plays the role of the RMI registry.
7. **Type mapping.** IDL `long` becomes Java `int`, `string` becomes `String`, a `struct` becomes a class and a `sequence` an array.

**Comparison.**

| Aspect | RMI | CORBA |
|---|---|---|
| Languages | Java only | many |
| Contract | a Java interface | IDL file |
| Wire protocol | JRMP (7-byte stream header) | IIOP (12-byte GIOP header) |
| Complexity | low | high |
| Services | few | naming, events, transactions, security |
| Status | in the JDK | removed in Java 11 |

**Today.** Needs once met by CORBA are now met by REST and JSON, by gRPC, whose `.proto` file replaces IDL, and by message queues (Fig. 5.12).

**Example.** In a bank, a Java teller program may call a COBOL account object through CORBA: both sides compile the same `Account` interface from IDL, the Java side gets an `Account` interface plus `AccountHelper` and `AccountHolder` classes, and the COBOL side gets its own skeleton. Neither team needs to know how the other stores its data, and a change of the contract means a change of the IDL file and a recompile of both sides.

**Conclusion.** CORBA gives language freedom at the price of complexity, and RMI gives simplicity at the price of being Java-only. New systems choose REST or gRPC, and CORBA is maintained but rarely started.

**Q8. What is a callback in RMI, and why must remote objects be thread-safe? (5 marks)**

A **callback** is a call from the server back to the client. The client creates a remote object of its own, a listener, and passes it to the server as an argument. Because the listener implements `Remote`, the server receives a stub and not a copy, and each call through it runs in the client's JVM. In the run the server received an object of a proxy class that was not an instance of the real listener class, and three `ping` calls arrived in a thread named `RMI TCP Connection` (Fig. 5.6). Callbacks suit events such as a lab result being ready or a new chat message, because the client does not have to ask again and again. Each side now acts as both client and server, so both need an open port and a reachable host name.

**Thread safety.** The server runs every call in its own thread. Four clients calling a 200 ms method finished in 203 ms, not 802 ms, so the calls overlapped (Fig. 5.7). If two threads change one field together, an update can be lost, as shown in Unit 1. The shared counter therefore used `synchronized`, and similar fields need `synchronized`, a lock or an atomic class.

**Q9. Which technology would you choose today for a remote call, and why? (5 marks)**

The choice depends on four questions, as the decision chart shows (Fig. 5.12).

1. **Can the caller move on without waiting?** Then use a message queue such as Kafka or RabbitMQ. It decouples the two sides in time, and a lost reply does not stall the caller.
2. **Are all callers Java and in one team?** RMI works, but it is Java only, needs extra ports and ties the two sides to the same classes. An old system may keep it, while a new one should still prefer gRPC.
3. **Are the calls typed, fast and internal?** Choose gRPC. The `.proto` file serves as the contract, as IDL did, and HTTP/2 carries compact binary messages.
4. **Must any language or a browser call it?** Choose REST with JSON over HTTPS. This is the choice of the Nagarik App style of service, because every language has an HTTP client.

CORBA is chosen only to maintain an old system that already depends on an ORB, usually with a gateway in front of it. Whatever the choice, the lessons of this unit apply: calls are slow compared with local calls (53 microseconds against 1 nanosecond), arguments are copies, failures are silent, and a retry must be safe.
