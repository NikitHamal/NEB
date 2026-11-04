# Java labs behind the Advanced Java (BCA 303) figures

Real programs whose printed numbers appear in Units 5-7 (figures and captions). Not part of the PDF build.

- `RmiLab.java`: Unit 5, registry + remote object + client in one JVM with a byte-counting RMISocketFactory.
- `ServLab.java` (+ `demo.jsp`, `list.jsp` under `/tmp/j/web`): Unit 6, embedded Tomcat 9.0.89 + Jasper + JSTL 1.2.
- `BeanLab.java` + `edu/nebians/StudentBean.java`: Unit 7, Introspector, bound/constrained events, serialization, `jsp:useBean` on Tomcat.
- Setup: JDK 17 (`sudo -n apt-get install -y openjdk-17-jdk-headless maven`), then `mvn dependency:copy-dependencies -DoutputDirectory=/tmp/j/lib` with `pom.xml`; compile with `javac -cp "/tmp/j/lib/*"` and run with `java -cp ".:/tmp/j/lib/*"`. Timings vary a little from run to run; the book uses one recorded run.
