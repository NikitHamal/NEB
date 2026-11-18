/* Small streaming-safe Markdown renderer for the admin chat test. Escapes first, then adds tags. */
(function () {
  'use strict';
  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function inline(s) {
    var codes = [];
    s = s.replace(/`([^`\n]+)`/g, function (_, c) { codes.push(c); return '\u0001' + (codes.length - 1) + '\u0001'; });
    s = s.replace(/\[([^\]\n]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
      .replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<i>$2</i>')
      .replace(/~~([^~\n]+)~~/g, '<s>$1</s>');
    return s.replace(/\u0001(\d+)\u0001/g, function (_, i) { return '<code>' + codes[+i] + '</code>'; });
  }
  function cells(line) { return line.trim().replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); }

  function render(src) {
    var lines = esc(src).split('\n'), out = [], i = 0;
    while (i < lines.length) {
      var ln = lines[i], m;
      if ((m = /^```\s*([\w+#.-]*)\s*$/.exec(ln))) {
        var code = []; i++;
        while (i < lines.length && !/^```\s*$/.test(lines[i])) code.push(lines[i++]);
        i++;
        out.push('<div class="ac-code"><div class="ac-code-bar"><span>' + (m[1] || 'text') + '</span><button type="button" class="ac-copy-code">Copy</button></div><pre><code>' + code.join('\n') + '</code></pre></div>');
      } else if ((m = /^(#{1,4})\s+(.*)$/.exec(ln))) {
        out.push('<h' + (m[1].length + 2) + '>' + inline(m[2]) + '</h' + (m[1].length + 2) + '>'); i++;
      } else if (/^\s*([-*])\s+/.test(ln) || /^\s*\d+[.)]\s+/.test(ln)) {
        var ord = /^\s*\d+[.)]\s+/.test(ln), items = [];
        while (i < lines.length && (ord ? /^\s*\d+[.)]\s+/ : /^\s*[-*]\s+/).test(lines[i])) {
          items.push('<li>' + inline(lines[i].replace(/^\s*(?:[-*]|\d+[.)])\s+/, '')) + '</li>'); i++;
        }
        out.push((ord ? '<ol>' : '<ul>') + items.join('') + (ord ? '</ol>' : '</ul>'));
      } else if (/^&gt;\s?/.test(ln)) {
        var q = [];
        while (i < lines.length && /^&gt;\s?/.test(lines[i])) q.push(inline(lines[i++].replace(/^&gt;\s?/, '')));
        out.push('<blockquote>' + q.join('<br>') + '</blockquote>');
      } else if (/^\s*\|.*\|\s*$/.test(ln) && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1])) {
        var head = cells(ln), rows = []; i += 2;
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) rows.push(cells(lines[i++]));
        out.push('<div class="ac-table"><table><thead><tr>' + head.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>');
      } else if (/^\s*(-{3,}|\*{3,})\s*$/.test(ln)) { out.push('<hr>'); i++; }
      else if (!ln.trim()) { i++; }
      else {
        var p = [];
        while (i < lines.length && lines[i].trim() && !/^(```|#{1,4}\s|\s*[-*]\s|\s*\d+[.)]\s|&gt;)/.test(lines[i])) p.push(inline(lines[i++]));
        if (!p.length) { p.push(inline(lines[i++])); }
        out.push('<p>' + p.join('<br>') + '</p>');
      }
    }
    return out.join('');
  }
  window.AcMd = { render: render, esc: esc };
})();
