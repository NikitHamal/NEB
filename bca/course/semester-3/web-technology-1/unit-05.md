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

## 5.9 Seeing XML: trees, errors, validation and size

XML is a text format with strict rules, and its rules are easiest to remember by seeing them broken. The plate shows Tim Bray, one of the editors of the XML 1.0 specification, next to the family of standards built around it. The figures that follow draw the tree, the well-formed rules, the validation pipeline, namespaces, DOM against SAX parsing, and a real size comparison with JSON.

```photogrid label="5.1" cols="2" ratio="1.2" caption="(a) Tim Bray, co-editor of the XML 1.0 recommendation published by the W3C in February 1998. XML was designed as a simplified SGML that anyone could parse without special software. (b) The XML family: XML holds the data, DTD and XSD define the allowed structure, namespaces avoid name clashes, CSS and XSLT present the data, and DOM and SAX are two ways for programs to read it."
@ photo id="bca203/bray" cap="Tim Bray"
fit 1.2
focus 0.5 0.62
@ svg cap="The XML family"
f = Fig(330, 275)
f.box(95, 10, 140, 36, "XML  data", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.box(224, 90, 98, 40, "CSS / XSLT", fill=ROSE, stroke=RED, size=12.5, bold=True)
f.box(4, 90, 98, 40, "DTD / XSD", fill=MINT, stroke=TEAL, size=12.5, bold=True)
f.box(114, 90, 104, 40, "Namespace", fill=SAND, stroke=AMBER, size=12.5, bold=True)
f.arrow([(130, 46), (53, 90)], color=SLATE); f.arrow([(165, 46), (165, 90)], color=SLATE); f.arrow([(200, 46), (273, 90)], color=SLATE)
f.box(60, 180, 100, 38, "DOM", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(176, 180, 100, 38, "SAX", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.arrow([(165, 130), (110, 180)], color=SLATE, dash=True); f.arrow([(165, 130), (226, 180)], color=SLATE, dash=True)
f.text(165, 244, "programs read XML with DOM or SAX", size=12.5, color=SLATE, bold=True)
```

```svgfig label="5.1" caption="An XML document as a tree. The single root element students has three student children; each student has an attribute id and two child elements, name and marks, which contain text. Everything between a start tag and its end tag is the element's content. Attributes describe an element (id=101), while child elements hold the data. A rule of thumb: use an attribute for identity and metadata, and an element for data that may repeat or have its own structure."
f = Fig(580, 214)
f.box(240, 6, 100, 28, "students", fill=BLUE, stroke=NAVY, size=11, bold=True)
for i, (idn, nm, mk) in enumerate([("101", "Sita Sharma", "78"), ("102", "Ram Thapa", "65"), ("103", "Gita Rai", "91")]):
    cx = 100 + i * 190
    f.box(cx - 50, 70, 100, 28, "student", fill=MINT, stroke=TEAL, size=11, bold=True)
    f.line(290, 34, cx, 70, color=SLATE)
    f.text(cx, 62, "id=" + idn, size=10, color=RED, bold=True)
    f.box(cx - 70, 130, 64, 26, "name", fill=SAND, stroke=AMBER, size=10.5, bold=True)
    f.box(cx + 6, 130, 64, 26, "marks", fill=SAND, stroke=AMBER, size=10.5, bold=True)
    f.line(cx, 98, cx - 38, 130, color=SLATE); f.line(cx, 98, cx + 38, 130, color=SLATE)
    f.text(cx - 38, 176, nm, size=9.5, color=SLATE, bold=True)
    f.text(cx + 38, 176, mk, size=10.5, color=SLATE, bold=True)
f.text(290, 204, "Root = students.   Text nodes at the bottom.   id = attribute.", size=10, color=NAVY, bold=True)
```

