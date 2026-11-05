---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 2
title: GUI Programming: Swing, Layouts and Event Handling
hours: 10
area: BCA 303 · Advanced Java Programming · Unit 2
---

A console program asks questions in a fixed order; a graphical program waits, and the user decides what happens next: clicking, typing, choosing from a menu. That reversal of control is the whole idea of GUI programming: you build a tree of components, register **listeners** for the events you care about, and hand control to an **event loop**. Swing, part of the JDK since 1998, is still the standard desktop toolkit taught in Java courses and it is what this unit uses. Because the build machine has no display, the programs here exercise components, models, layouts and events *headlessly* (they run for real); the one program that opens a window is compiled but not run.

::: key What this unit gives you
- AWT and Swing: containers, components, look and feel.
- Layout managers: flow, border, grid, box, grid-bag.
- The delegation event model: sources, listeners, adapters, lambdas.
- Models (MVC): list, table, button models; the event dispatch thread; dialogs and menus.
- JavaFX in outline.
:::

## 2.1 AWT and Swing

The **AWT** (Abstract Window Toolkit) wraps the operating system's native widgets, so a button looks and behaves like the platform's. **Swing** (`javax.swing`) draws its own components in Java ("lightweight"), so they look the same everywhere, have a **pluggable look and feel**, and offer far more components (tables, trees, tabbed panes). Swing still uses the AWT event classes and layout managers. Swing class names start with **J**: `JFrame`, `JButton`, `JLabel`.

| Swing class | Role |
|---|---|
| `JFrame` | top-level window with title bar and border |
| `JDialog`, `JOptionPane` | dialog windows; standard message and input boxes |
| `JPanel` | plain container for grouping components |
| `JLabel`, `JButton`, `JTextField`, `JPasswordField`, `JTextArea` | label, push button, one-line text, password, multi-line text |
| `JCheckBox`, `JRadioButton` (with `ButtonGroup`), `JComboBox`, `JList` | choices |
| `JTable`, `JTree`, `JScrollPane`, `JTabbedPane`, `JSplitPane` | data views and containers |
| `JMenuBar`, `JMenu`, `JMenuItem`, `JToolBar` | menus and toolbars |

Every visible object is a **component** (`java.awt.Component`); a **container** holds components; a **top-level container** (frame, dialog) owns a **content pane** to which you add things. The component tree is displayed by the **AWT event dispatch thread (EDT)**, the single thread on which all Swing work must happen.

## 2.2 Building a window

A typical program creates the frame, adds components, packs it and shows it, all inside `SwingUtilities.invokeLater` so it runs on the EDT. `pack()` sizes the window to fit the components' preferred sizes; `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)` ends the program when the window closes. The program below is a temperature converter; it is compiled by the build but, being a window, not run on this display-less machine.

```java
// compile-only
import javax.swing.*;
import java.awt.*;
public class TempConverter {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Celsius to Fahrenheit");
            JTextField input = new JTextField(8);
            JLabel result = new JLabel("Result: ");
            JButton convert = new JButton("Convert");
            convert.addActionListener(e -> {
                try {
                    double c = Double.parseDouble(input.getText().trim());
                    result.setText(String.format("Result: %.1f F", c * 9 / 5 + 32));
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "Enter a number", "Error", JOptionPane.ERROR_MESSAGE);
                }
            });
            JPanel p = new JPanel(new FlowLayout());
            p.add(new JLabel("Celsius:")); p.add(input); p.add(convert); p.add(result);
            frame.setContentPane(p);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}
```
Typing 100 and clicking Convert shows "Result: 212.0 F". Long-running work (a download, a database query) must **not** run on the EDT or the window freezes; use a `SwingWorker` (work in `doInBackground()`, update the display in `done()`) or an executor with `invokeLater` for the update.

## 2.3 Layout managers

A **layout manager** decides the size and position of the components in a container, so the interface adapts to window size, fonts and platforms. Avoid absolute positioning (`setLayout(null)`).

| Manager | Rule | Default for |
|---|---|---|
| `FlowLayout` | left to right, wrapping to a new row | `JPanel` |
| `BorderLayout` | five regions: NORTH, SOUTH, EAST, WEST, CENTER; CENTER takes the leftover space | content pane of `JFrame` |
| `GridLayout` | equal-size cells in rows × columns | none |
| `BoxLayout` | one row or column, honours alignment and preferred sizes | `Box` |
| `GridBagLayout` | grid with cells of different sizes and weights, set by `GridBagConstraints` | none |
| `CardLayout` | stack of panels, one visible at a time | wizards, tabs |

