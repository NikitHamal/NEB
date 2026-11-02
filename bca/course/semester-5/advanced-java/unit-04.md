---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 4
title: Network Programming with Sockets and HTTP
hours: 7
area: BCA 303 · Advanced Java Programming · Unit 4
---

In the Computer Networking book you saw TCP segments, UDP datagrams and HTTP messages as formats. Java turns each of them into a few lines of code: a `Socket` is one end of a TCP connection, a `DatagramSocket` sends UDP packets and `HttpClient` makes web requests. This unit writes real clients and servers and runs them on the loopback interface; every listing was compiled and executed, and the output is genuine. (The server picks a free port itself, so the programs never clash with anything on the machine.)

::: key What this unit gives you
- Addresses and ports in Java: `InetAddress`, `URI`, `URL`.
- TCP sockets: `ServerSocket`, `Socket`, one thread per client.
- UDP sockets: `DatagramSocket`, `DatagramPacket`.
- HTTP: a tiny `HttpServer` and the `HttpClient` API.
:::

## 4.1 Addresses, ports and URLs

A network endpoint is an **IP address plus a port**. `InetAddress.getByName("localhost")` resolves a host name (using DNS) and `getLoopbackAddress()` returns 127.0.0.1. A **`URI`** parses a resource name into its parts; a **`URL`** can also open a connection. Ports 0–1023 are well known and need administrator rights to bind; passing port **0** to a `ServerSocket` asks the system for any free port, which `getLocalPort()` then reveals.

## 4.2 TCP sockets

A TCP server follows a fixed pattern: create a `ServerSocket(port)`; loop on `accept()`, which blocks until a client connects and returns a `Socket` for that conversation; read and write through the socket's streams. A client creates `new Socket(host, port)` (which performs the three-way handshake) and uses the same streams. Wrap the streams: a `BufferedReader` for lines of text and a `PrintWriter` (with auto-flush) for replies. Closing the socket sends the FIN.

A server that handles one client at a time makes everyone else wait, because `accept()` and the read loop are sequential. The standard fix is to hand each accepted socket to a **new thread** (or a thread pool) so the main loop returns to `accept()` at once.

```java
import java.io.*;
import java.net.*;
import java.util.concurrent.*;
public class TcpEcho {
    public static void main(String[] args) throws Exception {
        ServerSocket server = new ServerSocket(0, 10, InetAddress.getLoopbackAddress());
        int port = server.getLocalPort();
        ExecutorService pool = Executors.newFixedThreadPool(4);
        Thread acceptor = new Thread(() -> {
            try {
                while (true) {
                    Socket s = server.accept();
                    pool.submit(() -> {
                        try (s; BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
                             PrintWriter out = new PrintWriter(s.getOutputStream(), true)) {
                            String line;
                            while ((line = in.readLine()) != null) {
                                if (line.equals("BYE")) { out.println("GOODBYE"); break; }
                                out.println(line.toUpperCase() + " (" + line.length() + " chars)");
                            }
                        } catch (IOException e) { }
                    });
                }
            } catch (IOException e) { }
        });
        acceptor.setDaemon(true); acceptor.start();
        for (String client : new String[]{"first", "second"}) {
            try (Socket s = new Socket(InetAddress.getLoopbackAddress(), port);
                 BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
                 PrintWriter out = new PrintWriter(s.getOutputStream(), true)) {
                out.println("hello from " + client); System.out.println(client + " got: " + in.readLine());
                out.println("advanced java"); System.out.println(client + " got: " + in.readLine());
                out.println("BYE"); System.out.println(client + " got: " + in.readLine());
                System.out.println(client + " connected from a high port: " + (s.getLocalPort() > 1023));
            }
        }
        server.close(); pool.shutdownNow();
    }
}
```
```output
first got: HELLO FROM FIRST (16 chars)
first got: ADVANCED JAVA (13 chars)
first got: GOODBYE
first connected from a high port: true
second got: HELLO FROM SECOND (17 chars)
second got: ADVANCED JAVA (13 chars)
second got: GOODBYE
second connected from a high port: true
```
Each client sees its own reply stream, because the server runs each connection in its own pool task. Always flush: `PrintWriter(…, true)` flushes on `println`; a buffered stream that is never flushed leaves the other side waiting forever, which is the most common socket bug.

### Typical problems

- **`BindException: Address already in use`**: another process (or an earlier run of your own server) holds the port.
- **`ConnectException: Connection refused`**: nothing is listening at that address and port, or a firewall blocks it.
- **`SocketTimeoutException`**: set `setSoTimeout(ms)` so `read()` does not block forever.
- **Message boundaries**: TCP is a byte stream; the protocol must mark where a message ends (newline, length prefix).

