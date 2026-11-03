---
subject: Mobile Programming
grade: BCA Semester 6
unit: 4
title: Data Storage - Preferences, Files, SQLite and Room
hours: 7
area: BCA 352 · Mobile Programming · Unit 4
---

An app that forgets everything when it is closed is a toy. Phones lose power, processes are killed and users expect their notes, settings and half-filled forms to be there tomorrow. Android offers several storage mechanisms, each suited to a size and shape of data: key–value preferences, files, and a full relational database (**SQLite**, wrapped by the **Room** library). Because Android's SQLite is the same engine that Python ships with, the SQL in this unit was *executed*, and the query results below are real output; its transaction behaviour, the heart of reliable storage, is demonstrated with a deliberate failure.

::: key What this unit gives you
- Choosing storage: preferences/DataStore, files, SQLite/Room, content providers, cloud.
- SQL on Android: schema, queries, indexes, transactions (executed), and the Room entity–DAO–database layers.
- Business-logic testing outside the emulator: a Java loan calculator run on the JVM.
- Security of stored data.
:::

## 4.1 Choosing a storage mechanism

| Mechanism | Holds | Good for | Notes |
|---|---|---|---|
| **SharedPreferences / DataStore** | Small key–value pairs | Settings, flags, last login name | DataStore (Preferences or Proto) is the modern, asynchronous replacement |
| **Internal storage** (files) | Private files in the app's directory | Caches, downloaded JSON, drafts | Deleted on uninstall; no permission needed |
| **External/shared storage** | Media and documents | Photos, exports, downloads | Scoped storage: use MediaStore or the Storage Access Framework |
| **SQLite via Room** | Structured relational data | Notes, transactions, offline copies of server data | Queries, indexes, relations |
| **Content provider** | Data shared with other apps | Contacts, shared documents | URI-based interface |
| **Cloud (REST, Firebase)** | Server-side data | Sync across devices, backup | Needs network; cache locally |

The rule of thumb: *settings* in DataStore, *the user's records* in Room, *big blobs* as files, and always treat the server as the source of truth with the local database as an offline cache.

## 4.2 Preferences and files

Not executed (needs the Android SDK): saving and reading a setting with DataStore, and writing a private file.

```kotlin
val Context.dataStore by preferencesDataStore("settings")
val DARK = booleanPreferencesKey("dark_mode")

suspend fun saveDark(ctx: Context, on: Boolean) =
    ctx.dataStore.edit { it[DARK] = on }
fun darkFlow(ctx: Context) = ctx.dataStore.data.map { it[DARK] ?: false }

File(context.filesDir, "draft.txt").writeText("Dear ward office...")
```

Preferences are *not* a database: do not store lists of records. Never keep passwords or tokens in plain preferences; use the **Android Keystore** with `EncryptedSharedPreferences`/encrypted DataStore. Since Android 10, **scoped storage** limits an app to its own directories plus media it created; pickers return URIs rather than paths.

## 4.3 SQLite and SQL

**SQLite** is a small, serverless, transactional SQL database stored in one file per database; Android includes it. A table is created with typed columns and constraints, rows are added with INSERT, read with SELECT, changed with UPDATE and removed with DELETE. **Indexes** speed up lookups by a column at the cost of space and write time; **transactions** group statements so that all succeed or none do (atomicity).

