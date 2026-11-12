---
subject: Distributed System
grade: BCA Semester 6
unit: 2
title: Communication: Sockets, RPC, RMI, gRPC and Message Queues
hours: 8
area: BCA 355 · Distributed System · Unit 2
---

Every distributed algorithm in the later units ends in the same primitive: *process A sends bytes to process B, and B may or may not receive them*. This unit climbs the ladder from raw sockets to remote procedure calls, remote objects, gRPC and message queues, and studies the question that hides in every rung: what happens when a message or a reply is lost and the caller tries again?

::: key What this unit gives you
- Sockets (TCP vs UDP) and the client-server pattern.
- Marshalling: how data structures become bytes (fixed binary, JSON, Protocol Buffers varints), with verified byte layouts.
- RPC: stubs, the call sequence, parameter passing, and call semantics (maybe, at-least-once, at-most-once); why idempotence and request identifiers matter.
- RMI and gRPC; synchronous vs asynchronous and streaming calls.
- Message-oriented middleware: queues, publish-subscribe, delivery guarantees.
:::

## 2.1 Sockets

A **socket** is an endpoint of communication identified by an IP address and port number. The transport protocol decides the behaviour:

| | TCP (stream socket) | UDP (datagram socket) |
|---|---|---|
| Connection | Connection-oriented (three-way handshake) | Connectionless |
| Delivery | Reliable, ordered, byte stream, retransmits | Best effort, may lose, reorder or duplicate |
| Message boundaries | None (application must frame messages) | Preserved (one datagram per send) |
| Overhead | Higher (state, congestion control) | Low |
| Typical use | HTTP, SSH, databases, RPC | DNS queries, video/voice, game state, QUIC |

A TCP server calls `socket`, `bind`, `listen`, then loops on `accept`, giving a new socket per client; a client calls `socket` and `connect`. Because TCP is a *stream*, two `send` calls may arrive as one `recv`; programs add **framing**, such as a length prefix or a delimiter (a newline in HTTP/1.1 headers, a 4-byte length in many binary protocols). TCP's reliability is between two live endpoints only: if the peer crashes after the data reached its kernel but before the application handled it, the sender learns nothing. End-to-end acknowledgements must therefore be built at the application level. This idea (the end-to-end argument) is the reason RPC systems need their own retry logic.

## 2.2 Marshalling and serialization

Two machines can disagree about the representation of data: byte order (big-endian vs little-endian), the size of an `int`, character encoding, structure padding. **Marshalling** (serialization) flattens a data structure into a byte sequence in an agreed external format; **unmarshalling** rebuilds it. Common formats:

- **Fixed binary** such as XDR (Sun RPC) or C `struct` packing with network byte order. Compact and fast; the schema is outside the message.
- **Text:** XML (SOAP, XML-RPC), JSON (REST). Human-readable, self-describing, larger and slower to parse.
- **Schema-based binary:** Protocol Buffers, Avro, Thrift, MessagePack. Compact, versionable, fast.

The Protocol Buffers wire format encodes integers as **varints**: groups of 7 bits, least significant group first, with the top bit of each byte set when more bytes follow. A field is preceded by a **tag** byte equal to `(field_number << 3) | wire_type`; wire type 0 means varint, so field 1 with a varint has tag `0x08`. Small numbers take one byte, which is why protobuf messages are compact. The program packs a record by hand and encodes protobuf varints; the outputs are checked independently.

```python
import struct, json
rec = struct.pack("!I5sH", 150, b"Ram".ljust(5, b"\0"), 2082)
print("fixed binary:", rec.hex(" "), f"({len(rec)} bytes)")

def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)

print("varint(150):", varint(150).hex(" "))
print("varint(300):", varint(300).hex(" "))
msg = bytes([0x08]) + varint(150)
print("protobuf field 1 = 150:", msg.hex(" "))
js = json.dumps({"id": 150, "name": "Ram", "year": 2082}, separators=(",", ":"))
print("JSON:", js, f"({len(js)} bytes)")
```
```output
fixed binary: 00 00 00 96 52 61 6d 00 00 08 22 (11 bytes)
varint(150): 96 01
varint(300): ac 02
protobuf field 1 = 150: 08 96 01
JSON: {"id":150,"name":"Ram","year":2082} (35 bytes)
```
Read the first line: `!` selects network (big-endian) order, so 150 becomes `00 00 00 96`, the name is padded to five bytes and the year 2082 is `08 22`: eleven bytes in all, against 35 bytes for the same record in compact JSON. The varint of 150 is `96 01`: 150 = 1001 0110 in binary; the low seven bits `0010110` with the continuation bit set give `0x96`, and the remaining high part `1` gives `0x01`. Pointers and object references cannot be marshalled by value; systems either copy the whole reachable graph (Java serialization) or pass a *remote reference*.