## 4.3 UDP sockets

A `DatagramSocket` has no connection. Each `DatagramPacket` carries up to about 64 KB of data plus the sender's or receiver's address; `receive()` blocks until a packet arrives; packets may be lost or reordered (on loopback they are not, so the demo is deterministic).

```java
import java.net.*;
import java.nio.charset.StandardCharsets;
public class UdpDemo {
    public static void main(String[] args) throws Exception {
        DatagramSocket server = new DatagramSocket(0, InetAddress.getLoopbackAddress());
        Thread t = new Thread(() -> {
            try {
                byte[] buf = new byte[512];
                DatagramPacket p = new DatagramPacket(buf, buf.length);
                server.receive(p);
                String msg = new String(p.getData(), 0, p.getLength(), StandardCharsets.UTF_8);
                byte[] reply = ("echo: " + msg.toUpperCase()).getBytes(StandardCharsets.UTF_8);
                server.send(new DatagramPacket(reply, reply.length, p.getAddress(), p.getPort()));
            } catch (Exception e) { }
        });
        t.start();
        try (DatagramSocket client = new DatagramSocket()) {
            client.setSoTimeout(2000);
            byte[] data = "namaste".getBytes(StandardCharsets.UTF_8);
            client.send(new DatagramPacket(data, data.length, InetAddress.getLoopbackAddress(), server.getLocalPort()));
            DatagramPacket in = new DatagramPacket(new byte[512], 512);
            client.receive(in);
            System.out.println(new String(in.getData(), 0, in.getLength(), StandardCharsets.UTF_8));
        }
        t.join(); server.close();
    }
}
```
```output
echo: NAMASTE
```
Use UDP for DNS-style queries, streaming and games where speed beats reliability; use TCP when every byte must arrive in order.

## 4.4 HTTP in Java

The JDK contains a small web server (`com.sun.net.httpserver.HttpServer`, handy for tests and tiny services) and, since Java 11, a modern client (`java.net.http.HttpClient`) supporting HTTP/1.1 and HTTP/2, synchronous and asynchronous calls. Older code uses `URL.openConnection()` and `HttpURLConnection`.

```java
import com.sun.net.httpserver.*;
import java.io.*;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
public class HttpDemo {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/hello", ex -> {
            String q = ex.getRequestURI().getQuery(); String body = "{\"greeting\":\"Namaste " + (q == null ? "guest" : q.replace("name=", "")) + "\"}";
            byte[] b = body.getBytes(StandardCharsets.UTF_8);
            ex.getResponseHeaders().add("Content-Type", "application/json"); ex.sendResponseHeaders(200, b.length);
            try (OutputStream os = ex.getResponseBody()) { os.write(b); }
        });
        server.createContext("/echo", ex -> {
            String in = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            byte[] b = ("method=" + ex.getRequestMethod() + " body=" + in).getBytes(StandardCharsets.UTF_8);
            ex.sendResponseHeaders(201, b.length);
            try (OutputStream os = ex.getResponseBody()) { os.write(b); }
        });
        server.start();
        String base = "http://127.0.0.1:" + server.getAddress().getPort();
        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> r1 = client.send(HttpRequest.newBuilder(URI.create(base + "/hello?name=Sita")).GET().build(), HttpResponse.BodyHandlers.ofString());
        System.out.println(r1.statusCode() + " " + r1.headers().firstValue("content-type").orElse("?") + " " + r1.body());
        HttpResponse<String> r2 = client.send(HttpRequest.newBuilder(URI.create(base + "/echo")).POST(HttpRequest.BodyPublishers.ofString("a=1&b=2")).build(), HttpResponse.BodyHandlers.ofString());
        System.out.println(r2.statusCode() + " " + r2.body());
        HttpResponse<String> r3 = client.send(HttpRequest.newBuilder(URI.create(base + "/missing")).GET().build(), HttpResponse.BodyHandlers.ofString());
        System.out.println(r3.statusCode() + " (no context registered)");
        URI u = URI.create("https://example.com:8443/notes/unit4.html?v=2#sockets");
        System.out.println(u.getScheme() + " | " + u.getHost() + " | " + u.getPort() + " | " + u.getPath() + " | " + u.getQuery() + " | " + u.getFragment());
        System.out.println("localhost resolves to " + InetAddress.getByName("localhost").getHostAddress());
        server.stop(0);
    }
}
```
```output
200 application/json {"greeting":"Namaste Sita"}
201 method=POST body=a=1&b=2
404 (no context registered)
https | example.com | 8443 | /notes/unit4.html | v=2 | sockets
localhost resolves to 127.0.0.1
```
The 404 for an unknown path is generated by the server itself; the `URI` parser splits a URL into scheme, host, port, path, query and fragment, the same parts you met in the Computer Networking book.

