---
subject: Mobile Programming
grade: BCA Semester 6
unit: 3
title: User Interface - Layouts, RecyclerView and Fragments
hours: 8
area: BCA 352 · Mobile Programming · Unit 3
---

A screen full of text and buttons is easy; a screen showing a ten-thousand-row transaction history that scrolls smoothly on a low-end phone is where UI programming gets interesting. This unit covers how Android describes interfaces (the View system and XML layouts, with Jetpack Compose as the modern declarative alternative), how resources give you Nepali strings and density-specific assets for free, and how **RecyclerView** keeps a huge list fast by creating only the rows that are visible. It then explains **Fragments**, and verifies the efficiency numbers and the **DiffUtil** list-update computation with code.

::: key What this unit gives you
- Views, ViewGroups and the common layouts; resources and localisation (Nepali).
- RecyclerView: adapter, ViewHolder, recycling arithmetic, and a diff computation as DiffUtil does.
- Fragments, their lifecycle and navigation; event handling; Jetpack Compose in outline.
:::

## 3.1 Views and layouts

Everything on screen is a **View** (a rectangle that draws itself and handles input): `TextView`, `EditText`, `Button`, `ImageView`, `CheckBox`. A **ViewGroup** is a view that contains and positions other views; the **view hierarchy** is a tree with a ViewGroup at the root. The system performs **measure** (how big does each view want to be), **layout** (where does it go) and **draw** passes on the tree; deep hierarchies make these passes slow.

| Layout | Positions children | Use |
|---|---|---|
| **LinearLayout** | In a single row or column, with weights | Simple stacks, forms |
| **ConstraintLayout** | By constraints to siblings, parent and guidelines | Flat, responsive screens (the default) |
| **FrameLayout** | Stacked, one on top of another | A fragment container, overlays |
| **RelativeLayout** | Relative to siblings (older) | Legacy |
| **GridLayout / Grid in RecyclerView** | In rows and columns | Galleries |
| **CoordinatorLayout / ScrollView** | Scrolling and behaviours | Collapsing toolbars, long forms |

Not executed (needs the Android SDK): a ConstraintLayout fragment of a login screen.

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent" android:layout_height="match_parent"
    android:padding="16dp">
    <EditText android:id="@+id/phone" android:layout_width="0dp"
        android:layout_height="wrap_content" android:hint="@string/phone_hint"
        android:inputType="phone"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />
    <Button android:id="@+id/send" android:layout_width="wrap_content"
        android:layout_height="48dp" android:text="@string/send_otp"
        app:layout_constraintTop_toBottomOf="@id/phone"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

`match_parent` fills the parent, `wrap_content` fits the content, and `0dp` in ConstraintLayout means "as the constraints dictate". The layout is **inflated** into view objects, and code reaches them through **View Binding** (`binding.send.setOnClickListener { ... }`) instead of `findViewById`.

### Resources and localisation

Everything that is not code goes in `res/`, and the system picks the right alternative using **qualifiers** in the folder name: `values-ne/strings.xml` (Nepali), `values-night/` (dark mode), `layout-sw600dp/` (tablets), `drawable-xxhdpi/`, `layout-land/`. Never hard-code visible text: use `@string/send_otp` and provide `values/strings.xml` (English) and `values-ne/strings.xml` (Nepali) so that a phone set to Nepali shows Nepali without code changes. Use **plurals** and format arguments rather than concatenation, and support right-to-left only if needed. Colours and sizes go in `values/colors.xml` and `dimens.xml`; **themes and styles** (Material Design components) give a consistent look. Check that the font renders Devanagari conjuncts correctly, and that text with `sp` units scales with the user's setting.

## 3.2 Handling events and input

