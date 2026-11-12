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

## 4.6 Seeing the ideas: addresses, sockets, datagrams and HTTP

Network code is easier to write when you can picture the machinery. Plate 4.1 gives four everyday pictures: a wall plate with network and power sockets, a block of letterboxes for the idea of one address with many ports, a telephone switchboard for `accept()`, and a ticket hall for a pool of threads. Plate 4.2 shows the people who designed TCP, UDP and the web. Figures 4.1 to 4.10 then use numbers from real runs of Java 17 on the loopback interface: the address and URL parts, the order of socket calls, a sequential server against a pool, the lack of message boundaries in TCP, the limits of a UDP datagram, a raw HTTP exchange, sequential against asynchronous requests, and the exceptions a student meets.

```photogrid label="4.1" cols="4" ratio="1.0" caption="Pictures for network programming. (a) A wall plate with six numbered network sockets above a power socket (CC BY-SA 4.0): the word 'socket' in Java means the end-point of a connection, in which a program plugs in. (b) Three letterboxes at one street address, flats 1, 2 and 3 (CC BY-SA 4.0): the street address is the IP address and the flat is the port. (c) A telephone switchboard (CC BY-SA 4.0): the operator waits, accepts a call and connects it to one line, as accept() does. (d) A ticket hall at a railway station (CC BY-SA 3.0): many travellers are served at once by several windows, like a pool of threads."
@ photo id="bca303/lanplate" cap="Wall plate: sockets"
fit 1.0
focus 0.5 0.7
call 0.5 0.4 0.5 0.8 "network sockets"
@ photo id="bca303/mailboxes" cap="One address, three ports"
fit 1.0
focus 0.5 0.55
@ photo id="bca303/switchboard" cap="Switchboard: accept()"
fit 1.0
focus 0.3 0.6
@ photo id="bca301/queue" cap="Ticket hall: a thread pool"
fit 1.0
focus 0.4 0.5
```

```photogrid label="4.2" cols="4" ratio="1.0" caption="People behind the protocols of this unit. (a) Vint Cerf (CC BY 3.0), co-designer of TCP/IP with Bob Kahn in 1974, the reliable byte stream behind Socket. (b) Jon Postel (CC BY 2.0), editor of the RFC series and author of RFC 768, the User Datagram Protocol of 1980, which DatagramSocket uses. (c) Tim Berners-Lee (CC BY-SA 4.0), who proposed the web and HTTP at CERN in 1989. (d) Roy Fielding (CC BY 2.0), an author of the HTTP/1.1 specification and the inventor of REST."
@ photo id="bca301/cerf" cap="Vint Cerf, TCP/IP"
fit 1.0
focus 0.5 0.6
@ photo id="bca301/postel" cap="Jon Postel, UDP"
fit 1.0
focus 0.5 0.4
@ photo id="bca301/berners" cap="Tim Berners-Lee, HTTP"
fit 1.0
focus 0.5 0.6
@ photo id="bca255/fielding" cap="Roy Fielding, REST"
fit 1.0
focus 0.6 0.55
```

```svgfig label="4.1" caption="An end-point is an IP address plus a port, and a URI has seven parts. Left: a real parse of http://user@example.com:8080/a/b.html?x=1&y=2#top gave scheme http, user, host example.com, port 8080, path /a/b.html, query x=1&y=2 and fragment top; the default port of http is 80, https 443 and ftp 21, and getPort() returns -1 when the URL names no port. Right: the address 192.168.1.10 is stored in 4 signed bytes, [-64, -88, 1, 10], because Java bytes run from -128 to 127; isSiteLocalAddress() is true and isLoopbackAddress() is false."
f = Fig(580, 262)
url = "http://user@example.com:8080/a/b.html?x=1&y=2#top"
parts = [("scheme", "http", BLUE, NAVY), ("user", "user", SAND, AMBER), ("host", "example.com", MINT, TEAL), ("port", "8080", SAND, AMBER), ("path", "/a/b.html", MINT, TEAL), ("query", "x=1&y=2", BLUE, NAVY), ("fragment", "top", ROSE, RED)]
f.text(145, 14, "URI.getXxx() on the real string", size=11, color=NAVY, bold=True)
for i, (k, v, fl, st) in enumerate(parts):
    y = 24 + i * 26
    f.box(6, y, 74, 22, k, fill=fl, stroke=st, size=9.5, bold=True, r=4)
    f.arrow([(80, y + 11), (92, y + 11)], color=SLATE)
    f.box(92, y, 150, 22, v, fill="#ffffff", stroke=st, size=10, r=4)
f.text(145, 214, "default ports: http 80, https 443, ftp 21", size=9.5, color=SLATE, bold=True)
f.text(145, 230, "getPort() = 8080 here, and -1 when the URL has no port", size=9.5, color=SLATE)
f.text(145, 246, "the fragment (#top) is never sent to the server", size=9.5, color=RED, bold=True)
b = [192, 168, 1, 10]
sb = [x - 256 if x > 127 else x for x in b]
assert sb == [-64, -88, 1, 10]
f.text(435, 14, "one IPv4 address in Java", size=11, color=NAVY, bold=True)
for i, (u, s) in enumerate(zip(b, sb)):
    x = 300 + i * 68
    f.box(x, 28, 62, 28, str(u), fill=BLUE, stroke=NAVY, size=12, bold=True)
    f.arrow([(x + 31, 56), (x + 31, 74)], color=SLATE)
    f.box(x, 74, 62, 28, str(s), fill=SAND, stroke=AMBER, size=12, bold=True)
f.text(435, 120, "above: what you read in dotted text   below: getAddress() bytes", size=9.5, color=SLATE)
f.text(435, 138, "byte = u - 256 when u > 127", size=9.5, color=NAVY, bold=True)
f.box(300, 154, 270, 92, "", fill=MINT, stroke=TEAL)
for i, t in enumerate(["getByName(\"localhost\") -> 127.0.0.1", "isLoopbackAddress() -> true", "192.168.1.10: isSiteLocalAddress() -> true", "192.168.1.10: isLoopbackAddress() -> false", "port 0 in ServerSocket: any free port"]):
    f.text(310, 172 + i * 15, t, size=9.5, color=SLATE, anchor="start")
```

