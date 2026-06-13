const KEYWORDS = new Set(['if', 'elif', 'else', 'while', 'for', 'in', 'def', 'return', 'break', 'continue', 'and', 'or', 'not', 'True', 'False', 'None']);
const OPS2 = ['**', '//', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/='];
const OPS1 = '+-*/%<>=()[],:.';
const MAX_STEPS = 100000;

function pyErr(line, msg) {
  const e = new Error(msg);
  e.pyMessage = (line ? 'Line ' + line + ': ' : '') + msg;
  return e;
}

function tokenize(src) {
  const lines = String(src).replace(/\r\n?/g, '\n').split('\n');
  const tokens = [];
  const indents = [0];
  for (let li = 0; li < lines.length; li++) {
    const lineNo = li + 1;
    const line = lines[li];
    let i = 0;
    let indent = 0;
    while (i < line.length && (line[i] === ' ' || line[i] === '\t')) {
      indent += line[i] === '\t' ? 4 : 1;
      i++;
    }
    if (i >= line.length || line[i] === '#') continue;
    if (indent > indents[indents.length - 1]) {
      indents.push(indent);
      tokens.push({ type: 'indent', line: lineNo });
    } else {
      while (indent < indents[indents.length - 1]) {
        indents.pop();
        tokens.push({ type: 'dedent', line: lineNo });
      }
      if (indent !== indents[indents.length - 1]) throw pyErr(lineNo, 'IndentationError: this line does not match any indentation level');
    }
    while (i < line.length) {
      const ch = line[i];
      if (ch === ' ' || ch === '\t') { i++; continue; }
      if (ch === '#') break;
      if (ch >= '0' && ch <= '9') {
        let j = i;
        while (j < line.length && line[j] >= '0' && line[j] <= '9') j++;
        if (line[j] === '.' && line[j + 1] >= '0' && line[j + 1] <= '9') {
          j++;
          while (j < line.length && line[j] >= '0' && line[j] <= '9') j++;
        }
        tokens.push({ type: 'num', value: parseFloat(line.slice(i, j)), line: lineNo });
        i = j;
        continue;
      }
      if (/[A-Za-z_]/.test(ch)) {
        let j = i;
        while (j < line.length && /[A-Za-z0-9_]/.test(line[j])) j++;
        const word = line.slice(i, j);
        if ((word === 'f' || word === 'F') && (line[j] === '"' || line[j] === "'")) {
          const res = readString(line, j, lineNo);
          tokens.push({ type: 'fstr', value: res.value, line: lineNo });
          i = res.end;
          continue;
        }
        tokens.push({ type: KEYWORDS.has(word) ? 'kw' : 'name', value: word, line: lineNo });
        i = j;
        continue;
      }
      if (ch === '"' || ch === "'") {
        const res = readString(line, i, lineNo);
        tokens.push({ type: 'str', value: res.value, line: lineNo });
        i = res.end;
        continue;
      }
      const two = line.slice(i, i + 2);
      if (OPS2.includes(two)) {
        tokens.push({ type: 'op', value: two, line: lineNo });
        i += 2;
        continue;
      }
      if (OPS1.includes(ch)) {
        tokens.push({ type: 'op', value: ch, line: lineNo });
        i++;
        continue;
      }
      throw pyErr(lineNo, "SyntaxError: unexpected character '" + ch + "'");
    }
    tokens.push({ type: 'newline', line: lineNo });
  }
  while (indents.length > 1) {
    indents.pop();
    tokens.push({ type: 'dedent', line: lines.length });
  }
  tokens.push({ type: 'eof', line: lines.length });
  return tokens;
}

function readString(line, start, lineNo) {
  const quote = line[start];
  let i = start + 1;
  let out = '';
  while (i < line.length) {
    const ch = line[i];
    if (ch === '\\') {
      const nx = line[i + 1];
      if (nx === 'n') out += '\n';
      else if (nx === 't') out += '\t';
      else if (nx === '\\') out += '\\';
      else if (nx === quote) out += quote;
      else out += nx === undefined ? '\\' : nx;
      i += 2;
      continue;
    }
    if (ch === quote) return { value: out, end: i + 1 };
    out += ch;
    i++;
  }
  throw pyErr(lineNo, 'SyntaxError: unterminated string — did you forget a closing quote?');
}

function makeParser(tokens) {
  let pos = 0;
  let exprDepth = 0;
  const peek = (k) => tokens[Math.min(pos + (k || 0), tokens.length - 1)];
  const next = () => tokens[pos++];
  const isOp = (v) => peek().type === 'op' && peek().value === v;
  const isKw = (v) => peek().type === 'kw' && peek().value === v;

  function checkDepth(line) {
    if (exprDepth > 80) throw pyErr(line, 'SyntaxError: expression too deeply nested — try simplifying it');
  }

  function expectOp(v) {
    if (!isOp(v)) throw pyErr(peek().line, "SyntaxError: expected '" + v + "'");
    return next();
  }

  function expectName() {
    if (peek().type !== 'name') throw pyErr(peek().line, 'SyntaxError: expected a name here');
    return next().value;
  }

  function skipNewlines() {
    while (peek().type === 'newline') next();
  }

  function parseProgram() {
    const body = [];
    skipNewlines();
    while (peek().type !== 'eof') {
      body.push(parseStatement());
      skipNewlines();
    }
    return body;
  }

  function parseBlock(headLine) {
    expectOp(':');
    if (peek().type !== 'newline') throw pyErr(peek().line, "SyntaxError: put the body on a new indented line after ':'");
    next();
    skipNewlines();
    if (peek().type !== 'indent') throw pyErr(headLine, 'IndentationError: expected an indented block (indent with spaces)');
    next();
    const body = [];
    skipNewlines();
    while (peek().type !== 'dedent' && peek().type !== 'eof') {
      body.push(parseStatement());
      skipNewlines();
    }
    if (peek().type === 'dedent') next();
    return body;
  }

  function endStatement() {
    if (peek().type === 'newline') next();
    else if (peek().type !== 'eof' && peek().type !== 'dedent') throw pyErr(peek().line, 'SyntaxError: invalid syntax after end of statement');
  }

  function parseStatement() {
    const tok = peek();
    if (tok.type === 'kw') {
      if (tok.value === 'if') return parseIf();
      if (tok.value === 'while') {
        next();
        const cond = parseExpression();
        const body = parseBlock(tok.line);
        return { t: 'while', cond, body, line: tok.line };
      }
      if (tok.value === 'for') {
        next();
        const name = expectName();
        if (!isKw('in')) throw pyErr(tok.line, "SyntaxError: expected 'in' after the loop variable");
        next();
        const iter = parseExpression();
        const body = parseBlock(tok.line);
        return { t: 'for', name, iter, body, line: tok.line };
      }
      if (tok.value === 'def') {
        next();
        const name = expectName();
        expectOp('(');
        const params = [];
        if (!isOp(')')) {
          params.push(expectName());
          while (isOp(',')) { next(); params.push(expectName()); }
        }
        expectOp(')');
        const body = parseBlock(tok.line);
        return { t: 'def', name, params, body, line: tok.line };
      }
      if (tok.value === 'return') {
        next();
        let value = null;
        if (peek().type !== 'newline' && peek().type !== 'eof' && peek().type !== 'dedent') value = parseExpression();
        endStatement();
        return { t: 'return', value, line: tok.line };
      }
      if (tok.value === 'break' || tok.value === 'continue') {
        next();
        endStatement();
        return { t: tok.value, line: tok.line };
      }
      if (tok.value === 'elif' || tok.value === 'else') throw pyErr(tok.line, "SyntaxError: '" + tok.value + "' without a matching 'if'");
    }
    const expr = parseExpression();
    if (isOp('=')) {
      next();
      const value = parseExpression();
      if (expr.t !== 'name' && expr.t !== 'index') throw pyErr(tok.line, 'SyntaxError: you can only assign to a variable or list item');
      endStatement();
      return { t: 'assign', target: expr, value, line: tok.line };
    }
    const aug = ['+=', '-=', '*=', '/='].find((o) => isOp(o));
    if (aug) {
      next();
      const value = parseExpression();
      if (expr.t !== 'name' && expr.t !== 'index') throw pyErr(tok.line, 'SyntaxError: you can only assign to a variable or list item');
      endStatement();
      return { t: 'aug', op: aug[0], target: expr, value, line: tok.line };
    }
    endStatement();
    return { t: 'expr', expr, line: tok.line };
  }

  function parseIf() {
    const tok = next();
    const branches = [{ cond: parseExpression(), body: parseBlock(tok.line) }];
    let orelse = [];
    skipNewlines();
    while (isKw('elif')) {
      const e = next();
      branches.push({ cond: parseExpression(), body: parseBlock(e.line) });
      skipNewlines();
    }
    if (isKw('else')) {
      const e = next();
      orelse = parseBlock(e.line);
    }
    return { t: 'if', branches, orelse, line: tok.line };
  }

  function parseExpression() {
    exprDepth++;
    checkDepth(peek().line);
    const node = parseOr();
    exprDepth--;
    return node;
  }

  function parseOr() {
    let left = parseAnd();
    while (isKw('or')) {
      const line = next().line;
      left = { t: 'logic', op: 'or', left, right: parseAnd(), line };
    }
    return left;
  }

  function parseAnd() {
    let left = parseNot();
    while (isKw('and')) {
      const line = next().line;
      left = { t: 'logic', op: 'and', left, right: parseNot(), line };
    }
    return left;
  }

  function parseNot() {
    if (isKw('not')) {
      exprDepth++;
      checkDepth(peek().line);
      const line = next().line;
      const node = { t: 'not', value: parseNot(), line };
      exprDepth--;
      return node;
    }
    return parseCompare();
  }

  function parseCompare() {
    const first = parseArith();
    const ops = [];
    const operands = [first];
    while ((peek().type === 'op' && ['==', '!=', '<', '<=', '>', '>='].includes(peek().value)) || isKw('in')) {
      if (isKw('in')) { next(); ops.push('in'); }
      else ops.push(next().value);
      operands.push(parseArith());
    }
    if (!ops.length) return first;
    return { t: 'compare', ops, operands, line: first.line };
  }

  function parseArith() {
    let left = parseTerm();
    while (isOp('+') || isOp('-')) {
      const op = next();
      left = { t: 'bin', op: op.value, left, right: parseTerm(), line: op.line };
    }
    return left;
  }

  function parseTerm() {
    let left = parseFactor();
    while (isOp('*') || isOp('/') || isOp('//') || isOp('%')) {
      const op = next();
      left = { t: 'bin', op: op.value, left, right: parseFactor(), line: op.line };
    }
    return left;
  }

  function parseFactor() {
    if (isOp('-') || isOp('+')) {
      exprDepth++;
      checkDepth(peek().line);
      const op = next();
      const node = { t: 'unary', op: op.value, value: parseFactor(), line: op.line };
      exprDepth--;
      return node;
    }
    return parsePower();
  }

  function parsePower() {
    const base = parsePostfix();
    if (isOp('**')) {
      const op = next();
      return { t: 'bin', op: '**', left: base, right: parseFactor(), line: op.line };
    }
    return base;
  }

  function parsePostfix() {
    let node = parsePrimary();
    for (;;) {
      if (isOp('(')) {
        const line = next().line;
        const args = [];
        if (!isOp(')')) {
          args.push(parseExpression());
          while (isOp(',')) { next(); args.push(parseExpression()); }
        }
        expectOp(')');
        node = { t: 'call', callee: node, args, line };
      } else if (isOp('[')) {
        const line = next().line;
        const index = parseExpression();
        expectOp(']');
        node = { t: 'index', obj: node, index, line };
      } else if (isOp('.')) {
        const line = next().line;
        const name = expectName();
        node = { t: 'attr', obj: node, name, line };
      } else break;
    }
    return node;
  }

  function parsePrimary() {
    const tok = peek();
    if (tok.type === 'num') { next(); return { t: 'num', value: tok.value, line: tok.line }; }
    if (tok.type === 'str') { next(); return { t: 'str', value: tok.value, line: tok.line }; }
    if (tok.type === 'fstr') { next(); return parseFStringNode(tok); }
    if (tok.type === 'name') { next(); return { t: 'name', name: tok.value, line: tok.line }; }
    if (tok.type === 'kw') {
      if (tok.value === 'True') { next(); return { t: 'const', value: true, line: tok.line }; }
      if (tok.value === 'False') { next(); return { t: 'const', value: false, line: tok.line }; }
      if (tok.value === 'None') { next(); return { t: 'const', value: null, line: tok.line }; }
    }
    if (isOp('(')) {
      next();
      const inner = parseExpression();
      expectOp(')');
      return inner;
    }
    if (isOp('[')) {
      next();
      const items = [];
      if (!isOp(']')) {
        items.push(parseExpression());
        while (isOp(',')) {
          next();
          if (isOp(']')) break;
          items.push(parseExpression());
        }
      }
      expectOp(']');
      return { t: 'list', items, line: tok.line };
    }
    throw pyErr(tok.line, 'SyntaxError: invalid syntax');
  }

  function parseFStringNode(tok) {
    const raw = tok.value;
    const parts = [];
    let lit = '';
    let i = 0;
    while (i < raw.length) {
      const ch = raw[i];
      if (ch === '{' && raw[i + 1] === '{') { lit += '{'; i += 2; continue; }
      if (ch === '}' && raw[i + 1] === '}') { lit += '}'; i += 2; continue; }
      if (ch === '{') {
        const close = raw.indexOf('}', i + 1);
        if (close < 0) throw pyErr(tok.line, "SyntaxError: f-string is missing a closing '}'");
        if (lit) { parts.push({ lit }); lit = ''; }
        const exprSrc = raw.slice(i + 1, close).trim();
        if (!exprSrc) throw pyErr(tok.line, 'SyntaxError: empty {} in f-string');
        parts.push({ expr: parseExpressionSource(exprSrc, tok.line) });
        i = close + 1;
        continue;
      }
      lit += ch;
      i++;
    }
    if (lit) parts.push({ lit });
    return { t: 'fstr', parts, line: tok.line };
  }

  return { parseProgram, parseExpression };
}

function parseExpressionSource(src, line) {
  let toks;
  try {
    toks = tokenize(src);
  } catch (e) {
    throw pyErr(line, 'SyntaxError: bad expression inside f-string {}');
  }
  toks = toks.filter((t) => t.type !== 'newline' && t.type !== 'indent' && t.type !== 'dedent');
  toks.forEach((t) => { t.line = line; });
  const p = makeParser(toks);
  return p.parseExpression();
}

export { tokenize, makeParser, pyErr, MAX_STEPS };
