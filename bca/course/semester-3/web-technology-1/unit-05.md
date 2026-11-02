---
subject: Web Technology I
grade: BCA Semester 3
unit: 5
title: XML (Extensible Markup Language)
area: BCA 203 · Web Technology I · Unit 5
---

**XML** is a text format for describing *data* with your own tags. HTML has a fixed tag set for presentation; XML lets you invent tags (`<student>`, `<marks>`) so that data can be exchanged between different systems.

::: key What this unit gives you
- XML syntax and the rules of a **well-formed** document.
- **Valid** documents: DTD and XML Schema.
- Namespaces, XPath, and displaying XML with CSS or XSLT.
- Parsing XML, and XML versus JSON and HTML.
:::

## 5.1 Why XML? Syntax

XML (W3C, 1998) is self-describing, plain text, platform independent and both human- and machine-readable. Uses: configuration files, RSS/Atom feeds, SOAP web services, Office documents (`.docx` is zipped XML), SVG, Android layouts.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- a college register -->
<college name="NEBians College">
  <student id="1" status="active">
    <name>Sita Sharma</name>
    <marks subject="DBMS">85</marks>
    <marks subject="DSA">72</marks>
    <note><![CDATA[Uses <b> and & freely here]]></note>
  </student>
  <student id="2">
    <name>Ram Thapa</name>
    <marks subject="DBMS">64</marks>
    <address/>
  </student>