```svgfig label="5.2" caption="Five typical well-formedness errors (left) and their corrections (right). (1) Elements must be properly nested: close b before a. (2) Every start tag needs an end tag. (3) Attribute values need quotes. (4) Tag names are case-sensitive: Name and name differ. (5) A document has exactly one root element. A single such error makes a conforming parser stop and report a fatal error; unlike HTML, XML never guesses what you meant."
f = Fig(580, 218)
bad = ["<a><b>text</a></b>", "<p>First<p>Second", "<student id=101>", "<Name>Sita</name>", "<a>1</a><a>2</a>  (two roots)"]
good = ["<a><b>text</b></a>", "<p>First</p><p>Second</p>", "<student id=\"101\">", "<name>Sita</name>", "<list><a>1</a><a>2</a></list>"]
f.box(10, 4, 280, 24, "Not well-formed", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(300, 4, 270, 24, "Well-formed", fill=MINT, stroke=TEAL, size=11, bold=True)
for i, (b, g) in enumerate(zip(bad, good)):
    y = 38 + i * 36
    f.box(10, y, 280, 30, "", fill=SOFT, stroke=RED)
    f.text(20, y + 15, f"{i+1}  " + b, size=10.5, color=RED, bold=True, anchor="start")
    f.box(300, y, 270, 30, "", fill=SOFT, stroke=TEAL)
    f.text(310, y + 15, g, size=10.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="5.3" caption="The two checks an XML document passes. The parser first tests that the document is well-formed (syntax). If a DTD or XSD is attached, a validating parser then tests that it is valid (it follows the declared structure and types). A document can be well-formed but invalid: for example, <marks>excellent</marks> is correct XML but fails an XSD that says marks must be an integer between 0 and 100."
f = Fig(580, 150)
f.box(10, 50, 90, 44, "XML\ndocument", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(150, 50, 120, 44, "Parser:\nwell-formed?", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(320, 50, 120, 44, "Validator:\nDTD / XSD?", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(490, 50, 80, 44, "Program\nuses data", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(100, 72), (150, 72)], color=SLATE); f.arrow([(270, 72), (320, 72)], color=TEAL); f.arrow([(440, 72), (490, 72)], color=TEAL)
f.text(295, 64, "yes", size=10, color=TEAL, bold=True); f.text(465, 64, "yes", size=10, color=TEAL, bold=True)
f.arrow([(210, 94), (210, 128)], color=RED); f.text(216, 118, "no: fatal error, stop", size=10, color=RED, bold=True, anchor="start")
f.arrow([(380, 94), (380, 128)], color=RED); f.text(386, 118, "no: invalid", size=10, color=RED, bold=True, anchor="start")
```

```svgfig label="5.4" caption="Namespaces remove name clashes. Two vocabularies both use the element title: one for a book (library namespace) and one for a person (hr namespace). The prefix is only a nickname; the identity is the URI after xmlns:. Both documents below can be merged because lib:title and hr:title are different names, even though the local name is the same. The URI need not be a real web page; it is just a unique string."
f = Fig(580, 160)
f.box(10, 10, 270, 140, "", fill=SOFT, stroke=SLATE)
f.text(20, 28, '<record xmlns:lib="http://lib.example/ns"', size=9.5, color=NAVY, bold=True, anchor="start")
f.text(20, 46, '        xmlns:hr="http://hr.example/ns">', size=9.5, color=NAVY, bold=True, anchor="start")
f.text(20, 68, '  <lib:title>Web Technology</lib:title>', size=10, color=TEAL, bold=True, anchor="start")
f.text(20, 88, '  <hr:title>Professor</hr:title>', size=10, color=AMBER, bold=True, anchor="start")
f.text(20, 108, "</record>", size=10, color=NAVY, bold=True, anchor="start")
f.text(20, 134, "prefix = nickname,  URI = real identity", size=10, color=RED, bold=True, anchor="start")
f.box(310, 20, 260, 40, "lib:title  =  {lib.example/ns}title", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(310, 76, 260, 40, "hr:title  =  {hr.example/ns}title", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(440, 140, "Different names, no clash", size=10.5, color=NAVY, bold=True)
```

```svgfig label="5.5" caption="Two ways to read the same XML. DOM loads the whole document into a tree in memory, which allows random access, edits and XPath, but needs memory in proportion to the file. SAX reads the file once from top to bottom and fires events (start element, text, end element), using almost no memory but giving no backward movement. A 2 GB export of exam records is a job for SAX; a 20 KB configuration file is a job for DOM."
f = Fig(580, 170)
f.box(10, 10, 270, 150, "", fill=BLUE, stroke=NAVY)
f.text(145, 28, "DOM: whole tree in memory", size=11, color=NAVY, bold=True)
f.box(115, 44, 60, 24, "root", fill=SOFT, stroke=NAVY, size=10, bold=True)
for i, x in enumerate((40, 120, 200)):
    f.box(x, 90, 60, 24, "child", fill=SOFT, stroke=NAVY, size=10, bold=True); f.line(145, 68, x + 30, 90, color=SLATE)
f.text(145, 140, "random access, edit, XPath", size=10, color=TEAL, bold=True)
f.box(300, 10, 270, 150, "", fill=MINT, stroke=TEAL)
f.text(435, 28, "SAX: stream of events", size=11, color=TEAL, bold=True)
for i, e in enumerate(["startElement students", "startElement student", "characters Sita Sharma", "endElement student"]):
    f.box(330, 38 + i * 26, 210, 22, e, fill=SOFT, stroke=TEAL, size=9.5, bold=True)
f.text(435, 150, "one pass, tiny memory", size=10, color=TEAL, bold=True)
```

