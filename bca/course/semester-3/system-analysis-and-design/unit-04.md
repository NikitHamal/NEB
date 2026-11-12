---
subject: System Analysis and Design
grade: BCA Semester 3
unit: 4
title: Design
hours: 12
area: BCA 204 · System Analysis and Design · Unit 4
---

**Design** turns the requirements into a specification that programmers can build: the data structures (database design), the physical files, the screens and reports users see, and the dialogue between user and system.

::: key What this unit gives you
- Logical database design: relations, normalization, converting E-R diagrams, merging relations.
- Physical design: fields, tables, file organisation, indexes and denormalization.
- Designing forms and reports, assessing usability.
- Designing interfaces and dialogues: interaction methods, devices, graphical environments.
:::

## 4.1 Designing databases

Database design moves from the conceptual E-R model (Unit 3) to **logical design** (relations in the relational model) and then **physical design** (files, indexes). Inputs: the conceptual data model, normalised relations from user views, and volume and usage estimates. Outputs: a **normalised relational schema** and physical file specifications.

### The relational database model

A **relation** is a named, two-dimensional table of data with rows (tuples) and columns (attributes). Properties: each cell is single-valued, each row is unique, rows and columns have no order, and every column holds values of one domain. A **primary key** identifies each row uniquely; a **foreign key** is an attribute (or set) that is the primary key of another relation, linking rows. **Integrity rules:** *entity integrity* (primary key never null), *referential integrity* (a foreign key value must match a primary key value in the referenced relation, or be null), and *domain integrity*.

Relation notation: `STUDENT(student_id, name, dob, program_id)` with the primary key underlined and foreign keys marked; `program_id` references `PROGRAM`.

### Normalization

Normalization removes anomalies by splitting relations according to functional dependencies (the DBMS course covers the theory in detail): **1NF** atomic values and a primary key; **2NF** no partial dependency on part of a composite key; **3NF** no transitive dependency between non-key attributes; BCNF a stronger form. In systems design we normalise the **user views** (screens, reports) and then *merge* the resulting relations.

::: example Worked example: normalising an invoice
User view: `INVOICE(invoice_no, date, customer_id, customer_name, customer_address, {item_no, item_desc, unit_price, qty})`, where braces mean a repeating group.
**1NF:** remove the repeating group: `INVOICE(invoice_no, date, customer_id, customer_name, customer_address)` and `INVOICE_LINE(invoice_no, item_no, item_desc, unit_price, qty)` with key (invoice_no, item_no).
**2NF:** `item_desc` and `unit_price` depend on `item_no` alone, a partial dependency. Split: `ITEM(item_no, item_desc, unit_price)` and `INVOICE_LINE(invoice_no, item_no, qty)`.
**3NF:** in `INVOICE`, `customer_name` and `customer_address` depend on `customer_id`, not on the key `invoice_no` (transitive). Split: `CUSTOMER(customer_id, customer_name, customer_address)` and `INVOICE(invoice_no, date, customer_id)`.
**Final 3NF relations:** CUSTOMER, INVOICE, ITEM, INVOICE_LINE.
:::

### Transforming E-R diagrams into relations

| E-R element | Becomes |
|---|---|
| Entity | a relation; attributes are columns; identifier is the primary key |
| One-to-many relationship | the **primary key of the "one" side is added as a foreign key to the "many" side** |
| Many-to-many relationship or associative entity | a **new relation** whose primary key combines the keys of both sides, plus any relationship attributes |
| One-to-one | foreign key on either side (usually on the optional side), or merge the relations |
| Multivalued attribute | a new relation with the owner's key and the value |
| Unary one-to-many (employee manages employee) | a recursive foreign key (`manager_id` in EMPLOYEE) |
| Unary many-to-many (part contains part) | a new relation with two foreign keys to the same entity |
| Supertype/subtype | a relation for the supertype and one per subtype keyed by the supertype's key |

### Merging relations (view integration)

Relations designed from different user views often overlap and must be merged into one consistent set. Problems to resolve: **synonyms** (two names for the same thing: `cust_no` vs `customer_id`), **homonyms** (one name for different things: `date` meaning order date or ship date) and **transitive dependencies** that appear after merging, which are removed by normalising again. Relations with the same primary key are merged into one, and the union of their attributes is taken.