Nested panels with different managers build any design: a `BorderLayout` frame whose CENTER holds a `JTable` and whose SOUTH holds a `FlowLayout` panel of buttons.

```java
import javax.swing.*;
import java.awt.*;
public class LayoutDemo {
    public static void main(String[] args) {
        JPanel grid = new JPanel(new GridLayout(1, 3, 0, 0)); grid.setSize(300, 100);
        for (String s : new String[]{"A", "B", "C"}) grid.add(new JButton(s));
        grid.doLayout();
        for (Component c : grid.getComponents()) System.out.println(((JButton) c).getText() + " -> " + c.getBounds());
        JPanel border = new JPanel(new BorderLayout()); border.setSize(400, 300);
        String[] names = {"North", "South", "West", "East", "Center"};
        String[] where = {BorderLayout.NORTH, BorderLayout.SOUTH, BorderLayout.WEST, BorderLayout.EAST, BorderLayout.CENTER};
        Dimension[] pref = {new Dimension(10, 40), new Dimension(10, 30), new Dimension(50, 10), new Dimension(70, 10), new Dimension(10, 10)};
        for (int i = 0; i < names.length; i++) {
            JButton b = new JButton(names[i]); b.setPreferredSize(pref[i]); border.add(b, where[i]);
        }
        border.doLayout();
        for (Component c : border.getComponents()) System.out.println(((JButton) c).getText() + " -> " + c.getBounds());
    }
}
```
```output
A -> java.awt.Rectangle[x=0,y=0,width=100,height=100]
B -> java.awt.Rectangle[x=100,y=0,width=100,height=100]
C -> java.awt.Rectangle[x=200,y=0,width=100,height=100]
North -> java.awt.Rectangle[x=0,y=0,width=400,height=40]
South -> java.awt.Rectangle[x=0,y=270,width=400,height=30]
West -> java.awt.Rectangle[x=0,y=40,width=50,height=230]
East -> java.awt.Rectangle[x=330,y=40,width=70,height=230]
Center -> java.awt.Rectangle[x=50,y=40,width=280,height=230]
```
The grid divides 300 × 100 into three equal cells. In the border layout the NORTH and SOUTH regions keep their preferred height (40 and 30) and span the full width, WEST and EAST keep their preferred width (50 and 70) and fill the height between, and CENTER receives everything that is left (400 − 50 − 70 = 280 wide, 300 − 40 − 30 = 230 tall).

## 2.4 The delegation event model

An **event** is an object describing something that happened. The model has three roles:

- the **event source** (a button, text field, window) generates events;
- the **event object** (`ActionEvent`, `MouseEvent`, `KeyEvent`, …) carries the details;
- the **event listener** is an object implementing a listener interface, **registered** with the source (`addActionListener`). The source calls the listener's method when the event occurs.

This is the observer pattern: the source does not know what the listeners do, and one listener can serve several sources.

| Event class | Listener interface (methods) | Typical source |
|---|---|---|
| `ActionEvent` | `ActionListener` (`actionPerformed`) | button click, Enter in a text field, menu item |
| `ItemEvent` | `ItemListener` (`itemStateChanged`) | check box, radio button, combo box |
| `MouseEvent` | `MouseListener` (pressed, released, clicked, entered, exited), `MouseMotionListener` (moved, dragged) | any component |
| `KeyEvent` | `KeyListener` (keyPressed, keyReleased, keyTyped) | focused component |
| `WindowEvent` | `WindowListener` (opened, closing, closed, iconified, …) | frame |
| `TextEvent`/`DocumentEvent` | `DocumentListener` | text component's document |
| `ListSelectionEvent` | `ListSelectionListener` | list, table |
| `TableModelEvent` | `TableModelListener` | table model |