```svgfig label="5.6" caption="The same three student records written as compact XML and as compact JSON. XML: <students><student id='101'><name>Sita Sharma</name><marks>78</marks></student> ... </students> is 223 bytes, JSON: [{id:'101', name:'Sita Sharma', marks:78}, ...] is 131 bytes, about 41 percent smaller. After gzip compression the sizes are 119 and 98 bytes, so compression closes much of the gap. XML pays for its closing tags but gains comments, namespaces, schemas and mixed content, which is why it still dominates documents, configuration and web feeds."
f = Fig(580, 150)
f.text(10, 24, "Raw bytes", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(100, 8, 223 * 1.7, 26, "XML  223 B", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True, r=3)
f.box(100, 40, 131 * 1.7, 26, "JSON  131 B", fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True, r=3)
f.text(10, 100, "After gzip", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(100, 84, 119 * 1.7, 26, "XML  119 B", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True, r=3)
f.box(100, 116, 98 * 1.7, 26, "JSON  98 B", fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True, r=3)
```

### 5.9.1 Eight applications of XML

1. **Configuration files.** Many tools store settings in XML, such as the Android manifest and Maven build files. The format is readable by people and by programs, and it can carry comments. A student who opens an Android project sees AndroidManifest.xml and learns the same rules used in this unit.
2. **Web feeds (RSS and Atom).** News sites publish a feed as an XML file that readers poll for new items. An online newspaper in Nepal can offer one feed per section. A feed reader app downloads only a small XML file, then shows new headlines without opening the website.
3. **Document formats.** Office files such as DOCX, XLSX and ODT are zip archives full of XML. This is why a program can read a spreadsheet without Excel. A tool that prepares result sheets for a college can generate such files directly.
4. **Vector graphics.** SVG is XML for drawings, so a logo can be scaled to any size and styled by CSS. All the diagrams in this book are SVG. A college can keep one logo file for the website and for print.
5. **Data exchange between organisations.** Older government and banking systems send messages in XML or SOAP envelopes with a schema that both sides trust. A schema allows the receiver to reject bad data automatically. Customs declarations and bank messages between systems often work this way.
6. **Android layouts and resources.** Screens, colours and strings of an Android app are written in XML. The same layout file can be styled for phones and tablets. A Nepali translation of an app is simply another XML file of strings.
7. **Sitemaps and metadata.** Search engines read sitemap.xml to find the pages of a website and library catalogues exchange book records in XML. This lets a university library share its catalogue with national systems. Correct metadata makes resources easier to find.
8. **Transformation to other formats.** With XSLT one XML source can be turned into HTML pages, PDF or another XML. A result file for 3 students with marks 78, 65 and 91 can be turned into a table with total 234 and average 78. The data is written once and shown in many forms.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is XML? Explain the rules that make an XML document well-formed, with an example.**

*Introduction.* XML (eXtensible Markup Language) is a W3C text format for storing and transporting structured data, where the author invents the tag names (section 5.1, Figures 5.1 and 5.2).

1. **One root.** A document has exactly one root element that contains all others.
2. **Matching tags.** Every start tag has an end tag, or the element is self-closing like `<br/>`.
3. **Proper nesting.** Elements close in the reverse order of opening: `<a><b></b></a>`.
4. **Quoted attributes.** Attribute values must be in single or double quotes, and an attribute name appears once per element.
5. **Case sensitivity.** `<Name>` and `<name>` are different; names cannot start with a digit or contain spaces.
6. **Special characters.** The characters < and & in text must be written as `&lt;` and `&amp;`, or placed in a CDATA section.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<students>
  <student id="101"><name>Sita Sharma</name><marks>78</marks></student>