## 4.2 Physical file and database design

Logical design says *what*; physical design says *how it is stored*. Goals: **fast retrieval**, **efficient use of space**, **data integrity and security**, and ease of **recovery**. Decisions use estimates of data volume and the frequency of each query and update.

### Designing fields

A **field** is the smallest unit of named data. Choose a **data type** (integer, decimal, character, date, boolean, BLOB), a **length** (large enough for realistic values), and a **format**. Techniques:

- **Coding and compression:** store `M`/`F` rather than "Male"/"Female"; use lookup (code) tables.
- **Controlling data integrity:** a **default value**, an **input mask**, a **range or referential check** (marks 0–100, `program_id` must exist), and **null policy** (which fields may be empty; what a missing value means).
- **Handling missing data:** substitute a default, or prompt the user, or allow null and report.

### Designing physical tables and denormalization

A physical table usually corresponds to a 3NF relation, but a designer may deliberately **denormalize**: combine relations or duplicate data to reduce joins. Reasons: the two relations are almost always read together, the duplicated data rarely changes, and read speed matters more than update simplicity. Forms: join two tables into one, store a **derived total** (invoice total) or **repeat an attribute** (customer name in the invoice). Costs: more storage, possible inconsistency and more complex updates. **Partitioning** splits a large table by rows (horizontal, e.g. by year) or columns (vertical) for speed and management.

### File organisations and indexes

| Organisation | How records are stored | Best for | Weakness |
|---|---|---|---|
| **Sequential** | in key order | reports that process all records | slow random access; insertion needs reorganisation |
| **Indexed (ISAM / B-tree)** | an index maps keys to record locations | both direct access and range queries | index storage and maintenance |
| **Hashed** | a hash function computes the record's address from the key | fast direct access by key | no range queries; collisions |

An **index** is a table of key values with pointers to records; a **secondary index** speeds search on non-key fields. Index fields used in `WHERE`, `JOIN` and `ORDER BY`; avoid indexing fields that change constantly or have few distinct values. **Rules of thumb:** put the most selective columns first in composite indexes; use a **clustered** index on the commonly range-scanned column; monitor and revise physical design as usage changes. Choosing a **file's blocking** and the **database architecture** (centralised, client–server, distributed) is also part of physical design.

## 4.3 Designing forms and reports

**Forms** capture input; **reports** present output. Both are the part of the system users judge it by.

| Aspect | Form | Report |
|---|---|---|
| Purpose | collect data | communicate information |
| Typical types | data entry, query, menu | detailed, summary, exception, executive |
| Design focus | accuracy, ease, speed of entry | readability, selection of content |

**General guidelines:**

- **Meaningful titles** and clear headings; **consistent** layout across screens.
- **Logical grouping and flow**: left to right, top to bottom, related fields together, the order matching the source document.
- **Labels** close to fields, aligned; **tab order** follows the flow; required fields marked.
- **Appropriate controls:** radio buttons for 2–5 exclusive options, check boxes for many-of-many, drop-down lists for long lists, text boxes for free input, date pickers for dates.
- **Defaults** and **auto-fill** to cut typing; **validation** with clear messages at entry ("Enter marks between 0 and 100"), not a bare error code.
- **Accurate and timely information**, only what is needed; for reports use totals and subtotals, sorted order, **exception reports** (only the unusual), page numbers and dates.

### Formatting forms and reports

Use the right **text style** (consistent fonts, sizes about 10–12 pt, upper and lower case for sentences, caps for short headings); **colour** sparingly and with contrast, never the only signal; **alignment** (text left, numbers right or decimal-aligned); **white space** to group; **tables and graphs** for comparisons (a bar chart for categories, line chart for trends, pie chart for parts of a whole with few slices); **number formats** with thousand separators and fixed decimals.

### Assessing usability