**Adapter classes** (`MouseAdapter`, `KeyAdapter`, `WindowAdapter`) implement all methods of a multi-method listener as empty methods, so you override only the one you need. Ways to write a listener: a **named class**, an **inner class** (can use the enclosing object's fields), an **anonymous class**, or, for single-method interfaces such as `ActionListener`, a **lambda** `e -> ...`.

```java
import javax.swing.*;
import java.awt.event.*;
import java.util.*;
public class EventDemo {
    public static void main(String[] args) {
        JButton b = new JButton("Add"); JTextField f = new JTextField("5"); JLabel out = new JLabel("0");
        int[] total = {0}; List<String> log = new ArrayList<>();
        b.addActionListener(e -> { total[0] += Integer.parseInt(f.getText()); out.setText("Total = " + total[0]); log.add(e.getActionCommand()); });
        b.addActionListener(new ActionListener() { public void actionPerformed(ActionEvent e) { log.add("second listener"); } });
        b.doClick(); f.setText("10"); b.doClick(); b.doClick();
        System.out.println(out.getText());
        System.out.println(log);
        JComboBox<String> box = new JComboBox<>(new String[]{"BCA", "BBA", "BIT"});
        box.addItemListener(e -> { if (e.getStateChange() == ItemEvent.SELECTED) System.out.println("selected " + e.getItem()); });
        box.setSelectedIndex(2);
        JCheckBox cb = new JCheckBox("Agree");
        cb.addItemListener(e -> System.out.println("checkbox selected=" + (e.getStateChange() == ItemEvent.SELECTED)));
        cb.doClick(); cb.doClick();
        DefaultListModel<String> model = new DefaultListModel<>();
        model.addElement("Java"); model.addElement("Swing"); model.add(0, "Advanced");
        System.out.println("list model: " + model + " size " + model.size() + ", element 1 = " + model.getElementAt(1));
    }
}
```
```output
Total = 25
[second listener, Add, second listener, Add, second listener, Add]
selected BIT
checkbox selected=true
checkbox selected=false
list model: [Advanced, Java, Swing] size 3, element 1 = Java
```
`doClick()` simulates a user click, so the buttons and their listeners are exercised without a display. The two listeners on one button are both called, in the order they were added (an action command defaults to the button text). The combo box fires a SELECTED item event when the selection changes, and the check box fires one each time it toggles.

## 2.5 Models and the MVC architecture

Swing separates **what is shown** from **how it is stored**: the **model** holds the data (`ListModel`, `TableModel`, `ButtonModel`, `Document`, `TreeModel`), the **view** (a `JList`, `JTable`) draws it and the **controller** (listeners) changes it. When the model changes it fires an event and every view updates itself. This is why two tables can share one model, and why you update a table by changing its model, never the component.

```java
import javax.swing.table.*;
public class TableModelDemo {
    public static void main(String[] args) {
        DefaultTableModel m = new DefaultTableModel(new Object[]{"Name", "Marks"}, 0);
        m.addTableModelListener(e -> System.out.println("event type=" + e.getType() + " rows " + e.getFirstRow() + ".." + e.getLastRow()));
        m.addRow(new Object[]{"Ram", 72});
        m.addRow(new Object[]{"Sita", 91});
        m.addRow(new Object[]{"Hari", 64});
        m.setValueAt(80, 2, 1);
        double sum = 0;
        for (int r = 0; r < m.getRowCount(); r++) sum += (Integer) m.getValueAt(r, 1);
        System.out.printf("rows=%d average=%.2f%n", m.getRowCount(), sum / m.getRowCount());
        m.removeRow(0);
        System.out.println("after delete: " + m.getRowCount() + " rows, first = " + m.getValueAt(0, 0));
    }
}
```
```output
event type=1 rows 0..0
event type=1 rows 1..1
event type=1 rows 2..2
event type=0 rows 2..2
rows=3 average=81.00
event type=-1 rows 0..0
after delete: 2 rows, first = Sita
```
The event types are `TableModelEvent.INSERT` = 1, `UPDATE` = 0 and `DELETE` = −1. A `JTable(model)` wrapped in a `JScrollPane` would redraw by itself after each of these events. For your own data classes extend `AbstractTableModel` and implement `getRowCount`, `getColumnCount` and `getValueAt`.

## 2.6 Dialogs, menus and other details

- **`JOptionPane`**: `showMessageDialog` (information), `showConfirmDialog` (yes/no), `showInputDialog` (one text value). **`JFileChooser`** and **`JColorChooser`** are ready-made dialogs.
- **Menus**: a `JMenuBar` holds `JMenu`s that hold `JMenuItem`s with their own `ActionListener`s; accelerators (`KeyStroke`) and mnemonics add keyboard shortcuts.
- **Painting**: override `paintComponent(Graphics g)` in a `JPanel` and call `super.paintComponent(g)` first; draw with `g.drawLine`, `fillRect`, `drawString`; call `repaint()` to request a redraw (never call `paintComponent` yourself).
- **Mouse and key input**: add a `MouseListener` or `KeyListener`; use `getX()`, `getY()`, `getKeyCode()`.
- **Threads**: only the EDT may touch components; `SwingUtilities.invokeLater(Runnable)` hands work to it.
- **Look and feel**: `UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())` before creating components.

## 2.7 JavaFX in outline

**JavaFX** is the modern replacement for Swing: a scene graph (`Stage` → `Scene` → nodes), layout panes (`HBox`, `VBox`, `BorderPane`, `GridPane`), properties with **binding**, CSS styling, FXML (XML description of the interface) and built-in animation and media. Since Java 11 it is no longer part of the JDK and is added as a separate library (OpenJFX). The same program as Section 2.2 looks like this (the JavaFX library is not installed on the build machine, so this listing is **not compiled** here):

```text
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

public class TempFx extends Application {
    @Override public void start(Stage stage) {
        TextField input = new TextField(); Label result = new Label("Result: "); Button convert = new Button("Convert");
        convert.setOnAction(e -> result.setText(String.format("Result: %.1f F", Double.parseDouble(input.getText()) * 9 / 5 + 32)));
        stage.setScene(new Scene(new HBox(8, new Label("Celsius:"), input, convert, result)));
        stage.setTitle("Celsius to Fahrenheit"); stage.show();
    }
    public static void main(String[] args) { launch(args); }
}
```

The differences you are asked about in examinations: JavaFX uses a scene graph and `Application.start(Stage)` instead of frames and the EDT (it has its own *JavaFX Application Thread*), `setOnAction` instead of `addActionListener`, properties and binding instead of manual synchronisation, CSS and FXML for styling and layout.

## Formula and fact sheet

- Swing top level: `JFrame` + `getContentPane()`; build on the EDT with `SwingUtilities.invokeLater`.
- Layouts: Flow (rows), Border (N/S/E/W/Center), Grid (equal cells), Box, GridBag, Card; `JPanel` default Flow, `JFrame` content pane default Border.
- Event model: source → event object → listener; register with `addXxxListener`; adapters for multi-method listeners.
- Listener styles: named, inner, anonymous, lambda.
- MVC: model fires events; `TableModelEvent` INSERT = 1, UPDATE = 0, DELETE = −1.

## Chapter summary

- Swing components (`J...`) form a tree under a top-level container and are drawn by the event dispatch thread; long work belongs in a `SwingWorker`.
- Layout managers position components; nesting panels with different managers builds any layout.
- In the delegation event model a source notifies registered listeners; adapters and lambdas shorten the code.
- Swing separates models from views (MVC): changing the model updates every view through events.
- JavaFX offers a scene graph, binding, CSS and FXML as a modern alternative.

## Practice

1. Differentiate AWT from Swing. Name five Swing components.
2. Why must Swing code run on the event dispatch thread? How do you start a GUI correctly?
3. Name the default layout managers of `JPanel` and the `JFrame` content pane and describe the five `BorderLayout` regions.
4. In the BorderLayout example, why is the CENTER button 280 × 230?
5. Explain the delegation event model with the roles of source, event and listener.
6. What is an adapter class and when do you use it? Write a `MouseListener` that prints the click position using `MouseAdapter`.
7. Write the code for a button that increments a label counter, using a lambda.
8. What does MVC mean in Swing? Why does a `JTable` update when its model changes?
9. How do you keep a window responsive during a long task?
10. List three differences between Swing and JavaFX.

::: note Answers and worked solutions
**1.** AWT uses native peer components; Swing draws its own lightweight, platform-independent components with pluggable look and feel and a larger set. Examples: `JFrame`, `JButton`, `JLabel`, `JTextField`, `JTable`.
**2.** Swing components are not thread-safe; all access must be on the EDT to avoid corrupted state. Start with `SwingUtilities.invokeLater(() -> createAndShowGui())`.
**3.** `JPanel`: `FlowLayout`; content pane: `BorderLayout`. Regions: NORTH and SOUTH (full width, preferred height), WEST and EAST (preferred width, between north and south), CENTER (all the remaining space).
**4.** The panel is 400 × 300. West and east take 50 and 70 of the width, leaving 280. North and south take 40 and 30 of the height, leaving 230.
**5.** The source (e.g. a button) creates an event object (`ActionEvent`) and calls `actionPerformed` on every listener registered with `addActionListener`; the listener holds the program's reaction.
**6.** An adapter implements all methods of a listener interface with empty bodies. `component.addMouseListener(new MouseAdapter() { public void mouseClicked(MouseEvent e) { System.out.println(e.getX() + "," + e.getY()); } });`
**7.** `int[] n = {0}; button.addActionListener(e -> label.setText("Count: " + (++n[0])));`
**8.** Model–view–controller: the model stores data, the view displays it and the controller (listeners) edits it. The model fires events (`TableModelEvent`) that the table listens to, so it repaints itself.
**9.** Run the work in a `SwingWorker.doInBackground()` or another thread and update the components through `done()` or `invokeLater`.
**10.** JavaFX: scene graph with `Stage` and `Scene`; properties with binding; CSS and FXML styling; `setOnAction` handlers; separate JavaFX Application Thread; and it is a separate library since Java 11.
:::