## 2.3 Remote procedure call

An **RPC** (Birrell and Nelson, 1984) lets a program call a procedure in another address space with the syntax of a local call. The programmer writes an **interface definition** (IDL); a compiler generates a **client stub** and a **server stub**. The steps of one call:

1. The client calls the stub as if it were the procedure.
2. The client stub **marshals** the parameters into a message and asks the runtime to send it.
3. The network carries the request to the server machine, where the server runtime hands it to the server stub.
4. The server stub **unmarshals** the parameters and calls the real procedure.
5. The procedure returns; the server stub marshals the result and sends the reply.
6. The client stub unmarshals the reply and returns to the caller.

**Parameter passing.** Call-by-value is natural. Call-by-reference does not work across address spaces; it is replaced by copy-restore (copy in, copy back), or by remote references to objects.

**Binding.** The client needs the server's address; a naming or registry service (port mapper, Consul, Kubernetes DNS) resolves the service name at run time.

RPC *looks* local but is not. A local call cannot fail halfway, cannot lose its reply and takes microseconds; a remote call can time out with no knowledge of whether the server ran the procedure. Waldo and colleagues' 1994 note "A Note on Distributed Computing" argued that hiding these differences is a design error: interfaces should expose latency and partial failure.

### Call semantics

When the client's timer expires with no reply, three situations are indistinguishable: the request was lost, the server crashed (before or after executing), or the reply was lost. Retrying fixes the first and the third but may execute the procedure twice.

| Semantics | Client behaviour | Server behaviour | Executions |
|---|---|---|---|
| **Maybe** | Send once, no retry | None | 0 or 1 |
| **At-least-once** | Retransmit until a reply arrives | None | 1 or more (duplicates possible) |
| **At-most-once** | Retransmit | Detect duplicate request IDs; replay the saved reply | 0 or 1 |
| **Exactly-once** | Ideal; achievable only with application-level transactions and idempotence | | Exactly 1 |

An operation is **idempotent** if repeating it has the same effect as doing it once: "set balance to 900", "read file block 7", HTTP `PUT`. "Subtract 100" is not idempotent. At-least-once is safe for idempotent operations; others need a unique **request ID** and a server-side table of completed requests, the at-most-once design. The experiment retries a withdrawal whose first two replies are lost:

```python
class Account:
    def __init__(self):
        self.balance, self.seen = 1000, {}

    def withdraw(self, req_id, amount, dedup):
        if dedup and req_id in self.seen:
            return self.seen[req_id]
        self.balance -= amount
        self.seen[req_id] = self.balance
        return self.balance

def call(acct, req_id, amount, dedup, lost_replies):
    attempts = 0
    while True:
        attempts += 1
        result = acct.withdraw(req_id, amount, dedup)
        if attempts not in lost_replies:
            return result, attempts

for dedup in (False, True):
    acct = Account()
    result, attempts = call(acct, "req-1", 100, dedup, lost_replies={1, 2})
    print(f"dedup={dedup!s:5}: attempts={attempts}, balance={acct.balance}, reply={result}")
```
```output
dedup=False: attempts=3, balance=700, reply=700
dedup=True : attempts=3, balance=900, reply=900
```
Without duplicate suppression the customer is charged three times (balance 700, not 900). With a request ID the server executes once and replays the stored reply. Payment APIs (Stripe, eSewa-style gateways) expose exactly this as an *idempotency key* header. The server's table cannot grow forever, so entries expire after a window; a retry after the window is a new request, so clients bound their retry period.

**Timeouts and back-off.** Retry with exponential back-off and random jitter (wait 100 ms, 200 ms, 400 ms, each randomised) to avoid synchronised retry storms that crush a recovering server.

### A real RPC round trip

