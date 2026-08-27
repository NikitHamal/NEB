(function(window){
"use strict";

var I = window.LazyIcons;

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function(c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

var TOOL_LABEL_MAP = {
  "ask_clarification": "Asked clarification",
  "generate_doc": "Drafted document",
  "edit_doc": "Revised document",
  "append_section": "Added section",
  "breakdown": "Task checklist",
  "parallel_subagents": "Parallel subagents",
  "subagent": "Subagent task",
  "synthesis": "Document synthesis",
  "pdf_to_docx": "Convert PDF to Word",
  "pdf_merge": "Merge PDFs",
  "pdf_split": "Split PDF",
  "pdf_extract_pages": "Extract pages",
  "pdf_rotate": "Rotate PDF",
  "pdf_compress": "Compress PDF",
  "pdf_extract_images": "Extract images",
  "images_to_pdf": "Convert images to PDF",
  "word_count": "Count words",
  "pdf_info": "Inspect PDF metadata"
};

function formatToolLabel(raw) {
  if (!raw) return "Action";
  if (TOOL_LABEL_MAP[raw]) return TOOL_LABEL_MAP[raw];
  var s = String(raw).replace(/_/g, " ").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

var Primitives = {
  /* ── Dot Matrix Thinking State with Live Timer ────────── */
  createThinkingState: function(opts) {
    opts = opts || {};
    var variant = opts.variant || "Steps";
    var title = opts.title || (variant === "Search" ? "Searching the web" : "Thinking");
    var doneTitle = opts.doneTitle || "Thought for a few moments";
    var steps = opts.steps || [];
    var isDone = opts.isDone === true;
    var expanded = opts.expanded === true;
    var startTime = Date.now();
    var timerInterval = null;

    var wrap = document.createElement("div");
    wrap.className = "lz-think-container";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "lz-tool-header-btn" + (isDone ? " is-done" : "");

    var matrixHtml = '<span class="lz-matrix-dots">' +
      '<span class="lz-matrix-dot"></span><span class="lz-matrix-dot"></span>' +
      '<span class="lz-matrix-dot"></span><span class="lz-matrix-dot"></span>' +
      '<span class="lz-matrix-dot"></span><span class="lz-matrix-dot"></span>' +
      '</span>';

    var durationSpan = document.createElement("span");
    durationSpan.className = "lz-think-duration";
    durationSpan.textContent = isDone ? "" : "0.1s";

    var labelSpan = document.createElement("span");
    labelSpan.className = "lz-think-label";
    labelSpan.textContent = isDone ? doneTitle : title;

    btn.innerHTML = matrixHtml;
    btn.appendChild(labelSpan);
    btn.appendChild(durationSpan);

    var chevron = document.createElement("span");
    chevron.className = "lz-chevron-icon";
    chevron.innerHTML = I.chevronDown({ size: 12 });
    btn.appendChild(chevron);

    var body = document.createElement("div");
    body.className = "lz-think-box";
    body.style.display = (expanded && steps.length > 0) ? "flex" : "none";

    steps.forEach(function(st) {
      var row = document.createElement("div");
      row.className = "lz-think-step" + (st.done || isDone ? " done" : "");
      var iconHtml = (st.done || isDone) ? I.check({ size: 12, className: "text-green" }) : '<span class="lz-tool-spin"></span>';
      row.innerHTML = iconHtml + '<span>' + esc(st.text || st) + '</span>';
      body.appendChild(row);
    });

    function updateDuration() {
      if (isDone) return;
      var sec = ((Date.now() - startTime) / 1000).toFixed(1);
      durationSpan.textContent = sec + "s";
    }

    if (!isDone) {
      timerInterval = setInterval(updateDuration, 100);
    }

    btn.addEventListener("click", function() {
      if (!body.children.length) return;
      expanded = !expanded;
      body.style.display = expanded ? "flex" : "none";
      chevron.style.transform = expanded ? "rotate(180deg)" : "rotate(0)";
    });

    wrap.appendChild(btn);
    wrap.appendChild(body);

    return {
      el: wrap,
      addStep: function(text, done) {
        body.querySelectorAll(".lz-think-step:not(.done)").forEach(function(el) {
          el.classList.add("done");
          var spin = el.querySelector(".lz-tool-spin");
          if (spin) spin.outerHTML = I.check({ size: 12, className: "text-green" });
        });

        var row = document.createElement("div");
        row.className = "lz-think-step" + (done ? " done" : "");
        var iconHtml = done ? I.check({ size: 12, className: "text-green" }) : '<span class="lz-tool-spin"></span>';
        row.innerHTML = iconHtml + '<span>' + esc(text) + '</span>';
        body.appendChild(row);

        if (expanded) {
          body.style.display = "flex";
        }
      },
      setDone: function(finalTitle) {
        isDone = true;
        if (timerInterval) {
          clearInterval(timerInterval);
          timerInterval = null;
        }
        var totalSec = ((Date.now() - startTime) / 1000).toFixed(1);
        btn.classList.add("is-done");
        labelSpan.textContent = finalTitle || ("Thought for " + totalSec + "s");
        durationSpan.textContent = "";
        
        var dots = btn.querySelectorAll(".lz-matrix-dot");
        dots.forEach(function(d) {
          d.style.animation = "none";
          d.style.opacity = "0.5";
        });

        body.querySelectorAll(".lz-think-step").forEach(function(el) {
          el.classList.add("done");
          var spin = el.querySelector(".lz-tool-spin");
          if (spin) spin.outerHTML = I.check({ size: 12, className: "text-green" });
        });
      }
    };
  },

  /* ── Tool Group & File Diff Primitive ──────────────────── */
  createToolGroup: function(opts) {
    opts = opts || {};
    var title = opts.title || ( (opts.tools ? opts.tools.length : 1) + " tool calls" );
    var items = opts.items || opts.tools || [];
    var diffs = opts.diffs || [];
    var isExpanded = opts.expanded !== false;

    var wrap = document.createElement("div");
    wrap.className = "lz-tool-group-card";

    var head = document.createElement("button");
    head.type = "button";
    head.className = "lz-tool-group-header";
    head.innerHTML = I.chevronDown({ size: 13, className: "lz-group-chevron" }) +
      '<span class="lz-group-title">' + esc(title) + '</span>';

    var body = document.createElement("div");
    body.className = "lz-tool-group-body";
    body.style.display = isExpanded ? "flex" : "none";

    items.forEach(function(it) {
      var row = document.createElement("div");
      row.className = "lz-tool-group-row";

      var iconSvg = I.sparkle({ size: 13, className: "text-muted" });
      var actionName = it.action || formatToolLabel(it.name || "Action");
      var argVal = it.arg || it.summary || it.param || "";

      if (it.type === "write" || actionName.toLowerCase().indexOf("write") !== -1 || actionName.toLowerCase().indexOf("draft") !== -1) {
        iconSvg = I.edit({ size: 13 });
      } else if (it.type === "run" || it.type === "cmd" || actionName.toLowerCase().indexOf("rebuild") !== -1 || actionName.indexOf(">_") !== -1) {
        iconSvg = '<span style="font-family:var(--font-mono);font-size:11px;font-weight:700;color:var(--ink-3);">&gt;_</span>';
      } else if (it.type === "file" || actionName.toLowerCase().indexOf("read") !== -1 || actionName.toLowerCase().indexOf("image") !== -1) {
        iconSvg = I.doc({ size: 13 });
      }

      row.innerHTML = '<span class="lz-tool-action-icon">' + iconSvg + '</span>' +
        '<span class="lz-tool-action-name">' + esc(actionName) + '</span>' +
        (argVal ? '<span class="lz-tool-pill">' + esc(argVal) + '</span>' : '');

      body.appendChild(row);
    });

    if (diffs && diffs.length) {
      var sep = document.createElement("div");
      sep.className = "lz-tool-sep";
      body.appendChild(sep);

      var diffRow = document.createElement("div");
      diffRow.className = "lz-diff-row";

      diffs.forEach(function(d) {
        var pill = document.createElement("div");
        pill.className = "lz-diff-pill";
        pill.innerHTML = '<span class="font-mono">' + esc(d.file || d.name) + '</span>' +
          (d.add != null ? '<span class="lz-diff-add">+' + d.add + '</span>' : '') +
          (d.del != null ? '<span class="lz-diff-del">-' + d.del + '</span>' : '');
        diffRow.appendChild(pill);
      });

      if (opts.moreCount) {
        var morePill = document.createElement("span");
        morePill.className = "lz-diff-more";
        morePill.textContent = "+" + opts.moreCount + " more";
        diffRow.appendChild(morePill);
      }

      body.appendChild(diffRow);
    }

    head.addEventListener("click", function() {
      isExpanded = !isExpanded;
      body.style.display = isExpanded ? "flex" : "none";
      head.querySelector(".lz-group-chevron").style.transform = isExpanded ? "rotate(0)" : "rotate(-90deg)";
    });

    wrap.appendChild(head);
    wrap.appendChild(body);
    return wrap;
  },

  /* ── Tool Chips with Live Diff inspection ──────────────── */
  createToolChips: function(tools) {
    var wrap = document.createElement("div");
    wrap.className = "lz-tool-chips-wrap";

    tools = tools || [];
    tools.forEach(function(t) {
      var chip = document.createElement("div");
      chip.className = "lz-tool-chip";
      var icon = t.live ? '<span class="lz-tool-spin"></span>' : I.check({ size: 12, className: "text-green" });
      var label = t.summary || t.label || t.name || "Tool";
      chip.innerHTML = icon + '<span>' + esc(label) + '</span>';
      if (t.diff) {
        var diffPill = document.createElement("span");
        diffPill.style.fontFamily = "var(--font-mono)";
        diffPill.style.fontSize = "11px";
        diffPill.style.marginLeft = "4px";
        diffPill.innerHTML = '<span style="color:var(--green)">+' + (t.diff.add || 0) + '</span> <span style="color:var(--red)">-' + (t.diff.del || 0) + '</span>';
        chip.appendChild(diffPill);
      }
      wrap.appendChild(chip);
    });

    return wrap;
  },

  /* ── Diff Table (Proposed edits with toggleable rows) ─── */
  createDiffTable: function(opts) {
    opts = opts || {};
    var title = opts.title || "Proposed document edits";
    var rows = opts.rows || [];
    var onApply = opts.onApply;

    var card = document.createElement("div");
    card.className = "lz-diff-card";

    var head = document.createElement("div");
    head.className = "lz-card-head";
    head.innerHTML = '<span>' + esc(title) + '</span><span style="font-size:11px;color:var(--ink-3);">Click rows to include/exclude</span>';
    card.appendChild(head);

    var body = document.createElement("div");
    body.className = "lz-card-body";
    body.style.padding = "0";

    var table = document.createElement("table");
    table.style.width = "100%";
    table.style.borderCollapse = "collapse";
    table.style.fontSize = "12.5px";

    var selectedMap = {};
    rows.forEach(function(r, idx) {
      selectedMap[idx] = true;
      var tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--line)";
      tr.style.cursor = "pointer";
      tr.style.transition = "background-color 140ms ease";
      var isAdd = r.type === "add";
      tr.style.background = isAdd ? "var(--green-tint)" : "var(--red-tint)";
      tr.style.color = isAdd ? "var(--green)" : "var(--red)";

      tr.innerHTML = '<td style="padding:8px 12px;font-family:var(--font-mono);width:30px;">' + (isAdd ? "+" : "-") + '</td>' +
        '<td style="padding:8px 12px;">' + esc(r.text) + '</td>' +
        '<td style="padding:8px 12px;text-align:right;width:30px;"><span class="diff-check">' + I.check({ size: 12 }) + '</span></td>';

      tr.addEventListener("click", function() {
        selectedMap[idx] = !selectedMap[idx];
        tr.style.opacity = selectedMap[idx] ? "1" : "0.35";
      });

      table.appendChild(tr);
    });

    body.appendChild(table);
    card.appendChild(body);

    var foot = document.createElement("div");
    foot.className = "lz-card-footer";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "lz-btn-pill primary";
    btn.innerHTML = I.check({ size: 14 }) + "<span>Apply changes</span>";
    btn.addEventListener("click", function() {
      btn.disabled = true;
      btn.innerHTML = I.check({ size: 14 }) + "<span>Changes applied</span>";
      if (onApply) onApply(selectedMap);
    });
    foot.appendChild(document.createElement("div"));
    foot.appendChild(btn);
    card.appendChild(foot);

    return card;
  },

  /* ── Approval Card (Human in the loop multi-choice) ───── */
  createApprovalCard: function(opts) {
    opts = opts || {};
    var questions = opts.questions || [
      { q: "How detailed should the output be?", type: "radio", options: ["Concise summary", "Standard assignment", "Comprehensive report"] }
    ];
    var onSubmitted = opts.onSubmitted;
    var onDismiss = opts.onDismiss;

    var card = document.createElement("div");
    card.className = "lz-approval-card";

    var currentQ = 0;
    var answers = {};

    var head = document.createElement("div");
    head.className = "lz-card-head";
    var titleSpan = document.createElement("span");
    titleSpan.style.fontWeight = "600";
    titleSpan.style.fontSize = "13.5px";

    var closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "lz-card-close-btn";
    closeBtn.title = "Dismiss";
    closeBtn.innerHTML = I.close({ size: 13 });
    closeBtn.addEventListener("click", function() {
      card.remove();
      if (onDismiss) onDismiss();
    });

    head.appendChild(titleSpan);
    head.appendChild(closeBtn);
    card.appendChild(head);

    var body = document.createElement("div");
    body.className = "lz-card-body";
    card.appendChild(body);

    var foot = document.createElement("div");
    foot.className = "lz-card-footer";

    var navWrap = document.createElement("div");
    navWrap.className = "lz-approval-nav";
    var prevArrow = document.createElement("button");
    prevArrow.type = "button";
    prevArrow.className = "lz-approval-arrow";
    prevArrow.innerHTML = I.chevronLeft({ size: 12 });
    var counterSpan = document.createElement("span");
    counterSpan.className = "lz-approval-counter";
    var nextArrow = document.createElement("button");
    nextArrow.type = "button";
    nextArrow.className = "lz-approval-arrow";
    nextArrow.innerHTML = I.chevronRight({ size: 12 });

    prevArrow.addEventListener("click", function() {
      if (currentQ > 0) {
        currentQ--;
        renderQuestion();
      }
    });

    nextArrow.addEventListener("click", function() {
      if (currentQ < questions.length - 1) {
        currentQ++;
        renderQuestion();
      }
    });

    navWrap.appendChild(prevArrow);
    navWrap.appendChild(counterSpan);
    navWrap.appendChild(nextArrow);
    foot.appendChild(navWrap);

    var actionsWrap = document.createElement("div");
    actionsWrap.style.display = "flex";
    actionsWrap.style.gap = "6px";
    actionsWrap.style.alignItems = "center";

    var skipBtn = document.createElement("button");
    skipBtn.type = "button";
    skipBtn.className = "lz-btn-pill secondary";
    skipBtn.textContent = "Skip";

    var nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.className = "lz-btn-pill primary";
    nextBtn.textContent = "Continue";

    actionsWrap.appendChild(skipBtn);
    actionsWrap.appendChild(nextBtn);
    foot.appendChild(actionsWrap);
    card.appendChild(foot);

    function renderQuestion() {
      var q = questions[currentQ];
      titleSpan.textContent = q.q;
      counterSpan.textContent = (currentQ + 1) + " / " + questions.length;
      prevArrow.disabled = (currentQ === 0);
      prevArrow.style.opacity = (currentQ === 0) ? "0.35" : "1";
      nextArrow.disabled = (currentQ === questions.length - 1);
      nextArrow.style.opacity = (currentQ === questions.length - 1) ? "0.35" : "1";

      body.innerHTML = "";

      var optionsWrap = document.createElement("div");
      optionsWrap.style.display = "flex";
      optionsWrap.style.flexDirection = "column";
      optionsWrap.style.gap = "4px";

      q.options.forEach(function(opt, idx) {
        var optBtn = document.createElement("button");
        optBtn.type = "button";
        optBtn.className = "lz-approval-opt-btn";
        var isPicked = answers[currentQ] === opt || answers[currentQ] === idx;
        if (isPicked) optBtn.classList.add("active");

        optBtn.innerHTML = '<span class="lz-approval-radio-ring">' +
          (isPicked ? '<span class="lz-approval-radio-dot"></span>' : '') + '</span>' +
          '<span class="lz-approval-opt-text">' + esc(opt) + '</span>';

        optBtn.addEventListener("click", function() {
          answers[currentQ] = opt;
          renderQuestion();
          if (q.type !== "multi") {
            setTimeout(advance, 220);
          }
        });

        optionsWrap.appendChild(optBtn);
      });

      // Custom "Something else..." input
      var customRow = document.createElement("div");
      customRow.className = "lz-approval-custom-row";
      var customInput = document.createElement("input");
      customInput.type = "text";
      customInput.className = "lz-approval-custom-input";
      customInput.placeholder = "Something else…";
      if (answers[currentQ] && !q.options.includes(answers[currentQ])) {
        customInput.value = answers[currentQ];
      }
      customInput.addEventListener("input", function() {
        if (customInput.value.trim()) {
          answers[currentQ] = customInput.value.trim();
        }
      });
      customInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && customInput.value.trim()) {
          answers[currentQ] = customInput.value.trim();
          advance();
        }
      });
      customRow.appendChild(customInput);
      optionsWrap.appendChild(customRow);

      body.appendChild(optionsWrap);
      nextBtn.textContent = (currentQ === questions.length - 1) ? "Submit" : "Continue";
    }

    function advance() {
      if (currentQ < questions.length - 1) {
        currentQ++;
        renderQuestion();
      } else {
        card.innerHTML = '<div style="padding:14px;display:flex;align-items:center;gap:8px;color:var(--green);font-weight:500;font-size:13px;">' +
          I.check({ size: 15, className: "text-green" }) + '<span>Preferences confirmed — drafting with selected options…</span></div>';
        if (onSubmitted) onSubmitted(answers);
      }
    }

    skipBtn.addEventListener("click", function() {
      card.remove();
      if (onSubmitted) onSubmitted(answers);
    });
    nextBtn.addEventListener("click", advance);

    renderQuestion();
    return card;
  },

  /* ── Task Checklist Rows ──────────────────────────────── */
  createTaskRows: function(tasks) {
    var wrap = document.createElement("div");
    wrap.style.display = "flex";
    wrap.style.flexDirection = "column";
    wrap.style.gap = "6px";
    wrap.style.margin = "10px 0";

    tasks = tasks || [];
    tasks.forEach(function(t) {
      var row = document.createElement("div");
      row.className = "lz-sb-recent-item";
      row.style.background = "var(--surface)";
      row.style.border = "1px solid var(--line)";
      row.innerHTML = '<span style="display:flex;align-items:center;gap:8px;">' +
        (t.done ? I.check({ size: 14, className: "text-green" }) : '<span style="width:12px;height:12px;border:1.5px solid var(--ink-3);border-radius:3px;"></span>') +
        '<span style="' + (t.done ? 'text-decoration:line-through;color:var(--ink-3);' : '') + '">' + esc(t.label) + '</span>' +
        '</span>';
      wrap.appendChild(row);
    });

    return wrap;
  },

  /* ── Context Reference Cards ──────────────────────────── */
  createContextCards: function(cards) {
    var wrap = document.createElement("div");
    wrap.style.display = "flex";
    wrap.style.flexDirection = "column";
    wrap.style.gap = "8px";
    wrap.style.margin = "10px 0";

    cards = cards || [];
    cards.forEach(function(c) {
      var item = document.createElement("div");
      item.style.padding = "10px 12px";
      item.style.borderRadius = "var(--radius-card)";
      item.style.background = "var(--surface)";
      item.style.border = "1px solid var(--line)";
      item.style.boxShadow = "var(--shadow-card)";
      item.innerHTML = '<div style="font-weight:600;font-size:13px;color:var(--ink);margin-bottom:4px;">' + esc(c.title) + '</div>' +
        '<div style="font-size:12px;color:var(--ink-2);line-height:1.5;">' + esc(c.desc || "") + '</div>';
      wrap.appendChild(item);
    });

    return wrap;
  },

  /* ── Selection Actions (Contextual AI toolbar) ───────── */
  createSelectionActions: function(opts) {
    opts = opts || {};
    var onAction = opts.onAction;
    var actions = opts.actions || [
      { key: "improve", label: "Improve", icon: "sparkle" },
      { key: "shorten", label: "Shorten", icon: "tasks" },
      { key: "explain", label: "Explain", icon: "chat" }
    ];

    var bar = document.createElement("div");
    bar.className = "lz-selection-actions";
    bar.style.display = "inline-flex";
    bar.style.alignItems = "center";
    bar.style.gap = "4px";
    bar.style.padding = "4px 6px";
    bar.style.borderRadius = "var(--radius-pill)";
    bar.style.background = "var(--surface)";
    bar.style.border = "1px solid var(--line)";
    bar.style.boxShadow = "var(--shadow-raised)";

    actions.forEach(function(act) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lz-btn-pill secondary";
      btn.style.height = "26px";
      btn.style.padding = "0 10px";
      btn.style.fontSize = "12px";
      var iconFn = I[act.icon] || I.sparkle;
      btn.innerHTML = iconFn({ size: 12 }) + "<span>" + esc(act.label) + "</span>";
      btn.addEventListener("click", function() {
        if (onAction) onAction(act.key);
      });
      bar.appendChild(btn);
    });

    return bar;
  },

  /* ── Insight Card (Callout / Metric card) ──────────────── */
  createInsightCard: function(opts) {
    opts = opts || {};
    var title = opts.title || "Insight";
    var value = opts.value || "";
    var desc = opts.desc || "";
    var delta = opts.delta || "";
    var isPositive = opts.positive !== false;

    var card = document.createElement("div");
    card.className = "lz-insight-card";
    card.style.padding = "14px";
    card.style.margin = "10px 0";

    card.innerHTML = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">' +
      '<span style="font-size:12px;font-weight:600;color:var(--ink-3);text-transform:uppercase;letter-spacing:0.04em;">' + esc(title) + '</span>' +
      (delta ? '<span style="font-family:var(--font-mono);font-size:12px;font-weight:600;color:' + (isPositive ? "var(--green)" : "var(--red)") + ';">' + esc(delta) + '</span>' : '') +
      '</div>' +
      (value ? '<div style="font-size:20px;font-weight:700;color:var(--ink);margin-bottom:4px;">' + esc(value) + '</div>' : '') +
      '<div style="font-size:13px;color:var(--ink-2);line-height:1.5;">' + esc(desc) + '</div>';

    return card;
  }
};

window.LazyPrimitives = Primitives;
})(window);
