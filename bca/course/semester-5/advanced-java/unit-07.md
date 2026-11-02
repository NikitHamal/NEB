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
