import { tokenize, makeParser, pyErr, MAX_STEPS } from './python-parse.js';

const BREAK = { sig: 'break' };
const CONTINUE = { sig: 'continue' };

function typeName(v) {
  if (v === null) return 'NoneType';
  if (typeof v === 'number') return Number.isInteger(v) ? 'int' : 'float';
  if (typeof v === 'string') return 'str';
  if (typeof v === 'boolean') return 'bool';
  if (Array.isArray(v)) return 'list';
  if (v && v.range) return 'range';
  if (v && (v.params || v.builtin)) return 'function';
  return 'object';
}

function pyStr(v) {
  if (v === null) return 'None';
  if (v === true) return 'True';
  if (v === false) return 'False';
  if (typeof v === 'number') return String(v);
  if (typeof v === 'string') return v;
  if (Array.isArray(v)) return '[' + v.map(pyRepr).join(', ') + ']';
  if (v && v.range) return 'range(' + v.start + ', ' + v.stop + ')';
  if (v && (v.params || v.builtin)) return '<function ' + (v.name || v.builtin) + '>';
  return String(v);
}

function pyRepr(v) {
  if (typeof v === 'string') return "'" + v.replace(/\\/g, '\\\\').replace(/'/g, "\\'") + "'";
  return pyStr(v);
}

function truthy(v) {
  if (v === null || v === false) return false;
  if (v === true) return true;
  if (typeof v === 'number') return v !== 0;
  if (typeof v === 'string') return v.length > 0;
  if (Array.isArray(v)) return v.length > 0;
  return true;
}

class Env {
  constructor(parent) {
    this.vars = new Map();
    this.parent = parent;
  }
  get(name, line) {
    if (this.vars.has(name)) return this.vars.get(name);
    if (this.parent) return this.parent.get(name, line);
    throw pyErr(line, "NameError: name '" + name + "' is not defined");
  }
  set(name, value) { this.vars.set(name, value); }
}

const BUILTIN_NAMES = ['print', 'input', 'str', 'int', 'float', 'abs', 'min', 'max', 'sum', 'len', 'range'];

export function runPython(code, opts = {}) {
  const output = [];
  const onOutput = opts.onOutput || (() => {});
  const inputs = Array.isArray(opts.inputs) ? opts.inputs.slice() : null;
  let steps = 0;
  let depth = 0;

  function emit(text) {
    output.push(text);
    onOutput(text);
  }

  function step(line) {
    if (++steps > MAX_STEPS) throw pyErr(line, 'RuntimeError: program ran too many steps (100,000) — check for an infinite loop!');
  }

  function checkNum(v, line, what) {
    if (typeof v !== 'number') throw pyErr(line, 'TypeError: ' + what + ' needs a number, not ' + typeName(v));
    return v;
  }

  function iterate(value, line, fn) {
    if (Array.isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        step(line);
        const sig = fn(value[i]);
        if (sig === BREAK) return;
        if (sig && sig.ret !== undefined) return sig;
      }
      return;
    }
    if (typeof value === 'string') {
      for (let i = 0; i < value.length; i++) {
        step(line);
        const sig = fn(value[i]);
        if (sig === BREAK) return;
        if (sig && sig.ret !== undefined) return sig;
      }
      return;
    }
    if (value && value.range) {
      const { start, stop, stepBy } = value;
      for (let i = start; stepBy > 0 ? i < stop : i > stop; i += stepBy) {
        step(line);
        const sig = fn(i);
        if (sig === BREAK) return;
        if (sig && sig.ret !== undefined) return sig;
      }
      return;
    }
    throw pyErr(line, "TypeError: '" + typeName(value) + "' object is not iterable");
  }

  function toList(value, line) {
    if (Array.isArray(value)) return value;
    if (typeof value === 'string') return value.split('');
    if (value && value.range) {
      const arr = [];
      iterate(value, line, (v) => { arr.push(v); });
      return arr;
    }
    throw pyErr(line, "TypeError: '" + typeName(value) + "' object is not iterable");
  }

  function callBuiltin(name, args, line) {
    if (name === 'print') { emit(args.map(pyStr).join(' ')); return null; }
    if (name === 'input') {
      if (args.length && typeof args[0] === 'string') emit(args[0]);
      if (inputs && inputs.length) return String(inputs.shift());
      if (opts.inputValue !== undefined) return String(opts.inputValue);
      return '';
    }
    if (name === 'str') return args.length ? pyStr(args[0]) : '';
    if (name === 'int') {
      const v = args[0];
      if (typeof v === 'number') return Math.trunc(v);
      if (typeof v === 'boolean') return v ? 1 : 0;
      if (typeof v === 'string') {
        const n = parseInt(v.trim(), 10);
        if (Number.isNaN(n) || !/^[+-]?\d+$/.test(v.trim())) throw pyErr(line, "ValueError: invalid literal for int(): '" + v + "'");
        return n;
      }
      throw pyErr(line, "TypeError: int() can't convert " + typeName(v));
    }
    if (name === 'float') {
      const v = args[0];
      if (typeof v === 'number') return v;
      if (typeof v === 'string') {
        const n = parseFloat(v.trim());
        if (Number.isNaN(n)) throw pyErr(line, "ValueError: could not convert string to float: '" + v + "'");
        return n;
      }
      throw pyErr(line, "TypeError: float() can't convert " + typeName(v));
    }
    if (name === 'abs') return Math.abs(checkNum(args[0], line, 'abs()'));
    if (name === 'len') {
      const v = args[0];
      if (typeof v === 'string' || Array.isArray(v)) return v.length;
      throw pyErr(line, "TypeError: object of type '" + typeName(v) + "' has no len()");
    }
    if (name === 'min' || name === 'max') {
      let vals = args.length === 1 ? toList(args[0], line) : args;
      if (!vals.length) throw pyErr(line, 'ValueError: ' + name + '() got an empty list');
      let best = vals[0];
      for (const v of vals) {
        if (name === 'min' ? v < best : v > best) best = v;
      }
      return best;
    }
    if (name === 'sum') {
      const vals = toList(args[0], line);
      let total = 0;
      for (const v of vals) total += checkNum(v, line, 'sum()');
      return total;
    }
    if (name === 'range') {
      const nums = args.map((a) => checkNum(a, line, 'range()'));
      let start = 0;
      let stop = 0;
      let stepBy = 1;
      if (nums.length === 1) stop = nums[0];
      else if (nums.length === 2) { start = nums[0]; stop = nums[1]; }
      else if (nums.length === 3) { start = nums[0]; stop = nums[1]; stepBy = nums[2]; }
      else throw pyErr(line, 'TypeError: range() takes 1 to 3 numbers');
      if (stepBy === 0) throw pyErr(line, 'ValueError: range() step cannot be zero');
      return { range: true, start, stop, stepBy };
    }
    throw pyErr(line, "NameError: name '" + name + "' is not defined");
  }

  function binOp(op, a, b, line) {
    if (op === '+') {
      if (typeof a === 'number' && typeof b === 'number') return a + b;
      if (typeof a === 'string' && typeof b === 'string') return a + b;
      if (Array.isArray(a) && Array.isArray(b)) return a.concat(b);
      if (typeof a === 'string' || typeof b === 'string') throw pyErr(line, 'TypeError: can only join text with text — use str() to convert numbers first');
      throw pyErr(line, "TypeError: unsupported '+' between " + typeName(a) + ' and ' + typeName(b));
    }
    if (op === '*') {
      if (typeof a === 'number' && typeof b === 'number') return a * b;
      if (typeof a === 'string' && typeof b === 'number') return a.repeat(Math.max(0, Math.trunc(b)));
      if (typeof a === 'number' && typeof b === 'string') return b.repeat(Math.max(0, Math.trunc(a)));
      throw pyErr(line, "TypeError: unsupported '*' between " + typeName(a) + ' and ' + typeName(b));
    }
    checkNum(a, line, "'" + op + "'");
    checkNum(b, line, "'" + op + "'");
    if (op === '-') return a - b;
    if (op === '/') {
      if (b === 0) throw pyErr(line, 'ZeroDivisionError: division by zero');
      return a / b;
    }
    if (op === '//') {
      if (b === 0) throw pyErr(line, 'ZeroDivisionError: division by zero');
      return Math.floor(a / b);
    }
    if (op === '%') {
      if (b === 0) throw pyErr(line, 'ZeroDivisionError: modulo by zero');
      return ((a % b) + b) % b;
    }
    if (op === '**') return Math.pow(a, b);
    throw pyErr(line, "SyntaxError: unknown operator '" + op + "'");
  }

  function boolToInt(v) {
    return typeof v === 'boolean' ? (v ? 1 : 0) : v;
  }

  function compare(op, a, b, line) {
    if (op === '==') return pyEquals(a, b);
    if (op === '!=') return !pyEquals(a, b);
    if (op === 'in') {
      if (typeof b === 'string') {
        if (typeof a !== 'string') throw pyErr(line, "TypeError: 'in <string>' requires string as left operand, not " + typeName(a));
        return b.includes(a);
      }
      if (Array.isArray(b)) return b.some((x) => pyEquals(a, x));
      throw pyErr(line, "TypeError: 'in' needs a list or text on the right side");
    }
    const na = boolToInt(a);
    const nb = boolToInt(b);
    if ((typeof na === 'number' && typeof nb === 'number') || (typeof na === 'string' && typeof nb === 'string')) {
      if (op === '<') return na < nb;
      if (op === '<=') return na <= nb;
      if (op === '>') return na > nb;
      if (op === '>=') return na >= nb;
    }
    throw pyErr(line, "TypeError: can't compare " + typeName(a) + ' with ' + typeName(b));
  }

  function pyEquals(a, b) {
    if (Array.isArray(a) && Array.isArray(b)) {
      return a.length === b.length && a.every((v, i) => pyEquals(v, b[i]));
    }
    return boolToInt(a) === boolToInt(b);
  }

  function getIndex(obj, idx, line) {
    if (Array.isArray(obj) || typeof obj === 'string') {
      checkNum(idx, line, 'index');
      let i = Math.trunc(idx);
      if (i < 0) i += obj.length;
      if (i < 0 || i >= obj.length) throw pyErr(line, (Array.isArray(obj) ? 'IndexError: list' : 'IndexError: string') + ' index out of range');
      return obj[i];
    }
    throw pyErr(line, "TypeError: '" + typeName(obj) + "' is not indexable");
  }

  function evalExpr(node, env) {
    step(node.line);
    switch (node.t) {
      case 'num': case 'str': return node.value;
      case 'const': return node.value;
      case 'name': {
        if (BUILTIN_NAMES.includes(node.name) && !envHas(env, node.name)) return { builtin: node.name };
        return env.get(node.name, node.line);
      }
      case 'list': return node.items.map((it) => evalExpr(it, env));
      case 'fstr': return node.parts.map((p) => (p.lit !== undefined ? p.lit : pyStr(evalExpr(p.expr, env)))).join('');
      case 'unary': {
        const v = evalExpr(node.value, env);
        checkNum(v, node.line, "unary '" + node.op + "'");
        return node.op === '-' ? -v : v;
      }
      case 'not': return !truthy(evalExpr(node.value, env));
      case 'logic': {
        const left = evalExpr(node.left, env);
        if (node.op === 'and') return truthy(left) ? evalExpr(node.right, env) : left;
        return truthy(left) ? left : evalExpr(node.right, env);
      }
      case 'bin': return binOp(node.op, evalExpr(node.left, env), evalExpr(node.right, env), node.line);
      case 'compare': {
        let prev = evalExpr(node.operands[0], env);
        for (let i = 0; i < node.ops.length; i++) {
          const cur = evalExpr(node.operands[i + 1], env);
          if (!compare(node.ops[i], prev, cur, node.line)) return false;
          prev = cur;
        }
        return true;
      }
      case 'index': return getIndex(evalExpr(node.obj, env), evalExpr(node.index, env), node.line);
      case 'attr': {
        const obj = evalExpr(node.obj, env);
        return { method: node.name, self: obj, line: node.line };
      }
      case 'call': return evalCall(node, env);
      default: throw pyErr(node.line, 'SyntaxError: invalid expression');
    }
  }

  function envHas(env, name) {
    let e = env;
    while (e) {
      if (e.vars.has(name)) return true;
      e = e.parent;
    }
    return false;
  }

  function evalCall(node, env) {
    const callee = evalExpr(node.callee, env);
    const args = node.args.map((a) => evalExpr(a, env));
    if (callee && callee.builtin) return callBuiltin(callee.builtin, args, node.line);
    if (callee && callee.method) {
      const { method, self } = callee;
      if (Array.isArray(self)) {
        if (method === 'append') {
          if (args.length !== 1) throw pyErr(node.line, 'TypeError: append() takes exactly one value');
          self.push(args[0]);
          return null;
        }
        if (method === 'pop') {
          if (!self.length) throw pyErr(node.line, 'IndexError: pop from empty list');
          return self.pop();
        }
      }
      if (typeof self === 'string') {
        if (method === 'upper') return self.toUpperCase();
        if (method === 'lower') return self.toLowerCase();
        if (method === 'strip') return self.trim();
      }
      throw pyErr(node.line, "AttributeError: '" + typeName(self) + "' object has no method '" + method + "'");
    }
    if (callee && callee.params) {
      if (args.length !== callee.params.length) {
        throw pyErr(node.line, 'TypeError: ' + callee.name + '() takes ' + callee.params.length + ' argument' + (callee.params.length === 1 ? '' : 's') + ' but ' + args.length + ' ' + (args.length === 1 ? 'was' : 'were') + ' given');
      }
      if (++depth > 200) { depth--; throw pyErr(node.line, 'RecursionError: too many nested function calls'); }
      const local = new Env(callee.globals);
      callee.params.forEach((p, i) => local.set(p, args[i]));
      const sig = execBlock(callee.body, local);
      depth--;
      if (sig === BREAK || sig === CONTINUE) {
        throw pyErr(node.line, "SyntaxError: '" + (sig === BREAK ? 'break' : 'continue') + "' outside a loop");
      }
      return sig && sig.ret !== undefined ? sig.ret : null;
    }
    throw pyErr(node.line, "TypeError: '" + typeName(callee) + "' is not callable");
  }

  function assign(target, value, env) {
    if (target.t === 'name') {
      env.set(target.name, value);
      return;
    }
    const obj = evalExpr(target.obj, env);
    const idx = evalExpr(target.index, env);
    if (!Array.isArray(obj)) throw pyErr(target.line, "TypeError: '" + typeName(obj) + "' does not support item assignment");
    let i = Math.trunc(checkNum(idx, target.line, 'index'));
    if (i < 0) i += obj.length;
    if (i < 0 || i >= obj.length) throw pyErr(target.line, 'IndexError: list assignment index out of range');
    obj[i] = value;
  }

  function execBlock(body, env) {
    for (const stmt of body) {
      const sig = execStmt(stmt, env);
      if (sig) return sig;
    }
    return null;
  }

  function execStmt(stmt, env) {
    step(stmt.line);
    switch (stmt.t) {
      case 'expr': evalExpr(stmt.expr, env); return null;
      case 'assign': assign(stmt.target, evalExpr(stmt.value, env), env); return null;
      case 'aug': {
        const cur = evalExpr(stmt.target, env);
        assign(stmt.target, binOp(stmt.op, cur, evalExpr(stmt.value, env), stmt.line), env);
        return null;
      }
      case 'if': {
        for (const br of stmt.branches) {
          if (truthy(evalExpr(br.cond, env))) return execBlock(br.body, env);
        }
        return execBlock(stmt.orelse, env);
      }
      case 'while': {
        while (truthy(evalExpr(stmt.cond, env))) {
          step(stmt.line);
          const sig = execBlock(stmt.body, env);
          if (sig === BREAK) break;
          if (sig && sig.ret !== undefined) return sig;
        }
        return null;
      }
      case 'for': {
        const iterable = evalExpr(stmt.iter, env);
        const result = iterate(iterable, stmt.line, (v) => {
          env.set(stmt.name, v);
          return execBlock(stmt.body, env);
        });
        return result && result.ret !== undefined ? result : null;
      }
      case 'def': {
        env.set(stmt.name, { params: stmt.params, body: stmt.body, name: stmt.name, globals: globalEnv });
        return null;
      }
      case 'return': return { ret: stmt.value ? evalExpr(stmt.value, env) : null };
      case 'break': return BREAK;
      case 'continue': return CONTINUE;
      default: throw pyErr(stmt.line, 'SyntaxError: unknown statement');
    }
  }

  const globalEnv = new Env(null);

  try {
    const tokens = tokenize(code);
    const ast = makeParser(tokens).parseProgram();
    const sig = execBlock(ast, globalEnv);
    if (sig === BREAK || sig === CONTINUE) throw pyErr(0, "SyntaxError: 'break' or 'continue' outside a loop");
    return { ok: true, output, steps };
  } catch (e) {
    const msg = e && e.pyMessage ? e.pyMessage : 'Error: ' + (e && e.message ? e.message : String(e));
    if (opts.onError) opts.onError(msg);
    return { ok: false, output, error: msg, steps };
  }
}
