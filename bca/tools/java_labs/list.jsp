<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<table><c:forEach var="s" items="${students}"><tr><td>${s.name}</td><td>${s.marks}</td></tr>
</c:forEach></table>
<p>average=${average}</p>