</college>
```

Parts: **prolog** (`<?xml …?>`, optional but recommended), **elements** (`<name>…</name>`), **attributes** (`id="1"`), **text**, **comments**, **CDATA** (raw text not parsed), and **processing instructions**.

## 5.2 Well-formed rules

A document must obey all of these or parsers must reject it (XML is strict, unlike HTML):

1. Exactly **one root** element.
2. Every start tag has a matching **end tag** (or is self-closing `<address/>`).
3. Elements are **properly nested** (`<a><b></b></a>`, never `<a><b></a></b>`).
4. Names are **case-sensitive** (`<Name>` ≠ `<name>`), start with a letter or `_`, no spaces.
5. Attribute values are **quoted**; an attribute cannot repeat on one element.
6. Special characters are escaped: `&lt;` `&gt;` `&amp;` `&quot;` `&apos;`.

```text
<student><name>Sita</student></name>      -- not well-formed: crossing tags
<a x=1/>                                  -- not well-formed: unquoted attribute
<a/><b/>                                  -- not well-formed: two roots
```

**Element or attribute?** Use attributes for metadata about an element (`id`, `lang`, `currency`) and elements for the data itself, especially if it may repeat or have structure.

## 5.3 Valid XML: DTD

A document is **valid** if it is well-formed *and* follows a declared grammar. A **Document Type Definition (DTD)** declares the allowed elements and attributes:

| Declaration | Meaning |
|---|---|
| `<!ELEMENT students (student+)>` | `students` contains one or more `student` |
| `<!ELEMENT student (name, marks)>` | exactly `name` then `marks`, in order |
| `<!ELEMENT name (#PCDATA)>` | text only |
| `<!ELEMENT br EMPTY>` / `ANY` | no content / anything |
| `?`, `*`, `+`, `|` | optional, zero-or-more, one-or-more, choice |
| `<!ATTLIST student id CDATA #REQUIRED>` | attribute with type and default (`#REQUIRED`, `#IMPLIED`, a fixed or default value) |

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE students [
  <!ELEMENT students (student+)>
  <!ELEMENT student (name, marks)>
  <!ATTLIST student id CDATA #REQUIRED status (active|passed) "active">
  <!ELEMENT name (#PCDATA)>
  <!ELEMENT marks (#PCDATA)>
]>
<students>
  <student id="1"><name>Sita</name><marks>85</marks></student>
  <student id="2" status="passed"><name>Ram</name><marks>64</marks></student>
</students>
```

This document was checked with `xmllint --valid`: it conforms to its internal DTD. Remove the `<name>` of one student and it becomes invalid (still well-formed). A DTD can be **internal** (inside `<!DOCTYPE>`) or **external** (`<!DOCTYPE students SYSTEM "students.dtd">`). **Limitations of DTD:** no data types (everything is text), not written in XML, no namespaces.

## 5.4 XML Schema (XSD)

XML Schema is the richer replacement: written in XML, with **data types** (`xs:integer`, `xs:date`, `xs:string`), ranges, patterns, and namespaces.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="students">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="student" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="name" type="xs:string"/>
              <xs:element name="marks">
                <xs:simpleType>
                  <xs:restriction base="xs:integer">
                    <xs:minInclusive value="0"/><xs:maxInclusive value="100"/>
                  </xs:restriction>
                </xs:simpleType>
              </xs:element>
            </xs:sequence>
            <xs:attribute name="id" type="xs:integer" use="required"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

A schema can say that `marks` is an integer from 0 to 100, which a DTD cannot.

## 5.5 Namespaces

Two vocabularies may use the same tag name (`<table>` in HTML and `<table>` for furniture). A **namespace**, identified by a URI (just a unique name; nothing is fetched), removes the clash:

```xml
<?xml version="1.0"?>
<doc xmlns:h="http://www.w3.org/1999/xhtml" xmlns:f="http://example.com/furniture">
  <h:table><h:tr><h:td>cell</h:td></h:tr></h:table>
  <f:table><f:material>wood</f:material></f:table>
</doc>
```

## 5.6 Displaying XML: CSS and XSLT

Browsers show raw XML as a tree. **CSS** can style it (`<?xml-stylesheet type="text/css" href="s.css"?>` with rules such as `name { display: block; font-weight: bold; }`), but cannot reorder or compute. **XSLT** (XSL Transformations) is a language that *transforms* XML into HTML or other XML using templates and **XPath**:

```xml
<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html><body><h2>Students</h2>
      <ul>
        <xsl:for-each select="college/student">
          <xsl:sort select="name"/>
          <li><xsl:value-of select="name"/> (<xsl:value-of select="marks"/>)</li>
        </xsl:for-each>
      </ul>
    </body></html>
  </xsl:template>
</xsl:stylesheet>
```

**XPath** addresses nodes like a file path: `/college/student` (all students), `//name` (all names anywhere), `student[@id='2']/name` (name of student 2), `student[marks>80]`, `count(//student)`, `text()`, `@id`.

## 5.7 Parsing XML

| Parser | Style | Memory | Use |
|---|---|---|---|
| **DOM** | loads the whole document as a tree you navigate and edit | high | small files, random access |
| **SAX** | event-driven stream: callbacks for start tag, text, end tag; read-only, forward-only | low | huge files |
| **Pull / StAX** | the program asks for the next event | low | streaming with control |

## 5.8 XML versus HTML and JSON

| | HTML | XML | JSON |
|---|---|---|---|
| Purpose | display documents | describe and exchange data | exchange data |
| Tags | fixed | user-defined | none (key/value) |
| Strictness | forgiving | strict, well-formed | strict |
| Size | – | verbose | compact |
| Schemas, namespaces, XSLT | no | yes | JSON Schema (separate) |
| Typical use today | web pages | documents, feeds, enterprise/SOAP | web APIs |

The same record in JSON is `{"student": {"id": 1, "name": "Sita", "marks": 85}}`: shorter, but without attributes, comments or built-in validation.

## Formula and fact sheet

- Well-formed: one root, matched and nested tags, case-sensitive names, quoted attributes, escaped `< > & " '`.
- Valid = well-formed + conforms to DTD or XSD. XSD supports data types and namespaces.
- DTD symbols: `?` `*` `+` `|`; `#PCDATA`, `EMPTY`, `#REQUIRED`.
- XPath: `/`, `//`, `[@a='v']`, `text()`. XSLT turns XML into HTML.
- DOM = whole tree in memory; SAX = streaming events.

## Chapter summary

- XML describes data with custom tags under strict well-formedness rules.
- DTDs and XML Schemas make a document valid against a grammar; namespaces avoid name clashes.
- CSS and XSLT present XML; DOM and SAX parse it; JSON has taken over most web-API use.

## Practice

1. List the rules of a well-formed XML document; correct `<a><b>text</a></b>`.
2. Write an XML document for a library with two books (id attribute; title, author, price elements).
3. Write a DTD for it.
4. Differentiate well-formed and valid; DTD and XSD.
5. What problem do namespaces solve?
6. Write XPath for: titles of books priced over 500; the author of book id 2.
7. Compare DOM and SAX.
8. Differentiate XML and HTML.

::: note Answers and worked solutions
**1.** See 5.2. Corrected: `<a><b>text</b></a>`.
**2.** `<library><book id="1"><title>DSA</title><author>Weiss</author><price>650</price></book><book id="2"><title>DBMS</title><author>Korth</author><price>480</price></book></library>`
**3.** `<!ELEMENT library (book+)> <!ELEMENT book (title, author, price)> <!ATTLIST book id CDATA #REQUIRED> <!ELEMENT title (#PCDATA)> <!ELEMENT author (#PCDATA)> <!ELEMENT price (#PCDATA)>`
**4.** Well-formed obeys the syntax rules; valid is well-formed and conforms to a DTD/XSD. DTD: non-XML syntax, no data types; XSD: XML syntax, types, namespaces.
**5.** They prevent clashes when different vocabularies use the same element names in one document.
**6.** `//book[price>500]/title`; `//book[@id='2']/author`.
**7.** DOM builds the full tree (easy navigation, memory heavy); SAX streams events (low memory, forward only).
**8.** HTML has predefined tags for display and tolerates errors; XML has user-defined tags for data and must be well-formed.
:::