Python's standard library includes XML-RPC. The next program starts a server on a free local port in a thread, makes real calls over HTTP, calls the introspection method and provokes a protocol fault by passing the wrong number of arguments:

```python
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

def add(a, b):
    return a + b

def stats(values):
    return {"n": len(values), "mean": sum(values) / len(values)}

server = SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=False)
server.register_introspection_functions()
server.register_function(add)
server.register_function(stats)
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
proxy = ServerProxy(f"http://127.0.0.1:{port}")
print("add(2, 3) =", proxy.add(2, 3))
print("stats([4, 8, 9]) =", proxy.stats([4, 8, 9]))
print("methods:", sorted(m for m in proxy.system.listMethods() if not m.startswith("system.")))
try:
    proxy.add(1)
except Exception as e:
    print("bad call ->", type(e).__name__)
server.shutdown()
```
```output
add(2, 3) = 5
stats([4, 8, 9]) = {'n': 3, 'mean': 7.0}
methods: ['add', 'stats']
bad call -> Fault
```
The stub (`proxy.add`) is generated dynamically; the XML in the HTTP body is the marshalled request. The remote exception arrives as a `Fault` object, one of the rare cases where the caller learns that the server *did* receive the request.

## 2.4 Remote method invocation (RMI)

**RMI** extends RPC to objects: a client holds a **remote reference** to an object living in another JVM and invokes methods on it. Java RMI works as follows: the remote interface extends `java.rmi.Remote` and each method declares `throws RemoteException`, a deliberate reminder that the call can fail. The server creates the object, exports it (producing a **stub**) and binds the stub in the **RMI registry** under a name. A client looks the name up and receives the stub, whose method calls are marshalled to the server.

```text
public interface Greeter extends java.rmi.Remote {
    String greet(String name) throws java.rmi.RemoteException;
}
// server: Registry r = LocateRegistry.createRegistry(1099);
//         r.rebind("greeter", UnicastRemoteObject.exportObject(new GreeterImpl(), 0));
// client: Greeter g = (Greeter) LocateRegistry.getRegistry("host").lookup("greeter");
//         System.out.println(g.greet("Sita"));
```

Parameters of a *serializable* type are passed by value (a copy is made); parameters that are themselves remote objects are passed by reference (the stub is copied). Static typing of the interface, passing of objects including behaviour and distributed garbage collection (leases) make RMI richer than RPC. CORBA generalised the idea across languages with the ORB and IDL; modern systems prefer language-neutral services (gRPC, REST).

## 2.5 gRPC

**gRPC** is Google's open-source RPC framework. Services and messages are declared in a `.proto` file; the compiler generates client and server code in many languages. Messages use Protocol Buffers on the wire and the transport is **HTTP/2**, giving multiplexed streams over one TCP connection, header compression and flow control. gRPC supports four call types:

| Type | Pattern | Example |
|---|---|---|
| Unary | One request, one response | `GetUser(id)` |
| Server streaming | One request, a stream of responses | Stock-price feed |
| Client streaming | Stream of requests, one response | Upload file in chunks |
| Bidirectional streaming | Both sides stream independently | Chat, collaborative editing |

```text
syntax = "proto3";
service Wallet {
  rpc Transfer (TransferRequest) returns (TransferReply);
}
message TransferRequest { string idempotency_key = 1; string from = 2; string to = 3; int64 paise = 4; }
message TransferReply   { bool ok = 1; string txn_id = 2; }
```

gRPC carries a **deadline** with each call (an absolute time budget propagated to downstream calls), status codes (`OK`, `DEADLINE_EXCEEDED`, `UNAVAILABLE`, ...) and metadata for authentication and tracing. Note the idempotency key in the message: the application, not the framework, supplies at-most-once behaviour. Compared with REST/JSON, gRPC is faster, strongly typed and streaming, but harder to call from a browser and to debug by eye.

## 2.6 Message-oriented communication

RPC is **synchronous and coupled**: caller and callee must be up together and the caller waits. **Message-oriented middleware** (MOM) decouples them through a **queue** held by a broker. Sender and receiver need not be running at the same time (*temporal decoupling*) nor know each other (*spatial decoupling*).