</students>
```

*Conclusion.* A document that obeys these rules is well-formed, and a conforming parser must reject any document that does not, which makes XML predictable to process.

**Q2 (5 marks). Distinguish between DTD and XML Schema (XSD). Write a DTD or XSD for the student element.**

*Introduction.* A well-formed document may still have the wrong structure, so a DTD or XSD declares the allowed elements and, in XSD, their data types (sections 5.3 and 5.4, Figure 5.3).

1. **Syntax.** A DTD uses its own non-XML syntax; an XSD is itself written in XML and can be processed with the same tools.
2. **Data types.** A DTD has almost only text (#PCDATA); XSD has integers, dates, decimals, patterns and ranges.
3. **Namespaces.** XSD supports namespaces; DTD does not.
4. **Occurrence control.** XSD can say minOccurs and maxOccurs precisely; a DTD uses ?, * and +.
5. **Example (DTD).**

```xml
<!ELEMENT student (name, marks)>
<!ATTLIST student id CDATA #REQUIRED>
<!ELEMENT name (#PCDATA)>
<!ELEMENT marks (#PCDATA)>
```

6. **Example (XSD, marks limited to 0-100).**

```xml
<xs:element name="marks">
  <xs:simpleType>
    <xs:restriction base="xs:integer">
      <xs:minInclusive value="0"/><xs:maxInclusive value="100"/>
    </xs:restriction>
  </xs:simpleType>
</xs:element>
```

| Point | DTD | XSD |
|---|---|---|
| Syntax | Non-XML | XML |
| Types | Text only | Rich types |
| Namespaces | No | Yes |

*Conclusion.* XSD is more powerful and is preferred for data exchange; DTD is short and still found in older systems.

**Q3 (10 marks). Explain how XML data can be displayed and processed. Describe CSS, XSLT, DOM and SAX, and compare XML with JSON.**

*Introduction.* XML stores data but says nothing about how it should look or how a program should read it. Two jobs follow: presenting the data to a person (CSS or XSLT) and reading it inside a program (DOM or SAX). Modern web services also use JSON for the same data, so the formats are compared (sections 5.6 to 5.8, Figures 5.5 and 5.6).

1. **CSS display.** A style sheet linked by `<?xml-stylesheet type="text/css" href="s.css"?>` can set display, colour and fonts for each element, but it cannot reorder, filter or compute.
2. **XSLT.** The XML-based language XSLT matches nodes with XPath and builds a new document from templates, so it can sort, filter, add up and produce HTML. For the three students, summing the marks gives 78 + 65 + 91 = 234 and the average is 78.
3. **XPath.** An expression such as `/students/student[marks>70]/name` selects nodes from the tree; it is used by XSLT and by many APIs.
4. **DOM parsing.** The parser builds a tree of all nodes in memory; the program can move up, down and sideways, change nodes and write the tree back. It is easy to use but needs memory proportional to the file size.
5. **SAX parsing.** The parser reads once and fires events: startElement, characters and endElement. It uses little memory and suits very large files but cannot go backwards.
6. **Choosing.** Small files or editing: DOM. Huge files read once: SAX.
7. **XML versus JSON.** The same three records are 223 bytes in XML and 131 bytes in JSON (41 percent smaller); gzip reduces the gap to 119 against 98 bytes (Figure 5.6).
8. **Where each fits.** JSON is lighter and maps directly to JavaScript objects, so it dominates web APIs. XML offers comments, namespaces, schemas and mixed text-and-tags content, so it dominates documents and configuration.

```xml
<xsl:template match="/students">
  <table>
    <xsl:for-each select="student">
      <tr><td><xsl:value-of select="name"/></td><td><xsl:value-of select="marks"/></td></tr>
    </xsl:for-each>
    <tr><td>Total</td><td><xsl:value-of select="sum(student/marks)"/></td></tr>
  </table>
</xsl:template>
```

| Point | XML | JSON |
|---|---|---|
| Size (3 records) | 223 B | 131 B |
| Comments | Yes | No |
| Schema and namespaces | XSD, namespaces | JSON Schema only |
| Typical use | Documents, configuration, feeds | Web APIs |

*Conclusion.* XML separates data from presentation: CSS or XSLT show it, DOM or SAX let programs read it. JSON is lighter for APIs, but XML remains the better choice when documents need structure, validation and namespaces.