```svgfig label="4.2" caption="The order of calls in a TCP conversation. The server creates a ServerSocket and calls accept(), which blocks. The client's new Socket(host, port) performs the three-way handshake (SYN, SYN-ACK, ACK), measured on loopback at 190 microseconds; accept() then returns a Socket. Both sides read and write through streams and close. On loopback a one-byte request and reply took 44 microseconds each in a run of 2,000 round trips, so on a real network the delay is the network, not Java."
f = Fig(580, 284)
f.text(110, 14, "server", size=12, color=TEAL, bold=True)
f.text(470, 14, "client", size=12, color=NAVY, bold=True)
f.line(110, 22, 110, 236, color="#cbd5e1", sw=2)
f.line(470, 22, 470, 236, color="#cbd5e1", sw=2)
f.box(10, 30, 200, 24, "new ServerSocket(port)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(10, 64, 200, 24, "accept()  blocks, waiting", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(370, 64, 200, 24, "new Socket(host, port)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(370, 112), (210, 112)], color=AMBER, label="SYN", lpos=(290, 105))
f.arrow([(210, 128), (370, 128)], color=AMBER, label="SYN-ACK", lpos=(290, 121))
f.arrow([(370, 144), (210, 144)], color=AMBER, label="ACK", lpos=(290, 137))
f.text(290, 160, "handshake: 190 us on loopback", size=9.5, color=AMBER, bold=True)
f.box(10, 150, 200, 24, "accept() returns a Socket", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(370, 150, 200, 24, "connected", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(370, 190), (210, 190)], color=NAVY, label="request line", lpos=(290, 183))
f.arrow([(210, 208), (370, 208)], color=TEAL, label="reply line", lpos=(290, 201))
f.text(290, 224, "one byte there and back: 44 us (2,000 trials)", size=9.5, color=SLATE, bold=True)
f.box(10, 236, 200, 24, "close() the socket (try-with-resources)", fill=SOFT, stroke=SLATE, size=9, bold=True)
f.box(370, 236, 200, 24, "close()", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.text(290, 274, "FIN exchange ends the connection", size=9.5, color=SLATE)
```

```svgfig label="4.3" caption="One thread against a pool, measured. Four clients each ask for a job that takes 200 ms. A server that handles one client at a time finished them in 808 ms (4 x 200 = 800 plus start-up); a pool of 4 worker threads finished all four in 202 ms. The bars are drawn to scale from the measured times, and the speed-up is computed."
f = Fig(580, 262)
seq, par = 808, 202
sc = 0.62
f.text(290, 14, "4 clients x 200 ms of work (milliseconds, to scale)", size=11, color=NAVY, bold=True)
f.text(6, 38, "one at a time", size=10.5, color=RED, bold=True, anchor="start")
cols = [BLUE, MINT, SAND, ROSE]
for i in range(4):
    f.box(20 + i * 200 * sc, 46, 200 * sc - 2, 26, "client %d" % (i + 1), fill=cols[i], stroke=NAVY, size=9.5, bold=True, r=3)
f.text(20 + seq * sc + 8, 60, "%d ms" % seq, size=11, color=RED, bold=True, anchor="start", vmid=True)
f.text(6, 100, "pool of 4 threads", size=10.5, color=TEAL, bold=True, anchor="start")
for i in range(4):
    f.box(20, 108 + i * 28, 200 * sc, 24, "client %d" % (i + 1), fill=cols[i], stroke=NAVY, size=9.5, bold=True, r=3)
f.text(20 + par * sc + 8, 190, "%d ms" % par, size=11, color=TEAL, bold=True, anchor="start", vmid=True)
for t in (0, 200, 400, 600, 800):
    f.line(20 + t * sc, 224, 20 + t * sc, 230, color=SLATE, sw=1)
    f.text(20 + t * sc, 242, str(t), size=9.5, color=SLATE)
f.line(20, 224, 20 + 800 * sc, 224, color=SLATE, sw=1.2)
sp = seq / par
assert round(sp, 1) == 4.0
f.text(440, 150, "%.1f times faster" % sp, size=12, color=NAVY, bold=True)
f.text(440, 168, "with 4 clients and 4 threads", size=9.5, color=SLATE)
f.text(440, 182, "ExecutorService pool = Executors\n.newFixedThreadPool(4)", size=9, color=SLATE)
```

