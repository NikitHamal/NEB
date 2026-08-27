(function(window){
"use strict";

var I = window.LazyIcons;

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function(c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

var STRENGTHS = {
  strong: { label: "High Priority", color: "var(--green)" },
  medium: { label: "Moderate", color: "var(--orange)" },
  low: { label: "Optional", color: "var(--ink-3)" }
};

var SAMPLE_RECORDS = [
  { id: "1", title: "Physics Grade 12 - Mechanics", category: "Core Subject", status: "strong", author: "NEB Curriculum", note: "Final term exam focus" },
  { id: "2", title: "Chemistry Grade 12 - Organic", category: "Core Subject", status: "strong", author: "Dr. K. Sharma", note: "Reaction mechanisms & isomers" },
  { id: "3", title: "Mathematics Grade 12 - Calculus", category: "Core Subject", status: "medium", author: "NEB Faculty", note: "Integration techniques" },
  { id: "4", title: "Computer Science - DBMS & SQL", category: "Elective", status: "strong", author: "S. Bhattarai", note: "ER diagrams & Normalization" },
  { id: "5", title: "English Grade 12 - Model Questions", category: "Compulsory", status: "medium", author: "CDC Nepal", note: "Free writing & Grammar" },
  { id: "6", title: "Nepali Grade 12 - Sahitya & Vyakaran", category: "Compulsory", status: "low", author: "CDC Nepal", note: "Essay and letter drafting" }
];

function RecordsTable(container, opts) {
  opts = opts || {};
  this.container = container;
  this.records = opts.records || SAMPLE_RECORDS;
  this.filterText = "";
  this.sortKey = "title";
  this.init();
}

RecordsTable.prototype.init = function() {
  var self = this;
  this.container.innerHTML = "";

  var shell = document.createElement("div");
  shell.style.display = "flex";
  shell.style.flexDirection = "column";
  shell.style.flex = "1";
  shell.style.minHeight = "0";
  shell.style.height = "100%";
  shell.style.background = "var(--surface)";

  // Toolbar
  var tb = document.createElement("div");
  tb.style.display = "flex";
  tb.style.alignItems = "center";
  tb.style.justifyContent = "space-between";
  tb.style.padding = "8px 12px";
  tb.style.borderBottom = "1px solid var(--line)";
  tb.style.gap = "8px";

  var left = document.createElement("div");
  left.style.display = "flex";
  left.style.alignItems = "center";
  left.style.gap = "8px";

  var searchInp = document.createElement("input");
  searchInp.type = "text";
  searchInp.placeholder = "Filter records…";
  searchInp.style.padding = "4px 8px";
  searchInp.style.borderRadius = "var(--radius-control)";
  searchInp.style.background = "var(--field)";
  searchInp.style.border = "1px solid var(--line)";
  searchInp.style.fontSize = "12.5px";
  searchInp.style.color = "var(--ink)";
  searchInp.addEventListener("input", function() {
    self.filterText = searchInp.value.toLowerCase();
    self.renderRows();
  });
  left.appendChild(searchInp);

  var addBtn = document.createElement("button");
  addBtn.className = "lz-btn-pill primary";
  addBtn.style.height = "26px";
  addBtn.style.fontSize = "12px";
  addBtn.innerHTML = I.plus({ size: 12 }) + "<span>Add Record</span>";
  addBtn.addEventListener("click", function() {
    var title = prompt("Enter study resource title:");
    if (title) {
      self.records.unshift({
        id: String(Date.now()),
        title: title,
        category: "Study Material",
        status: "strong",
        author: "User",
        note: "Added to workspace"
      });
      self.renderRows();
    }
  });
  left.appendChild(addBtn);

  tb.appendChild(left);
  shell.appendChild(tb);

  // Table wrapper
  var scroll = document.createElement("div");
  scroll.style.flex = "1";
  scroll.style.overflow = "auto";

  this.table = document.createElement("table");
  this.table.style.width = "100%";
  this.table.style.borderCollapse = "collapse";
  this.table.style.fontSize = "13px";
  this.table.style.textAlign = "left";

  this.table.innerHTML = '<thead style="position:sticky;top:0;background:var(--page);border-bottom:1px solid var(--line-strong);">' +
    '<tr>' +
    '<th style="padding:8px 12px;font-weight:600;color:var(--ink-2);width:35%;">Title / Topic</th>' +
    '<th style="padding:8px 12px;font-weight:600;color:var(--ink-2);width:20%;">Category</th>' +
    '<th style="padding:8px 12px;font-weight:600;color:var(--ink-2);width:20%;">Priority</th>' +
    '<th style="padding:8px 12px;font-weight:600;color:var(--ink-2);width:25%;">Notes / Context</th>' +
    '</tr>' +
    '</thead>' +
    '<tbody></tbody>';

  this.tbody = this.table.querySelector("tbody");
  scroll.appendChild(this.table);
  shell.appendChild(scroll);

  this.container.appendChild(shell);
  this.renderRows();
};

RecordsTable.prototype.renderRows = function() {
  var self = this;
  this.tbody.innerHTML = "";

  var filtered = this.records.filter(function(r) {
    if (!self.filterText) return true;
    return r.title.toLowerCase().indexOf(self.filterText) !== -1 ||
      r.category.toLowerCase().indexOf(self.filterText) !== -1 ||
      (r.note && r.note.toLowerCase().indexOf(self.filterText) !== -1);
  });

  if (!filtered.length) {
    var emptyTr = document.createElement("tr");
    emptyTr.innerHTML = '<td colspan="4" style="padding:24px;text-align:center;color:var(--ink-3);">No matching records found.</td>';
    this.tbody.appendChild(emptyTr);
    return;
  }

  filtered.forEach(function(r) {
    var tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid var(--line)";
    tr.style.transition = "background-color 100ms ease";
    tr.addEventListener("mouseenter", function(){ tr.style.background = "var(--hover)"; });
    tr.addEventListener("mouseleave", function(){ tr.style.background = "transparent"; });

    var st = STRENGTHS[r.status] || STRENGTHS.medium;

    tr.innerHTML = '<td style="padding:9px 12px;font-weight:500;color:var(--ink);">' + esc(r.title) + '</td>' +
      '<td style="padding:9px 12px;"><span style="display:inline-block;padding:2px 8px;border-radius:var(--radius-chip);background:var(--inset);border:1px solid var(--line);font-size:11.5px;color:var(--ink-2);">' + esc(r.category) + '</span></td>' +
      '<td style="padding:9px 12px;"><span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--ink);"><span style="width:7px;height:7px;border-radius:50%;background:' + st.color + ';"></span>' + esc(st.label) + '</span></td>' +
      '<td style="padding:9px 12px;color:var(--ink-2);font-size:12.5px;">' + esc(r.note || "") + '</td>';

    self.tbody.appendChild(tr);
  });
};

window.LazyRecordsTable = RecordsTable;
})(window);
