---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 7
title: JavaBeans and the Enterprise Java Landscape
hours: 5
area: BCA 303 · Advanced Java Programming · Unit 7
---

Every graphical builder, every JSP and every framework needs the same thing from your data classes: a predictable way to find out what properties an object has, to read and write them, and to be told when they change. The **JavaBeans** conventions (1996) provide exactly that, and they are the reason `<jsp:getProperty>`, `${student.name}`, GUI form designers and persistence libraries work with *your* class without knowing it in advance. This closing unit defines a bean precisely, builds one with bound and constrained properties (run for real), and maps the enterprise technologies that sit on top of the ideas in this book.

::: key What this unit gives you
- The JavaBeans conventions; property kinds (simple, indexed, bound, constrained); events and introspection.
- Beans in JSP; POJO versus bean versus EJB.
- A map of Jakarta EE and the frameworks you will meet next.
:::

## 7.1 What is a JavaBean?

A **JavaBean** is a reusable Java class that follows these conventions:

1. It has a **public no-argument constructor**.
2. Its state is exposed as **properties** through **getter and setter methods** named `getXxx()` / `setXxx(value)` (for `boolean`, `isXxx()` may be used), while the fields themselves are **private**.
3. It is **serializable** (`implements java.io.Serializable`) so that its state can be saved and restored.
4. Optionally it supports **events**: bound properties notify `PropertyChangeListener`s and constrained properties ask `VetoableChangeListener`s for permission.

The property name comes from the method name with the first letter lower-cased: `getMarks`/`setMarks` define the property `marks`. A property with only a getter is **read-only** (here `passed`, computed from the marks); only a setter, **write-only**.

### Kinds of properties

| Kind | Meaning |
|---|---|
| Simple | a single value with getter/setter |
| Indexed | an array of values: `getScore(int i)`, `setScore(int i, int v)`, plus whole-array forms |
| Bound | changes are announced to `PropertyChangeListener`s through `PropertyChangeSupport.firePropertyChange(name, old, new)` |
| Constrained | listeners (`VetoableChangeListener`) may **veto** a change by throwing `PropertyVetoException`; the setter must declare it |

### Introspection

**Introspection** is how a tool discovers a bean's properties, methods and events *without being told*. `java.beans.Introspector.getBeanInfo(Class)` builds a `BeanInfo` by examining the class through reflection and the naming conventions (a `BeanInfo` class can override the result). JSP's `jsp:useBean` and EL, form builders and frameworks all rely on it.

```java
import java.beans.*;
import java.io.*;
public class BeanDemo {
    public static class StudentBean implements Serializable {
        private static final long serialVersionUID = 1L;
        private String name = "unknown";
        private int marks;
        private final PropertyChangeSupport changes = new PropertyChangeSupport(this);
        private final VetoableChangeSupport vetoes = new VetoableChangeSupport(this);
        public StudentBean() { }
        public String getName() { return name; }
        public void setName(String n) { String old = name; name = n; changes.firePropertyChange("name", old, n); }
        public int getMarks() { return marks; }
        public void setMarks(int m) throws PropertyVetoException {
            vetoes.fireVetoableChange("marks", marks, m);
            int old = marks; marks = m; changes.firePropertyChange("marks", old, m);
        }
        public boolean isPassed() { return marks >= 40; }
        public void addPropertyChangeListener(PropertyChangeListener l) { changes.addPropertyChangeListener(l); }
        public void removePropertyChangeListener(PropertyChangeListener l) { changes.removePropertyChangeListener(l); }
        public void addVetoableChangeListener(VetoableChangeListener l) { vetoes.addVetoableChangeListener(l); }
        public void removeVetoableChangeListener(VetoableChangeListener l) { vetoes.removeVetoableChangeListener(l); }
    }
    public static void main(String[] args) throws Exception {
        StudentBean s = new StudentBean();
        s.addPropertyChangeListener(e -> System.out.println("bound: " + e.getPropertyName() + " " + e.getOldValue() + " -> " + e.getNewValue()));
        s.addVetoableChangeListener(e -> {
            int v = (Integer) e.getNewValue();
            if (v < 0 || v > 100) throw new PropertyVetoException("marks must be 0..100 but was " + v, e);
        });
        s.setName("Sita");
        s.setMarks(72);
        try { s.setMarks(150); } catch (PropertyVetoException ex) { System.out.println("vetoed: " + ex.getMessage()); }
        System.out.println("marks is still " + s.getMarks() + ", passed = " + s.isPassed());
        for (PropertyDescriptor pd : Introspector.getBeanInfo(StudentBean.class, Object.class).getPropertyDescriptors())
            System.out.println("property " + pd.getName() + " : " + pd.getPropertyType().getSimpleName() + (pd.getReadMethod() != null ? " readable" : "") + (pd.getWriteMethod() != null ? " writable" : ""));
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(bos)) { out.writeObject(s); }
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bos.toByteArray()))) {
            StudentBean copy = (StudentBean) in.readObject();
            System.out.println("restored: " + copy.getName() + " " + copy.getMarks());
        }
    }
}
```
```output
bound: name unknown -> Sita
bound: marks 0 -> 72
vetoed: marks must be 0..100 but was 150
marks is still 72, passed = true
property marks : int readable writable
property name : String readable writable
property passed : boolean readable
restored: Sita 72
```
The two changes that succeeded were announced to the bound-property listener; the out-of-range change was vetoed *before* the field was altered, so the marks remain 72. The introspector found three properties from the method names alone: `marks` and `name` read-write, `passed` read-only. The bean was saved and restored with ordinary serialization.