Views report events through **listeners**: `setOnClickListener`, `addTextChangedListener`, touch and gesture detectors. Heavy work in a click handler freezes the screen, because all UI code runs on the single **main (UI) thread**, and **if the main thread is blocked for about five seconds the system shows an "Application Not Responding" dialog**. Network and disk calls therefore run on background threads (Unit 5), and results are posted back to the main thread. Validate input (`inputType`, regex, length), show errors in `TextInputLayout`, hide the keyboard when done, and give feedback quickly with a progress indicator, a `Snackbar` or a `Toast` for brief messages.

## 3.3 RecyclerView

A list of 10,000 items cannot have 10,000 views in memory. **RecyclerView** creates only enough **ViewHolder** objects to fill the screen plus a small margin, and as a row scrolls off the top its holder is *recycled*: rebound to the data of a row about to appear at the bottom. Its parts:

- **Adapter:** supplies the data and creates holders (`onCreateViewHolder`), binds data to a holder (`onBindViewHolder`) and reports the item count.
- **ViewHolder:** caches references to the row's views, avoiding repeated lookups.
- **LayoutManager:** positions rows (`LinearLayoutManager`, `GridLayoutManager`, `StaggeredGridLayoutManager`).
- **ItemAnimator and DiffUtil:** animate changes and compute them efficiently.

Not executed (needs the Android SDK): a minimal adapter.

```kotlin
class NoteAdapter(private var items: List<Note>) :
    RecyclerView.Adapter<NoteAdapter.VH>() {
    class VH(val row: RowNoteBinding) : RecyclerView.ViewHolder(row.root)
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): VH =
        VH(RowNoteBinding.inflate(LayoutInflater.from(parent.context), parent, false))
    override fun onBindViewHolder(holder: VH, position: Int) {
        holder.row.title.text = items[position].title
    }
    override fun getItemCount() = items.size
}
```

### How much does recycling save?

The phone of Unit 1 is 914.29 dp tall; with rows of 72 dp, about 13 rows are at least partly visible; RecyclerView keeps roughly the visible rows plus a couple of spare ones (15 holders) instead of 10,000. A naive list of 10,000 inflated views would be **667 times** as many view objects, and inflating them would take seconds; recycling makes the cost depend on the *screen size*, not the *list size*. *Each* row should be cheap to bind: no network calls, no big bitmaps decoded on the main thread, flat layouts.

### Updating a list with DiffUtil

When data changes (a new list from the database), calling `notifyDataSetChanged()` redraws everything and loses animations. **DiffUtil** compares the old and new lists and dispatches the *minimum* inserts, removals and moves. It uses Myers' diff algorithm, whose edit script has length (n + m − 2·LCS) for lists of sizes n and m with a longest common subsequence of length LCS. The program computes that edit script for IDs of a note list and checks its size against the LCS formula:

```python
def lcs_table(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                t[i][j] = 1 + t[i + 1][j + 1]
            else:
                t[i][j] = max(t[i + 1][j], t[i][j + 1])
    return t

def diff(a, b):
    t = lcs_table(a, b)
    i = j = 0
    ops = []
    while i < len(a) or j < len(b):
        if i < len(a) and j < len(b) and a[i] == b[j]:
            i += 1
            j += 1
        elif j < len(b) and (i == len(a) or t[i][j + 1] >= t[i + 1][j]):
            ops.append("insert " + b[j] + " at " + str(j))
            j += 1
        else:
            ops.append("remove " + a[i])
            i += 1
    return ops

old = ["n1", "n2", "n3", "n4", "n5"]
new = ["n1", "n3", "n6", "n4", "n5", "n7"]
ops = diff(old, new)
print(ops)
print(len(ops), "operations; formula n + m - 2*LCS =", len(old) + len(new) - 2 * lcs_table(old, new)[0][0])
```
```output
['remove n2', 'insert n6 at 2', 'insert n7 at 5']
3 operations; formula n + m - 2*LCS = 3
```
The list update becomes "remove n2, insert n6, insert n7" with three notifications instead of redrawing eleven rows. In real code you subclass `DiffUtil.ItemCallback` (`areItemsTheSame` compares IDs, `areContentsTheSame` compares fields) and use **`ListAdapter`**, which runs the diff on a background thread.