- **Point-to-point queue:** each message is consumed by one of the competing consumers (work distribution; RabbitMQ queues, Amazon SQS).
- **Publish-subscribe:** each message goes to every subscriber of a topic (event notification; Kafka topics, MQTT in IoT).
- **Log-based brokers** (Kafka) store messages in an append-only partitioned log with offsets; consumers track their own position and can replay.

**Delivery guarantees.** *At-most-once* (fire and forget, may lose); *at-least-once* (the broker redelivers until the consumer **acknowledges**, so duplicates occur and consumers must be idempotent); *exactly-once* effects (idempotent consumers or transactional writes). A message that a consumer fetched but never acknowledged becomes visible again after a **visibility timeout**, and is delivered again, possibly after later messages:

```python
from collections import deque
queue = deque(["m1", "m2", "m3"])
crash_once = {"m2"}
order, processed = [], []
while queue:
    m = queue.popleft()
    order.append(m)
    if m in crash_once:
        crash_once.discard(m)
        queue.append(m)
        continue
    processed.append(m)
print("delivery order:", " ".join(order))
print("processed:", processed)
print(f"{len(order)} deliveries for {len(processed)} messages")
```
```output
delivery order: m1 m2 m3 m2
processed: ['m1', 'm3', 'm2']
4 deliveries for 3 messages
```
The consumer crashed on `m2` before acknowledging, so `m2` came back last: four deliveries for three messages, and the processing order changed. Practical consequences: do not rely on global ordering (Kafka orders within a partition only), make handlers idempotent, and send poisoned messages to a **dead-letter queue** after a retry limit.

## 2.7 Seeing communication: wires, handshakes, stubs and queues

Every message in this unit travels through hardware first. Plate 2.1 shows the machines at the three ends of the story: the box that forwards frames, the first web server that answered requests, and the cable that carries them. Figures 2.1 to 2.3 then show the protocols that run over that hardware.

```photogrid label="2.1" cols="3" ratio="1.1" caption="The hardware under every socket. (a) A small Ethernet switch with two cables plugged in: it learns which computer is on which port and forwards each frame only there, so many nodes can talk at once. (b) The NeXT computer that Tim Berners-Lee used at CERN as the first web server in 1990-91: it was a server process listening on a TCP socket, with a handwritten label asking that it not be switched off. (c) The RJ-45 plug of a twisted-pair cable: eight thin copper wires in four twisted pairs carry the bits between the network card and the switch."
@ photo id="bca101/switch" cap="Ethernet switch"
fit 1.1
focus 0.5 0.5
call 0.35 0.62 0.3 0.45 "ports"
@ photo id="bca203/firstserver" cap="First web server (CERN)"
fit 1.1
focus 0.75 0.5
call 0.82 0.35 0.45 0.12 "the server"
@ photo id="cs12/utp-cable" cap="RJ-45 plug, twisted pairs"
fit 1.1
focus 0.4 0.5
call 0.45 0.5 0.7 0.3 "eight wires"
```

```svgfig label="2.1" caption="The TCP socket calls and the three-way handshake. The server runs socket, bind, listen and accept and then waits. The client runs socket and connect, which sends SYN; the server answers SYN-ACK; the client sends ACK. After one round trip the connection is open, and data can flow in both directions. A round trip over a 3,000 km fibre link already costs about 30 ms before any data is sent."
f = Fig(580, 270)
f.box(40, 10, 150, 34, "Client", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(390, 10, 150, 34, "Server", fill=MINT, stroke=TEAL, size=12, bold=True)
f.line(115, 44, 115, 262, color=NAVY); f.line(465, 44, 465, 262, color=TEAL)
f.text(465, 58, "socket, bind, listen, accept", size=9.5, color=TEAL, bold=True, anchor="middle")
f.text(115, 74, "socket, connect", size=9.5, color=NAVY, bold=True)
f.arrow([(115, 100), (465, 130)], color=SLATE, label="SYN (seq = x)", lpos=(290, 104))
f.arrow([(465, 150), (115, 180)], color=SLATE, label="SYN-ACK (seq = y, ack = x + 1)", lpos=(290, 154))
f.arrow([(115, 196), (465, 222)], color=SLATE, label="ACK (ack = y + 1)", lpos=(290, 198))
f.text(290, 255, "open after one round trip, then send and recv", size=10, color=RED, bold=True)
```