::: caution Serialization and listeners
`PropertyChangeSupport` and `VetoableChangeSupport` are themselves serializable and, when a bean is written, they write only those listeners that are serializable themselves; the lambda listeners in the program above are not, so they were silently left out (which is why the restored copy has no listeners). A listener that *is* serializable would be saved with the bean. Keep this in mind: a restored bean is a bean without its listeners, and they must be registered again.
:::

## 7.2 Beans in JSP and in frameworks

JSP can create and read a bean without Java code:

```text
<jsp:useBean id="student" class="edu.nebians.StudentBean" scope="session"/>
<jsp:setProperty name="student" property="name" param="name"/>
<jsp:getProperty name="student" property="name"/>
${student.passed}
```

`useBean` finds the bean in the given scope or creates it with the no-argument constructor; `setProperty` copies a request parameter into a property, converting types; `getProperty` and EL call the getters. That is the same convention exploited by form-binding in Spring MVC and Jakarta Faces, by serializers such as Jackson and by ORM tools.

## 7.3 POJO, bean, DTO and EJB

| Term | Meaning |
|---|---|
| **POJO** | "plain old Java object": any ordinary class, no framework dependency |
| **JavaBean** | a POJO following the conventions above (no-arg constructor, getters/setters, serializable) |
| **DTO** (data transfer object) | a bean that only carries data between layers (JDBC → servlet → JSP) |
| **Entity** | a bean mapped to a database table by JPA/Hibernate (`@Entity`) |
| **EJB** (Enterprise JavaBean) | a *server-managed* component with container services; **session beans** (stateless, stateful, singleton) hold business logic, **message-driven beans** consume messages; not the same thing as a JavaBean |
| **Spring bean** | any object whose life cycle and dependencies are managed by the Spring container |

## 7.4 The enterprise Java map

| Layer | Technology | Purpose |
|---|---|---|
| Presentation | Servlets, JSP, **Jakarta Faces (JSF)**, Spring MVC, Thymeleaf | web pages and controllers |
| Web services | JAX-RS (REST), JAX-WS (SOAP), Spring Boot REST | APIs |
| Business logic | EJB, CDI, Spring services | transactions, security, injection |
| Persistence | JDBC, **JPA** (Hibernate, EclipseLink), Spring Data | object-relational mapping |
| Messaging | JMS, Kafka clients | asynchronous communication |
| Naming | JNDI | look up pools, beans and resources by name |
| Platform | Tomcat (web only), Jetty, WildFly, Payara, Spring Boot embedded server | run it all |

How the units of this book fit: sockets and HTTP (Unit 4) are what the container hides; JDBC (Unit 3) is what JPA wraps; servlets and JSP (Unit 6) are what JSF and Spring MVC are built on; RMI (Unit 5) is the ancestor of EJB remote calls and of REST/gRPC clients; beans (this unit) are the data every layer passes around; threads (Unit 1) are how the container serves many requests; Swing (Unit 2) is the desktop counterpart of the web presentation layer.

### Where to go next

Build a small student-management application: a SQLite or MySQL table and DAO (Unit 3), a controller servlet and JSP views (Unit 6), a bean for the student (this unit), a Swing admin client that calls a REST endpoint (Units 2 and 4), packaged as a WAR for Tomcat. Then learn **Spring Boot**, which wires these pieces together with far less configuration.

## 7.5 Seeing the ideas: beans, events, serialization and the enterprise map

JavaBeans are a set of naming rules, so the best way to understand them is to ask a tool what it sees in a class and to watch the events fly. Plate 7.1 gives four everyday pictures: coffee beans for the name, toy bricks for reusable components, a dashboard for bound properties and a boom barrier for a veto. Plate 7.2 shows a shelf of sealed tins for serialization and a real GUI builder that reads a bean's properties. Figures 7.1 to 7.8 then use numbers from one real run of Java 17: the Introspector on a StudentBean, bound and constrained events, serialization and what it loses, the same bean inside a JSP on Apache Tomcat 9, and the time that each layer of a server costs.

```photogrid label="7.1" cols="4" ratio="1.0" caption="Four pictures for the ideas of JavaBeans. (a) Roasted coffee beans (CC0): Java is also the name of coffee, and a bean is a small, reusable unit of Java. (b) A heap of toy building bricks (CC BY-SA 4.0): every brick has the same studs, so any brick fits any other, as a bean with the standard conventions fits any tool. (c) A car instrument cluster (CC BY 2.0): the needles move as soon as the engine changes its speed, like a bound property that announces each change to its listeners. (d) A parking boom barrier (CC BY 4.0): the barrier asks whether the car may pass, and when the answer is no it stays closed, like a constrained property and its veto."
@ photo id="bca303/beans" cap="Coffee beans: the name"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/lego" cap="Bricks: reusable parts"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/dash" cap="Dashboard: bound properties"
fit 1.0
focus 0.5 0.55
call 0.7 0.55 0.9 0.2 "speed"
@ photo id="bca303/barrier" cap="Boom barrier: veto"
fit 1.0
focus 0.5 0.55
```

```photogrid label="7.2" cols="2" ratio="1.0" caption="Serialization and tools. (a) Sealed tins on a shop shelf (CC BY-SA 4.0): the food is packed so that it keeps its state for a long time and can be opened later, which is what serialization does for an object; but anything that is not packed in the tin, like a loose lid, is lost. (b) The GUI builder of the NetBeans development environment (CC BY-SA 3.0): the properties panel at the right edge lists the properties of the selected component, found by introspection from the getters and setters of the bean."
@ photo id="bca303/tins" cap="Sealed tins: serialization"
fit 1.0
focus 0.5 0.4
@ photo id="bca303/nbgui" cap="GUI builder: introspection at work"
fit 1.0
focus 0.85 0.3
```