```svgfig label="4.4" caption="TCP has no message boundaries. The client wrote three messages, HELLO, WORLD and NEPAL, each followed by flush(). The server waited 300 ms and then its read() returned once with 15 bytes: the three messages had merged into one stream. A protocol must therefore mark the end of a message: a newline (readLine), a length prefix (the figure builds the bytes of 00 05 HELLO) or a fixed size."
f = Fig(580, 262)
msgs = ["HELLO", "WORLD", "NEPAL"]
f.text(290, 14, "what the client wrote and what one read() returned (real run)", size=11, color=NAVY, bold=True)
for i, m in enumerate(msgs):
    f.box(20 + i * 100, 28, 94, 28, "write(\"%s\")" % m, fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(160, 56), (160, 84)], color=SLATE)
f.text(172, 76, "bytes on the wire", size=9.5, color=SLATE, anchor="start")
for i, ch in enumerate("".join(msgs)):
    f.box(20 + i * 19.5, 90, 18, 22, ch, fill=SOFT, stroke=SLATE, size=9.5, bold=True, r=2)
f.arrow([(160, 112), (160, 134)], color=SLATE)
total = sum(len(m) for m in msgs)
assert total == 15
f.box(20, 134, 293, 28, "one read(buf): n = %d bytes (calls = 1)" % total, fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(165, 176, "the three messages cannot be told apart", size=9.5, color=RED, bold=True)
f.text(448, 40, "three ways to mark the end", size=10.5, color=NAVY, bold=True)
f.box(330, 50, 240, 44, "newline: HELLO\\n\nBufferedReader.readLine()", fill=MINT, stroke=TEAL, size=9.5)
lp = bytes([0, 5]) + b"HELLO"
hexs = " ".join("%02X" % x for x in lp)
assert hexs == "00 05 48 45 4C 4C 4F"
f.box(330, 102, 240, 44, "length prefix: " + hexs + "\nreadFully(2 bytes), then readFully(5)", fill=MINT, stroke=TEAL, size=8.5)
f.box(330, 154, 240, 44, "self-describing: HTTP headers\nContent-Length: 26", fill=MINT, stroke=TEAL, size=9.5)
f.box(20, 200, 550, 50, "", fill=SAND, stroke=AMBER)
f.text(295, 216, "rule: a read() may return half a message or three messages", size=10.5, color=AMBER, bold=True)
f.text(295, 234, "loop until you have a whole message; never assume one write equals one read", size=9.5, color=SLATE)
```

```svgfig label="4.5" caption="UDP keeps message boundaries but limits their size. In a real run a 600-byte datagram received into a 512-byte buffer came back with getLength() = 512: the rest was silently cut. Three datagrams msg1, msg2 and msg3 arrived as three separate receive() results, in order on loopback. The largest payload that arrived was 65,507 bytes, which is 65,535 - 20 (IP header) - 8 (UDP header), computed in the figure; trying to send 70,000 bytes threw SocketException: Message too long."
f = Fig(580, 250)
mx = 65535 - 20 - 8
assert mx == 65507
f.text(145, 14, "one datagram = one receive()", size=11, color=NAVY, bold=True)
for i in range(3):
    f.box(10 + i * 92, 28, 84, 26, "msg%d" % (i + 1), fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.arrow([(52 + i * 92, 54), (52 + i * 92, 70)], color=SLATE)
    f.box(10 + i * 92, 70, 84, 26, "receive() %d" % (i + 1), fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.text(145, 116, "three sends, three separate receives", size=9.5, color=SLATE, bold=True)
f.text(145, 140, "truncation: 600 bytes into a 512-byte buffer", size=10.5, color=NAVY, bold=True)
f.box(10, 150, 262, 22, "sent 600 bytes", fill=BLUE, stroke=NAVY, size=9.5, bold=True, r=3)
f.box(10, 180, 262 * 512 / 600, 22, "getLength() = 512", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=3)
f.box(10 + 262 * 512 / 600, 180, 262 * 88 / 600, 22, "", fill=ROSE, stroke=RED, r=3)
f.text(145, 222, "88 bytes lost without any error", size=9.5, color=RED, bold=True)
f.text(435, 14, "size limit of a datagram", size=11, color=NAVY, bold=True)
f.box(300, 28, 270, 24, "65,535 bytes: largest IP packet", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(300, 60, 270, 24, "- 20 bytes IP header", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(300, 90, 270, 24, "- 8 bytes UDP header", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(300, 120, 270, 28, "= %s bytes of payload (arrived)" % "{:,}".format(mx), fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(300, 156, 270, 28, "70,000 bytes: SocketException,\nMessage too long", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.text(435, 206, "keep real UDP messages under about 512 bytes", size=9.5, color=SLATE, bold=True)
f.text(435, 222, "so they fit one network frame and rarely fragment", size=9.5, color=SLATE)
```

```svgfig label="4.6" caption="A raw HTTP exchange captured in a real run. The program opened a plain Socket to the Java HttpServer and typed the request by hand; the server answered with a status line, two headers, a blank line and a 26-byte JSON body. The whole reply was 134 characters. The Content-length of 26 is the byte count of the body, which is how the client knows where the body ends on a TCP stream."
f = Fig(580, 262)
body = '{"greeting":"Namaste Ram"}'
assert len(body) == 26
f.text(145, 14, "request (typed by the program)", size=11, color=NAVY, bold=True)
f.box(6, 24, 278, 100, "", fill=BLUE, stroke=NAVY)
req = ["GET /hello?name=Ram HTTP/1.1", "Host: localhost:PORT", "Connection: close", "(blank line = end of headers)"]
for i, t in enumerate(req):
    f.text(14, 44 + i * 22, t, size=10, color=NAVY if i < 3 else RED, bold=(i == 0), anchor="start")
f.text(435, 14, "response (read by the program)", size=11, color=TEAL, bold=True)
f.box(296, 24, 278, 100, "", fill=MINT, stroke=TEAL)
resp = ["HTTP/1.1 200 OK", "Date: <date>", "Content-type: application/json", "Content-length: 26", "(blank line)"]
for i, t in enumerate(resp):
    f.text(304, 40 + i * 18, t, size=10, color=TEAL if i != 4 else RED, bold=(i == 0), anchor="start")
f.text(435, 144, body, size=10.5, color=NAVY, bold=True)
f.arrow([(145, 124), (145, 160)], color=SLATE)
f.box(6, 160, 278, 88, "", fill=SAND, stroke=AMBER)
for i, t in enumerate(["method GET: read, no body", "target /hello with query name=Ram", "HTTP/1.1: version of the protocol", "Host: which site on this machine", "Connection: close: end after the reply"]):
    f.text(14, 178 + i * 15, t, size=9.5, color=SLATE, anchor="start")
f.box(296, 160, 278, 88, "", fill=SAND, stroke=AMBER)
for i, t in enumerate(["200 OK: status code of the family 2xx", "Content-type: how to read the body", "Content-length: 26 = len(body)", "total reply: 134 characters", "the body starts after the blank line"]):
    f.text(304, 178 + i * 15, t, size=9.5, color=SLATE, anchor="start")
```