The following program runs on SQLite exactly as an Android app would; amounts are whole rupees.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount INTEGER NOT NULL,
    day TEXT NOT NULL
);
CREATE INDEX idx_expense_day ON expense(day);
""")
rows = [("Food", 450, "2082-01-03"), ("Transport", 120, "2082-01-03"),
        ("Food", 300, "2082-01-04"), ("Rent", 8000, "2082-01-05"),
        ("Transport", 200, "2082-01-05"), ("Food", 700, "2082-02-01")]
db.executemany("INSERT INTO expense(category, amount, day) VALUES (?, ?, ?)", rows)
db.commit()
print(db.execute("SELECT category, SUM(amount) FROM expense GROUP BY category ORDER BY category").fetchall())
print(db.execute("SELECT substr(day, 1, 7) AS month, COUNT(*), SUM(amount) FROM expense GROUP BY month ORDER BY month").fetchall())
try:
    with db:
        db.execute("UPDATE expense SET amount = amount - 100 WHERE id = 1")
        db.execute("INSERT INTO expense(category, amount, day) VALUES (NULL, 5, '2082-02-02')")
except sqlite3.IntegrityError as e:
    print("rolled back:", e)
print(db.execute("SELECT amount FROM expense WHERE id = 1").fetchone())
```
```output
[('Food', 1450), ('Rent', 8000), ('Transport', 320)]
[('2082-01', 5, 9070), ('2082-02', 1, 700)]
rolled back: NOT NULL constraint failed: expense.category
(450,)
```
The `?` placeholders are **parameter binding**: never build SQL by concatenating user input, which allows **SQL injection**. The first query groups by category (Food 450 + 300 + 700 = 1450; Transport 120 + 200 = 320; Rent 8000). The second groups by month using the first seven characters of the date. Note the `db.commit()` after the inserts: *without it* the later rollback would also have discarded the six uncommitted inserted rows (an earlier draft of this program printed `None` for exactly that reason, caught when the output was inspected). In the last step the first UPDATE succeeded, but the second statement violated `NOT NULL`, so the transaction was **rolled back** and the amount of row 1 is still 450: the half-finished change never became visible, which is the property that keeps a bank-style app consistent after a crash.

## 4.4 Room

**Room** is the Jetpack library that maps Kotlin classes to SQLite and checks queries at compile time. It has three kinds of component:

- **Entity:** a class annotated `@Entity` that defines a table.
- **DAO (data access object):** an interface annotated `@Dao` whose methods carry `@Insert`, `@Query`, `@Update`, `@Delete`.
- **Database:** an abstract class annotated `@Database` listing entities and the version, from which Room builds the implementation.

Not executed (needs the Android SDK, Room and KSP): the same `expense` table as above.

```kotlin
@Entity(tableName = "expense", indices = [Index("day")])
data class Expense(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val category: String,
    val amount: Int,
    val day: String
)

@Dao
interface ExpenseDao {
    @Insert suspend fun add(e: Expense)
    @Query("SELECT category, SUM(amount) AS total FROM expense GROUP BY category")
    fun totals(): Flow<List<CategoryTotal>>
}

@Database(entities = [Expense::class], version = 1)
abstract class AppDb : RoomDatabase() { abstract fun expenses(): ExpenseDao }
```

Room refuses to run queries on the main thread (use `suspend` functions or `Flow`), and a `Flow` return type re-emits whenever the table changes, so the UI (via a ViewModel) updates itself. When the schema changes you raise the **version** and supply a **Migration** (the SQL that upgrades old data) — shipping a new version without one crashes or wipes users' data. Export the schema JSON and test migrations. The **repository pattern** hides whether data comes from Room or the network from the rest of the app.

## 4.5 Testing business logic off the device

Logic that does not touch Android classes can be unit-tested on a plain JVM in seconds, without an emulator. The Java program below, a loan EMI calculator and the first three rows of its amortisation schedule, is such logic: the formula EMI = P·r·(1 + r)ⁿ / ((1 + r)ⁿ − 1) with monthly rate r. It was compiled and run on a JDK.

```java
public class Emi {
    static double emi(double principal, double annualPct, int months) {
        double r = annualPct / 12 / 100;
        double f = Math.pow(1 + r, months);
        return principal * r * f / (f - 1);
    }

    public static void main(String[] args) {
        double e = emi(500000, 12, 24);
        System.out.printf("EMI = %.2f%n", e);
        double balance = 500000;
        double r = 0.01;
        for (int m = 1; m <= 3; m++) {
            double interest = balance * r;
            double principalPart = e - interest;
            balance -= principalPart;
            System.out.printf("Month %d: interest %.2f principal %.2f balance %.2f%n",
                    m, interest, principalPart, balance);
        }
    }
}
```
```output
EMI = 23536.74
Month 1: interest 5000.00 principal 18536.74 balance 481463.26
Month 2: interest 4814.63 principal 18722.10 balance 462741.16
Month 3: interest 4627.41 principal 18909.32 balance 443831.84
```
The checker computes the same schedule independently in Python. Good structure follows: ViewModel and repository classes hold the logic, Android classes stay thin, and **instrumented tests** (on a device) cover the UI and Room.

## 4.6 Security of stored data

Files in the app's private directory are protected by the sandbox, but a **rooted** phone or a backup can expose them. Encrypt sensitive records (SQLCipher or Keystore-backed keys), keep secrets such as API keys out of the APK (they can be extracted: put them on a server), disable auto-backup for sensitive data (`android:allowBackup`), clear caches on logout and never log personal data. Request only the storage access you need; scoped storage exists to protect users.

## 4.7 Seeing where data lives: flash, files, tables and keys

Data on a phone is stored in flash memory, organised by the operating system into private folders, and queried by SQLite as tables. The plate below starts with the physical memory, and the figures that follow draw the storage areas, the results of the SQL of section 4.3, the effect of an index, a rolled-back transaction, the layers of Room and the protection of keys.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Flash memory in three forms. (a) microSD cards of 2 GB, 4 GB and 8 GB, the removable storage of many Nepali phones, where photos and downloads go (shared storage). (b) An NVMe solid-state drive; the internal storage of a phone is the same kind of NAND flash soldered to the main board as eMMC or UFS. (c) A USB flash drive with its controller and NAND chip visible. In all three the data survives power-off, but every cell wears out after a limited number of writes."
@ photo id="bca352/microsd" cap="microSD cards"
fit 1.0
focus 0.5 0.5
call 0.30 0.92 0.30 0.55 "2 GB"
@ photo id="bca101/nvme" cap="NVMe flash drive"
fit 1.0
focus 0.5 0.5
@ photo id="bca101/pendrive" cap="USB flash drive"
fit 1.0
focus 0.5 0.5
```

```svgfig label="4.1" caption="Where an app's data lives. Internal storage is private: /data/data/<package> holds the app's files, its databases and its preferences, and no other app can read it. Shared storage (photos, downloads) is reached through MediaStore or the Storage Access Framework. A memory card is shared storage too. The server is the source of truth, and the local database is an offline copy."
f = Fig(580, 250)
f.box(10, 10, 360, 232, "", fill=SOFT, stroke=SLATE)
f.text(190, 28, "Phone flash memory", size=11, color=SLATE, bold=True)
f.box(22, 40, 160, 190, "", fill=MINT, stroke=TEAL)
f.text(102, 58, "Internal (private)", size=10.5, color=TEAL, bold=True)
for i, t in enumerate(["filesDir / cache", "databases/ (Room)", "shared_prefs / DataStore", "no permission needed", "deleted on uninstall"]):
    f.box(32, 70 + i * 31, 140, 25, t, fill="#ffffff", stroke=TEAL, size=9.5)
f.box(198, 40, 160, 120, "", fill=BLUE, stroke=NAVY)
f.text(278, 58, "Shared storage", size=10.5, color=NAVY, bold=True)
for i, t in enumerate(["Photos, video, music", "Downloads, documents", "MediaStore / SAF"]):
    f.box(208, 70 + i * 28, 140, 22, t, fill="#ffffff", stroke=NAVY, size=9.5)
f.box(198, 172, 160, 58, "microSD card\n(shared, removable)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(420, 70, 150, 100, "Server / cloud\nsource of truth\nREST, Firebase", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(372, 120), (420, 120)], color=RED, both=True)
f.text(396, 108, "sync", size=10, color=RED, bold=True)
f.text(495, 195, "local DB = offline copy", size=9.5, color=SLATE, bold=True)
```

```svgfig label="4.2" caption="The result of the two queries of section 4.3 on the six expense rows (amounts in rupees, total 9,770). By category: Food 1,450 (14.8 per cent), Rent 8,000 (81.9 per cent), Transport 320 (3.3 per cent). By month: 2082-01 has 5 rows and 9,070; 2082-02 has 1 row and 700. A GROUP BY query turns raw rows into the totals that a chart in the app displays."
f = Fig(580, 230)
f.text(150, 16, "SUM(amount) GROUP BY category", size=10.5, color=NAVY, bold=True)
for i, (n, v, c) in enumerate([("Food", 1450, TEAL), ("Rent", 8000, RED), ("Transport", 320, AMBER)]):
    y = 34 + i * 38
    f.text(10, y + 18, n, size=10.5, color=c, bold=True, anchor="start")
    w = v / 8000 * 190
    f.box(80, y + 2, w, 28, "", fill=BLUE, stroke=c, r=3)
    f.text(80 + w + 8, y + 18, f"{v:,}", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(440, 16, "per month (SUM, rows)", size=10.5, color=NAVY, bold=True)
for i, (n, v, k, c) in enumerate([("2082-01", 9070, 5, NAVY), ("2082-02", 700, 1, TEAL)]):
    y = 34 + i * 38
    f.text(340, y + 18, n, size=10.5, color=c, bold=True, anchor="start")
    w = v / 9070 * 110
    f.box(400, y + 2, w, 28, "", fill=BLUE, stroke=c, r=3)
    f.text(400 + w + 8, y + 18, f"{v:,} ({k})", size=10, color=SLATE, bold=True, anchor="start")
f.text(290, 170, "total = 1,450 + 8,000 + 320 = 9,770 = 9,070 + 700", size=11, color=AMBER, bold=True)
f.text(290, 196, "Food 14.8 %   Rent 81.9 %   Transport 3.3 %", size=10.5, color=SLATE, bold=True)
```

```svgfig label="4.3" caption="What an index saves. The query WHERE day = '2082-01-05' on the 6-row table without an index reads all 6 rows (full scan) to find the 2 matches, Rent 8,000 and Transport 200 (sum 8,200). With the index idx_expense_day the database walks the index to the matching entries and reads only those 2 rows. On a table of a million rows the scan reads a million rows, while the index reads about 20 index levels and the matches."
f = Fig(580, 250)
rows = [("Food", "01-03"), ("Transport", "01-03"), ("Food", "01-04"), ("Rent", "01-05"), ("Transport", "01-05"), ("Food", "02-01")]
f.text(120, 14, "Full scan: 6 rows read", size=11, color=RED, bold=True)
f.text(440, 14, "With index: 2 rows read", size=11, color=TEAL, bold=True)
for i, (n, d) in enumerate(rows):
    hit = d == "01-05"
    f.box(20, 26 + i * 34, 200, 28, f"{n}   2082-{d}", fill=SAND if hit else ROSE, stroke=AMBER if hit else RED, size=10.5)
    f.box(340, 26 + i * 34, 200, 28, f"{n}   2082-{d}", fill=MINT if hit else SOFT, stroke=TEAL if hit else "#cbd5e1", size=10.5, color=SLATE if not hit else TEAL)
f.arrow([(290, 40 + 3 * 34), (338, 40 + 3 * 34)], color=TEAL, sw=1.8)
f.arrow([(290, 40 + 4 * 34), (338, 40 + 4 * 34)], color=TEAL, sw=1.8)
f.box(236, 120, 50, 60, "index\nday", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.text(290, 240, "matches: Rent 8,000 + Transport 200 = 8,200", size=10.5, color=NAVY, bold=True)
```

```svgfig label="4.4" caption="A transaction is all or nothing. Inside one transaction the first statement lowers the amount of row 1 from 450 to 350 and succeeds; the second statement inserts a row with category NULL and fails the NOT NULL constraint. The database rolls back both statements, so row 1 is still 450, as the program output shows. Without the transaction the first change would stay while the second failed, leaving inconsistent data."
f = Fig(580, 170)
S = [("BEGIN", BLUE, NAVY), ("UPDATE\n450 -> 350", MINT, TEAL), ("INSERT\ncategory NULL", ROSE, RED), ("ROLLBACK", SAND, AMBER), ("Row 1 = 450", MINT, TEAL)]
for i, (t, fl, st) in enumerate(S):
    x = 10 + i * 114
    f.box(x, 40, 98, 50, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 98, 65), (x + 114, 65)], color=SLATE)
f.text(450, 112, "fails: NOT NULL constraint", size=9.5, color=RED, bold=True)
f.text(290, 30, "one transaction", size=10.5, color=NAVY, bold=True)
f.text(290, 150, "atomic: both statements are undone, nothing is half-written", size=10.5, color=AMBER, bold=True)
```

```svgfig label="4.5" caption="The layers of an app that uses Room. The Entity defines the table, the DAO holds the SQL, the Database class ties them together and creates the SQLite file. A Flow returned by the DAO emits a new list whenever the table changes; the ViewModel collects it and the screen redraws itself. Queries run off the main thread, and Room checks the SQL at compile time."
f = Fig(580, 200)
L = [("Screen\n(Activity / Compose)", SAND, AMBER), ("ViewModel", BLUE, NAVY), ("DAO\n@Query SQL", MINT, TEAL), ("Room Database\n+ Entity", BLUE, NAVY), ("SQLite file\nexpense.db", ROSE, RED)]
for i, (t, fl, st) in enumerate(L):
    x = 10 + i * 114
    f.box(x, 60, 100, 56, t, fill=fl, stroke=st, size=10, bold=True)
    if i < 4:
        f.arrow([(x + 114, 80), (x + 100, 80)], color=TEAL)
        f.arrow([(x + 100, 98), (x + 114, 98)], color=SLATE)
f.text(290, 30, "Flow of changes goes left (new list); calls go right (insert, query)", size=10.5, color=SLATE, bold=True)
f.text(290, 150, "suspend / Flow: never on the main thread", size=10.5, color=AMBER, bold=True)
f.text(290, 172, "compile-time SQL check, migration when version changes", size=10, color=NAVY)
```

```photogrid label="4.2" cols="2" ratio="1.05" caption="Keeping secrets out of reach. (a) A Trusted Platform Module chip on a circuit board, the PC counterpart of the secure hardware (a trusted execution environment or a secure element) that holds Android Keystore keys. (b) The path of a secret: the app asks Keystore to encrypt; the key is generated and used inside secure hardware and never leaves it; only the ciphertext reaches DataStore or a file."
@ photo id="bca401/tpm" cap="TPM security chip"
fit 1.05
focus 0.5 0.5
@ svg cap="Android Keystore path"
f = Fig(300, 286)
for i, (t, fl, st) in enumerate([("App\nasks to encrypt", SAND, AMBER), ("Android Keystore\nAPI", BLUE, NAVY), ("Secure hardware\nkey never leaves", ROSE, RED), ("Ciphertext in\nDataStore / file", MINT, TEAL)]):
    y = 10 + i * 68
    f.box(40, y, 220, 48, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 3: f.arrow([(150, y + 48), (150, y + 68)], color=SLATE)
f.text(150, 282, "plaintext password never stored", size=9.5, color=NAVY, bold=True)
```

### 4.7.1 Eight rules for storing data on a phone

1. **Choose the lightest store that fits.** A dark-mode flag belongs in DataStore, a list of orders in Room, and a downloaded PDF in a file. Using a database for one setting adds code, and using preferences for a list becomes a slow tangle. An app for a cooperative's members can use all three, each for its own job.
2. **Treat the server as the source of truth.** The local database is an offline copy that makes the screen open instantly and work without signal. When the connection returns, the app syncs and replaces stale rows. This is how a bank statement shown by a mobile banking app stays readable in a village without data.
3. **Bind parameters, never concatenate SQL.** A `?` placeholder keeps user input as data, so a name such as `x'; DROP TABLE expense; --` does nothing. Room's `@Query` parameters work the same way. SQL injection is as dangerous on a phone as on a web server.
4. **Use transactions for multi-step changes.** A transfer between two accounts or an order with several lines must be written all together or not at all (Figure 4.4). The database rolls back everything when one step fails. This keeps balances correct when the phone loses power half-way.
5. **Add indexes for the columns you search.** An index on the date or the customer id turns a scan of every row into a short lookup (Figure 4.3). Each index slows inserts a little and takes space, so index only the columns that appear in WHERE. A shop app with five years of sales needs this.
6. **Keep the main thread free.** Reading a file or running a query on the UI thread freezes the screen and may cause an ANR. Room refuses to do it, and DataStore is asynchronous for this reason. Use suspend functions or Flow and let the ViewModel hand results to the screen.
7. **Never keep secrets in plain text.** Passwords, tokens and card numbers must not go in ordinary preferences or files. Use the Android Keystore with encrypted preferences so that the key stays in secure hardware (Plate 4.2). A lost phone is common, and the data must stay unreadable.
8. **Plan for migration and limited space.** Raise the database version and write a Migration when the schema changes, or users lose their data on update. Keep caches small, because many phones in Nepal have 16 or 32 GB of storage and users delete heavy apps first. Clean up temporary files and large exports.

## Chapter summary

- Match storage to data: DataStore for settings, files for blobs, Room/SQLite for records, content providers for sharing, a server for the source of truth.
- SQL queries use parameter binding; transactions roll back on failure (the executed example left row 1 at 450).
- Room provides Entity, DAO and Database with compile-time-checked queries, Flow updates and migrations.
- Pure business logic is testable on a JVM (the EMI example); keep Android classes thin.
- Encrypt sensitive data and keep secrets off the device.

## Practice

1. Choose a storage mechanism for each: dark-mode flag, 50,000 transactions, a downloaded PDF.
2. What is parameter binding and what attack does it prevent?
3. What does a transaction guarantee? Explain with the failed update in the example.
4. Write a SQL query for the total amount spent on "Food" in month 2082-01 in the sample table.
5. What are the three Room component types?
6. Why does Room reject queries on the main thread?
7. What is a Room migration and why is it needed?
8. Compute the EMI formula's monthly rate for 9% a year.
9. Why should API keys not be stored in the APK?
10. Why is the repository pattern useful?

::: note Answers and worked solutions
**1.** DataStore; Room database; a file (internal or via MediaStore).
**2.** Values are passed separately from the SQL text with `?` placeholders; it prevents SQL injection.
**3.** All statements succeed or none do; the second statement failed, so the first (a 100 deduction) was undone and row 1 still shows 450.
**4.** `SELECT SUM(amount) FROM expense WHERE category = 'Food' AND day LIKE '2082-01%'` gives 450 + 300 = **750**.
**5.** Entity, DAO, Database.
**6.** Disk access can freeze the UI (ANR); queries must be `suspend` or return `Flow`.
**7.** SQL steps that upgrade an existing database from version n to n + 1; without it the app crashes or loses data after an update.
**8.** 9 / 12 / 100 = **0.0075** per month.
**9.** An APK can be unpacked and the key extracted; keep secrets on a server.
**10.** It hides whether data comes from the database or the network, so the UI and logic do not depend on the source.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Which storage mechanism would you choose for each item: the dark-mode flag, a list of 5,000 expense records, a 3 MB downloaded PDF, a login token and a photo taken for a loan form? Give reasons.**

*Introduction.* The rule of thumb is settings in DataStore, records in Room, large blobs as files, secrets encrypted (section 4.1, Figure 4.1).

1. **Dark-mode flag.** A single boolean is a key–value pair, so DataStore (Preferences) is best. It is asynchronous and survives restarts.
2. **5,000 expense records.** These are structured, searched and summed, so they belong in a Room (SQLite) table with an index on the date column. The totals in Figure 4.2 come from `GROUP BY`.
3. **3 MB PDF.** A large blob is stored as a file in internal storage (filesDir or cache). No permission is needed, and it is deleted on uninstall.
4. **Login token.** A secret must never be stored in plain text. Encrypt it with a key from the Android Keystore and store the ciphertext in encrypted preferences or DataStore (Plate 4.2).
5. **Loan-form photo.** If the user may want it in the gallery, save it to shared storage through MediaStore; if it is only an attachment, keep it private in internal storage and delete it after upload.

| Item | Mechanism |
|---|---|
| Dark flag | DataStore |
| 5,000 records | Room |
| PDF | File in internal storage |
| Token | Keystore + encrypted store |
| Photo | MediaStore or private file |

*Conclusion.* Match the store to the shape, size and sensitivity of the data, and keep the server as the source of truth.

**Q2 (5 marks). Explain a SQLite transaction with the expense example. What is the result of the program in section 4.3 and why?**

*Introduction.* A transaction groups several SQL statements so that they succeed or fail as one unit; SQLite is transactional and ships with Android (section 4.3, Figure 4.4).

1. **Statements.** Inside the transaction, `UPDATE expense SET amount = amount - 100 WHERE id = 1` changes 450 to 350. The second statement, `INSERT ... category NULL`, breaks the `NOT NULL` constraint and raises `IntegrityError`.
2. **Rollback.** Because the exception leaves the `with db:` block, SQLite rolls back both statements. The program prints `rolled back: NOT NULL constraint failed: expense.category`.
3. **Result.** `SELECT amount FROM expense WHERE id = 1` returns **450**, the original value; the UPDATE was undone.
4. **ACID.** This is atomicity. Consistency (constraints), isolation (other readers do not see half-done work) and durability (committed data survive a crash) complete the ACID properties.
5. **Totals.** The earlier query gives Food 1,450, Rent 8,000 and Transport 320, which add up to 9,770; per month the totals are 9,070 and 700, which also add up to 9,770.

*Conclusion.* The transaction protects the data from half-finished changes: the final value is 450, not 350.

**Q3 (10 marks). Explain Room and its components. How does it differ from using raw SQLite? Show the architecture of an app that uses Room.**

*Introduction.* Room is the Jetpack library that maps Kotlin classes to SQLite tables and checks queries at compile time (section 4.4, Figure 4.5).

1. **Entity.** A class annotated `@Entity` defines a table; each property is a column and `@PrimaryKey` marks the key; `indices` add indexes.
2. **DAO.** An interface annotated `@Dao` whose methods carry `@Insert`, `@Query`, `@Update` and `@Delete`. The SQL lives here.
3. **Database.** An abstract class annotated `@Database(entities = [...], version = 1)` from which Room generates the implementation and the SQLite file.
4. **Compile-time checking.** A wrong column name in `@Query` fails the build instead of crashing the app.
5. **Threading.** Room refuses queries on the main thread. DAO methods are `suspend` functions or return a `Flow`.
6. **Observable queries.** A `Flow<List<...>>` emits again whenever the table changes, so the ViewModel and screen update by themselves.
7. **Migrations.** When the schema changes, the version is raised and a `Migration` converts old data; without it users lose data on update.
8. **Parameter binding.** Method parameters become `?` placeholders, which prevents SQL injection.

| Point | Raw SQLite | Room |
|---|---|---|
| SQL checking | At run time | At compile time |
| Boilerplate | Cursors, ContentValues | Generated |
| Main-thread safety | Programmer's job | Enforced |
| Live updates | Manual | Flow |
| Migration | Manual SQL | Migration objects |

*Architecture.* The screen observes the ViewModel, the ViewModel collects the DAO's Flow, the DAO runs SQL against the Room database and SQLite file (Figure 4.5).

*Conclusion.* Room removes boilerplate and whole classes of bugs while keeping the full power of SQL, so it is the standard choice for structured data on Android.

**Q4 (5 marks). A loan of Rs 1,00,000 is repaid in 12 monthly instalments at 12 per cent a year. Find the EMI and explain why such logic should be unit-tested on a plain JVM.**

*Introduction.* The EMI formula of section 4.5 is EMI = P · r · (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1), where r is the monthly rate.

1. **Values.** P = 1,00,000, r = 12 ÷ 12 ÷ 100 = 0.01, n = 12.
2. **Growth factor.** (1.01)¹² = 1.126825.
3. **EMI.** 1,00,000 × 0.01 × 1.126825 ÷ 0.126825 = **Rs 8,884.88**.
4. **Total paid.** 12 × 8,884.88 = Rs 1,06,618.56, so the interest is about Rs 6,618.56.
5. **Why test off the device.** The calculation uses no Android classes, so a JUnit test runs in seconds on a normal computer without an emulator. Tests of such logic can run on every code change and catch a wrong formula before users see a wrong instalment.

*Conclusion.* The EMI is Rs 8,884.88; keeping business logic free of Android classes makes it quickly testable.