```svgfig label="7.1" caption="A bean seen by the Introspector, from a real run on the class StudentBean. The tool found five properties without being told: class (read-only, inherited from Object), marks (int, getMarks and setMarks, bound and constrained), name (String, bound), passed (boolean, read through isPassed, no setter, so read-only) and scores (an indexed int array with getScores, getScores(int) and setScores). It also found one event set, propertyChange, because the class has addPropertyChangeListener and removePropertyChangeListener, and 22 method descriptors in all. The fields themselves stay private."
f = Fig(580, 262)
f.box(10, 8, 150, 244, "", fill=SOFT, stroke="#cbd5e1")
f.text(85, 24, "class StudentBean", size=10.5, color=NAVY, bold=True)
for i, t in enumerate(["private String name", "private int marks", "private int[] scores", "public StudentBean()", "getName / setName", "getMarks / setMarks", "isPassed", "getScores(i) / setScores", "add/removePropertyChange-", "Listener"]):
    f.text(18, 44 + i * 19, t, size=8.5, color=RED if i < 3 else (TEAL if i == 3 else SLATE), anchor="start", bold=(i == 3))
f.arrow([(160, 130), (186, 130)], color=AMBER)
f.text(85, 240, "found by the Introspector", size=9, color=AMBER, bold=True)
hd = [("property", 190, 70), ("type", 262, 50), ("read", 314, 64), ("write", 380, 70), ("kind", 452, 118)]
for t, x, w in hd:
    f.box(x, 8, w, 22, t, fill=NAVY, stroke=NAVY, color="#ffffff", size=9.5, bold=True, r=3)
rows = [("class", "Class", "getClass", "-", "read-only"), ("marks", "int", "getMarks", "setMarks", "bound, constrained"), ("name", "String", "getName", "setName", "bound"), ("passed", "boolean", "isPassed", "-", "read-only"), ("scores", "int[]", "getScores", "setScores", "indexed, bound")]
for i, r in enumerate(rows):
    y = 34 + i * 30
    for (t, x, w), v in zip(hd, r):
        fl = SAND if v in ("-", "read-only") else "#ffffff"
        f.box(x, y, w, 26, v, fill=fl, stroke="#cbd5e1", color=SLATE, size=8.5, bold=(t == "property"), r=3)
f.box(190, 188, 380, 66, "event set found: propertyChange\n22 method descriptors in all\nname = method name without get/set,\nfirst letter in lower case", fill=BLUE, stroke=NAVY, size=9, bold=True)
```

```svgfig label="7.2" caption="The cost of introspection and reflection, measured. Left: the first call of Introspector.getBeanInfo for StudentBean took 18.85 ms, because the class had to be examined, while the second call took 0.011 ms from the cache, a ratio of about 1,700 (computed). Right: setting the name property 2,000,000 times took 49.4 ns per call directly (this setter also fires a property-change event to one listener) and 68.2 ns through the Method object found by introspection, a factor of 1.38, so reflection is cheap enough for frameworks once the lookup is cached."
f = Fig(580, 214)
first, second = 18.85, 0.011
ratio = first / second
assert 1700 < ratio < 1730
d, r = 49.4, 68.2
assert 1.37 < r / d < 1.39
f.text(145, 14, "getBeanInfo(StudentBean.class)", size=11, color=NAVY, bold=True)
f.box(10, 30, 270, 30, "first call 18.85 ms (examines the class)", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(10, 68, 3, 30, "", fill=MINT, stroke=TEAL, r=1)
f.text(22, 83, "second call 0.011 ms (cached)", size=9.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(145, 122, "ratio = %s" % format(int(round(ratio, -2)), ","), size=11, color=NAVY, bold=True)
f.text(145, 142, "cache the BeanInfo or the Method: do not look up on every call", size=9, color=SLATE, bold=True)
f.text(435, 14, "setName called 2,000,000 times", size=11, color=NAVY, bold=True)
sc = 250 / 68.2
f.box(300, 30, d * sc, 30, "direct setter 49.4 ns", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(300, 68, r * sc, 30, "Method.invoke 68.2 ns", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.text(435, 122, "reflective / direct = %.2f" % (r / d), size=11, color=NAVY, bold=True)
f.box(10, 160, 560, 42, "JSP, EL, form builders and frameworks all call getters and setters this way,\nso a class that follows the naming convention works in all of them", fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9)
```

```svgfig label="7.3" caption="Bound properties announce changes, but only real changes. In the run, five setter calls were made on a bean with one PropertyChangeListener: setName(Sita), setName(Sita) again, setMarks(72), setMarks(72) again, setScores(1, 9). The listener received exactly three events: name unknown to Sita, marks 0 to 72 and the indexed event scores 0 to 9. PropertyChangeSupport suppresses an event when the old and new values are equal, so a repeated assignment is silent; the events carry the property name, the old value and the new value."
f = Fig(580, 222)
calls = [("setName\n(Sita)", "name: unknown -> Sita", True), ("setName\n(Sita)", "no event: same value", False), ("setMarks\n(72)", "marks: 0 -> 72", True), ("setMarks\n(72)", "no event: same value", False), ("setScores\n(1, 9)", "scores: 0 -> 9", True)]
events = sum(1 for c in calls if c[2])
assert events == 3
f.text(290, 14, "calls on one bean with one PropertyChangeListener", size=11, color=NAVY, bold=True)
for i, (a, b, ev) in enumerate(calls):
    x = 10 + i * 114
    f.box(x, 30, 104, 40, a, fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    f.arrow([(x + 52, 70), (x + 52, 96)], color=TEAL if ev else "#94a3b8", dash=not ev)
    f.box(x, 96, 104, 50, b.replace(": ", ":\n"), fill=MINT if ev else SOFT, stroke=TEAL if ev else "#94a3b8", color=TEAL if ev else SLATE, size=9, bold=True)
f.box(10, 164, 270, 46, "5 setter calls, %d events delivered\n(2 repeated values fired nothing)" % events, fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(300, 164, 270, 46, "event = property name + old value + new value\nindexed property: also the index", fill=MINT, stroke=TEAL, size=9, bold=True)
```