```svgfig label="2.2" caption="The path of one remote procedure call. The client program calls an ordinary-looking function; the client stub marshals the arguments into bytes (a 3-field record is 11 bytes in fixed binary, 11 bytes in Protocol Buffers and 35 bytes as JSON text); the network carries the request; the server stub unmarshals, calls the real procedure and sends the result back by the same route. The caller waits for the whole round trip."
f = Fig(580, 210)
f.box(10, 20, 100, 60, "Client\nprogram", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(130, 20, 100, 60, "Client stub\nmarshal", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(350, 20, 100, 60, "Server stub\nunmarshal", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(470, 20, 100, 60, "Server\nprocedure", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(110, 40), (130, 40)], color=SLATE); f.arrow([(230, 40), (350, 40)], color=SLATE, label="request bytes", lpos=(290, 28))
f.arrow([(450, 40), (470, 40)], color=SLATE)
f.arrow([(470, 62), (450, 62)], color=AMBER); f.arrow([(350, 62), (230, 62)], color=AMBER, label="reply bytes", lpos=(290, 76))
f.arrow([(130, 62), (110, 62)], color=AMBER)
f.box(10, 120, 560, 70, "", fill=SAND, stroke=AMBER)
f.text(290, 142, "Failure cases the caller cannot tell apart: request lost, server crashed,", size=10.5, color=NAVY, bold=True)
f.text(290, 160, "reply lost, or just slow. Semantics: at-most-once (no retry) or at-least-once", size=10.5, color=NAVY, bold=True)
f.text(290, 178, "(retry, so the procedure must be idempotent).", size=10.5, color=NAVY, bold=True)
```

```svgfig label="2.3" caption="Message-oriented middleware. In a point-to-point queue (top), each message is taken by exactly one of the competing consumers, which shares the work. In publish-subscribe (bottom), each message is copied to every subscriber of the topic. Producers and consumers need not be running at the same time because the broker stores the messages until they are acknowledged."
f = Fig(580, 240)
f.box(10, 28, 90, 44, "Producer", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(150, 28, 140, 44, "Queue: m1 m2 m3 m4", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(350, 6, 100, 36, "Consumer A", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(350, 58, 100, 36, "Consumer B", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(100, 50), (150, 50)], color=SLATE); f.arrow([(290, 40), (350, 24)], color=SLATE); f.arrow([(290, 60), (350, 76)], color=SLATE)
f.text(462, 50, "to one consumer", size=9.5, color=TEAL, bold=True, anchor="start")
f.line(10, 116, 570, 116, color=SLATE, dash=True)
f.box(10, 150, 90, 44, "Publisher", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(150, 150, 140, 44, "Topic: result-day", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(350, 126, 100, 34, "Subscriber 1", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(350, 168, 100, 34, "Subscriber 2", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(350, 210, 100, 28, "Subscriber 3", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(100, 172), (150, 172)], color=SLATE)
for y in (143, 185, 224):
    f.arrow([(290, 172), (350, y)], color=SLATE)
f.text(462, 185, "to every subscriber", size=9.5, color=TEAL, bold=True, anchor="start")
```

### 2.7.1 Eight advantages of message queues and RPC frameworks

1. **Decoupling in time.** A producer can send a message even when the consumer is switched off. The broker stores the message until the consumer returns. A result-day SMS system uses this so that a slow gateway does not stop the examination system.
2. **Smoothing sudden load.** Thousands of requests may arrive in one second, for example when a payment offer is announced. The queue absorbs the burst and the consumers work through it at their own speed. Users wait a little longer but nothing is lost.
3. **Load sharing.** Several competing consumers can read from one queue, and the broker gives each message to only one of them. Adding a consumer increases throughput without changing the producer. This is the simplest way to scale a worker pool.
4. **Fault isolation.** If a consumer crashes while it is working, the message is not acknowledged and is delivered again to another consumer. One failing component does not bring down the sender. The cost is possible duplicates, so consumers should be idempotent.
5. **Broadcast to many parties.** In publish-subscribe, one event reaches many subscribers. A bank can publish one 'payment received' event that is used by the SMS service, the statement service and the fraud checker. New subscribers can be added without touching the publisher.
6. **Compact and fast encoding.** gRPC with Protocol Buffers sends the same record in 11 bytes instead of the 35 bytes of JSON text. Smaller messages mean less bandwidth and less parsing time, which matters on mobile data in the hills. The schema also keeps old and new versions compatible.
7. **Strongly typed contracts.** An interface definition file generates client and server code in many languages. A wrong field name is found when the code is compiled and not on the live system. This keeps teams that work on different services in agreement.
8. **Streaming and multiplexing.** HTTP/2 lets gRPC send many calls at once over one connection and stream data in both directions. This avoids opening a new TCP handshake for every call, saving one round trip each time. Live location, chat and sensor feeds use this style.