**Usability** is *effectiveness, efficiency and satisfaction* (ISO 9241): can users complete tasks, how fast and with how many errors, and do they like it. Also **learnability**, **memorability** and **error recovery**. Assess by **usability testing** (observe real users doing tasks, count errors and time), **heuristic evaluation** (experts check against Nielsen's heuristics such as visibility of system status, error prevention, consistency), questionnaires such as the **System Usability Scale (SUS)**, and prototype reviews. Fix problems before coding.

## 4.4 Designing interfaces and dialogues

The **user interface** is how the user and system interact; a **dialogue** is the sequence of interactions to complete a task.

### Interaction methods

| Method | Description | Suited to |
|---|---|---|
| **Command language** | user types commands | experts, scripting (shell) |
| **Menus** | choose from a list (menu bar, pop-up, context, cascading) | occasional users; the most common method |
| **Forms** | fill in blanks | data entry |
| **Object-based / direct manipulation (GUI)** | icons, drag and drop, click | most desktop and mobile users |
| **Natural language / voice** | speak or type sentences | hands-free, accessibility |

**Menu design guidelines:** the wording is clear and parallel; items are grouped logically and in an expected order (frequency or workflow); limit depth (a flat 5–9 items beats five nested levels); indicate the current choice and give a way back/home; support keyboard shortcuts; disable (grey out) unavailable options rather than hiding them.

### Interaction devices

Keyboard, mouse, trackpad, **touch screen** (large targets, gestures), stylus, **voice**, scanners/barcode, cameras (face/fingerprint), and **sensors**. Pick the device to match task, environment and user (a barcode scanner for stock counting, a touch screen for a kiosk).

### Designing interfaces and dialogues in graphical environments

**Graphical user interfaces** are built from standard controls: windows, menus, buttons, text boxes, check boxes, radio buttons, lists, sliders, tabs, icons and dialog boxes (*modal* dialogs demand an answer; *modeless* do not). **Principles:** *consistency* (same action, same result, platform conventions); *feedback* for every action (progress bars, confirmation messages); **user control** (undo, cancel, escape); *error prevention* before error messages; *recognition rather than recall* (show options); **minimal memory load**; *aesthetic* uncluttered design; **accessibility** (keyboard, contrast, resizable text).

**Dialogue design process:** (1) list the tasks and sequence; (2) design the dialogue sequence (a **dialogue diagram** shows each screen or state as a box and each action as an arrow); (3) build a **prototype** or storyboard; (4) test with users; (5) refine. **Help** should be context-sensitive; **error messages** should say what went wrong and how to fix it ("Roll number must be 6 digits", not "Error 7"). Design for the **novice and the expert**: shortcuts for the expert, guidance for the novice.

::: example Worked example: a dialogue for "view result"
Login screen → (valid) Menu → choose *View result* → Select semester (drop-down) → Result screen → *Print* / *Back* / *Log out*. Alternate paths: invalid login → error message and retry (max 3 times then lock); no result published → informative message with a *Back* button. Each arrow is a user action; each box a screen. Drawing this diagram first exposes the missing "no result yet" path before any screen is coded.
:::

## 4.5 Normalisation and screen design, drawn out

Figure 4.1 follows one badly designed table through the three normal forms. The starting table repeats customer and item facts on every row, so a price change or a spelling correction must be made in many places. Each normal form removes one kind of repetition: **1NF** makes every value atomic, **2NF** removes facts that depend on only part of the key, and **3NF** removes facts that depend on a non-key column. The end result is four small tables joined by keys. Figure 4.2 and Plate 4.1 then move from data design to the screen: the same care that keeps tables clean is needed to keep forms and interfaces clear.

```svgfig label="4.1" caption="Normalising ORDER_FORM(order_id, date, cust_id, cust_name, item_id, item_name, price, qty) with key (order_id, item_id). 2NF moves facts that depend on only part of the key; 3NF moves cust_name, which depends on cust_id rather than on the key."
f = Fig(600, 280)
f.box(10, 10, 580, 40, "Unnormalised: ORDER_FORM(order_id, date, cust_id, cust_name, item_id, item_name, price, qty)", fill="#fecaca", stroke=RED, color=NAVY, size=11, bold=True)
f.arrow([(300, 50), (300, 80)], color=SLATE, sw=2, label="2NF: remove partial dependencies", lpos=(440, 66), lsize=10)
f.box(10, 82, 190, 56, "ORDER\norder_id, date, cust_id, cust_name", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(210, 82, 180, 56, "ITEM\nitem_id, item_name, price", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(400, 82, 190, 56, "ORDER_LINE\norder_id, item_id, qty", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.arrow([(105, 138), (105, 178)], color=SLATE, sw=2, label="3NF: remove transitive dependency", lpos=(240, 160), lsize=10)
f.box(10, 180, 150, 50, "ORDER\norder_id, date, cust_id", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(180, 180, 140, 50, "CUSTOMER\ncust_id, cust_name", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(340, 180, 120, 50, "ITEM", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.box(470, 180, 120, 50, "ORDER_LINE", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.text(300, 258, "result: four tables, each fact stored once, joined by order_id, cust_id, item_id", size=11, color=TEAL, bold=True)
```

```photogrid label="4.1" cols="2" ratio="1.2" caption="Interfaces in everyday use in Nepal. (a) An ATM screen and keypad: few choices per screen, large buttons and a fixed order of steps. (b) A smartphone app screen: touch targets, icons and immediate feedback."
@ photo id="bca101/atm-nepal" cap="ATM in Nepal"
fit 1.2
@ photo id="bca101/android" cap="Smartphone interface"
fit 1.2
```

```svgfig label="4.2" caption="Layout of a good data-entry form. Related fields are grouped, labels sit above or beside their boxes, required fields are marked, a drop-down limits Faculty to valid values, the date format is shown, and the primary action is the most visible button."
f = Fig(600, 250)
f.box(60, 10, 480, 230, "", fill="#ffffff", stroke=NAVY)
f.box(60, 10, 480, 30, "Student admission form", fill=NAVY, color="#ffffff", size=12, bold=True)
for i, (lab, y) in enumerate((("Full name *", 54), ("Date of birth *  (YYYY-MM-DD)", 96), ("Faculty *", 138))):
    f.text(80, y, lab, size=11, color=NAVY, bold=True, anchor="start")
    f.box(80, y + 6, 240, 24, "", fill="#f1f5f9", stroke=SLATE)
f.text(300, 150, "v", size=12, color=NAVY, bold=True)
f.box(80, 190, 90, 32, "Save", fill=TEAL, color="#ffffff", size=12, bold=True)
f.box(184, 190, 90, 32, "Cancel", fill="#e2e8f0", stroke=SLATE, color=NAVY, size=12)
f.text(338, 74, "(1) grouped,", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 90, "labelled fields", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 118, "(2) format hint", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 160, "(3) drop-down", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 176, "validates input", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 206, "(4) clear primary", size=10.5, color=RED, bold=True, anchor="start")
f.text(338, 222, "action", size=10.5, color=RED, bold=True, anchor="start")
```

## 4.6 Eight rules for good forms, reports and interfaces

1. **Be consistent.** Use the same layout, terms and colours on every screen. A user who learns one screen of the college system should be able to guess how the next works.
2. **Group related items.** Put name, address and contact fields together, and mark required ones. A grouped form is quicker to fill and has fewer missing values.
3. **Limit what can be typed.** Use drop-down lists, date pickers and check boxes where the set of valid values is known. The faculty field then cannot contain a spelling mistake.
4. **Validate at once.** Check the value when it is entered and say what is wrong in plain words. "Roll number must have 6 digits" is better than "Error 12".
5. **Give feedback.** Show a confirmation after saving, a progress message for long jobs and a clear error when something fails. Users should never wonder whether a payment went through.
6. **Keep reports readable.** Give each report a title, date, page numbers and column headings; align numbers to the right and total them. A mark sheet should be understood at a glance.
7. **Design for the user's skill.** Beginners need guidance and menus; experts want shortcuts. A public service kiosk needs very simple screens, while an accountant prefers keyboard commands.
8. **Make errors forgivable.** Offer undo, confirmation before deleting and safe defaults. A confirmation dialog before deleting a student record saves hours of recovery work.

## 4.7 Transforming ER diagrams into relations, and merging relations

Logical database design has four steps: (1) collect the conceptual ER diagram, (2) **transform** it into relations, (3) **normalise** the relations to third normal form (4.5), and (4) **merge** the relations from different user views into one consistent design.

### The relational model in brief

A **relation** is a two-dimensional table with a name, columns (attributes) and rows (tuples). Properties: each cell holds one atomic value, each row is unique, column order and row order do not matter. The **primary key** uniquely identifies a row; a **foreign key** is an attribute that is the primary key of another relation and links the two. **Entity integrity**: no primary-key part may be null. **Referential integrity**: a foreign key must match an existing primary key value or be null.

### Transformation rules

| ER construct | Becomes | Key points |
|---|---|---|
| Regular entity | one relation | simple attributes become columns; choose an identifier as primary key |
| Composite attribute | only its simple parts | Address becomes street, city, district |
| Multivalued attribute | a new relation | key is the owner key plus the attribute (STUDENT_PHONE(student_id, phone)) |
| Weak entity | a relation | key is the owner key plus the partial identifier |
| 1:N relationship | foreign key on the N side | the key of the *one* side is copied into the *many* side (COURSE key goes into STUDENT) |
| M:N relationship | a new (associative) relation | key is the two foreign keys combined, plus relationship attributes |
| 1:1 relationship | foreign key on either side | place it on the side with total participation to avoid nulls |
| Unary relationship | foreign key to the same table (1:N) or a new relation (M:N) | EMPLOYEE(emp_id, name, manager_id) |
| Ternary relationship | a new relation with three foreign keys | SUPPLY(supplier_id, part_id, project_id, qty) |
| Supertype/subtype | a relation for each, subtype key = supertype key | PERSON(person_id...), STUDENT(person_id, program) |

::: example Worked example: library ER diagram to relations
Entities: MEMBER(member_id, name, phone*) where phone is multivalued; BOOK(book_id, title); PUBLISHER(pub_id, name); relationships: PUBLISHER publishes BOOK (1:N); MEMBER borrows BOOK (M:N, attributes issue_date, due_date).
**Result:**
MEMBER(**member_id**, name)
MEMBER_PHONE(**member_id**, **phone**) with member_id a foreign key.
PUBLISHER(**pub_id**, name)
BOOK(**book_id**, title, pub_id) with pub_id a foreign key (the 1 side's key goes to the N side).
LOAN(**member_id**, **book_id**, **issue_date**, due_date) with member_id and book_id foreign keys; issue_date is included in the key if a member may borrow the same book again later.
Five entities and relationships became five relations, and the M:N relationship needed its own relation.
:::

### Merging relations (view integration)

When the relations designed for different users are combined, the same real-world thing may have been modelled twice. Problems to resolve:

- **Synonyms:** two names for one attribute (EMP_NO and STAFF_ID). Choose one name.
- **Homonyms:** one name for two different attributes (ADDRESS meaning home in one view and office in another). Rename.
- **Transitive dependencies** that appear after merging (a key in one relation determines non-key attributes in another): remove again.
- **Supertype/subtype** relationships that the views reveal: model explicitly.

Steps: list all relations, group those with the same primary key, merge groups into one relation (union of attributes, removing duplicates), re-check normalisation and check referential integrity.

::: example Worked example: merging two views
View 1: STUDENT(student_id, name, program). View 2: STUDENT_RECORD(roll_no, name, phone) where roll_no and student_id are the same identifier (synonym). Merge to STUDENT(student_id, name, program, phone), and record in the data dictionary that roll_no is an alias.
:::

**Likely questions.** (a) Transform a given ER diagram into relations (10). (b) State the rules for converting M:N and multivalued attributes (5). (c) What are synonyms and homonyms? How are they resolved when merging relations (5).

## 4.8 Physical design: fields, tables, indexes and usability

**Physical design** turns logical relations into a storage structure that is fast and safe in a chosen DBMS. Its inputs are the normalised relations, definitions of attributes, the expected volume, response-time needs and the DBMS features. Its goals are **fast access**, **efficient use of space** and **data integrity and security**.

### Designing fields

A **field** is the smallest named unit of stored data. Choose:

1. **Data type:** integer, decimal, character, date or Boolean. Pick the smallest type that safely holds the largest value (a person's age fits in a small integer, a phone number is text because of leading zeros and plus signs).
2. **Length:** allow for growth, but not excess.
3. **Coding and compression:** store codes ("M", "F") instead of long text and decode them when displayed; use lookup tables.
4. **Default value** and whether the field is **required** (null control).
5. **Range or set control** (age between 16 and 60; status from a list).
6. **Referential integrity** (the foreign key must exist).
7. **Handling of missing data:** substitute a default, flag it and report it, or reject the entry.

### Denormalisation

Normalisation reduces redundancy, but it also produces more tables and more joins. **Denormalisation** deliberately combines tables (or duplicates a column) to speed up reading. It is justified when (a) a join is required in nearly every query, (b) the data is read very much more often than updated, and (c) the response time is critical. Cost: more storage, risk of inconsistency, more update logic.

::: example Worked example: when to denormalise
A report shows every order with the customer name, using three joins on a table of 5 million rows and it runs hourly. Copying CUSTOMER_NAME into ORDER_SUMMARY removes one join and cuts the time from 40 seconds to 8 seconds in testing. Because customer names change rarely, the risk of stale data is small and acceptable, and a nightly job refreshes the copy.
:::

### Designing physical tables and files

- **Partitioning:** split a large table horizontally (by year or by branch) or vertically (rarely used columns in another table).
- **File organisation:** sequential (good for batch processing), indexed (fast for random and sequential access) and hashed (fastest for exact-key lookup). Most DBMS use B-tree **indexes**.
- **Indexes** speed up queries on the indexed column, but slow down inserts and updates and use space. Index primary keys, foreign keys and columns used often in WHERE and ORDER BY; do not index columns with very few values or that are frequently updated.
- **Clustering and fill factor** of storage pages, **backup**, **recovery** and **security** (roles, encryption).

### Assessing usability of forms and reports

Usability is how effectively, efficiently and satisfactorily users reach their goals (ISO 9241). Measure it with: **speed** (time to complete a task), **accuracy** (error rate), **learnability** (time to first success), **user satisfaction** (a 1 to 5 survey or the System Usability Scale), and **memorability** after a break. Methods: **heuristic evaluation** (experts check against Nielsen's ten heuristics), **user testing** with five to eight users thinking aloud, and **A/B tests** for production sites.

::: example Worked example: a usability test result
Eight users register a new patient. Mean time is 94 seconds, 3 of 8 enter the date in the wrong format. Fix: show a date picker and an example. Retest: mean 71 seconds and 0 of 8 wrong. A drop of 23 seconds is about 24 percent faster, with error rate from 37.5 percent to 0.
:::

**Likely questions.** (a) Explain the guidelines for designing fields (5). (b) What is denormalisation? When is it justified? (5). (c) How do indexes help? What are their costs? (5). (d) Describe three methods to assess usability (5).

## 4.9 Interaction methods, devices and dialogue design

### Interaction methods

| Method | How it works | Good for | Weakness |
|---|---|---|---|
| **Command language** | user types commands (SQL, shell) | experts, scripting | must be memorised |
| **Menus** | choose from lists (menu bar, drop-down, pop-up) | occasional users | deep menus are slow |
| **Forms** | fill fields on a screen | data entry | can be long |
| **Object-based (GUI)** | click, drag, drop icons | most users | needs a pointing device |
| **Natural language and voice** | speak or type a request | hands-free, accessibility | recognition errors |
| **Touch and gesture** | tap, swipe, pinch | mobile, kiosks | no hover state, fat fingers |

### Interaction devices

Keyboard, mouse, touchpad, touch screen, stylus, **barcode and QR scanner**, **fingerprint reader**, microphone, camera, joystick and **haptic** feedback. Choose by task: a cashier needs a scanner and a numeric keypad, a designer a stylus and large display, a kiosk a robust touch screen. Think about **accessibility**: screen readers, keyboard-only use, enough contrast, large touch targets (about 9 mm).

### Principles of dialogue design

A **dialogue** is the sequence of exchanges between user and system. Good dialogues give: **consistency** (same words and positions everywhere), **feedback** (a message or change after every action), **shortcuts** for experts, **error prevention** (disable impossible choices, confirm destructive actions), **easy reversal** (undo) and **user control** (the user, not the system, leads).

A **dialogue diagram** shows the screens as boxes and the user actions as arrows, so the whole interaction can be checked before programming.

```svgfig label="4.3" caption="Dialogue diagram for a login and billing flow. Boxes are screens, arrows are user actions. Note that every screen has a way back, and a failed login returns to the same screen with an error message."
f = Fig(600, 210)
f.box(10, 80, 110, 50, "Login", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(170, 80, 120, 50, "Main menu", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(350, 20, 120, 50, "New bill", fill="#fde68a", stroke=AMBER, color=NAVY, size=12, bold=True)
f.box(350, 140, 120, 50, "Reports", fill="#fde68a", stroke=AMBER, color=NAVY, size=12, bold=True)
f.box(500, 80, 90, 50, "Print", fill="#fbcfe8", color=NAVY, size=12, bold=True)
f.arrow([(120, 105), (170, 105)], color=NAVY, sw=1.8, label="valid", lpos=(145, 94), lsize=9.5)
f.arrow([(290, 95), (350, 50)], color=NAVY, sw=1.8)
f.arrow([(290, 118), (350, 165)], color=NAVY, sw=1.8)
f.arrow([(470, 45), (545, 80)], color=NAVY, sw=1.8, label="save", lpos=(520, 54), lsize=9.5)
f.arrow([(65, 80), (65, 40), (30, 40), (30, 80)], color=RED, sw=1.5, label="invalid", lpos=(48, 30), lsize=9.5)
f.arrow([(350, 175), (290, 125)], color=SLATE, sw=1.4, dash=True, label="back", lpos=(300, 162), lsize=9)
```

### Designing for graphical environments

Use standard **widgets** with their usual meaning: **radio buttons** for one choice from few, **check boxes** for several choices, **drop-down lists** for one choice from many, **text boxes** for free text, **sliders** for ranges, **date pickers** for dates. Group related fields, align labels, put the primary action button where the eye ends (bottom right) and use colour only as a second signal (never colour alone). Provide **tooltips**, clear error messages ("Phone number must have 10 digits", not "Invalid input") and **progress indicators** for slow operations.

::: example Worked example: choosing the widget
| Field | Choices | Widget |
|---|---|---|
| Gender | 3 options, pick one | radio buttons |
| District | 77 options, pick one | searchable drop-down |
| Interests | 6 options, pick many | check boxes |
| Date of birth | any date | date picker with typing allowed |
| Volume | 0 to 100 | slider |
:::

### Formatting forms and reports

Forms: logical order (top to bottom, left to right), group with headings or boxes, label every field, show format hints, mark required fields, use the same layout as the paper source form when staff transcribe from paper. Reports: title, date and page number, grouped and sorted rows with subtotals, totals at the end, numbers right-aligned and text left-aligned, sensible white space, and units shown in the heading.

**Likely questions.** (a) Compare interaction methods (5). (b) State guidelines for dialogue design (5). (c) Draw a dialogue diagram for ATM withdrawal (5). (d) Which widget would you use for each of these fields and why? (5).

## Formula and fact sheet

- Normalised relations: CUSTOMER, INVOICE, ITEM, INVOICE_LINE (invoice example). Merge relations, resolve synonyms and homonyms.
- E-R to relations: 1:N → foreign key on the many side; M:N → new relation with composite key.
- Physical design: field types, defaults, checks; denormalize only with reason; index fields used in WHERE/JOIN/ORDER BY.
- Usability = effectiveness + efficiency + satisfaction. Interaction methods: command, menu, form, GUI, natural language.

## Chapter summary

- Logical design normalises user views, converts E-R diagrams to relations and merges them.
- Physical design chooses field formats, tables, file organisations and indexes, trading storage and update cost for speed.
- Forms and reports follow consistent, logical, accurate-and-usable guidelines and are assessed with usability testing.
- Interface and dialogue design uses the interaction method suited to the user, consistent GUI controls and clear feedback and error messages.

## Practice

1. Normalise `ORDER(order_no, date, cust_id, cust_name, {product_id, product_name, price, qty})` to 3NF.
2. Convert to relations: Student and Course with an M:N *enrols* relationship carrying `grade`; Department offers Course (1:N).
3. What are synonyms and homonyms in view integration? Give examples.
4. Why would a designer denormalize? State the risk.
5. Compare sequential, indexed and hashed file organisation.
6. List six guidelines for form design.
7. Define usability and name two ways to assess it.
8. Compare menus and command languages as interaction methods.
9. Draw a dialogue diagram for withdrawing cash at an ATM.

::: note Answers and worked solutions
**1.** 1NF: `ORDER(order_no, date, cust_id, cust_name)`, `ORDER_LINE(order_no, product_id, product_name, price, qty)`. 2NF: `PRODUCT(product_id, product_name, price)`, `ORDER_LINE(order_no, product_id, qty)`. 3NF: `CUSTOMER(cust_id, cust_name)`, `ORDER(order_no, date, cust_id)`.
**2.** `DEPARTMENT(dept_id, name)`, `STUDENT(student_id, name, …)`, `COURSE(course_id, title, dept_id)` with `dept_id` a foreign key, and `ENROLMENT(student_id, course_id, grade)` with composite primary key.
**3.** Synonyms: different names for the same attribute (`cust_no`, `customer_id`). Homonyms: one name for different things (`date` for order date and delivery date). Resolve by agreeing one name per meaning.
**4.** To avoid joins and speed reads when two relations are always used together. Risk: duplicated data may become inconsistent and updates cost more.
**5.** Sequential: ordered, good for full scans; indexed: direct and range access via an index; hashed: fastest exact-key access, no range queries.
**6.** Meaningful title; logical grouping; consistent layout; labels near fields; right control types; defaults and validation with clear messages.
**7.** Usability is effectiveness, efficiency and satisfaction. Assess with usability testing with real users and heuristic evaluation (or SUS).
**8.** Menus: easy for novices, recognition-based, slower for experts. Command languages: fast and powerful for experts, hard to learn and remember.
**9.** Insert card → enter PIN (3 tries) → menu → withdraw → choose amount → balance check (insufficient: message and back to amount) → dispense cash → receipt? → return card.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is normalisation? Normalise ORDER_FORM(order_id, date, cust_id, cust_name, item_id, item_name, price, qty) up to third normal form.**

*Introduction.* Normalisation is the process of organising data into tables so that each fact is stored once. It removes redundancy and the insertion, deletion and update anomalies it causes (Figure 4.1).

*Normal forms.*

1. **1NF.** Every column holds one atomic value and there are no repeating groups. ORDER_FORM already satisfies this with the composite key (order_id, item_id).
2. **2NF.** No non-key column depends on only part of the key. Here date, cust_id and cust_name depend only on order_id, and item_name and price depend only on item_id, so the table is split.
3. **3NF.** No non-key column depends on another non-key column. cust_name depends on cust_id, so it moves to its own table.

*Result.*

| Table | Columns | Key |
|---|---|---|
| ORDER | order_id, date, cust_id | order_id |
| CUSTOMER | cust_id, cust_name | cust_id |
| ITEM | item_id, item_name, price | item_id |
| ORDER_LINE | order_id, item_id, qty | (order_id, item_id) |

*Benefit.* A price change is made in one row of ITEM, and a customer's name is corrected in one row of CUSTOMER.

*Conclusion.* Each normal form removes one kind of dependency, and 3NF gives tables that are free of the main update anomalies.

**Q2 (10 marks). Explain the guidelines for designing forms, reports and user interfaces, and describe how a student admission form should be laid out.**

*Introduction.* Input and output design decide whether users can work accurately and quickly. A system with correct logic still fails if its screens confuse people (Plate 4.1, Figure 4.2).

*General guidelines.*

1. **Consistency** in layout, terms and colours.
2. **Grouping** of related fields, with required fields marked.
3. **Restricted input** through drop-down lists, check boxes, date pickers and masks.
4. **Immediate validation** with clear error messages: type, range, format, presence and check-digit tests.
5. **Feedback** on every action, such as confirmation after saving.
6. **Defaults** for common values to reduce typing.
7. **Error recovery** with undo and confirmation before destructive actions.
8. **Accessibility:** readable fonts, enough contrast and large touch targets.

*Reports.* A report needs a title, date, page numbers, column headings, sensible sort order, right-aligned numeric columns with totals, and only the information the reader needs.

*Interface types.* Command line (fast for experts), menus (easy to learn), forms (data entry), graphical or touch interfaces (direct manipulation) and voice (hands-free).

*Admission form layout (Figure 4.2).* The title bar names the form. Fields are grouped in one column with labels above the boxes; required ones carry an asterisk; the date hint shows the format; the **Faculty** field is a drop-down so only valid faculties can be chosen; **Save** is the most visible button and **Cancel** is secondary. After saving, a message shows the new roll number.

| Interface | Strength | Weakness |
|---|---|---|
| Command line | fast, scriptable | hard to learn |
| Menu | easy to learn | slow for experts |
| Form | structured data entry | needs careful design |
| Touch (GUI) | direct and intuitive | needs larger controls |

*Conclusion.* Good design makes the right action obvious and the wrong action hard. Applying these guidelines reduces data-entry errors and training cost.