```svgfig label="7.4" caption="A constrained property asks permission first. The setter setMarks calls fireVetoableChange before it assigns anything, and a listener may throw PropertyVetoException. In the run the rule was marks between 0 and 100: setMarks(150) was vetoed with the message marks must be 0..100, got 150 and the marks stayed 72, so passed stayed true; setMarks(-5) was vetoed too. A valid change passes the vetoers, is assigned, and only then is announced to the bound listeners. A veto is how a bean enforces a rule without the caller knowing the rule."
f = Fig(580, 238)
f.text(290, 14, "order of events inside setMarks(int m)", size=11, color=NAVY, bold=True)
st = [("1 fireVetoableChange\n(marks, old, m)", SAND, AMBER), ("2 vetoers may throw\nPropertyVetoException", ROSE, RED), ("3 marks = m", MINT, TEAL), ("4 firePropertyChange\n(marks, old, m)", BLUE, NAVY)]
for i, (t, fl, c) in enumerate(st):
    x = 10 + i * 144
    f.box(x, 30, 134, 44, t, fill=fl, stroke=c, size=9, bold=True)
    if i < 3:
        f.arrow([(x + 134, 52), (x + 144, 52)], color=SLATE, sw=1.2)
f.box(10, 98, 270, 56, "setMarks(150): vetoed\nmessage: marks must be 0..100, got 150\nmarks stays 72, passed stays true", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(300, 98, 270, 56, "setMarks(-5): vetoed\nmessage: marks must be 0..100, got -5\nno bound event is sent", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(10, 170, 270, 56, "setMarks(72): allowed\nassigned, then one event: marks 0 -> 72", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(300, 170, 270, 56, "the setter must declare\nthrows PropertyVetoException,\nso the caller is forced to handle it", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

```svgfig label="7.5" caption="What serialization keeps and what it loses, from a real run. The bean with name Sita, marks 72 and scores[1] = 9 was 540 bytes serialized, and 576 bytes (36 more) after one serializable listener was added. After restoring, the data were intact: name Sita, marks 72, scores[1] = 9, and the serializable listener came back (bound listeners 1). But the veto rule, registered as a lambda in the constructor, was not serializable and was dropped (veto listeners 0), so the restored bean accepted setMarks(150) and held 150. State survives; behaviour wired by listeners may not."
f = Fig(580, 244)
f.box(10, 12, 150, 88, "original bean\nname Sita\nmarks 72, scores[1] = 9\nbound listeners: 1\nveto listeners: 1", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.arrow([(160, 56), (215, 56)], color=AMBER, label="write", lpos=(188, 48), lsize=9)
f.box(215, 20, 150, 72, "540 bytes\n(576 with one\nserializable listener)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.arrow([(365, 56), (420, 56)], color=AMBER, label="read", lpos=(392, 48), lsize=9)
f.box(420, 12, 150, 88, "restored bean\nname Sita\nmarks 72, scores[1] = 9\nbound listeners: 1\nveto listeners: 0", fill=MINT, stroke=TEAL, size=9, bold=True)
assert 576 - 540 == 36
f.box(10, 118, 270, 54, "kept: all fields, and listeners that\nimplement Serializable", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(300, 118, 270, 54, "lost: lambdas and other listeners that\nare not Serializable", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(10, 186, 560, 46, "restored.setMarks(150) was accepted: marks = 150. Register validation again after readObject,\nor write the rule inside the setter, not in a listener.", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

```svgfig label="7.6" caption="A bean inside a JSP, run on a real Tomcat. The page used jsp:useBean in session scope and jsp:setProperty with property star, which copies request parameters into the bean by name. The request name=Sita and marks=72 gave name=Sita marks=72 passed=true; a later request of the same session with no parameters still showed Sita and 72; a visitor without the cookie got a new bean (unknown, 0, false). With request scope, the bean lived for one request only (Ram, then unknown). A vetoed value (marks=150) and a non-number (marks=abc) both gave status 500, and the session bean kept 72."
f = Fig(580, 262)
for t, x, w in [("request to the JSP", 10, 250), ("result", 264, 306)]:
    f.box(x, 6, w, 22, t, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=3)
rows = [("session: ?name=Sita&marks=72", "name=Sita marks=72 passed=true", TEAL, MINT), ("session again, no parameters", "name=Sita marks=72 passed=true", TEAL, MINT), ("a visitor without the cookie", "name=unknown marks=0 passed=false", AMBER, SAND), ("request scope: ?name=Ram", "name=Ram", NAVY, BLUE), ("request scope again, no params", "name=unknown", AMBER, SAND), ("session: ?marks=150 (vetoed)", "status 500", RED, ROSE), ("session: ?marks=abc", "status 500", RED, ROSE), ("session afterwards, no params", "name=Sita marks=72 passed=true", TEAL, MINT)]
for i, (a, b, c, fl) in enumerate(rows):
    y = 34 + i * 27
    f.box(10, y, 250, 23, a, fill="#ffffff", stroke="#cbd5e1", color=SLATE, size=9, r=3)
    f.box(264, y, 306, 23, b, fill=fl, stroke=c, size=9, bold=True, r=3)
f.text(290, 258, "jsp:setProperty property=* matches parameter names to setters and converts the types", size=9, color=SLATE, bold=True)
```

```svgfig label="7.7" caption="The enterprise Java map. At the centre sits the plain object (POJO). Adding the bean conventions makes a JavaBean, and the same class used only to carry data between layers is a data transfer object (DTO). An entity is a bean mapped to a database table by JPA, and an Enterprise JavaBean is a component managed by an application server. Around them are the Jakarta EE technologies of this book: servlets and JSP (Unit 6) for web pages, JDBC and JPA for data (Unit 3), JMS for messages, JNDI for naming, RMI and CORBA as the old remote calls (Unit 5) with REST and gRPC today, and threads (Unit 1) inside the container."
f = Fig(580, 262)
f.text(145, 14, "kinds of Java data classes", size=11, color=NAVY, bold=True)
ch = [("POJO", "any plain class", BLUE, NAVY), ("JavaBean", "POJO + conventions\n(no-arg, getters, Serializable)", MINT, TEAL), ("DTO", "a bean that only carries\ndata between layers", SAND, AMBER), ("Entity (JPA)", "a bean mapped to\na database table", ROSE, RED), ("EJB", "component managed by\nan application server", BLUE, NAVY)]
for i, (a, b, fl, st) in enumerate(ch):
    y = 28 + i * 44
    f.box(10, y, 90, 36, a, fill=fl, stroke=st, size=9.5, bold=True)
    f.box(104, y, 176, 36, b, fill="#ffffff", stroke=st, size=8.5, color=SLATE)
f.text(435, 14, "Jakarta EE technologies in this book", size=11, color=NAVY, bold=True)
mp = [("Servlet, JSP, JSF", "web pages (Unit 6)"), ("JDBC, JPA", "database (Unit 3)"), ("JAX-RS (REST)", "services, modern remote calls"), ("RMI, CORBA", "old remote calls (Unit 5)"), ("JMS", "asynchronous messages"), ("JNDI", "naming and lookup"), ("threads", "in every container (U1)")]
for i, (a, b) in enumerate(mp):
    y = 28 + i * 31
    f.box(300, y, 120, 26, a, fill=MINT, stroke=TEAL, size=8.5, bold=True, r=4)
    f.box(424, y, 146, 26, b, fill="#ffffff", stroke=TEAL, size=8.5, color=SLATE, r=4)
f.box(10, 252 - 24 + 4, 270, 22, "", fill="#ffffff", stroke="#ffffff")
```

```svgfig label="7.8" caption="Where the time goes in a Java server, on a log scale, collecting the measurements of this book. A reflective bean setter took 68 ns (Fig. 7.2); a JDBC connection taken from a pool, 27 microseconds, against 186 microseconds to open a new one (Unit 3); a remote call through RMI, 53.0 microseconds (Unit 5); and a trivial page through the servlet container, 456 microseconds (Unit 6). The runs were separate programs on the same machine and loopback interface, so compare the orders of magnitude, not the last digit. Work outside the JVM, a network or a disk, costs far more."
import math
f = Fig(580, 236)
items = [("reflective bean setter", 68.2, TEAL, MINT), ("pooled JDBC connection", 27000, NAVY, BLUE), ("RMI call, loopback", 53000, AMBER, SAND), ("open a new JDBC connection", 186000, RED, ROSE), ("servlet page, loopback", 456000, RED, ROSE)]
def X(ns): return 190 + math.log10(ns / 10) * 62
for d, lab in enumerate(["10 ns", "100 ns", "1 us", "10 us", "100 us", "1 ms"]):
    x = 190 + d * 62
    f.line(x, 26, x, 176, color="#e2e8f0", sw=1)
    f.text(x, 190, lab, size=8.5, color=SLATE)
for i, (t, v, c, fl) in enumerate(items):
    y = 30 + i * 29
    f.text(184, y + 11, t, size=9.5, color=SLATE, anchor="end", bold=True, vmid=True)
    f.box(190, y, X(v) - 190, 22, "", fill=fl, stroke=c, r=2)
    lab = ("%.1f ns" % v) if v < 1000 else ("%.1f us" % (v / 1000)) if v < 1e6 else "x"
    f.text(X(v) + 6, y + 11, lab, size=9.5, color=c, anchor="start", bold=True, vmid=True)
r = 186 / 27
assert 6.8 < r < 6.9
f.text(290, 14, "time per operation, log scale", size=11, color=NAVY, bold=True)
f.box(10, 202, 560, 26, "new connection / pooled connection = %.1f times; a page costs about 456 / 53 = %.1f RMI calls" % (r, 456 / 53), fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9.5, bold=True)
```

### 7.5.1 Eight uses of JavaBeans in Nepal

Every Java web or desktop project of a Nepali company or college uses beans, because frameworks look for the conventions of this unit.

1. **Student and result records.** A bean such as `StudentBean` holds a name, marks and a computed `passed` property, and the same class is shown in a JSP, saved with JDBC and sent as JSON (Figure 7.1). Because `passed` has no setter, nobody can set it wrongly: it follows the marks.
2. **Forms in government and bank portals.** A form with twenty fields is filled into one bean with `jsp:setProperty property="*"`, which matches each parameter name to a setter (Figure 7.6). A wrong number such as `marks=abc` gives an error page, so the page must validate or catch the failure.
3. **Validation rules in the bean.** A constrained property can refuse a mark of 150, as the veto of the real run did (Figure 7.4). Putting the rule in the setter or the vetoer keeps it in one place, and every form, import file and test obeys it.
4. **Live dashboards and desktop tools.** A Swing tool for a clinic or a shop updates its labels when a bound property changes, without the code asking again (Figure 7.3). The listener is told only about real changes, so a repeated value costs no redraw.
5. **GUI builders and IDEs.** NetBeans and other tools show the properties of a component in a panel and let the student change them with the mouse (Plate 7.2). They find the properties by introspection, so a class with correct names appears in the tool at once (Figure 7.1).
6. **Saving and restoring state.** A program that saves the settings of a tailoring or billing shop to a file serializes its beans (Figure 7.5). After restoring, the data is back, but a validation rule registered as a lambda is lost, so the rule is better placed in the setter.
7. **Layers of a college system.** A controller servlet receives a request, a DAO fills a list of beans with JDBC, and a JSP shows them (Units 3 and 6). The beans are the data that travels between the layers, and their conventions keep the layers independent (Figure 7.7).
8. **Performance in busy portals.** Frameworks use reflection to call the setters of every bean, and the cost of one call is small (68 ns) once the lookup is cached, while a new database connection (186 us) or a page (456 us) costs far more (Figures 7.2 and 7.8). Knowing the scale shows where to tune first: pools and caches before clever code.

## Formula and fact sheet

- Bean rules: public no-arg constructor, private fields with `getX`/`setX` (`isX` for boolean), `Serializable`, optional events.
- Property kinds: simple, indexed, bound (`PropertyChangeSupport`), constrained (`VetoableChangeSupport`, `PropertyVetoException`).
- Introspection: `Introspector.getBeanInfo(cls, Object.class)`.
- JSP: `jsp:useBean`, `jsp:setProperty`, `jsp:getProperty`, `${bean.prop}`.
- POJO ⊂ JavaBean (with conventions); EJB is a different, container-managed component.

## Chapter summary

- A JavaBean is a serializable class with a no-argument constructor and private properties exposed through getters and setters; tools discover these by introspection.
- Bound properties announce changes; constrained properties let listeners veto them before they take effect.
- Beans connect the layers of an application (DAO, servlet, JSP, GUI) and are the basis of form binding in frameworks.
- The enterprise Java stack (Jakarta EE, Spring) builds on the same ideas: servlets, JDBC, beans, injection and transactions.

## Practice

1. State the JavaBeans conventions.
2. Write a `Book` bean with properties `title` (read-write) and `inStock` (boolean, read-only, computed from a count).
3. Distinguish simple, indexed, bound and constrained properties.
4. What is introspection and who uses it?
5. In the program of this unit, why do the marks remain 72 after `setMarks(150)`?
6. Use `jsp:useBean` to create a bean in session scope and show a property with EL.
7. Differentiate a JavaBean, a POJO, an Enterprise JavaBean and an entity.
8. Name the Jakarta EE technology (or technologies) for: web pages, REST services, database mapping, asynchronous messaging, resource lookup.
9. Explain how threads, JDBC, servlets and beans cooperate when a browser requests a page of students.
10. What happens to the registered listeners when a bean is serialised and restored?

::: note Answers and worked solutions
**1.** Public no-argument constructor; private fields exposed by `getX`/`setX` (or `isX` for boolean); implements `Serializable`; optionally supports bound and constrained property events.
**2.** `public class Book implements java.io.Serializable { private String title; private int count; public Book() {} public String getTitle() { return title; } public void setTitle(String t) { title = t; } public boolean isInStock() { return count > 0; } public void setCount(int c) { count = c; } public int getCount() { return count; } }`; `inStock` has no setter so it is read-only.
**3.** Simple: one value. Indexed: an array with `getX(int)`/`setX(int, v)`. Bound: changes announced to `PropertyChangeListener`s. Constrained: listeners can veto changes via `PropertyVetoException`.
**4.** Discovering a class's properties, methods and events at run time from its structure and naming conventions (`Introspector`); IDEs, JSP, EL and frameworks use it.
**5.** The vetoable listener threw `PropertyVetoException` from `fireVetoableChange` before the setter assigned the new value, so the field kept 72.
**6.** `<jsp:useBean id="student" class="edu.nebians.StudentBean" scope="session"/>` then `${student.name}`.
**7.** POJO: any plain class. JavaBean: a POJO with the bean conventions. EJB: a container-managed server component (session or message-driven bean). Entity: a bean mapped to a database table by JPA.
**8.** Servlets/JSP/JSF; JAX-RS; JPA; JMS; JNDI.
**9.** The container's thread pool gives each request a thread (Unit 1); the servlet calls a DAO that uses JDBC (Unit 3) to fill a list of student beans; the servlet stores the beans in the request and forwards to the JSP, which reads their properties with EL.
**10.** The support objects write only the listeners that are themselves serializable; others (such as lambdas) are skipped, so the restored bean has no such listeners and they must be registered again.
:::

## Model answers for Unit 7

**Q1. What is a JavaBean? Explain the conventions and the kinds of properties with an example. (10 marks)**

**Introduction.** A JavaBean is a reusable Java class that follows a few naming and structure rules, so that tools, JSP pages and frameworks can use it without knowing its code in advance (Fig. 7.1).

**Conventions.**

1. A **public no-argument constructor**, so a tool can create the object.
2. **Private fields** with public **getters and setters**, named `getXxx`/`setXxx`, or `isXxx` for a boolean.
3. **Serializable**, so that the state can be saved and restored.
4. Optionally **event support**, with `addPropertyChangeListener` and `removePropertyChangeListener`.

The property name is the method name without `get` or `set`, with the first letter in lower case, so `getMarks` and `setMarks` define the property `marks`.

**Kinds of properties.**

1. **Simple:** one value with a getter and a setter, such as `name`.
2. **Read-only and write-only:** a getter without a setter, such as `passed`, which is computed from the marks.
3. **Indexed:** an array, with `getScores(int)` and `setScores(int, int)` besides the whole-array forms.
4. **Bound:** every change is announced to `PropertyChangeListener`s with `firePropertyChange` (Fig. 7.3).
5. **Constrained:** listeners may veto a change by throwing `PropertyVetoException` (Fig. 7.4).

**What a real run found.** Asked about `StudentBean`, the `Introspector` reported five properties: `class` (read-only), `marks` (int, bound, constrained), `name` (String, bound), `passed` (boolean, read-only) and `scores` (indexed), one event set `propertyChange` and 22 method descriptors.

| Property | Getter | Setter | Kind |
|---|---|---|---|
| `name` | `getName` | `setName` | bound |
| `marks` | `getMarks` | `setMarks` | bound, constrained |
| `passed` | `isPassed` | none | read-only |
| `scores` | `getScores` | `setScores` | indexed |

**Example.** `public class StudentBean implements Serializable { private int marks; public StudentBean() {} public int getMarks() { return marks; } public void setMarks(int m) { marks = m; } public boolean isPassed() { return marks >= 40; } }`

**Why the rules matter.** A tool that meets an unknown class cannot read its source. The naming rules let it find the properties by name, call the getter to show a value and the setter to change it, create a fresh object with the no-argument constructor and save the object because it is serializable. This is why a form builder, a JSP page and a framework can all handle `StudentBean` although none of them was written for it. A class that breaks a rule, for example a bean with only a constructor taking arguments, simply fails when a tool tries to create it.

**Conclusion.** The conventions cost almost nothing to follow, and in return a bean works in JSP, EL, GUI builders, JDBC helpers and every major framework.

**Q2. Distinguish bound and constrained properties with the results of the unit's run. (5 marks)**

A **bound property** announces a change after it has happened. The setter stores the new value and calls `firePropertyChange(name, old, new)`, and each registered `PropertyChangeListener` receives an event with the name, the old value and the new value. In the run, five setter calls produced only three events: `name: unknown -> Sita`, `marks: 0 -> 72` and `scores: 0 -> 9`. Repeating `setName("Sita")` or `setMarks(72)` fired nothing, because the support object ignores equal values (Fig. 7.3).

A **constrained property** asks permission before the change. The setter first calls `fireVetoableChange`, and any `VetoableChangeListener` may throw `PropertyVetoException`, which stops the assignment. The setter must declare `throws PropertyVetoException`. In the run, `setMarks(150)` and `setMarks(-5)` were vetoed with the message `marks must be 0..100`, and the marks stayed 72 (Fig. 7.4).

| Point | Bound | Constrained |
|---|---|---|
| When | after the change | before the change |
| Listener type | `PropertyChangeListener` | `VetoableChangeListener` |
| Can stop the change | no | yes, by exception |
| Example use | refresh a label | reject marks above 100 |

Many properties are both: the constrained check runs first, then the value is assigned, then the bound event is sent.

**Q3. What is introspection? Who uses it, and what does it cost? (5 marks)**

**Introspection** is the discovery of a class's properties, methods and events at run time, from its structure and naming conventions, without help from the programmer. `Introspector.getBeanInfo(Class)` examines the class by reflection and returns a `BeanInfo` with `PropertyDescriptor`s, `MethodDescriptor`s and `EventSetDescriptor`s. A class may supply its own `BeanInfo` to override the result.

The users are every tool that works with unknown classes: GUI builders such as NetBeans list the properties of a component in a panel (Plate 7.2), JSP and EL call `getXxx` and `setXxx` by name, form libraries copy request parameters into setters, and frameworks map beans to JSON or to database columns.

In the run, the first `getBeanInfo(StudentBean.class)` took 18.85 ms, and the second took 0.011 ms from the cache, about 1,700 times faster (Fig. 7.2). A setter called through `Method.invoke` took 68.2 ns, against 49.4 ns for a direct call, a factor of 1.38. The advice is to look up once and keep the result, and then reflection is cheap enough for every web request.

**Q4. Explain how beans are used in JSP with `jsp:useBean`, `jsp:setProperty` and EL. Describe the scopes. (10 marks)**

**Introduction.** A JSP can create, fill and display a bean without any Java code, using three standard actions and the expression language. This keeps data handling out of the page (Fig. 7.6).

**The actions.**

1. **`jsp:useBean`** looks for an attribute with the given `id` in the chosen scope and creates a new bean with the no-argument constructor if there is none: `<jsp:useBean id="st" class="edu.nebians.StudentBean" scope="session"/>`.
2. **`jsp:setProperty`** calls a setter. With `property="*"` it copies every request parameter whose name matches a property, converting the text to the property type.
3. **`jsp:getProperty`** or the EL form `${st.name}` reads a property through the getter, and `${st.passed}` uses `isPassed`.

**Scopes.** `page` lasts for one JSP execution, `request` for one request, `session` for one visitor and `application` for the whole web application.

**Behaviour measured on Tomcat.**

1. A request with `name=Sita&marks=72` printed `name=Sita marks=72 passed=true`.
2. A second request of the same session without parameters still printed Sita and 72, since the bean lives in the session.
3. A visitor without the cookie got a new bean: `name=unknown marks=0 passed=false`.
4. With request scope, the bean was new every time: Ram, then `unknown`.
5. `marks=150` was vetoed and `marks=abc` could not be converted; both gave status 500, and the bean kept 72.

| Scope | Lifetime | Example |
|---|---|---|
| request | one request | search result |
| session | one visitor | login, cart |
| application | all visitors | counters, settings |

**Cautions.** A bean without a public no-argument constructor cannot be created. Page-level validation is needed, because a bad number leads to an error page. User text must be escaped when it is printed (Unit 6).

**Example page.** The whole page of the run was one line of actions: `useBean` with `scope="session"`, `setProperty` with `property="*"`, and the text `name=${st.name} marks=${st.marks} passed=${st.passed}`. The page contains no Java statement, yet it created the bean once per visitor, filled it from the URL parameters and showed three properties, one of them computed. In a larger application the controller servlet, not the page, creates and fills the bean and the JSP only reads it.

**Conclusion.** `useBean` and EL move data handling into plain Java classes and leave the JSP with markup only, which is the basis of the MVC pattern.

**Q5. What happens to a bean's listeners when it is serialized and restored? (5 marks)**

Serialization writes the fields of an object into a byte stream, and a bean implements `Serializable` for this reason. In the run, the `StudentBean` with the name Sita, marks 72 and `scores[1]` equal to 9 was 540 bytes. The state came back intact: name, marks and scores were the same (Fig. 7.5).

The listeners are held by the support objects `PropertyChangeSupport` and `VetoableChangeSupport`, which write only those listeners that are themselves serializable. After one `Serializable` listener was added, the output grew to 576 bytes, and the restored bean had that listener back. A lambda is not serializable, so it is skipped. The veto rule of the bean was registered as a lambda in the constructor, and the restored bean had 0 veto listeners; `setMarks(150)` was then accepted and the marks became 150.

The remedies are three. Put validation in the setter itself, where it travels with the class. Register the listeners again after `readObject`. Make listener classes `Serializable`, or use `transient` for references that should not be saved. A bean that is saved in an HTTP session must also be serializable, because a server may move sessions to disk or to another machine.

**Q6. Differentiate POJO, JavaBean, DTO, entity and Enterprise JavaBean. (5 marks)**

These terms describe increasing levels of convention and of container support (Fig. 7.7).

1. **POJO** (Plain Old Java Object) is any ordinary class with no special rules and no framework dependency.
2. **JavaBean** is a POJO that follows the conventions: a public no-argument constructor, private fields with getters and setters, and `Serializable`. Tools can introspect it.
3. **DTO** (Data Transfer Object) is a bean whose only job is to carry data between layers or over the network, with no business logic, such as a `StudentSummary` sent to a JSP or as JSON.
4. **Entity** is a bean mapped to a database table by JPA annotations such as `@Entity` and `@Id`; the framework loads and saves it.
5. **Enterprise JavaBean (EJB)** is a server component managed by an application server, which supplies transactions, security, pooling and remote access. Session beans hold business logic, and message-driven beans react to messages.

| Kind | Needs a container | Typical job |
|---|---|---|
| POJO | no | any logic |
| JavaBean | no | data for tools and JSP |
| DTO | no | move data between layers |
| Entity | JPA provider | persistent data |
| EJB | application server | transactional business logic |

A class may be several of these at once: a `Student` can be a POJO, a JavaBean and an entity together.

**Q7. Draw and explain the enterprise Java map, and show how threads, JDBC, servlets and beans cooperate for the request of a student list. (10 marks)**

**Introduction.** Java EE, now Jakarta EE, is a family of specifications for server applications. Each specification solves one problem, and a real request passes through several of them (Fig. 7.7).

**The technologies.**

1. **Servlet, JSP and JSF** handle web requests and pages (Unit 6).
2. **JDBC and JPA** reach the database; JPA maps beans to tables (Unit 3).
3. **JAX-RS** builds REST services, the modern form of remote calls, with RMI and CORBA as older forms (Unit 5).
4. **JMS** sends asynchronous messages through a queue.
5. **JNDI** finds resources by name, such as a data source.
6. **CDI and EJB** manage objects, transactions and security.
7. **Threads** (Unit 1) run inside every container, one per request.

**One request, step by step.** The browser sends `GET /students`. The container takes a pool thread, which ran the page of the real run in about 456 microseconds (Fig. 7.8). Filters run, and the controller servlet is called. The servlet asks a DAO for the data; the DAO takes a pooled connection (27 microseconds against 186 for a new one), runs a prepared statement and fills a list of `Student` beans. The servlet stores the list as a request attribute and forwards to the JSP. The JSP reads the beans through EL, escapes the text and writes the HTML, and the container sends it with status 200.

| Step | Technology | Unit |
|---|---|---|
| thread per request | container pool | 1 |
| controller | servlet | 6 |
| data access | JDBC, pooled | 3 |
| data carriers | JavaBeans | 7 |
| view | JSP with EL | 6, 7 |

**Where to go next.** Spring Boot, Jakarta EE servers such as WildFly, and gRPC or REST for service calls build on exactly these pieces.

**Conclusion.** The technologies cooperate in layers, and the beans are the data that travels through all of them; learning the conventions once makes every layer work with the others.

**Q8. Why do frameworks depend on naming conventions and reflection, and what does that cost? (5 marks)**

A framework cannot know the classes that a programmer will write later, so it needs a rule for finding out what a class offers. The JavaBeans conventions are that rule: a property `marks` always has `getMarks` and `setMarks`, so a framework can read a request parameter named `marks` and call the setter by name. JSP and EL do this for `${st.marks}`, a JSON library does it to turn a bean into text, and a persistence framework does it to fill an object from a database row. The programmer writes plain classes, and no registration code is needed.

The cost is time and safety. In the run, the first introspection took 18.85 ms and the cached one 0.011 ms; a reflective setter call took 68.2 ns against 49.4 ns for a direct call, a factor of 1.38 (Fig. 7.2). The price is small next to a database connection (186 microseconds when new) or a page (456 microseconds), so the framework overhead is rarely the bottleneck (Fig. 7.8). Errors move to run time: a misspelt property name or a missing setter appears only when the page runs, and `marks=abc` gave status 500 (Fig. 7.6). Good practice is to cache the lookups, keep the names exact and test the pages.