## Chapter summary

- Sockets expose TCP streams (reliable, ordered, need framing) and UDP datagrams (lossy, message-preserving); TCP's reliability does not replace end-to-end application acknowledgements.
- Marshalling fixes byte order and layout: the 11-byte fixed record and the 35-byte JSON for the same data; protobuf varints encode 150 as `96 01` and 300 as `ac 02`.
- RPC hides communication behind stubs, but the caller must still handle timeouts; at-least-once plus a request ID gives at-most-once. The retry experiment charged 300 instead of 100 without dedup.
- RMI passes remote references; gRPC uses protobuf over HTTP/2 with unary and streaming calls and deadlines.
- Message queues decouple sender and receiver in time and space; at-least-once delivery means duplicates and reordering, so handlers must be idempotent.

## Practice

1. Contrast TCP and UDP sockets and give one application of each.
2. Why do TCP-based protocols need message framing? Name two framing methods.
3. Compute the protobuf encoding of the varint 300 and verify it by decoding.
4. Describe the six steps of an RPC call using the words *stub* and *marshalling*.
5. Explain at-least-once and at-most-once semantics. Which one needs server state and why?
6. A client retries a non-idempotent `append(x)` three times because replies are lost. How many copies of `x` can the server hold with and without request IDs?
7. Why is "set the balance to 900" safe to retry while "subtract 100" is not?
8. Compare RPC and RMI. How are a serializable object and a remote object passed as parameters?
9. List the four gRPC call types and one use for each.
10. Differentiate point-to-point queues and publish-subscribe. What happens to a message whose consumer crashes before acknowledging it?

::: note Answers and worked solutions
**1.** TCP: reliable ordered byte stream with connection (HTTP, SSH). UDP: connectionless datagrams, low overhead (DNS, live video).
**2.** A TCP stream has no message boundaries. Use a length prefix (4-byte length, then payload) or a delimiter (CRLF line endings in HTTP headers).
**3.** 300 = 100101100₂. Low seven bits 0101100 = 0x2C; set the continuation bit to get 0xAC. Remaining bits 10₂ = 0x02. Encoding: `ac 02`. Decode: (0xAC & 0x7F) + (0x02 << 7) = 44 + 256 = 300. Verified.
**4.** The client calls the client stub; the stub marshals the arguments and sends them; the server stub unmarshals and calls the procedure; the result is marshalled and returned; the client stub unmarshals it for the caller.
**5.** At-least-once retries until a reply arrives, so the procedure may run several times. At-most-once needs the server to keep a table of request IDs and saved replies, so a repeated request is answered from the table instead of executing again.
**6.** If three replies are lost the fourth attempt succeeds, so the server executes the append 4 times and holds 4 copies without request IDs; exactly 1 copy with request IDs.
**7.** Repeating "set to 900" leaves 900; repeating "subtract 100" subtracts each time.
**8.** RPC calls procedures; RMI calls methods on remote objects and passes remote references. A serializable object is copied by value; a remote object is passed as its stub (by reference).
**9.** Unary (get a user), server streaming (price feed), client streaming (chunked upload), bidirectional (chat).
**10.** A point-to-point message is delivered to one consumer; publish-subscribe delivers to every subscriber. An unacknowledged message becomes visible again after the visibility timeout and is redelivered, which can reorder messages.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare TCP and UDP sockets and say when each is suitable.**

*Introduction.* A socket is an endpoint identified by an IP address and a port; the transport protocol decides how it behaves (section 2.1, Figure 2.1).

