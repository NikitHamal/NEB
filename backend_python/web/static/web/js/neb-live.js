/* NebLive: write the way it will look. Posts, replies and comments are edited as formatted text: bold is bold the
   moment you press the button, a list is a list, a formula is a drawn formula. Nobody types ** or $ any more.

   Storage stays Markdown (so every old post, the apps and the renderers keep working): the editor turns what you see
   into Markdown on every change, and turns stored Markdown back into formatted text when it opens.

   Two ways in:
     NebLive.attach(textarea)   the textarea is hidden and replaced by an editable surface. `value`, `focus`,
                                `setRangeText`, key events and `input` events keep working, so existing composer code
                                runs unchanged and reads Markdown.
     NebLive.bind(editableDiv)  an editable element that already exists (the create-post page).
   Shared: NebLive.format(target, 'bold'|'italic'|'underline'|'strike'|'code'|'codeblock'|'h2'|'quote'|'ul'|'ol'|'link'
           |'math'|'hr'|'table'|'spoiler'|'step'), insertText, insertMath, toMarkdown, fromMarkdown. */
(function () {
  'use strict';
  if (window.NebLive) return;

  var NATIVE_VALUE = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
  var BLOCKS = { P: 1, DIV: 1, H1: 1, H2: 1, H3: 1, H4: 1, H5: 1, H6: 1, UL: 1, OL: 1, LI: 1, BLOCKQUOTE: 1, PRE: 1, HR: 1, TABLE: 1 };
  var ALLOWED = { P: 1, BR: 1, STRONG: 1, B: 1, EM: 1, I: 1, U: 1, S: 1, DEL: 1, STRIKE: 1, CODE: 1, PRE: 1, A: 1, UL: 1, OL: 1, LI: 1,
    H1: 1, H2: 1, H3: 1, H4: 1, H5: 1, H6: 1, BLOCKQUOTE: 1, HR: 1, TABLE: 1, THEAD: 1, TBODY: 1, TR: 1, TH: 1, TD: 1, SPAN: 1, DIV: 1 };

  /* ------------------------------------------------------------------ math from plain typing */
  var GREEK = 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau phi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega'.split(' ');
  var WORDS = { inf: '\\infty', infinity: '\\infty', deg: '^{\\circ}', degree: '^{\\circ}', sum: '\\sum', int: '\\int', integral: '\\int', lim: '\\lim', sin: '\\sin', cos: '\\cos', tan: '\\tan',
    log: '\\log', ln: '\\ln', cot: '\\cot', sec: '\\sec', csc: '\\csc', times: '\\times', cdot: '\\cdot', partial: '\\partial', nabla: '\\nabla', therefore: '\\therefore', angle: '\\angle', perp: '\\perp' };
  GREEK.forEach(function (g) { WORDS[g] = '\\' + g; });
  var SYMS = [['<=', '\\le '], ['>=', '\\ge '], ['!=', '\\ne '], ['->', '\\to '], ['<-', '\\leftarrow '], ['=>', '\\Rightarrow '], ['+-', '\\pm '], ['~=', '\\approx '], ['*', '\\cdot ']];

  /* "x^2 + sqrt(a/b)" -> "x^{2} + \sqrt{\frac{a}{b}}": what a calculator would take, no LaTeX needed. */
  function asciiToTex(src) {
    var s = String(src || ''), i = 0;
    function peek() { return s.charAt(i); }
    function skipSpace() { var m = /^\s*/.exec(s.slice(i)); i += m[0].length; }
    function word(w) {
      if (WORDS[w]) return WORDS[w] + (WORDS[w].charAt(0) === '\\' && /[a-z]$/.test(WORDS[w]) ? ' ' : '');
      return w;
    }
    function group() { /* one operand: (...), a word or a number */
      skipSpace();
      if (peek() === '(') { i++; var inner = expr(')'); if (peek() === ')') i++; return inner; }
      var m = /^(?:[A-Za-z]+|\d+(?:\.\d+)?|\S)/.exec(s.slice(i));
      if (!m) return '';
      i += m[0].length;
      return word(m[0]);
    }
    function atom() {
      skipSpace();
      var c = peek(), base = '';
      if (!c) return '';
      if (/^sqrt\s*\(/i.test(s.slice(i))) {
        i += 4; skipSpace(); i++;
        var r = expr(')'); if (peek() === ')') i++;
        base = '\\sqrt{' + r + '}';
      } else if (/^root\s*\(/i.test(s.slice(i))) {
        i += 4; skipSpace(); i++;
        var parts = exprList();
        base = parts.length > 1 ? '\\sqrt[' + parts[0] + ']{' + parts[1] + '}' : '\\sqrt{' + parts[0] + '}';
      } else if (c === '(') {
        i++; var e = expr(')'); if (peek() === ')') i++;
        base = '\\left(' + e + '\\right)';
      } else {
        for (var k = 0; k < SYMS.length; k++) {
          if (s.substr(i, SYMS[k][0].length) === SYMS[k][0]) { i += SYMS[k][0].length; return SYMS[k][1]; }
        }
        var mm = /^(?:[A-Za-z]+|\d+(?:\.\d+)?|\S)/.exec(s.slice(i));
        i += mm[0].length;
        base = word(mm[0]);
        if (/^(sin|cos|tan|cot|sec|csc|log|ln)$/.test(mm[0]) && peek() === '(') {
          i++; var fe = expr(')'); if (peek() === ')') i++;
          base += '\\left(' + fe + '\\right)';
        }
      }
      for (;;) { /* powers, subscripts, factorial */
        var save = i; skipSpace();
        var ch = peek();
        if (ch === '^') { i++; base += '^{' + group() + '}'; }
        else if (ch === '_') { i++; base += '_{' + group() + '}'; }
        else if (ch === '!' && s.charAt(i + 1) !== '=') { i++; base += '!'; }
        else { i = save; break; }
      }
      return base;
    }
    function stripParens(t) { var m = /^\\left\((.*)\\right\)$/.exec(t); return m ? m[1] : t; }
    function term() {
      var left = atom();
      var save = i; skipSpace();
      if (peek() === '/') {
        i++;
        var right = atom();
        return '\\frac{' + stripParens(left) + '}{' + stripParens(right) + '}';
      }
      i = save;
      return left + ' ';
    }
    function exprList() {
      var out = [], cur = '';
      for (;;) {
        skipSpace();
        var c = peek();
        if (!c) break;
        if (c === ')') { i++; break; }
        if (c === ',') { i++; out.push(cur.trim()); cur = ''; continue; }
        cur += term();
      }
      out.push(cur.trim());
      return out;
    }
    function expr(stop) {
      var out = '';
      for (;;) {
        skipSpace();
        var c = peek();
        if (!c || (stop && c === stop)) break;
        if (c === ',') { i++; out += ', '; continue; }
        out += term();
      }
      return out.replace(/\s+/g, ' ').trim();
    }
    try { return expr(null); } catch (e) { return s; }
  }

  function paintMath(el) {
    var tex = el.getAttribute('data-tex') || '';
    el.textContent = '';
    if (window.katex && typeof window.katex.render === 'function') {
      try { window.katex.render(tex, el, { throwOnError: false, displayMode: el.getAttribute('data-display') === '1' }); return; } catch (e) { /* fall through */ }
    }
    el.textContent = tex;
  }
  function texNode(tex, ascii, display) {
    var el = document.createElement('span');
    el.className = 'neb-math' + (display ? ' is-display' : '');
    el.setAttribute('contenteditable', 'false');
    el.setAttribute('data-tex', tex);
    if (ascii) el.setAttribute('data-ascii', ascii);
    if (display) el.setAttribute('data-display', '1');
    paintMath(el);
    return el;
  }

  /* ------------------------------------------------------------------ editable DOM -> Markdown */
  function escText(t) { return t.replace(/\u200b/g, '').replace(/\u00a0/g, ' ').replace(/([\\`*_~|])/g, '\\$1'); }
  function escLead(line) {
    return line.replace(/^(\s*)(#{1,6}\s|>|[-+]\s|\d+[.)]\s|={3,}|-{3,})/, function (m, sp, mark) { return sp + '\\' + mark; });
  }
  function wrapMark(mark, inner, end) {
    if (!inner.replace(/\s/g, '')) return inner;
    var m = /^(\s*)([\s\S]*?)(\s*)$/.exec(inner);
    return m[1] + mark + m[2] + (end || mark) + m[3];
  }
  function inlineOne(n) {
    var holder = document.createElement('div');
    holder.appendChild(n.cloneNode(true));
    return inline(holder);
  }

  function inline(node) {
    var out = '';
    for (var n = node.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) { out += escText(n.nodeValue); continue; }
      if (n.nodeType !== 1) continue;
      var tag = n.tagName, cls = n.classList;
      if (cls.contains('neb-chip')) { var iid = n.getAttribute('data-neb-img'); if (iid) out += '[[img:' + iid + ']]'; continue; }
      if (cls.contains('neb-math')) {
        var tex = n.getAttribute('data-tex') || '';
        out += n.getAttribute('data-display') === '1' ? '\n\n$$\n' + tex + '\n$$\n\n' : '$' + tex + '$';
        continue;
      }
      if (tag === 'BR') { out += '\n'; continue; }
      if (tag === 'IMG') continue;
      if (BLOCKS[tag]) { out += '\n' + inline(n) + '\n'; continue; }
      var inner = inline(n);
      if (tag === 'B' || tag === 'STRONG' || (n.style && /^(bold|[6-9]00)$/.test(n.style.fontWeight))) out += wrapMark('**', inner);
      else if (tag === 'I' || tag === 'EM' || (n.style && n.style.fontStyle === 'italic')) out += wrapMark('*', inner);
      else if (tag === 'S' || tag === 'STRIKE' || tag === 'DEL') out += wrapMark('~~', inner);
      else if (tag === 'U' || (n.style && /underline/.test(n.style.textDecoration || n.style.textDecorationLine || ''))) out += wrapMark('<u>', inner, '</u>');
      else if (tag === 'CODE') out += wrapMark('`', n.textContent.replace(/\u200b/g, ''));
      else if (tag === 'A') {
        var href = n.getAttribute('href') || '';
        out += href && inner.trim() ? '[' + inner + '](' + href.replace(/\)/g, '%29') + ')' : inner;
      } else if (cls.contains('neb-spoiler')) out += wrapMark('||', inner);
      else out += inner;
    }
    return out;
  }

  function listMd(list, depth) {
    var ordered = list.tagName === 'OL', n = parseInt(list.getAttribute('start') || '1', 10) || 1, lines = [];
    var pad = new Array(depth + 1).join('   ');
    for (var li = list.firstElementChild; li; li = li.nextElementSibling) {
      if (li.tagName !== 'LI') continue;
      var text = '', nested = [];
      for (var c = li.firstChild; c; c = c.nextSibling) {
        if (c.nodeType === 1 && (c.tagName === 'UL' || c.tagName === 'OL')) nested.push(listMd(c, depth + 1));
        else if (c.nodeType === 1 && (c.tagName === 'P' || c.tagName === 'DIV')) text += (text ? '\n' : '') + inline(c);
        else if (c.nodeType === 3) text += escText(c.nodeValue);
        else if (c.nodeType === 1) text += inlineOne(c);
      }
      var first = text.replace(/^\n+|\n+$/g, '').split('\n');
      var mark = ordered ? (n++) + '. ' : '- ';
      lines.push(pad + mark + escLead(first[0] || '').replace(/^\s+/, ''));
      for (var k = 1; k < first.length; k++) lines.push(pad + '   ' + first[k]);
      nested.forEach(function (nl) { lines.push(nl); });
    }
    return lines.join('\n');
  }

  function tableMd(table) {
    var rows = [].slice.call(table.querySelectorAll('tr')).map(function (tr) {
      return [].slice.call(tr.children).map(function (c) { return inline(c).replace(/\|/g, '\\|').replace(/\n/g, ' ').trim() || ' '; });
    });
    if (!rows.length) return '';
    var cols = Math.max.apply(null, rows.map(function (r) { return r.length; }));
    rows = rows.map(function (r) { while (r.length < cols) r.push(' '); return '| ' + r.join(' | ') + ' |'; });
    var sep = '|' + new Array(cols + 1).join(' --- |');
    return [rows[0], sep].concat(rows.slice(1)).join('\n');
  }

  function blocks(root) {
    var parts = [], line = '';
    function flush() {
      var t = line.replace(/^\n+|\n+$/g, '');
      line = '';
      if (t.replace(/\s/g, '')) parts.push(escLead(t));
    }
    for (var n = root.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) { line += escText(n.nodeValue); continue; }
      if (n.nodeType !== 1) continue;
      var tag = n.tagName;
      if (!BLOCKS[tag]) { line += inlineOne(n); continue; }
      flush();
      if (tag === 'P' || tag === 'DIV') {
        if (n.querySelector('p,div,ul,ol,blockquote,pre,table,h1,h2,h3,h4,h5,h6,hr')) { var sub = blocks(n); if (sub) parts.push(sub); }
        else { var t = inline(n).replace(/^\n+|\n+$/g, ''); if (t.replace(/\s/g, '')) parts.push(escLead(t)); }
      } else if (/^H[1-6]$/.test(tag)) {
        var h = inline(n).replace(/\n/g, ' ').trim();
        if (h) parts.push((tag === 'H1' || tag === 'H2' ? '## ' : '### ') + h);
      } else if (tag === 'UL' || tag === 'OL') parts.push(listMd(n, 0));
      else if (tag === 'BLOCKQUOTE') {
        var q = blocks(n);
        if (q) parts.push(q.split('\n').map(function (l) { return '> ' + l; }).join('\n'));
      } else if (tag === 'PRE') {
        parts.push('```\n' + n.textContent.replace(/\u200b/g, '').replace(/\n+$/, '') + '\n```');
      } else if (tag === 'HR') parts.push('---');
      else if (tag === 'TABLE') parts.push(tableMd(n));
      else if (tag === 'LI') parts.push(inline(n));
    }
    flush();
    return parts.join('\n\n');
  }

  function toMarkdown(root) { return blocks(root).replace(/\n{3,}/g, '\n\n').trim(); }

  /* ------------------------------------------------------------------ Markdown -> editable DOM */
  function clean(src) {
    var doc = new DOMParser().parseFromString('<body>' + src + '</body>', 'text/html');
    var out = document.createDocumentFragment();
    function walk(from, to) {
      for (var n = from.firstChild; n; n = n.nextSibling) {
        if (n.nodeType === 3) { to.appendChild(document.createTextNode(n.nodeValue)); continue; }
        if (n.nodeType !== 1) continue;
        var tag = n.tagName;
        if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'IFRAME' || tag === 'OBJECT') continue;
        if (!ALLOWED[tag]) { walk(n, to); continue; }
        if (tag === 'SPAN') {
          var st = n.style || {}, wrap = to;
          if (n.classList.contains('neb-spoiler')) { var sp = document.createElement('span'); sp.className = 'neb-spoiler'; to.appendChild(sp); walk(n, sp); continue; }
          if (/^(bold|[6-9]00)$/.test(st.fontWeight)) { var b = document.createElement('b'); wrap.appendChild(b); wrap = b; }
          if (st.fontStyle === 'italic') { var it = document.createElement('i'); wrap.appendChild(it); wrap = it; }
          walk(n, wrap);
          continue;
        }
        var name = tag === 'H1' ? 'H2' : (tag === 'H4' || tag === 'H5' || tag === 'H6') ? 'H3' : tag === 'STRONG' ? 'B' : tag === 'EM' ? 'I' : (tag === 'DEL' || tag === 'STRIKE') ? 'S' : tag === 'DIV' ? 'P' : tag;
        var el = document.createElement(name);
        if (tag === 'A') {
          var href = n.getAttribute('href') || '';
          if (/^(https?:|mailto:|\/|#)/i.test(href)) { el.setAttribute('href', href); el.setAttribute('target', '_blank'); el.setAttribute('rel', 'noopener noreferrer'); }
        }
        if (tag === 'OL' && n.getAttribute('start')) el.setAttribute('start', n.getAttribute('start'));
        to.appendChild(el);
        walk(n, el);
      }
    }
    walk(doc.body, out);
    return out;
  }

  function fromMarkdown(ed, md) {
    md = String(md || '');
    ed.textContent = '';
    if (!md.trim()) return;
    var stash = [];
    /* formulas are lifted out first so the Markdown parser cannot mangle the _ and * inside them */
    var work = md.replace(/\$\$\n?([\s\S]+?)\n?\$\$/g, function (m, t) { stash.push({ tex: t.trim(), display: true }); return '\u0001' + (stash.length - 1) + '\u0001'; })
      .replace(/(^|[^\\$\w])\$([^\s$](?:[^$\n]*[^\s$])?)\$(?![\w$])/g, function (m, pre, t) { stash.push({ tex: t, display: false }); return pre + '\u0001' + (stash.length - 1) + '\u0001'; });
    var html = null;
    if (typeof window.marked !== 'undefined') {
      try { html = window.marked.parse(work, { breaks: true, gfm: true }); } catch (e) { html = null; }
    }
    if (html == null) html = work.split(/\n{2,}/).map(function (p) { return '<p>' + p.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\n/g, '<br>') + '</p>'; }).join('');
    ed.appendChild(clean(html));
    /* put formulas, image chips and spoilers back */
    var walker = document.createTreeWalker(ed, NodeFilter.SHOW_TEXT, null), nodes = [], t;
    while ((t = walker.nextNode())) nodes.push(t);
    nodes.forEach(function (tn) {
      var v = tn.nodeValue;
      if (!/\u0001\d+\u0001|\[\[img:\d+\]\]|\|\|.+?\|\|/.test(v)) return;
      if (tn.parentNode.closest && tn.parentNode.closest('code,pre')) return;
      var f = document.createDocumentFragment(), last = 0, m, re = /\u0001(\d+)\u0001|\[\[img:(\d{1,10})\]\]|\|\|(.+?)\|\|/g;
      while ((m = re.exec(v))) {
        if (m.index > last) f.appendChild(document.createTextNode(v.slice(last, m.index)));
        if (m[1] != null) { var s = stash[+m[1]]; if (s) f.appendChild(texNode(s.tex, '', s.display)); }
        else if (m[2] != null) {
          if (window.InlineMedia && window.InlineMedia.chipElement) f.appendChild(window.InlineMedia.chipElement(parseInt(m[2], 10), { editor: true }));
          else f.appendChild(document.createTextNode(m[0]));
        } else { var sp = document.createElement('span'); sp.className = 'neb-spoiler'; sp.textContent = m[3]; f.appendChild(sp); }
        last = m.index + m[0].length;
      }
      if (last < v.length) f.appendChild(document.createTextNode(v.slice(last)));
      tn.parentNode.replaceChild(f, tn);
    });
  }

  /* ------------------------------------------------------------------ selection helpers */
  function sel() { return window.getSelection(); }
  function rangeNow() { var s = sel(); return s && s.rangeCount ? s.getRangeAt(0) : null; }
  function within(ed) { var r = rangeNow(); return !!(r && ed.contains(r.commonAncestorContainer)); }
  function ensureCaret(ed) {
    try { ed.focus({ preventScroll: true }); } catch (e) { ed.focus(); }
    if (!within(ed)) {
      var s = sel();
      if (ed.__range) { s.removeAllRanges(); s.addRange(ed.__range); }
      if (!within(ed)) { var r = document.createRange(); r.selectNodeContents(ed); r.collapse(false); s.removeAllRanges(); s.addRange(r); }
    }
  }
  function ancestor(node, ed, names) {
    for (var n = node; n && n !== ed; n = n.parentNode) if (n.nodeType === 1 && names.indexOf(n.tagName) >= 0) return n;
    return null;
  }
  function targetEd(target) {
    if (!target) return null;
    if (target.__neb) return target.__neb.ed;
    if (target._nebLive) return target;
    return target.closest ? target.closest('[data-neb-live]') : null;
  }
  function edOfNode(node) {
    var el = node && node.nodeType === 1 ? node : node && node.parentNode;
    return el && el.closest ? el.closest('[data-neb-live]') : null;
  }

  var uid = 0;
  function changed(ed) {
    var c = ed._nebLive; if (!c) return;
    ed.dispatchEvent(new Event('input', { bubbles: true }));
  }
  function isEmpty(ed) {
    if (ed.querySelector('.neb-math,.neb-chip,hr,table,img,li')) return false;
    return !ed.textContent.replace(/\u200b/g, '').trim();
  }

  /* Typing a list, heading or quote mark followed by a space at the start of a plain line. */
  function autoformat(ed) {
    var r = rangeNow();
    if (!r || !r.collapsed || r.startContainer.nodeType !== 3 || !ed.contains(r.startContainer)) return false;
    var blk = r.startContainer;
    while (blk && blk.parentNode !== ed) blk = blk.parentNode;
    if (!blk || (blk.nodeName !== 'P' && blk.nodeName !== 'DIV')) return false;
    var pre = document.createRange();
    pre.selectNodeContents(blk);
    pre.setEnd(r.startContainer, r.startOffset);
    var m = /^(-|\*|\d{1,3}[.)]|#{1,3}|>) $/.exec(pre.toString().replace(/\u00a0/g, ' '));
    if (!m) return false;
    pre.deleteContents();
    if (!blk.firstChild || !blk.textContent) { blk.innerHTML = '<br>'; }
    var nr = document.createRange(); nr.setStart(blk, 0); nr.collapse(true);
    var s = sel(); s.removeAllRanges(); s.addRange(nr);
    var k = m[1];
    if (k === '-' || k === '*') exec(ed, 'insertUnorderedList');
    else if (k === '>') exec(ed, 'formatBlock', 'BLOCKQUOTE');
    else if (k.charAt(0) === '#') exec(ed, 'formatBlock', k.length === 1 ? 'H2' : 'H3');
    else exec(ed, 'insertOrderedList');
    return true;
  }

  function exec(ed, cmd, arg) {
    ensureCaret(ed);
    try { document.execCommand('styleWithCSS', false, false); } catch (e) { /* ignore */ }
    try { document.execCommand(cmd, false, arg); } catch (e) { /* ignore */ }
    changed(ed);
  }

  function toggleBlock(ed, tag) {
    ensureCaret(ed);
    var r = rangeNow(), cur = r && ancestor(r.startContainer, ed, [tag.toUpperCase()]);
    exec(ed, 'formatBlock', cur ? 'P' : tag.toUpperCase());
  }

  function unwrap(el) { var pa = el.parentNode; while (el.firstChild) pa.insertBefore(el.firstChild, el); pa.removeChild(el); }

  function toggleCode(ed) {
    ensureCaret(ed);
    var r = rangeNow(); if (!r) return;
    var existing = ancestor(r.startContainer, ed, ['CODE']);
    if (existing) { unwrap(existing); changed(ed); return; }
    var code = document.createElement('code'), s = sel(), nr = document.createRange();
    if (r.collapsed) {
      code.appendChild(document.createTextNode('\u200b'));
      r.insertNode(code);
      nr.setStart(code.firstChild, 1); nr.collapse(true);
    } else {
      code.appendChild(r.extractContents());
      r.insertNode(code);
      nr.selectNodeContents(code);
    }
    s.removeAllRanges(); s.addRange(nr);
    changed(ed);
  }

  function toggleSpoiler(ed) {
    ensureCaret(ed);
    var r = rangeNow(); if (!r) return;
    var el = r.startContainer.nodeType === 1 ? r.startContainer : r.startContainer.parentNode;
    var existing = el && el.closest ? el.closest('.neb-spoiler') : null;
    if (existing && ed.contains(existing)) { unwrap(existing); changed(ed); return; }
    if (r.collapsed) return;
    var sp = document.createElement('span'); sp.className = 'neb-spoiler';
    sp.appendChild(r.extractContents()); r.insertNode(sp);
    changed(ed);
  }

  function insertHTML(ed, html) {
    ensureCaret(ed);
    var ok = false;
    try { ok = document.execCommand('insertHTML', false, html); } catch (e) { ok = false; }
    if (!ok) {
      var r = rangeNow();
      if (r) {
        var tmp = document.createElement('div'); tmp.innerHTML = html;
        var f = document.createDocumentFragment(); while (tmp.firstChild) f.appendChild(tmp.firstChild);
        r.deleteContents(); r.insertNode(f);
      }
    }
    changed(ed);
  }

  function insertNodeAtCaret(ed, node, after) {
    ensureCaret(ed);
    var r = rangeNow();
    if (!r) { ed.appendChild(node); changed(ed); return; }
    r.deleteContents();
    r.insertNode(node);
    var gap = document.createTextNode(after);
    node.parentNode.insertBefore(gap, node.nextSibling);
    var nr = document.createRange(); nr.setStart(gap, gap.nodeValue.length); nr.collapse(true);
    var s = sel(); s.removeAllRanges(); s.addRange(nr);
    changed(ed);
  }

  function insertText(target, text) {
    var ed = targetEd(target); if (!ed || !text) return;
    ensureCaret(ed);
    var ok = false;
    try { ok = document.execCommand('insertText', false, text); } catch (e) { ok = false; }
    if (!ok) { var r = rangeNow(); if (r) { r.deleteContents(); r.insertNode(document.createTextNode(text)); r.collapse(false); } }
    changed(ed);
  }

  function insertMath(target, tex, ascii, display, replaceNode) {
    var ed = targetEd(target); if (!ed || !tex) return;
    var node = texNode(tex, ascii, display);
    if (replaceNode && replaceNode.parentNode) { replaceNode.parentNode.replaceChild(node, replaceNode); changed(ed); return; }
    insertNodeAtCaret(ed, node, '\u200b');
  }

  /* ------------------------------------------------------------------ formulas: dialog */
  var mathDlg = null;
  var MATH_PARTS = [
    ['a/b', '(a)/(b)', 'Fraction'], ['x\u207f', 'x^2', 'Power'], ['x\u1d62', 'x_1', 'Subscript'], ['\u221ax', 'sqrt(x)', 'Square root'], ['\u221b', 'root(3, x)', 'Cube root'],
    ['\u2211', 'sum_(i=1)^n i', 'Sum'], ['\u222b', 'int_a^b f(x) dx', 'Integral'], ['lim', 'lim_(x->0)', 'Limit'], ['\u03c0', 'pi', 'Pi'], ['\u03b8', 'theta', 'Theta'],
    ['\u03b1', 'alpha', 'Alpha'], ['\u03b2', 'beta', 'Beta'], ['\u0394', 'Delta', 'Delta'], ['\u03bb', 'lambda', 'Lambda'], ['\u03c9', 'omega', 'Omega'], ['\u221e', 'inf', 'Infinity'],
    ['\u00b1', '+-', 'Plus or minus'], ['\u2264', '<=', 'At most'], ['\u2265', '>=', 'At least'], ['\u2260', '!=', 'Not equal'], ['\u2192', '->', 'Arrow'], ['\u00b0', 'deg', 'Degree']
  ];

  function closeMath() { if (mathDlg && mathDlg.parentNode) mathDlg.parentNode.removeChild(mathDlg); mathDlg = null; }

  function openMath(target, editNode, display) {
    var ed = targetEd(target); if (!ed) return;
    var saved = rangeNow();
    if (saved && ed.contains(saved.commonAncestorContainer)) ed.__range = saved.cloneRange();
    closeMath();
    var dlg = document.createElement('div');
    dlg.className = 'neb-live-pop neb-live-math';
    dlg.setAttribute('role', 'dialog'); dlg.setAttribute('aria-label', 'Formula');
    dlg.innerHTML = '<div class="nl-scrim"></div><div class="nl-card">' +
      '<div class="nl-title">Formula</div>' +
      '<div class="nl-preview is-empty" aria-live="polite"></div>' +
      '<input class="nl-in" type="text" autocomplete="off" spellcheck="false" placeholder="Type like a calculator: x^2 + 3/4, sqrt(5), pi">' +
      '<div class="nl-parts">' + MATH_PARTS.map(function (p, i) { return '<button type="button" class="nl-part" data-i="' + i + '" title="' + p[2] + '" aria-label="' + p[2] + '">' + p[0] + '</button>'; }).join('') + '</div>' +
      '<label class="nl-check"><input type="checkbox" class="nl-display"><span>On its own line</span></label>' +
      '<div class="nl-actions"><button type="button" class="nl-btn nl-cancel">Cancel</button><button type="button" class="nl-btn nl-ok">Insert</button></div></div>';
    document.body.appendChild(dlg);
    var input = dlg.querySelector('.nl-in'), prev = dlg.querySelector('.nl-preview'), disp = dlg.querySelector('.nl-display');
    var tex = '';
    disp.checked = !!display;
    if (editNode) {
      input.value = editNode.getAttribute('data-ascii') || editNode.getAttribute('data-tex') || '';
      disp.checked = editNode.getAttribute('data-display') === '1';
      dlg.querySelector('.nl-ok').textContent = 'Update';
    }
    function paint() {
      var v = input.value;
      tex = editNode && !editNode.getAttribute('data-ascii') && v === (editNode.getAttribute('data-tex') || '') ? v : asciiToTex(v);
      prev.textContent = '';
      if (!v.trim()) { prev.classList.add('is-empty'); return; }
      prev.classList.remove('is-empty');
      if (window.katex) { try { window.katex.render(tex, prev, { throwOnError: false, displayMode: false }); return; } catch (e) { /* plain */ } }
      prev.textContent = tex;
    }
    function done(ok) {
      var v = input.value.trim(), t = tex, d = disp.checked;
      closeMath();
      try { ed.focus({ preventScroll: true }); } catch (e) { ed.focus(); }
      if (ok && v) {
        if (ed.__range) { var s = sel(); s.removeAllRanges(); s.addRange(ed.__range); }
        insertMath(ed, t, v, d, editNode);
      }
    }
    input.addEventListener('input', paint);
    input.addEventListener('keydown', function (e) {
      e.stopPropagation();
      if (e.key === 'Enter') { e.preventDefault(); done(true); }
      else if (e.key === 'Escape') { e.preventDefault(); done(false); }
    });
    dlg.addEventListener('mousedown', function (e) { if (e.target.closest('.nl-part,.nl-btn')) e.preventDefault(); });
    dlg.addEventListener('click', function (e) {
      var part = e.target.closest('.nl-part');
      if (part) {
        var p = MATH_PARTS[+part.getAttribute('data-i')][1], at = input.selectionStart == null ? input.value.length : input.selectionStart;
        var sp = input.value && !/\s$/.test(input.value.slice(0, at)) && /^[A-Za-z(]/.test(p) ? ' ' : '';
        input.value = input.value.slice(0, at) + sp + p + input.value.slice(input.selectionEnd == null ? at : input.selectionEnd);
        paint(); input.focus();
        return;
      }
      if (e.target.closest('.nl-ok')) done(true);
      else if (e.target.closest('.nl-cancel') || e.target.closest('.nl-scrim')) done(false);
    });
    mathDlg = dlg;
    paint();
    setTimeout(function () { input.focus(); input.select(); }, 20);
  }

  /* ------------------------------------------------------------------ links */
  var linkPop = null;
  function closeLink() { if (linkPop && linkPop.parentNode) linkPop.parentNode.removeChild(linkPop); linkPop = null; }
  document.addEventListener('mousedown', function (e) { if (linkPop && !linkPop.contains(e.target)) closeLink(); }, true);

  function openLink(ed) {
    var r = rangeNow();
    if (!r || !ed.contains(r.commonAncestorContainer)) { ensureCaret(ed); r = rangeNow(); }
    if (!r) return;
    ed.__range = r.cloneRange();
    var existing = ancestor(r.startContainer, ed, ['A']);
    closeLink();
    var pop = document.createElement('div');
    pop.className = 'neb-live-pop neb-live-link';
    pop.innerHTML = '<input class="nl-in" type="text" autocomplete="off" placeholder="Paste a link">' +
      '<button type="button" class="nl-btn nl-ok">' + (existing ? 'Update' : 'Add') + '</button>' +
      (existing ? '<button type="button" class="nl-btn nl-rm">Remove</button>' : '');
    document.body.appendChild(pop);
    var input = pop.querySelector('.nl-in');
    if (existing) input.value = existing.getAttribute('href') || '';
    var rect = r.getBoundingClientRect();
    if (!rect || (!rect.width && !rect.height)) rect = ed.getBoundingClientRect();
    pop.style.left = Math.max(8, Math.min(window.innerWidth - 348, rect.left)) + 'px';
    pop.style.top = Math.max(8, Math.min(window.innerHeight - 64, rect.bottom + 8)) + 'px';
    function restore() { try { ed.focus({ preventScroll: true }); } catch (e) { ed.focus(); } var s = sel(); s.removeAllRanges(); s.addRange(ed.__range); }
    function apply() {
      var url = input.value.trim();
      if (url && !/^(https?:|mailto:|\/|#)/i.test(url)) url = 'https://' + url;
      closeLink(); restore();
      if (!url) return;
      if (existing) { existing.setAttribute('href', url); changed(ed); return; }
      if (ed.__range.collapsed) insertHTML(ed, '<a href="' + url.replace(/"/g, '&quot;') + '">' + url.replace(/</g, '&lt;') + '</a>');
      else exec(ed, 'createLink', url);
    }
    pop.addEventListener('mousedown', function (e) { if (e.target.closest('.nl-btn')) e.preventDefault(); });
    pop.addEventListener('click', function (e) {
      if (e.target.closest('.nl-ok')) apply();
      else if (e.target.closest('.nl-rm')) { closeLink(); restore(); exec(ed, 'unlink'); }
    });
    input.addEventListener('keydown', function (e) {
      e.stopPropagation();
      if (e.key === 'Enter') { e.preventDefault(); apply(); }
      else if (e.key === 'Escape') { e.preventDefault(); closeLink(); restore(); }
    });
    linkPop = pop;
    setTimeout(function () { input.focus(); input.select(); }, 20);
  }

  /* ------------------------------------------------------------------ commands */
  function format(target, cmd) {
    var ed = targetEd(target); if (!ed) return false;
    switch (cmd) {
      case 'bold': exec(ed, 'bold'); break;
      case 'italic': exec(ed, 'italic'); break;
      case 'underline': exec(ed, 'underline'); break;
      case 'strike': case 'strikethrough': exec(ed, 'strikeThrough'); break;
      case 'code': toggleCode(ed); break;
      case 'codeblock': toggleBlock(ed, 'pre'); break;
      case 'h2': case 'heading': toggleBlock(ed, 'h2'); break;
      case 'h3': toggleBlock(ed, 'h3'); break;
      case 'quote': toggleBlock(ed, 'blockquote'); break;
      case 'ul': exec(ed, 'insertUnorderedList'); break;
      case 'ol': exec(ed, 'insertOrderedList'); break;
      case 'link': openLink(ed); break;
      case 'math': openMath(ed, null, false); break;
      case 'mathblock': openMath(ed, null, true); break;
      case 'hr': insertHTML(ed, '<hr><p><br></p>'); break;
      case 'table': insertHTML(ed, '<table><thead><tr><th>Heading</th><th>Heading</th></tr></thead><tbody><tr><td>Cell</td><td>Cell</td></tr></tbody></table><p><br></p>'); break;
      case 'spoiler': toggleSpoiler(ed); break;
      case 'clear': exec(ed, 'removeFormat'); break;
      case 'step':
        insertHTML(ed, '<p><b data-step="1">Step ' + (ed.querySelectorAll('[data-step]').length + 1) + ':</b>&nbsp;</p>');
        break;
      default: return false;
    }
    refreshBar();
    return true;
  }

  function stateOf(ed) {
    var r = rangeNow(), st = {};
    if (!r || !ed.contains(r.startContainer)) return st;
    var a = r.startContainer;
    try {
      st.bold = document.queryCommandState('bold'); st.italic = document.queryCommandState('italic');
      st.underline = document.queryCommandState('underline'); st.strike = document.queryCommandState('strikeThrough');
      st.ul = document.queryCommandState('insertUnorderedList'); st.ol = document.queryCommandState('insertOrderedList');
    } catch (e) { /* ignore */ }
    st.code = !!ancestor(a, ed, ['CODE']);
    st.h2 = !!ancestor(a, ed, ['H2', 'H3']);
    st.quote = !!ancestor(a, ed, ['BLOCKQUOTE']);
    st.codeblock = !!ancestor(a, ed, ['PRE']);
    st.link = !!ancestor(a, ed, ['A']);
    return st;
  }

  /* ------------------------------------------------------------------ the floating bar over a selection */
  var bar = null, barEd = null;
  var BAR = [['bold', 'format_bold', 'Bold'], ['italic', 'format_italic', 'Italic'], ['underline', 'format_underlined', 'Underline'],
    ['strike', 'format_strikethrough', 'Strikethrough'], ['code', 'code', 'Code'], ['link', 'link', 'Link'], ['h2', 'title', 'Heading'], ['quote', 'format_quote', 'Quote'], ['math', 'function', 'Formula']];

  function ensureBar() {
    if (bar) return bar;
    bar = document.createElement('div');
    bar.className = 'neb-live-bar';
    bar.hidden = true;
    bar.setAttribute('role', 'toolbar'); bar.setAttribute('aria-label', 'Format');
    bar.innerHTML = BAR.map(function (b) {
      return '<button type="button" class="nl-tool" data-cmd="' + b[0] + '" aria-label="' + b[2] + '" title="' + b[2] + '"><span class="material-symbols-outlined" aria-hidden="true">' + b[1] + '</span></button>';
    }).join('');
    bar.addEventListener('mousedown', function (e) { e.preventDefault(); });
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('.nl-tool');
      if (b && barEd) format(barEd, b.getAttribute('data-cmd'));
    });
    document.body.appendChild(bar);
    return bar;
  }
  function refreshBar() {
    var s = sel();
    if (!s || !s.rangeCount || s.isCollapsed || mathDlg || linkPop) { if (bar) bar.hidden = true; return; }
    var r = s.getRangeAt(0), ed = edOfNode(r.commonAncestorContainer);
    if (!ed || ed.getAttribute('data-neb-bar') === '0') { if (bar) bar.hidden = true; return; }
    var rect = r.getBoundingClientRect();
    if (!rect.width && !rect.height) { if (bar) bar.hidden = true; return; }
    ensureBar();
    barEd = ed;
    var st = stateOf(ed);
    [].forEach.call(bar.querySelectorAll('.nl-tool'), function (b) { b.classList.toggle('is-on', !!st[b.getAttribute('data-cmd')]); });
    bar.hidden = false;
    var w = bar.offsetWidth, h = bar.offsetHeight;
    bar.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, rect.left + rect.width / 2 - w / 2)) + 'px';
    var top = rect.top - h - 10;
    bar.style.top = (top < 8 ? rect.bottom + 10 : top) + 'px';
  }
  var barTimer = 0;
  document.addEventListener('selectionchange', function () {
    clearTimeout(barTimer);
    barTimer = setTimeout(function () {
      refreshBar();
      var r = rangeNow();
      var ed = r && edOfNode(r.commonAncestorContainer);
      if (ed) ed.__range = r.cloneRange();
    }, 60);
  });
  window.addEventListener('scroll', function () { if (bar && !bar.hidden) refreshBar(); }, true);

  /* ------------------------------------------------------------------ the editable surface */
  function forward(ta, e) {
    var ev = new KeyboardEvent(e.type, { key: e.key, code: e.code, shiftKey: e.shiftKey, ctrlKey: e.ctrlKey, altKey: e.altKey, metaKey: e.metaKey, repeat: e.repeat, bubbles: true, cancelable: true });
    if (!ta.dispatchEvent(ev)) e.preventDefault();
  }

  function setup(ed, ta) {
    if (ed._nebLive) return ed._nebLive;
    var c = ed._nebLive = { ta: ta || null, md: '', dirty: true, id: ++uid };
    ed.setAttribute('data-neb-live', '1');
    ed.setAttribute('contenteditable', 'true');
    ed.setAttribute('role', 'textbox');
    ed.setAttribute('aria-multiline', 'true');
    ed.classList.add('neb-live');
    try { document.execCommand('defaultParagraphSeparator', false, 'p'); } catch (e) { /* ignore */ }

    /* One sync per frame: the Markdown copy (and every listener on the hidden textarea) runs once however fast
       the person types, so a key never waits for a full-document conversion. Reading `value` or leaving the field
       always flushes first, so nothing reads stale text. */
    c.pending = false; c.raf = 0;
    c.flush = function () {
      if (c.raf) { cancelAnimationFrame(c.raf); c.raf = 0; }
      if (!c.ta || !c.pending) return;
      c.pending = false;
      var md = toMarkdown(ed);
      c.md = md; c.dirty = false;
      NATIVE_VALUE.set.call(c.ta, md);
      c.ta.dispatchEvent(new Event('input', { bubbles: true }));
    };
    ed.addEventListener('input', function (e) {
      /* "- ", "1. ", "# ", "> " at the start of a line become a list, heading or quote, no code typed. */
      if (e && (e.inputType === 'insertText' || e.inputType === 'insertCompositionText') && (e.data == null || /\s$/.test(e.data) || e.data === '\u00a0') && autoformat(ed)) return;
      c.dirty = true;
      ed.classList.toggle('is-empty', isEmpty(ed));
      if (c.ta) {
        c.pending = true;
        if (!c.raf) c.raf = requestAnimationFrame(function () { c.raf = 0; c.flush(); });
      }
    });

    ed.addEventListener('keydown', function (e) {
      var k = e.key.toLowerCase(), mod = e.ctrlKey || e.metaKey;
      if (mod && !e.altKey && !e.shiftKey && k === 'k') { e.preventDefault(); format(ed, 'link'); return; }
      if (mod && !e.altKey && !e.shiftKey && k === 'e') { e.preventDefault(); format(ed, 'code'); return; }
      if (mod && e.shiftKey && k === 'x') { e.preventDefault(); format(ed, 'strike'); return; }
      if (mod && e.shiftKey && k === 'm') { e.preventDefault(); format(ed, 'math'); return; }
      if (e.key === 'Backspace') {
        /* an empty heading, quote or code block steps back to a plain line first */
        var r = rangeNow();
        if (r && r.collapsed) {
          var blk = ancestor(r.startContainer, ed, ['H2', 'H3', 'BLOCKQUOTE', 'PRE']);
          if (blk && r.startOffset === 0 && !(blk.textContent || '').replace(/\u200b/g, '')) { e.preventDefault(); exec(ed, 'formatBlock', 'P'); return; }
        }
      }
      if (c.ta) forward(c.ta, e);
    });
    ed.addEventListener('keyup', function (e) { if (c.ta) forward(c.ta, e); });
    ed.addEventListener('focus', function () { ed.classList.add('neb-focus'); if (c.ta) c.ta.dispatchEvent(new FocusEvent('focus')); });
    ed.addEventListener('blur', function () {
      ed.classList.remove('neb-focus');
      if (c.flush) c.flush();
      var r = rangeNow(); if (r && ed.contains(r.commonAncestorContainer)) ed.__range = r.cloneRange();
      if (c.ta) c.ta.dispatchEvent(new FocusEvent('blur'));
    });
    ed.addEventListener('dblclick', function (e) {
      var m = e.target.closest && e.target.closest('.neb-math');
      if (m && ed.contains(m)) { e.preventDefault(); openMath(ed, m); }
    });
    ed.addEventListener('click', function (e) {
      var sp = e.target.closest && e.target.closest('.neb-spoiler');
      if (sp) sp.classList.toggle('is-open');
      var a = e.target.closest && e.target.closest('a');
      if (a && ed.contains(a)) e.preventDefault();
    });
    ed.addEventListener('paste', function (e) {
      var cd = e.clipboardData;
      if (!cd || e.defaultPrevented) return;
      if (cd.files && cd.files.length) return;
      var html = cd.getData('text/html'), text = cd.getData('text/plain');
      if (!html && !text) return;
      e.preventDefault();
      if (html && /<(b|strong|i|em|a|ul|ol|h\d|blockquote|code|pre|table)\b/i.test(html) && !/urn:schemas-microsoft-com/i.test(html)) {
        var tmp = document.createElement('div');
        tmp.appendChild(clean(html.replace(/^[\s\S]*?<body[^>]*>|<\/body>[\s\S]*$/gi, '')));
        insertHTML(ed, tmp.innerHTML);
      } else if (/(\*\*[^*\n]+\*\*|^#{1,3}\s|^\s*[-*]\s|^\s*\d+\.\s|`[^`\n]+`|\$[^$\n]+\$|\[[^\]]+\]\(https?:)/m.test(text)) {
        var holder = document.createElement('div');
        fromMarkdown(holder, text);
        insertHTML(ed, holder.innerHTML);
      } else {
        insertText(ed, text);
      }
    });
    ed.classList.toggle('is-empty', isEmpty(ed));
    return c;
  }

  var COPY_STYLE = ['fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing', 'color', 'backgroundColor',
    'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
    'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle', 'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
    'borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius', 'textAlign'];

  /* Textarea mode: hide the textarea, mirror it, and keep its API alive for the code that already talks to it. */
  function attach(ta) {
    if (!ta) return null;
    if (ta.__neb) return ta.__neb.ed;
    var ed = document.createElement('div');
    ed.className = 'neb-live-surface ' + (ta.className || '');
    var cs = getComputedStyle(ta);
    COPY_STYLE.forEach(function (p) { try { ed.style[p] = cs[p]; } catch (e) { /* ignore */ } });
    var rows = parseInt(ta.getAttribute('rows'), 10) || 2, lh = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.5) || 22;
    var minH = parseFloat(cs.minHeight);
    if (!ta.hasAttribute('data-autoheight')) ed.style.minHeight = (minH > 0 ? minH : rows * lh + (parseFloat(cs.paddingTop) || 0) + (parseFloat(cs.paddingBottom) || 0)) + 'px';
    ed.style.setProperty('--nl-pt', cs.paddingTop);
    ed.style.setProperty('--nl-pl', cs.paddingLeft);
    var max = parseInt(ta.getAttribute('data-autoheight-max'), 10);
    if (max > 0) { ed.style.maxHeight = max + 'px'; ed.style.overflowY = 'auto'; }
    var ph = ta.getAttribute('placeholder'); if (ph) ed.setAttribute('data-placeholder', ph);
    if (ta.getAttribute('aria-label')) ed.setAttribute('aria-label', ta.getAttribute('aria-label'));
    ta.parentNode.insertBefore(ed, ta);
    ta.classList.add('neb-live-src');
    ta.setAttribute('tabindex', '-1');
    var c = setup(ed, ta);
    ta.__neb = { ed: ed };
    var start = ta.value || '';
    fromMarkdown(ed, start);
    ed.classList.toggle('is-empty', isEmpty(ed));
    c.md = start; c.dirty = false;

    var currentMd = function () { if (c.dirty) { c.md = toMarkdown(ed); c.dirty = false; } return c.md; };
    Object.defineProperty(ta, 'value', {
      configurable: true,
      get: function () { return currentMd(); },
      set: function (v) {
        var next = v == null ? '' : String(v);
        /* Writing back the text the editor already holds must not rebuild it: that is what moved the caret and
           flashed the formatting for a frame. */
        var same = next === currentMd();
        NATIVE_VALUE.set.call(ta, next);
        if (same) return;
        if (c.raf) { cancelAnimationFrame(c.raf); c.raf = 0; }
        c.pending = false;
        c.md = NATIVE_VALUE.get.call(ta); c.dirty = false;
        fromMarkdown(ed, c.md);
        ed.classList.toggle('is-empty', isEmpty(ed));
      }
    });
    Object.defineProperty(ta, 'selectionStart', { configurable: true, get: function () { return currentMd().length; }, set: function () {} });
    Object.defineProperty(ta, 'selectionEnd', { configurable: true, get: function () { return currentMd().length; }, set: function () {} });
    ta.setSelectionRange = function () {};
    ta.select = function () { try { ed.focus(); } catch (e) { /* ignore */ } var r = document.createRange(); r.selectNodeContents(ed); var s = sel(); s.removeAllRanges(); s.addRange(r); };
    ta.focus = function () { ensureCaret(ed); };
    ta.setRangeText = function (text) { insertText(ed, String(text)); };
    if (ta.form) ta.form.addEventListener('reset', function () { setTimeout(function () { fromMarkdown(ed, ''); ed.classList.add('is-empty'); }, 0); });
    return ed;
  }

  function bind(el) {
    if (!el || el._nebLive) return el;
    setup(el, null);
    return el;
  }

  /* Text of the current line before the caret (for @mentions), a way to swap it out, and where the caret is. */
  function textBefore(target) {
    var ed = targetEd(target), r = rangeNow();
    if (!ed || !r || !r.collapsed || !ed.contains(r.startContainer)) return null;
    var n = r.startContainer;
    if (n.nodeType !== 3) return '';
    return n.nodeValue.slice(0, r.startOffset).replace(/\u200b/g, '');
  }
  function replaceBefore(target, count, text) {
    var ed = targetEd(target), r = rangeNow();
    if (!ed || !r || r.startContainer.nodeType !== 3) return;
    var n = r.startContainer, off = r.startOffset, from = Math.max(0, off - count);
    n.nodeValue = n.nodeValue.slice(0, from) + text + n.nodeValue.slice(off);
    var nr = document.createRange(); nr.setStart(n, from + text.length); nr.collapse(true);
    var s = sel(); s.removeAllRanges(); s.addRange(nr);
    changed(ed);
  }
  function caretRect(target) {
    var ed = targetEd(target), r = rangeNow();
    if (!ed || !r) return null;
    var rect = r.getClientRects()[0];
    if (rect) return rect;
    var span = document.createElement('span'); span.textContent = '\u200b';
    var c = r.cloneRange(); c.insertNode(span);
    rect = span.getBoundingClientRect();
    var p = span.parentNode; p.removeChild(span); p.normalize();
    var s = sel(); s.removeAllRanges(); s.addRange(r);
    return rect;
  }

  function boot() {
    [].forEach.call(document.querySelectorAll('textarea[data-live]'), function (ta) { attach(ta); });
    if (!('MutationObserver' in window)) return;
    /* reply boxes are built later by page scripts: attach to them as they appear */
    new MutationObserver(function (list) {
      list.forEach(function (m) {
        [].forEach.call(m.addedNodes, function (n) {
          if (n.nodeType !== 1) return;
          if (n.matches && n.matches('textarea[data-live]')) attach(n);
          else if (n.querySelectorAll) [].forEach.call(n.querySelectorAll('textarea[data-live]'), function (ta) { attach(ta); });
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();

  window.NebLive = {
    attach: attach, bind: bind, format: format, insertText: insertText, insertMath: insertMath, openMath: openMath,
    toMarkdown: toMarkdown, fromMarkdown: fromMarkdown, asciiToTex: asciiToTex,
    state: function (t) { var e = targetEd(t); return e ? stateOf(e) : {}; },
    has: function (ta) { return !!(ta && ta.__neb); }, editor: targetEd,
    textBefore: textBefore, replaceBefore: replaceBefore, caretRect: caretRect
  };
})();