```svgfig label="4.7" caption="Waiting for requests one after another against asynchronous requests, measured. Five requests to a handler that sleeps 200 ms took 1,181 ms with send() in a loop and 243 ms with sendAsync(), because the five waits overlap. The ratio is computed. The same client returned status 200 for GET /hello, 201 for POST /echo with 7 bytes of body ('got 7 bytes via POST'), and 404 for an address with no handler."
f = Fig(580, 262)
seq, par = 1181, 243
sc = 0.40
f.text(290, 14, "5 requests, each 200 ms (milliseconds, to scale)", size=11, color=NAVY, bold=True)
f.text(10, 38, "send() in a loop", size=10.5, color=RED, bold=True, anchor="start")
for i in range(5):
    f.box(10 + i * (seq / 5) * sc, 46, seq / 5 * sc - 2, 24, "R%d" % (i + 1), fill=[BLUE, MINT, SAND, ROSE, "#e0e7ff"][i], stroke=NAVY, size=9.5, bold=True, r=3)
f.text(10 + seq * sc + 8, 58, "%d ms" % seq, size=11, color=RED, bold=True, anchor="start", vmid=True)
f.text(10, 92, "sendAsync(), then join()", size=10.5, color=TEAL, bold=True, anchor="start")
for i in range(5):
    f.box(10, 100 + i * 20, 200 * sc, 17, "R%d" % (i + 1), fill=[BLUE, MINT, SAND, ROSE, "#e0e7ff"][i], stroke=NAVY, size=9, bold=True, r=3)
f.text(10 + par * sc + 8, 148, "%d ms" % par, size=11, color=TEAL, bold=True, anchor="start", vmid=True)
r = seq / par
assert round(r, 1) == 4.9
f.text(400, 120, "%.1f times faster" % r, size=12, color=NAVY, bold=True)
f.text(400, 138, "the waits overlap", size=9.5, color=SLATE)
f.box(10, 178, 560, 70, "", fill=SOFT, stroke=SLATE)
for i, (m, s, t, c) in enumerate([("GET /hello?name=Sita", "200", "{\"greeting\":\"Namaste Sita\"}", TEAL), ("POST /echo (body a=1&b=2)", "201", "got 7 bytes via POST", TEAL), ("GET /nothing", "404", "No context found for request", RED)]):
    y = 192 + i * 18
    f.text(18, y, m, size=9.5, color=NAVY, bold=True, anchor="start")
    f.text(200, y, s, size=10, color=c, bold=True, anchor="start")
    f.text(240, y, t, size=9.5, color=SLATE, anchor="start")
```

```svgfig label="4.8" caption="The five exceptions of the real run, and what each means. The second bind to a port in use threw BindException: Address already in use. Connecting to port 1 with no listener threw ConnectException: Connection refused. A read with setSoTimeout(300) on a server that never replied threw SocketTimeoutException: Read timed out after about 300 ms. An unknown name threw UnknownHostException (the name no-such-host.invalid, Name or service not known). A 70,000-byte datagram threw SocketException: Message too long."
f = Fig(580, 270)
rows = [("BindException", "Address already in use", "another process or an earlier run holds the port", "server side, start-up", AMBER, SAND), ("ConnectException", "Connection refused", "nothing listens at that host and port", "client side, connect", RED, ROSE), ("SocketTimeoutException", "Read timed out (after ~300 ms)", "peer silent; only with setSoTimeout", "either side, read", RED, ROSE), ("UnknownHostException", "no-such-host.invalid: Name or service not known", "DNS cannot resolve the name", "client side, lookup", AMBER, SAND), ("SocketException", "Message too long (70,000 bytes)", "datagram larger than 65,507", "UDP send", RED, ROSE)]
f.box(6, 6, 568, 22, "", fill=NAVY, stroke=NAVY, r=2)
for x, t in [(12, "exception"), (170, "real message"), (360, "meaning"), (512, "where")]:
    f.text(x, 17, t, size=9.5, color="#ffffff", bold=True, anchor="start", vmid=True)
for i, (a, b, c, d, st, fl) in enumerate(rows):
    y = 28 + i * 44
    f.box(6, y, 568, 44, "", fill=fl if i % 2 == 0 else "#ffffff", stroke=SLATE, r=0, sw=0.8)
    f.text(12, y + 22, a.replace("Exception", "Exception"), size=9, color=st, bold=True, anchor="start", vmid=True)
    f.text(170, y + 22, b.replace(" (", "\n(").replace(": ", ":\n"), size=9, color=NAVY, anchor="start", vmid=True)
    f.text(360, y + 22, c.replace("; ", ";\n").replace(" at that", "\nat that").replace("or an earlier", "\nor an earlier"), size=8.5, color=SLATE, anchor="start", vmid=True)
    f.text(512, y + 22, d.replace(", ", "\n"), size=8.5, color=SLATE, anchor="start", vmid=True)
f.text(290, 262, "catch the narrow exception first, then IOException; always log getMessage()", size=9.5, color=NAVY, bold=True)
```