1. **Connection.** TCP is connection-oriented: a three-way handshake (SYN, SYN-ACK, ACK) opens a connection. UDP is connectionless and sends each datagram on its own.
2. **Reliability.** TCP numbers every byte, acknowledges it and retransmits losses, so data arrive complete and in order. UDP may lose, reorder or duplicate datagrams and does nothing about it.
3. **Boundaries.** TCP is a byte stream, so the application must mark where each message ends. UDP keeps one datagram as one message.
4. **Overhead and delay.** TCP keeps state and uses congestion control, which costs time; its throughput is also limited by window / round-trip time. With a 64 KB window and a 30 ms round trip the limit is 17.5 Mbit/s, and to fill a 100 Mbit/s link at that delay a window of 366 KB is needed. UDP has no such limit but no safety either.
5. **Uses.** TCP suits web pages, e-mail, databases and RPC, where every byte matters. UDP suits DNS queries, voice, video and games, where a late packet is worse than a lost one.

| Feature | TCP | UDP |
|---|---|---|
| Connection | yes, handshake | no |
| Delivery | reliable, ordered | best effort |
| Message boundary | none | kept |
| Overhead | higher | low |
| Example | HTTP, SSH | DNS, video call |

*Conclusion.* Choose TCP when correctness matters more than delay, and UDP when timeliness matters and the application can tolerate or repair loss.

**Q2 (5 marks). Explain how a remote procedure call works and discuss its call semantics.**

*Introduction.* RPC lets a program call a procedure on another machine as if it were local, hiding sockets and message formats (section 2.3, Figure 2.2).

1. **Client stub.** The client calls the stub, which marshals the arguments into bytes. A record of three fields takes 11 bytes in fixed binary, 11 in Protocol Buffers and 35 as JSON.
2. **Transport.** The request message is sent over the network with a request number so that the reply can be matched.
3. **Server stub.** It unmarshals the arguments, calls the real procedure and marshals the result.
4. **Reply.** The result returns by the same route and the client stub gives it to the caller as an ordinary return value.
5. **Semantics.** *Maybe*: no retry, no guarantee. *At-least-once*: the client retries until it gets a reply, so a procedure may run more than once and must be idempotent (for example 'set balance to 500', not 'add 500'). *At-most-once*: the server remembers request numbers and does not repeat a request, but a crash may lose the reply. Exactly-once cannot be guaranteed in general.

*Conclusion.* RPC makes distribution look simple, but delay and partial failure remain, so the caller must always handle timeouts.

**Q3 (10 marks). Compare sockets, RPC, RMI, gRPC and message queues as ways for distributed programs to communicate.**

*Introduction.* Distributed programs communicate by messages. The mechanisms differ in how much they hide and in how closely they bind the sender and the receiver (Figures 2.1 to 2.3).

*Sockets.* They give the most control: the programmer chooses TCP or UDP, frames the messages and handles errors. They are fast and universal but need the most code.

*RPC.* The stub hides marshalling and sockets behind a procedure call. Interfaces are described in an IDL file. The caller blocks until the reply arrives, so caller and callee must be running together.

*RMI.* Java's RMI extends the idea to objects: a remote object is called through a proxy, and arguments can be objects passed by value or by remote reference. It is convenient inside Java but ties the system to one language.

*gRPC.* It combines an IDL (Protocol Buffers), generated stubs in many languages and HTTP/2. It supports four styles: unary, server streaming, client streaming and bidirectional streaming. Binary encoding gives 11 bytes against 35 bytes of JSON for the same record.

*Message queues.* Brokers such as RabbitMQ and Kafka decouple sender and receiver in time. Point-to-point queues share work, publish-subscribe broadcasts events, and log-based brokers keep messages for replay. Delivery can be at-most-once, at-least-once (duplicates possible) or, with extra work, effectively once.

| Mechanism | Level | Coupling | Blocking | Typical use |
|---|---|---|---|---|
| Socket | bytes | tight | optional | custom protocols, games |
| RPC | procedure | tight in time | yes | internal services |
| RMI | object | tight, one language | yes | Java enterprise |
| gRPC | procedure, streams | tight in time | yes or stream | microservices, mobile |
| Message queue | message | loose | no | events, background jobs |

*Choosing.* Use RPC or gRPC for a quick answer needed now, a queue when the work can be done later or by many consumers, and raw sockets only when a standard mechanism does not fit.

*Conclusion.* The right choice trades simplicity, speed, language freedom and tolerance of failure. A real system, such as a payment platform, uses several: gRPC between services and queues for notifications and statements.
