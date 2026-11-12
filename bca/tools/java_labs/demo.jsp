<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<p>class=<%= this.getClass().getName() %></p>
<p>raw=${param.q}</p>
<p>out=<c:out value="${param.q}"/></p>
<p>loop=<c:forEach var="i" begin="1" end="3">[${i}]</c:forEach></p>
<p>sum=${2+3} method=${pageContext.request.method}</p>
<% int n = 0; for (int i = 1; i <= 4; i++) n += i; %>
<p>scriptlet=<%= n %></p>