## 4.5 Design notes for network programs

- **One thread per client** is simple but does not scale to thousands of connections; use a bounded **thread pool**, or **NIO** (`Selector`, non-blocking channels) / frameworks (Netty) for many mostly-idle connections.
- **Protocol design**: choose line-based text for simple tools, length-prefixed binary for efficiency, HTTP/JSON for interoperability. Always handle partial reads.
- **Security**: never trust input from the socket (validate lengths and formats); use TLS (`SSLSocket`, `HttpsURLConnection`, or HTTPS in `HttpClient`) rather than sending secrets in clear; do not deserialize objects from untrusted peers (Unit 1).
- **Resource cleanup**: close sockets in `finally` or try-with-resources; set timeouts.

## Formula and fact sheet

- TCP server: `ServerSocket(port)` → `accept()` → `Socket` → streams; client: `new Socket(host, port)`. Port 0 = any free port.
- One thread (or pool task) per accepted socket; flush output; set timeouts.
- UDP: `DatagramSocket`, `DatagramPacket(buf, len[, addr, port])`, `send`, `receive`; no connection.
- HTTP: `HttpClient.newHttpClient().send(HttpRequest, BodyHandlers.ofString())`; server `HttpServer.create`, `createContext`.
- `URI` parts: scheme, host, port, path, query, fragment.

## Chapter summary

- A TCP socket is a reliable byte-stream connection; the server accepts connections and typically serves each in its own thread; the client connects, writes and reads.
- UDP sockets send independent packets without a connection or guarantees.
- The JDK includes an HTTP client and a small HTTP server; `URI`/`URL` split names into their parts.
- Real programs need timeouts, framing, TLS, validation and cleanup.

## Practice

1. Write the steps and code of a TCP echo server and client.
2. Why does a single-threaded server serve one client at a time and how do you fix it?
3. What exceptions occur when the port is in use, when nothing is listening and when a read stalls?
4. Compare TCP and UDP sockets in Java and give an application for each.
5. What does port 0 mean in `new ServerSocket(0)`?
6. Why must `PrintWriter` be created with auto-flush (or flushed) in a request–reply protocol?
7. Write an `HttpClient` call that POSTs a string and prints the status code and body.
8. Split `https://example.com:8443/notes/unit4.html?v=2#sockets` into its components with `URI`.
9. Why are message boundaries a problem with TCP, and how can a protocol mark them?
10. Name three security precautions for network programs.

::: note Answers and worked solutions
**1.** Server: `ServerSocket ss = new ServerSocket(5000); Socket s = ss.accept(); BufferedReader in = ...; PrintWriter out = new PrintWriter(s.getOutputStream(), true); while ((line = in.readLine()) != null) out.println(line);` Client: `Socket s = new Socket("localhost", 5000);` write a line with `out.println`, read the reply with `in.readLine()`.
**2.** `accept()` and the read loop block, so the second client waits until the first finishes. Hand every accepted socket to a new thread or a thread pool task so the main thread goes back to `accept()`.
**3.** `BindException` (address in use); `ConnectException: Connection refused`; `SocketTimeoutException` if `setSoTimeout` was set.
**4.** TCP (`Socket`): connection, reliable ordered byte stream, e.g. file transfer, web. UDP (`DatagramSocket`): connectionless packets, unreliable, e.g. DNS lookups, streaming, games.
**5.** The operating system picks a free ephemeral port; `getLocalPort()` returns it.
**6.** The reply may sit in a buffer and never be sent; the other side then waits for it forever (deadlock). Auto-flush on `println`, or call `flush()`.
**7.** Create `HttpClient client = HttpClient.newHttpClient();` and a request `HttpRequest req = HttpRequest.newBuilder(URI.create(url)).POST(HttpRequest.BodyPublishers.ofString("a=1")).build();`, then `HttpResponse<String> r = client.send(req, HttpResponse.BodyHandlers.ofString());` and print `r.statusCode()` and `r.body()`.
**8.** scheme `https`, host `example.com`, port 8443, path `/notes/unit4.html`, query `v=2`, fragment `sockets`.
**9.** TCP delivers a stream of bytes, not messages; one `read` may return half a message or two. Use a delimiter (newline), a length prefix, or a self-describing format such as HTTP headers with Content-Length.
**10.** Use TLS for sensitive data; validate and limit all input; use timeouts and resource limits; never deserialize untrusted objects; run with least privilege.
:::
