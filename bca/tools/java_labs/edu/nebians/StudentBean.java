package edu.nebians;
import java.beans.*;
import java.io.Serializable;
public class StudentBean implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name = "unknown";
    private int marks;
    private int[] scores = new int[3];
    private final PropertyChangeSupport changes = new PropertyChangeSupport(this);
    private final VetoableChangeSupport vetoes = new VetoableChangeSupport(this);
    public StudentBean() {
        vetoes.addVetoableChangeListener(e -> { int v = (Integer) e.getNewValue(); if (v < 0 || v > 100) throw new PropertyVetoException("marks must be 0..100, got " + v, e); });
    }
    public String getName() { return name; }
    public void setName(String n) { String o = name; name = n; changes.firePropertyChange("name", o, n); }
    public int getMarks() { return marks; }
    public void setMarks(int m) throws PropertyVetoException { vetoes.fireVetoableChange("marks", marks, m); int o = marks; marks = m; changes.firePropertyChange("marks", o, m); }
    public boolean isPassed() { return marks >= 40; }
    public int[] getScores() { return scores.clone(); }
    public void setScores(int[] s) { scores = s.clone(); }
    public int getScores(int i) { return scores[i]; }
    public void setScores(int i, int v) { int o = scores[i]; scores[i] = v; changes.fireIndexedPropertyChange("scores", i, o, v); }
    public void addPropertyChangeListener(PropertyChangeListener l) { changes.addPropertyChangeListener(l); }
    public void removePropertyChangeListener(PropertyChangeListener l) { changes.removePropertyChangeListener(l); }
    public int listenerCount() { return changes.getPropertyChangeListeners().length; }
    public int vetoCount() { return vetoes.getVetoableChangeListeners().length; }
}