## 3.4 Fragments

A **Fragment** is a reusable portion of UI with its own lifecycle, hosted by an Activity. They let one activity show several panes (a list and a detail on a tablet) and let screens be swapped without a new activity. Its lifecycle extends the activity's: `onAttach`, `onCreate`, **`onCreateView`** (inflate the layout), `onViewCreated`, `onStart`, `onResume`, `onPause`, `onStop`, **`onDestroyView`** (the view is destroyed but the fragment may live on in the back stack), `onDestroy`, `onDetach`. The key trap: after `onDestroyView`, any reference to the views must be dropped (set the binding to null) or memory leaks. A fragment's view has its own `viewLifecycleOwner`, and flows must be collected in it. Communication: share a **ViewModel** scoped to the activity or use the Fragment Result API; avoid calling the activity directly.

**Navigation.** The **Navigation component** defines a graph of destinations (`nav_graph.xml`), a `NavHostFragment` that shows the current one, and `navController.navigate(R.id.action_list_to_detail, bundle)`; **Safe Args** generates type-safe arguments. Bottom navigation bars, drawers and tabs use the same mechanism. The system's Back button pops the fragment back stack.

## 3.5 Jetpack Compose in outline

**Jetpack Compose** is the modern **declarative** UI toolkit: you write functions that describe the UI for the *current state*, and the framework re-runs them when the state changes (recomposition). Not executed (needs the Android SDK):

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Column(Modifier.padding(16.dp)) {
        Text("Clicks: $count")
        Button(onClick = { count++ }) { Text("Add") }
    }
}
```

There are no XML layouts, no adapters (a `LazyColumn` does the recycling) and no findViewById; state is hoisted into a ViewModel and flows down while events flow up (**unidirectional data flow**). New apps use Compose; the View system remains everywhere in existing code, so both must be understood. The same ideas (state, lists, navigation) appear in SwiftUI and Flutter.

## 3.6 Seeing the interface: tools, trees, lists and panes

A screen is a tree of views, a list is a pool of recycled rows, and a tablet is the same app with a second pane. Each idea is clearer when drawn. The first plate is a real screenshot of Android Studio, the tool in which every layout in this unit is built.

```photo id="bca352/studio" caption="Plate 3.1 Android Studio with a layout open (a screenshot of version 3.1; later versions look similar). (1) The project panel with app/src/main/res, where layouts, strings and drawables live. (2) The XML editor holding a ConstraintLayout. (3) The live preview of the same layout on a phone, updated as the XML changes. (4) The profiler, which graphs CPU, memory and network use while the app runs on an emulator or a real phone." width="100"
mark 0.06 0.62 "1"
mark 0.30 0.52 "2"
mark 0.80 0.52 "3"
mark 0.50 0.17 "4"
key 1 Project panel
key 2 XML editor
key 3 Live preview
key 4 Profiler
```

```svgfig label="3.1" caption="The view tree of the login screen of section 3.1. The ConstraintLayout is the root ViewGroup; the EditText and Button are its children. The system walks this tree three times for every frame: measure (how big do you want to be?), layout (where do you go?) and draw. A flat tree such as this one is cheaper to measure than a deep tree of nested LinearLayouts."
f = Fig(580, 230)
f.box(210, 14, 160, 44, "ConstraintLayout\n(ViewGroup, root)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(80, 110, 140, 44, "EditText\n@+id/phone", fill=MINT, stroke=TEAL, size=10.5)
f.box(360, 110, 140, 44, "Button\n@+id/send", fill=MINT, stroke=TEAL, size=10.5)
f.arrow([(270, 58), (170, 110)], color=NAVY); f.arrow([(310, 58), (410, 110)], color=NAVY)
for i, (t, c) in enumerate([("1 measure", NAVY), ("2 layout", TEAL), ("3 draw", AMBER)]):
    f.box(100 + i * 140, 184, 120, 34, t, fill=SOFT, stroke=c, size=11, bold=True)
    if i < 2: f.arrow([(220 + i * 140, 201), (240 + i * 140, 201)], color=SLATE)
f.text(545, 201, "every\nframe", size=10, color=SLATE, bold=True)
```

```svgfig label="3.2" caption="The login screen to scale on the phone of Unit 1 (411.43 dp wide, density 2.625). The container has 16 dp padding on each side, so the EditText, which is 0 dp wide and constrained to both edges, becomes 411.43 - 32 = 379.43 dp wide (996 px). The Button is 48 dp high (126 px) and is constrained to the end of the parent and to the bottom of the EditText. Constraints, not coordinates, place both views, so the same file works on a 360 dp phone or a 600 dp tablet."
f = Fig(580, 250)
s = 0.55
f.box(20, 10, 411.43 * s, 230, "", fill=SOFT, stroke=SLATE)
f.box(20 + 16 * s, 26, 379.43 * s, 40, "EditText   379.43 dp x wrap_content", fill=BLUE, stroke=NAVY, size=10)
f.box(20 + (411.43 - 16 - 110) * s, 80, 110 * s, 48 * s + 10, "Button 48 dp", fill=MINT, stroke=TEAL, size=9)
f.arrow([(20 + 16 * s, 100), (20 + 16 * s, 70)], color=AMBER, lpos=(60, 90))
f.line(20, 150, 20 + 16 * s, 150, color=RED, sw=2); f.text(20 + 8 * s, 164, "16 dp", size=9, color=RED, bold=True)
f.line(20 + (411.43 - 16) * s, 150, 20 + 411.43 * s, 150, color=RED, sw=2); f.text(20 + (411.43 - 8) * s, 164, "16 dp", size=9, color=RED, bold=True)
f.text(20 + 411.43 * s / 2, 200, "411.43 dp wide = 1080 px", size=10, color=SLATE, bold=True)
f.text(275, 40, "match_parent: fill parent", size=10, color=NAVY, bold=True, anchor="start")
f.text(275, 58, "0dp: as constraints say", size=10, color=TEAL, bold=True, anchor="start")
f.text(275, 76, "wrap_content: fit content", size=10, color=AMBER, bold=True, anchor="start")
f.text(275, 108, "px = dp x 2.625", size=10, color=SLATE, bold=True, anchor="start")
f.text(275, 126, "379.43 dp = 996 px", size=10, color=SLATE, bold=True, anchor="start")
f.text(275, 144, "48 dp = 126 px", size=10, color=SLATE, bold=True, anchor="start")
```

```svgfig label="3.3" caption="RecyclerView recycling on the 914.29 dp screen with 72 dp rows. About 12.7 rows are visible, so 13 rows are at least partly shown and the pool keeps 2 spare holders, 15 in all. When row 1 scrolls off the top, its ViewHolder is rebound to row 14 and placed under row 13 instead of a new view being inflated. A list of 10,000 inflated views would need 667 times as many view objects."
f = Fig(580, 270)
f.box(20, 10, 150, 250, "", fill=SOFT, stroke=SLATE)
for i in range(13):
    y = 10 + i * 19.2
    f.box(24, y + 1, 142, 17, f"row {i + 3}", fill=MINT if 0 < i < 12 else SAND, stroke=TEAL if 0 < i < 12 else AMBER, size=9, r=2)
f.text(95, 270, "visible window", size=9.5, color=SLATE, bold=True)
f.box(230, 10, 110, 34, "Scrap / pool\n2 spare holders", fill=SAND, stroke=AMBER, size=9.5)
f.box(230, 214, 110, 34, "Row 14 appears\n(needs a holder)", fill=BLUE, stroke=NAVY, size=9.5)
f.box(230, 112, 110, 34, "Row 1 leaves\n(top)", fill=ROSE, stroke=RED, size=9.5)
f.arrow([(285, 112), (285, 44)], color=RED); f.arrow([(340, 27), (400, 27), (400, 231), (340, 231)], color=TEAL, label="rebind", lpos=(430, 130))
f.text(440, 60, "visible holders: 13", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(440, 80, "pool: +2 = 15", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(440, 100, "10,000 / 15 = 667x", size=10.5, color=RED, bold=True, anchor="start")
```

```svgfig label="3.4" caption="DiffUtil on the lists of section 3.3. The old list has 5 items and the new list 6. The longest common subsequence is n1, n3, n4, n5 (length 4), drawn with straight lines. The remaining items give the edit script remove n2, insert n6 at 2 and insert n7 at 5: n + m - 2 x LCS = 5 + 6 - 8 = 3 operations, instead of redrawing 11 rows."
f = Fig(580, 250)
old = ["n1", "n2", "n3", "n4", "n5"]; new = ["n1", "n3", "n6", "n4", "n5", "n7"]
f.text(90, 14, "old list (5)", size=11, color=NAVY, bold=True); f.text(380, 14, "new list (6)", size=11, color=NAVY, bold=True)
for i, t in enumerate(old):
    c = RED if t == "n2" else TEAL
    f.box(40, 26 + i * 38, 100, 30, t, fill=ROSE if t == "n2" else MINT, stroke=c, size=11.5, bold=True)
for j, t in enumerate(new):
    c = AMBER if t in ("n6", "n7") else TEAL
    f.box(330, 26 + j * 38, 100, 30, t, fill=SAND if t in ("n6", "n7") else MINT, stroke=c, size=11.5, bold=True)
for a, b in [(0, 0), (2, 1), (3, 3), (4, 4)]:
    f.line(140, 41 + a * 38, 330, 41 + b * 38, color=TEAL, sw=1.6)
f.text(150, 84, "removed", size=9.5, color=RED, bold=True, anchor="start")
f.text(450, 102, "insert at 2", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(450, 242, "insert at 5", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(500, 130, "3 operations", size=11, color=NAVY, bold=True)
f.text(500, 148, "not 11 redraws", size=10, color=SLATE)
```

```photogrid label="3.2" cols="3" ratio="1.0" caption="One app, two layouts. (a) Three foldable phones: the available width can change while the app is open. (b) On a phone (sw below 600 dp) the list and the detail are two separate screens, and Back returns from the detail to the list. (c) On a tablet or an unfolded foldable (sw 600 dp or more) the same two fragments sit side by side, 360 dp for the list and 920 dp for the detail on a 1280 dp window."
@ photo id="bca352/foldable" cap="Foldable phones"
fit 1.0
focus 0.5 0.5
@ svg cap="Phone: one pane at a time"
f = Fig(300, 286)
f.box(10, 30, 110, 190, "", fill=SOFT, stroke=SLATE, r=10)
f.box(18, 46, 94, 158, "List\nfrag.", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.box(180, 30, 110, 190, "", fill=SOFT, stroke=SLATE, r=10)
f.box(188, 46, 94, 158, "Detail\nfrag.", fill=MINT, stroke=TEAL, size=14, bold=True)
f.arrow([(122, 110), (178, 110)], color=AMBER, label="tap", lpos=(150, 98), lsize=13)
f.arrow([(178, 160), (122, 160)], color=SLATE, label="Back", lpos=(150, 186), lsize=13)
f.text(150, 252, "411 dp wide", size=14, color=NAVY, bold=True)
f.text(150, 274, "folder layout/", size=13, color=SLATE, bold=True)
@ svg cap="Tablet: two panes together"
f = Fig(300, 286)
f.box(6, 50, 288, 150, "", fill=SOFT, stroke=SLATE, r=8)
f.box(14, 58, 84, 134, "List\n360", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.box(104, 58, 182, 134, "Detail\n920 dp", fill=MINT, stroke=TEAL, size=14, bold=True)
f.text(150, 226, "1280 dp wide", size=14, color=NAVY, bold=True)
f.text(150, 248, "layout-sw600dp/", size=13, color=SLATE, bold=True)
f.text(150, 270, "360 + 920 = 1280", size=13, color=TEAL, bold=True)
```

```svgfig label="3.5" caption="Compose in one picture: unidirectional data flow. State flows down from the ViewModel into the composable functions, which describe the UI for that state; the user's tap becomes an event that flows up to the ViewModel; the state changes and Compose recomposes only the functions that read the changed value."
f = Fig(580, 200)
f.box(20, 70, 130, 56, "ViewModel\n(holds state)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(225, 70, 130, 56, "Composable\nfunctions", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(430, 70, 130, 56, "Screen +\nuser taps", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(150, 88), (225, 88)], color=NAVY, label="state down", lpos=(188, 80))
f.arrow([(355, 88), (430, 88)], color=TEAL, label="draws", lpos=(392, 80))
f.arrow([(495, 126), (495, 170), (85, 170), (85, 126)], color=AMBER, label="event up (onClick)", lpos=(290, 162))
f.text(290, 30, "recomposition: only readers of the changed state re-run", size=10.5, color=SLATE, bold=True)
```

### 3.6.1 Eight rules for screens that work on every phone

1. **Size in dp and text in sp.** A 48 dp button is about 9 mm on every screen, and 16 sp text grows when the user raises the font size in settings. Fixed pixel sizes break on dense screens. This is vital for a Nepali newspaper or exam-result app, because many readers enlarge the text.
2. **Prefer a flat ConstraintLayout.** One ConstraintLayout can replace three or four nested LinearLayouts. The system measures a shallow tree faster, so the screen opens quickly on a 2 GB phone. Deeply nested layouts are a common reason for slow screens in budget devices.
3. **Never hard-code text.** All visible text goes in strings.xml, with a values-ne/strings.xml for Nepali. The system chooses the language the user has set. A Nagarik App-style service for citizens needs both languages from the first release, not as an afterthought.
4. **Keep the main thread free.** Every click handler and layout pass runs on the single UI thread, and more than about five seconds of blocking produces the "App not responding" dialog. Move file, database and network work to background threads or coroutines. A loan calculator that downloads an interest table inside a click handler freezes the screen.
5. **Use RecyclerView or LazyColumn for lists.** They create only about fifteen rows for a screen even when the list holds ten thousand, as in Figure 3.3. This saves memory and keeps scrolling smooth. A list of ward offices, bus routes or students never needs an inflated view for every entry.
6. **Update lists with DiffUtil.** Calling notifyDataSetChanged redraws every row and loses the animation. DiffUtil works out the three changes of Figure 3.4 and notifies only those. A chat or price list that refreshes every few seconds stays steady.
7. **Plan for width classes.** Make the layout adapt at 600 dp and use fragments so that a list and a detail can be shown side by side (Plate 3.2). Foldables and tablets are growing in the market and a school may give students tablets. One code base, two layouts, and no change to the logic.
8. **Make targets reachable and readable.** Keep tap targets at 48 dp or more, give images content descriptions for TalkBack, and keep colour contrast high for sunlight. A farmer using a market-price app outdoors needs large, high-contrast text. These checks cost almost nothing at design time.

## Chapter summary

- UIs are trees of Views in ViewGroups; ConstraintLayout gives flat, responsive screens; resource qualifiers supply Nepali text, dark mode, tablets and density-specific assets.
- All UI work runs on the main thread; blocking it risks an ANR, so I/O goes to background threads.
- RecyclerView recycles a handful of ViewHolders (15 here instead of 10,000); DiffUtil computes the minimal list updates (n + m − 2·LCS operations).
- Fragments are lifecycle-aware UI pieces; drop view references in onDestroyView; Navigation manages destinations.
- Compose describes UI as functions of state.

## Practice

1. Differentiate View and ViewGroup and name three layout managers.
2. Why use dp and sp and `@string` references instead of fixed pixels and literal text?
3. Where would you put Nepali strings and how does the system choose them?
4. What is an ANR and how do you avoid it?
5. How does RecyclerView save memory?
6. How many operations does DiffUtil need to turn [a, b, c, d] into [a, c, d, e]?
7. Why is `notifyDataSetChanged()` inefficient?
8. Name the Fragment callback where the layout is inflated and the one where you must release the binding.
9. What is a ViewModel shared between two fragments used for?
10. State the main difference between the View system and Compose.

::: note Answers and worked solutions
**1.** A View draws itself and handles input; a ViewGroup contains and positions views. Layouts: LinearLayout, ConstraintLayout, FrameLayout.
**2.** dp keeps physical size the same across densities and sp respects the user's font setting; `@string` allows translation and reuse.
**3.** In `res/values-ne/strings.xml`; the system selects it when the device language is Nepali, falling back to `values/`.
**4.** "Application Not Responding" appears when the main thread is blocked for about five seconds; avoid it by running network, database and heavy computation off the main thread.
**5.** It keeps only visible rows plus a few spares as ViewHolders and rebinds them to new data as rows scroll.
**6.** LCS = [a, c, d] = 3; operations = 4 + 4 − 2·3 = **2** (remove b, insert e).
**7.** It redraws and rebinds every item and cancels animations even if only one item changed.
**8.** `onCreateView` (inflate); `onDestroyView` (null the binding).
**9.** Sharing data and events (for example the selected item) between the fragments.
**10.** The View system describes UI in XML and mutates view objects; Compose declares UI as functions of state and re-runs them when state changes.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how RecyclerView displays a long list efficiently. For a 914.29 dp screen with 72 dp rows, how many holders are needed?**

*Introduction.* A list of 10,000 rows cannot have 10,000 views in memory, so RecyclerView recycles a small pool of views (section 3.3, Figure 3.3).

1. **Adapter.** It supplies the data, creates holders in `onCreateViewHolder`, binds data in `onBindViewHolder` and reports `getItemCount`.
2. **ViewHolder.** It keeps references to the views of one row, so `findViewById` is not repeated.
3. **LayoutManager.** It positions the rows (Linear, Grid or Staggered) and decides when a row has left the screen.
4. **Recycling.** When a row scrolls off the top, its holder goes to a pool and is rebound to the data of the row that is about to appear at the bottom. No new view is inflated.
5. **Arithmetic.** Rows visible = 914.29 ÷ 72 = 12.70, so **13** rows are at least partly visible; with 2 spare holders the pool is **15**. A naive list would hold 10,000 views, which is 10,000 ÷ 15 = **667** times as many.

*Example.* A list of every ward office in Nepal can be scrolled smoothly even on a phone with 2 GB of RAM.

*Conclusion.* RecyclerView keeps memory and start-up time independent of the list length, and DiffUtil adds minimal updates on top.

**Q2 (5 marks). Compare LinearLayout and ConstraintLayout. In the login screen of Figure 3.2, find the width of the EditText.**

*Introduction.* A layout is a ViewGroup that measures and positions its children (section 3.1).

1. **LinearLayout.** Places children in one row or column, optionally sharing space by weights. It is simple and good for forms, but complex screens need nesting.
2. **ConstraintLayout.** Places each child by constraints to the parent, siblings or guidelines, so a complex screen stays flat. It is the default in Android Studio and works well with the layout editor (Plate 3.1).
3. **Cost.** Every nested level adds a measure and layout pass for each frame; a flat tree is cheaper.
4. **Calculation.** The screen is 1080 px at density 2.625, which is 411.43 dp. With padding 16 dp on both sides the EditText (width 0 dp, constrained to both edges) is 411.43 − 2 × 16 = **379.43 dp**, which is 379.43 × 2.625 = **996 px**.

| Point | LinearLayout | ConstraintLayout |
|---|---|---|
| Placement | Row or column | Constraints |
| Nesting | Often deep | Usually flat |
| Best for | Simple stacks | Responsive screens |

*Conclusion.* Use LinearLayout for simple stacks and ConstraintLayout for everything else; the EditText is 379.43 dp (996 px) wide.

**Q3 (10 marks). What is a Fragment? Explain its lifecycle and how fragments and the Navigation component are used to build phone and tablet layouts.**

*Introduction.* A Fragment is a reusable portion of user interface with its own lifecycle, hosted by an Activity (section 3.4). It lets one activity show several panes and lets screens be swapped without starting a new activity.

1. **Reuse.** The same list fragment is used on a phone and on a tablet.
2. **Own lifecycle.** It has onAttach, onCreate, onCreateView (inflate the layout), onViewCreated, onStart, onResume, and the reverse onPause, onStop, onDestroyView, onDestroy and onDetach.
3. **View lifecycle.** The view can be destroyed while the fragment object lives (for example on the back stack), so references to views must be cleared in onDestroyView.
4. **Fragment manager.** The activity's FragmentManager adds, replaces and removes fragments in transactions, which can be placed on the back stack.
5. **Navigation component.** A navigation graph (`nav_graph.xml`) lists destinations and actions; a NavHostFragment shows the current one, and `navController.navigate(R.id.action_list_to_detail, bundle)` moves between them. Safe Args generates type-safe arguments.
6. **Phone layout.** Under 600 dp the list and detail are separate destinations and Back returns to the list (Plate 3.2b).
7. **Tablet layout.** In `layout-sw600dp/` the two fragments are shown together: 360 dp for the list and 1280 − 360 = 920 dp for the detail (Plate 3.2c).
8. **Shared data.** Fragments of one screen share a ViewModel scoped to the activity, so selecting an item in the list updates the detail.

| Point | Activity | Fragment |
|---|---|---|
| Declared in | Manifest | Code or XML inside an activity |
| Lifecycle | 7 callbacks | Longer, plus view lifecycle |
| Reuse | One screen | Many hosts |
| Typical role | Entry point, container | A pane or screen |

*Conclusion.* Fragments plus Navigation give one code base for all screen sizes, with a single activity hosting many screens, which is the recommended structure for modern apps.

**Q4 (10 marks). Compare the View-based (XML) UI toolkit with Jetpack Compose.**

*Introduction.* The View system describes a screen in XML and changes it by calling methods on objects, whereas Jetpack Compose is declarative: you write functions that describe the UI for the current state (section 3.5, Figure 3.5).

1. **Definition of UI.** XML layouts are inflated into View objects; Compose uses Kotlin functions marked `@Composable`.
2. **Updating.** In the View system the code finds a view and calls `setText`; in Compose the state changes and the function runs again (recomposition).
3. **Lists.** RecyclerView needs an adapter, holders and DiffUtil; a `LazyColumn` does the recycling with a few lines.
4. **State.** Compose encourages unidirectional data flow: state flows down from the ViewModel and events flow up.
5. **Code volume.** A counter screen needs an XML file and a Kotlin class in the View system but about ten lines in Compose.
6. **Theming and reuse.** Compose composables are ordinary functions that accept parameters, so components are reused without custom views.
7. **Interoperability.** Both can live in one app: ComposeView embeds Compose in XML and AndroidView embeds a view in Compose.
8. **Maturity.** The View system exists in almost all older code and libraries, so both must be understood.

| Point | View system (XML) | Jetpack Compose |
|---|---|---|
| Style | Imperative | Declarative |
| UI files | XML + Kotlin | Kotlin only |
| Lists | RecyclerView + adapter | LazyColumn |
| Update | Call setters | Change state |
| Preview | Layout editor | @Preview functions |

*Conclusion.* New apps should use Compose for less code and fewer state bugs, while existing apps keep XML where it works and migrate screen by screen.
