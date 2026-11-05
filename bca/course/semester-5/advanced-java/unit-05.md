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