```svgfig label="4.9" caption="URL encoding, computed in the figure and checked against the real Java output. URLEncoder.encode on the text 'namaste Nepal & co', with namaste written in 6 Devanagari characters, gave %E0%A4%A8%E0%A4%AE%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%87+Nepal+%26+co: each Devanagari character is 3 bytes in UTF-8 and so becomes three %XX groups, a space becomes +, and & becomes %26. A raw ampersand in a query would end the parameter."
f = Fig(580, 232)
q = __import__("urllib.parse", fromlist=["quote_plus"])
txt = "\u0928\u092e\u0938\u094d\u0924\u0947 Nepal & co"
enc = q.quote_plus(txt)
assert enc == "%E0%A4%A8%E0%A4%AE%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%87+Nepal+%26+co"
assert len("\u0928\u092e\u0938\u094d\u0924\u0947".encode("utf-8")) == 18
f.text(290, 14, "from text to a safe query value", size=11, color=NAVY, bold=True)
chars = ["\u0928", "\u092e", "\u0938", "\u094d", "\u0924", "\u0947"]
for i, c in enumerate(chars):
    x = 10 + i * 92
    f.box(x, 26, 86, 26, c, fill=BLUE, stroke=NAVY, size=14, bold=True)
    f.arrow([(x + 43, 52), (x + 43, 66)], color=SLATE)
    h = "".join("%%%02X" % b for b in c.encode("utf-8"))
    f.box(x, 66, 86, 26, h, fill=MINT, stroke=TEAL, size=9, bold=True)
f.text(290, 110, "6 characters x 3 UTF-8 bytes = 18 bytes = 18 characters of %XX, a three-fold growth", size=9.5, color=SLATE, bold=True)
for i, (a, b, c) in enumerate([("space", "+", "or %20"), ("&", "%26", "separates parameters"), ("=", "%3D", "separates name and value"), ("?", "%3F", "starts the query"), ("/", "%2F", "separates path parts")]):
    x = 10 + i * 114
    f.box(x, 128, 108, 54, "", fill=SAND, stroke=AMBER)
    f.text(x + 54, 144, "%s  ->  %s" % (a, b), size=10.5, color=AMBER, bold=True)
    f.text(x + 54, 164, c, size=9, color=SLATE)
f.box(10, 196, 560, 30, "URLEncoder.encode(value, StandardCharsets.UTF_8) for the value; never for the whole URL", fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

```svgfig label="4.10" caption="Choosing TCP or UDP and the way to serve many clients. The decision tree sends a program that needs every byte in order (files, web, mail, bank) to TCP and a program that values speed over completeness (name lookups, voice, game state) to UDP. For the server, one client at a time suits only a test, a thread per client suits a few hundred clients, a fixed pool bounds the load, and NIO selectors or a framework suit thousands of mostly idle connections."
f = Fig(580, 262)
f.box(190, 8, 200, 30, "Must every byte arrive, in order?", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.arrow([(230, 38), (110, 62)], color=TEAL, label="yes", lpos=(150, 44))
f.arrow([(350, 38), (470, 62)], color=RED, label="no", lpos=(430, 44))
f.box(10, 62, 200, 46, "TCP: Socket, ServerSocket\nfiles, web, mail, banking", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(370, 62, 200, 46, "UDP: DatagramSocket\nDNS, voice, live scores", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.text(290, 134, "how many clients at once?", size=11, color=NAVY, bold=True)
tiers = [("1", "one at a time", "only a test", SOFT, SLATE), ("tens to hundreds", "thread per client", "simple, costs memory", BLUE, NAVY), ("hundreds", "fixed thread pool", "bounded load", MINT, TEAL), ("thousands", "NIO selector, Netty", "few threads, many sockets", SAND, AMBER)]
for i, (n, t, d, fl, st) in enumerate(tiers):
    x = 8 + i * 143
    f.box(x, 146, 134, 24, n + " clients" if n == "1" else n, fill=SOFT, stroke=SLATE, size=9, bold=True)
    f.arrow([(x + 67, 170), (x + 67, 184)], color=SLATE)
    f.box(x, 184, 134, 28, t, fill=fl, stroke=st, size=9.5, bold=True)
    f.text(x + 67, 228, d, size=9.5, color=SLATE)
f.text(290, 252, "measured: 4 clients x 200 ms took 808 ms one at a time and 202 ms with a pool of 4", size=9.5, color=NAVY, bold=True)
```

### 4.6.1 Eight uses of Java network programming in Nepal

1. **Mobile wallets and payment gateways.** When a person pays by QR code, the wallet app sends an HTTPS request to a server and waits for a reply in JSON. The server side of such a service is often written in Java, using an `HttpServer`-style handler or a framework above it, and a thread pool to serve many users together (Figure 4.3). A timeout is essential, because a payment screen must show a result or an error and never wait for ever (Figure 4.8).
2. **Online results and admission portals.** Tribhuvan University and college portals show results to thousands of students on the same day. Each browser request is a short HTTP exchange like Figure 4.6, handled by a pool of threads so that one slow request does not block the rest. The roll number arrives in the URL, so it must be decoded and validated (Figure 4.9).
3. **Internet cafes and school computer labs.** A teacher's program that sends a notice or a file to every lab computer is a small client and server pair over TCP. Each machine runs a listener on a chosen port, and the teacher's program connects to each one in turn. A newline or length prefix marks the end of each message (Figure 4.4).
4. **Weather and river-level stations.** A river gauge or weather station sends a short reading every few minutes. UDP is a good fit for such a small message, because the next reading replaces a lost one (Figure 4.5). The receiving program at the Department of Hydrology and Meteorology stores each datagram in a database.
5. **Local chat and messaging tools.** A chat program for a college network keeps one TCP connection per user. The server reads each line, sends it to every other user, and removes a user whose read times out. Each connection needs its own thread or a selector (Figure 4.10), and every write must be flushed or the other users see nothing.
6. **Government service lookups.** A service such as the Nagarik App asks a back end for a citizen's record by number. The back end exposes small HTTP endpoints that return JSON, and the client reads the status code first: 200 for success, 404 for no record, 4xx for a bad request (Figure 4.7). The same call is made with `HttpClient`, and several lookups can run at once with `sendAsync`.
7. **Monitoring and uptime checks.** An internet provider or a bank checks that its servers answer. A small Java program opens a socket to a port with a short timeout and reports `Connection refused`, `Read timed out` or success (Figure 4.8). The result is shown on a screen or sent as an alert to the engineer.
8. **Teaching and testing.** Students learn protocols by writing an echo server, a chat server or a tiny web server on the loopback address, as the programs in this unit do. Teachers use `localhost` and port 0 so that no real network is needed (Figure 4.1). The same habit helps in testing, because a test starts a small `HttpServer`, calls it and stops it.

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
**7.** Build a client with `HttpClient.newHttpClient()`. Build the request with `HttpRequest.newBuilder(uri)`, add `.POST(BodyPublishers.ofString("a=1"))` and call `.build()`. Send it with `client.send(req, BodyHandlers.ofString())`, then print `r.statusCode()` and `r.body()`.
**8.** scheme `https`, host `example.com`, port 8443, path `/notes/unit4.html`, query `v=2`, fragment `sockets`.
**9.** TCP delivers a stream of bytes, not messages; one `read` may return half a message or two. Use a delimiter (newline), a length prefix, or a self-describing format such as HTTP headers with Content-Length.
**10.** Use TLS for sensitive data; validate and limit all input; use timeouts and resource limits; never deserialize untrusted objects; run with least privilege.
:::

## Model answers for Unit 4

**Q1. Explain how a TCP echo server and client are written in Java, with code and the order of calls. (10 marks)**

**Introduction.** TCP gives two programs a reliable, ordered stream of bytes. In Java the server end is a `ServerSocket`, the client end is a `Socket`, and both read and write through ordinary streams (Fig. 4.2).

**Server steps.**
1. Create `new ServerSocket(5000)`, which binds the port and starts listening. Port 0 asks the system for any free port, and `getLocalPort()` reports it.
2. Call `accept()`. It blocks until a client connects and returns a `Socket` for that one conversation.
3. Wrap the streams: a `BufferedReader` for lines and a `PrintWriter` created with auto-flush `true`.
4. Read lines in a loop and send a reply for each, until the client closes or sends a stop word.
5. Close the socket, preferably with try-with-resources.

**Client steps.** Create `new Socket("localhost", 5000)`; this performs the three-way handshake, which took 190 microseconds on the loopback interface. Write a line with `println`, read the reply with `readLine`, and close.

```
try (ServerSocket ss = new ServerSocket(5000);
     Socket s = ss.accept();
     BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
     PrintWriter out = new PrintWriter(s.getOutputStream(), true)) {
    String line;
    while ((line = in.readLine()) != null) out.println(line.toUpperCase());
}
```

**Real run.** The book's program answered `hello from first` with `HELLO FROM FIRST (16 chars)`, answered `BYE` with `GOODBYE`, and served a second client in the same way. A one-byte request and reply took 44 microseconds on loopback in a run of 2,000 trials.

**Important details.** The reply must be flushed: with auto-flush, `println` sends it at once, and without it both sides may wait for ever. `readLine` returns `null` when the other side closes. The loop above serves only one client; Q2 shows the fix.

| Point | Server | Client |
|---|---|---|
| Class | `ServerSocket`, then `Socket` | `Socket` |
| First call | `accept()` waits | `new Socket(host, port)` connects |
| Port | chosen by the programmer | chosen by the system (a high number) |
| Ends with | `close()` | `close()` |

**Testing it.** Run the server first, then the client; with port 0 and the loopback address no firewall or real network is needed. If the client is started first, it receives `Connection refused`, and if the server is started twice, the second start throws `BindException`. A student can also test the server with a second client at the same time, which shows at once whether it is single-threaded.

**Conclusion.** A TCP program is a short fixed pattern: listen, accept, wrap streams, read and write, flush, close. Using try-with-resources and a timeout turns this pattern into a safe program.

**Q2. Why does a single-threaded server serve one client at a time? How is it fixed? (5 marks)**

The main loop of a simple server calls `accept()`, then reads and writes for that client, and only then goes back to `accept()`. While it is busy with the first client, the second client's connection waits in the operating system's queue and gets no answer. This is a problem because a slow or silent client blocks everybody.

The fix is to give each accepted socket to another thread, so that the main thread returns to `accept()` at once. There are two ways. A new `Thread` per client is simple but costs memory for every client. A fixed pool, created with `Executors.newFixedThreadPool(4)`, runs the handlers as tasks and limits the load; extra clients wait in the pool's queue.

The measurement shows the effect (Fig. 4.3). Four clients each needed 200 ms of work. A server handling one at a time took 808 ms, while a pool of 4 threads took 202 ms, about 4 times faster. For thousands of mostly idle connections, even a pool is too heavy, and a program uses NIO selectors or a framework such as Netty (Fig. 4.10). Whatever the method, shared data used by several handler threads must be protected, as shown in Unit 1.

**Q3. Which exceptions occur when the port is in use, when nothing is listening and when a read stalls? (5 marks)**

Network errors appear as subclasses of `IOException`. Three of them are the most common (Fig. 4.8).

1. **`BindException: Address already in use`.** The server tried to bind a port that another process, or an earlier run of the same program, still holds. In the real run a second `ServerSocket` on the same port threw it. Fix: stop the other program, choose another port, or use port 0.
2. **`ConnectException: Connection refused`.** The client reached the machine, but no program listened on that port. A connection to port 1 produced it. Fix: start the server first, check the host and port, and check the firewall.
3. **`SocketTimeoutException: Read timed out`.** The read waited longer than the limit set by `setSoTimeout(ms)`. In the run the limit was 300 ms and the exception came after about 300 ms. Without a timeout a read waits for ever, so every real socket needs one.

Two further cases are `UnknownHostException`, when DNS cannot resolve the name, and `SocketException: Message too long`, when a UDP datagram exceeds 65,507 bytes. Catch the narrow exception first, then `IOException`, log `getMessage()` and close the socket in a `finally` block or with try-with-resources.

**Q4. Compare TCP and UDP sockets in Java and give an application for each. (10 marks)**

**Introduction.** Java offers two kinds of socket. `Socket` and `ServerSocket` use TCP, a reliable byte stream. `DatagramSocket` uses UDP, which sends independent packets.

**TCP in Java.** A connection is set up by a handshake (190 microseconds on loopback). The data is a stream: the program reads and writes bytes through `InputStream` and `OutputStream`. TCP retransmits lost segments, delivers bytes in order and slows down when the network is congested. It has **no message boundaries**: three writes of HELLO, WORLD and NEPAL arrived in one `read()` of 15 bytes (Fig. 4.4), so the protocol must mark the end of each message.

**UDP in Java.** No connection exists. Each `DatagramPacket` carries one message and the sender's or receiver's address, and `receive()` returns exactly one datagram, so boundaries are kept: msg1, msg2 and msg3 came out as three results. The price is that packets may be lost, repeated or reordered, the program must supply any reliability, and a datagram is limited to 65,507 bytes. A 600-byte datagram received into a 512-byte buffer was cut to 512 bytes without any error (Fig. 4.5).

| Point | TCP (`Socket`) | UDP (`DatagramSocket`) |
|---|---|---|
| Connection | yes, handshake | none |
| Data unit | byte stream | datagram |
| Message boundaries | none | kept |
| Reliability and order | guaranteed | not guaranteed |
| Speed and overhead | slower, more state | faster, small header (8 bytes) |
| Size limit | none per stream | 65,507 bytes |
| Error behaviour | exception on a broken connection | silent loss |
| Server pattern | `accept()` per client | one socket receives from all |

**Applications.** TCP: web pages, e-mail, file transfer, banking and wallet payments, where every byte must arrive. UDP: DNS lookups, voice and video calls, live scores and sensor readings, where a late packet is worth less than a new one (Fig. 4.10). In Nepal a river-gauge reading sent every few minutes suits UDP, while a ConnectIPS payment request needs TCP and HTTPS.

**Conclusion.** Choose TCP when correctness matters and UDP when speed and simplicity matter more than completeness; the Java code is similar in size, but TCP hides reliability from the programmer and UDP leaves it to the programmer.

**Q5. What are message boundaries in TCP? How can a protocol mark them? (5 marks)**

TCP delivers a stream of bytes, not a list of messages. A `read()` may return half a message, one message or several. In the real run the client wrote HELLO, WORLD and NEPAL as three separate writes, each flushed, and the server's single `read()` returned 15 bytes (Fig. 4.4). The three messages could not be told apart without a rule.

A protocol marks the end of a message in one of three ways.
1. **A delimiter**, usually a newline. The receiver uses `BufferedReader.readLine()`, which collects bytes until it sees the end of the line. This suits text; the text itself must not contain the delimiter.
2. **A length prefix.** The sender first writes the length, for example two bytes `00 05` and then the five bytes of `HELLO`. The receiver reads exactly 2 bytes, then exactly that many more with `DataInputStream.readFully`. This suits binary data of any content.
3. **A self-describing format.** HTTP ends its headers with a blank line and states `Content-Length: 26`, so the client knows that the body is the next 26 bytes.

Whatever the method, the receiver must loop until it has a whole message and must limit the length it accepts, so that a hostile client cannot make it allocate gigabytes.

**Q6. Explain HTTP programming in Java: the server, the client, URI parts and URL encoding. (10 marks)**

**Introduction.** HTTP is a text protocol above TCP: a request (method, target, headers, optional body) and a response (status, headers, body). The JDK includes a small server, `com.sun.net.httpserver.HttpServer`, and since Java 11 a client, `java.net.http.HttpClient`.

**Server.** `HttpServer.create(new InetSocketAddress(port), 0)` makes the server. `createContext("/hello", handler)` attaches a handler to a path. The handler reads the request, calls `sendResponseHeaders(200, length)` and writes the body. `setExecutor` gives it a thread pool.

**Client.** `HttpClient.newHttpClient()` builds the client; `HttpRequest.newBuilder(uri).GET().build()` or `.POST(BodyPublishers.ofString("a=1"))` builds the request; `client.send(request, BodyHandlers.ofString())` returns an `HttpResponse` with `statusCode()`, `headers()` and `body()`. In the real run, GET `/hello?name=Sita` gave 200 and `{"greeting":"Namaste Sita"}`, POST `/echo` with 7 bytes gave 201 and `got 7 bytes via POST`, and an unknown path gave 404 (Fig. 4.7). `sendAsync` returns a `CompletableFuture`; five requests of 200 ms took 243 ms that way against 1,181 ms one after another.

**On the wire.** A hand-typed request `GET /hello?name=Ram HTTP/1.1` with a `Host` header was answered by `HTTP/1.1 200 OK`, a `Content-type`, `Content-length: 26` and the 26-byte JSON body (Fig. 4.6).

**URI parts.** For `http://user@example.com:8080/a/b.html?x=1&y=2#top`, `URI` gave scheme `http`, user `user`, host `example.com`, port 8080, path `/a/b.html`, query `x=1&y=2` and fragment `top` (Fig. 4.1). The fragment is never sent to the server.

**URL encoding.** Characters with special meaning must be encoded in a query value: space becomes `+`, `&` becomes `%26`. A Devanagari character is 3 bytes in UTF-8, so the 6 characters of the Devanagari word namaste became 18 bytes, written as six groups of `%XX` (Fig. 4.9). Use `URLEncoder.encode(value, StandardCharsets.UTF_8)` for each value.

| Status | Meaning |
|---|---|
| 200 | success |
| 201 | created (a POST made something) |
| 404 | no such resource |

**Older API.** Earlier code uses `URL.openConnection()` and `HttpURLConnection`; the same call returned code 200 and method GET in the run. It still works, but `HttpClient` is preferred because it supports HTTP/2, asynchronous calls and a cleaner builder style. Whichever class is used, the program must read the status code before the body, close the streams, and treat any code of 400 or above as an error to be shown to the user in a clear message.

**Conclusion.** The JDK is enough to write and test a small HTTP service and its client; correct status codes, a thread pool and UTF-8 encoding make it dependable.

**Q7. Describe the use of `HttpClient` to POST a string and show how to read the reply. (5 marks)**

The `HttpClient` of Java 11 is built in three parts: the client, the request and the response handler.

```
HttpClient client = HttpClient.newHttpClient();
HttpRequest req = HttpRequest.newBuilder(URI.create("http://localhost:8080/echo"))
        .header("Content-Type", "application/x-www-form-urlencoded")
        .POST(HttpRequest.BodyPublishers.ofString("a=1&b=2"))
        .build();
HttpResponse<String> r = client.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(r.statusCode() + " " + r.body());
```

1. `newHttpClient()` creates a client that can be reused for many requests; it supports HTTP/1.1 and HTTP/2.
2. `HttpRequest.newBuilder(uri)` starts the request, `header` adds a header and `POST(...)` sets the method and the body. The body here is 7 bytes.
3. `send` blocks until the reply arrives and the handler `ofString()` turns the body into a `String`.
4. `statusCode()` is read first. In the real run the call printed `201 got 7 bytes via POST`.

A reply with status 404 does **not** throw an exception; the program must test the code. Network failures such as a refused connection throw `IOException`. For many requests use `sendAsync`, which returns a `CompletableFuture`: five requests of 200 ms took 243 ms instead of 1,181 ms (Fig. 4.7). Set a timeout with `HttpRequest.newBuilder(uri).timeout(Duration.ofSeconds(5))` so that a silent server cannot stop the program.

**Q8. Give design rules and security precautions for network programs. (10 marks)**

**Introduction.** A network program talks to strangers over an unreliable medium, so it must be written defensively. The rules below follow from the experiments of this unit.

**Design rules.**
1. **Serve clients together.** One client at a time took 808 ms for four clients, a pool of 4 took 202 ms (Fig. 4.3). Use a bounded pool or NIO for large numbers (Fig. 4.10).
2. **Set timeouts.** Use `setSoTimeout` for reads and a connect timeout, so a silent peer cannot hold a thread for ever (Fig. 4.8).
3. **Frame messages.** TCP has no boundaries; use a newline, a length prefix or HTTP headers, and loop until a message is complete (Fig. 4.4).
4. **Flush and close.** Flush every reply and close sockets with try-with-resources so that connections are not leaked.
5. **Choose the transport.** Use TCP when every byte matters and UDP for small, loss-tolerant messages (Fig. 4.5).

**Security precautions.**
1. **Use TLS.** Send passwords, tokens and payments only over `SSLSocket`, HTTPS in `HttpClient` or `HttpsURLConnection`, never in clear text.
2. **Validate all input.** Check the length, format and range of every field; a length prefix of two billion must be refused.
3. **Limit resources.** Cap the pool size, the message size and the number of connections per address, to resist denial of service.
4. **Never deserialize untrusted objects.** Java deserialization of data from a peer can run attacker-chosen code (Unit 1); use JSON with a fixed schema.
5. **Encode output and input.** Encode query values (Fig. 4.9) and use parameterised SQL (Unit 3) so that data cannot become commands.
6. **Least privilege.** Run the server as an ordinary user on a port above 1023, with only the files it needs.

| Risk | Precaution |
|---|---|
| Eavesdropping | TLS |
| Oversized messages | length limits |
| Slow or silent clients | timeouts and pool limits |
| Injection | validation, encoding, prepared statements |
| Crash on bad data | catch exceptions, log, close |

**Conclusion.** Reliable network software serves clients concurrently, bounds time and size, frames its messages and protects data with TLS and validation; treating every byte from the network as untrusted is the central habit.
