//! LaTeX (the matplotlib-mathtext-compatible subset the notes are authored in)
//! → a flat list of styled `Span`s.
//!
//! egui cannot lay out two-dimensional maths, so we linearise sensibly:
//! variables are italic, digits/operators upright, `^`/`_` become real
//! raised/lowered text, `\frac{a}{b}` becomes `a/b` (parenthesised when
//! needed), `\sqrt` becomes `√`, Greek and operators map to Unicode.
use super::model::Span;

#[derive(Clone, Copy, Default)]
struct Ctx {
    sup: bool,
    sub: bool,
    upright: bool,
    bold: bool,
}

pub fn to_spans(src: &str) -> Vec<Span> {
    let mut p = P { c: src.chars().collect(), i: 0, out: vec![] };
    p.run(Ctx::default(), false);
    p.out
}

/// Display maths: same conversion, trimmed.
pub fn to_display_spans(src: &str) -> Vec<Span> {
    let mut v = to_spans(src);
    if let Some(f) = v.first_mut() {
        f.text = f.text.trim_start().to_string();
    }
    if let Some(l) = v.last_mut() {
        l.text = l.text.trim_end().to_string();
    }
    v.retain(|s| !s.text.is_empty());
    v
}

struct P {
    c: Vec<char>,
    i: usize,
    out: Vec<Span>,
}

fn symbol(name: &str) -> Option<&'static str> {
    Some(match name {
        "alpha" => "α", "beta" => "β", "gamma" => "γ", "delta" => "δ", "epsilon" => "ε", "varepsilon" => "ε", "zeta" => "ζ",
        "eta" => "η", "theta" => "θ", "vartheta" => "ϑ", "iota" => "ι", "kappa" => "κ", "lambda" => "λ", "mu" => "μ", "nu" => "ν",
        "xi" => "ξ", "pi" => "π", "varpi" => "ϖ", "rho" => "ρ", "varrho" => "ϱ", "sigma" => "σ", "varsigma" => "ς", "tau" => "τ",
        "upsilon" => "υ", "phi" => "φ", "varphi" => "φ", "chi" => "χ", "psi" => "ψ", "omega" => "ω",
        "Gamma" => "Γ", "Delta" => "Δ", "Theta" => "Θ", "Lambda" => "Λ", "Xi" => "Ξ", "Pi" => "Π", "Sigma" => "Σ", "Upsilon" => "Υ",
        "Phi" => "Φ", "Psi" => "Ψ", "Omega" => "Ω",
        "infty" => "∞", "partial" => "∂", "nabla" => "∇", "sum" => "∑", "prod" => "∏", "int" => "∫", "oint" => "∮", "iint" => "∬",
        "hbar" => "ħ", "ell" => "ℓ", "degree" => "°", "circ" => "°", "angle" => "∠", "perp" => "⟂", "parallel" => "∥",
        "therefore" => "∴", "because" => "∵", "forall" => "∀", "exists" => "∃", "emptyset" => "∅", "varnothing" => "∅",
        "in" => "∈", "notin" => "∉", "subset" => "⊂", "supset" => "⊃", "subseteq" => "⊆", "cup" => "∪", "cap" => "∩",
        "ldots" => "…", "dots" => "…", "cdots" => "⋯", "vdots" => "⋮", "prime" => "′", "langle" => "⟨", "rangle" => "⟩",
        "lbrace" => "{", "rbrace" => "}", "lbrack" => "[", "rbrack" => "]", "lvert" => "|", "rvert" => "|", "mid" => "|", "vert" => "|",
        "lfloor" => "⌊", "rfloor" => "⌋", "lceil" => "⌈", "rceil" => "⌉", "|" => "‖", "Vert" => "‖",
        "{" => "{", "}" => "}", "%" => "%", "$" => "$", "_" => "_", "&" => "&", "#" => "#", "textdegree" => "°",
        "Re" => "ℜ", "Im" => "ℑ", "aleph" => "ℵ", "dagger" => "†", "star" => "⋆", "ast" => "∗", "bullet" => "•", "oplus" => "⊕",
        "otimes" => "⊗", "neg" => "¬", "land" => "∧", "lor" => "∨", "top" => "⊤", "square" => "□", "triangle" => "△",
        "uparrow" => "↑", "downarrow" => "↓", "leftarrow" => "←", "Leftarrow" => "⇐", "updownarrow" => "↕", "mapsto" => "↦",
        _ => return None,
    })
}

/// Binary operators / relations, rendered with surrounding spaces.
fn spaced(name: &str) -> Option<&'static str> {
    Some(match name {
        "times" => "×", "cdot" => "·", "div" => "÷", "pm" => "±", "mp" => "∓", "le" | "leq" => "≤", "ge" | "geq" => "≥",
        "ne" | "neq" => "≠", "approx" => "≈", "sim" => "∼", "simeq" => "≃", "cong" => "≅", "equiv" => "≡", "propto" => "∝",
        "to" | "rightarrow" => "→", "Rightarrow" | "implies" => "⇒", "Leftrightarrow" | "iff" => "⇔", "leftrightarrow" => "↔",
        "rightleftharpoons" => "⇌", "ll" => "≪", "gg" => "≫", "setminus" => "∖", "longrightarrow" => "⟶", "uplus" => "⊎",
        _ => return None,
    })
}

const FUNCS: &[&str] = &[
    "sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "exp", "lim", "max", "min", "det", "arcsin", "arccos", "arctan", "sinh", "cosh",
    "tanh", "sup", "inf", "gcd", "deg", "dim", "ker", "arg", "Pr",
];

fn blackboard(c: char) -> char {
    match c {
        'R' => 'ℝ', 'N' => 'ℕ', 'Z' => 'ℤ', 'Q' => 'ℚ', 'C' => 'ℂ', 'P' => 'ℙ', 'H' => 'ℍ', o => o,
    }
}

impl P {
    fn peek(&self) -> Option<char> {
        self.c.get(self.i).copied()
    }

    fn skip_ws(&mut self) {
        while self.peek().is_some_and(|c| c.is_whitespace()) {
            self.i += 1;
        }
    }

    fn emit(&mut self, text: &str, ctx: Ctx, italic: bool) {
        if text.is_empty() {
            return;
        }
        let s = Span { text: text.to_string(), math: true, italic, bold: ctx.bold, sup: ctx.sup, sub: ctx.sub, ..Default::default() };
        if let Some(last) = self.out.last_mut() {
            if last.same_style(&s) {
                last.text.push_str(text);
                return;
            }
        }
        self.out.push(s);
    }

    fn last_char(&self) -> Option<char> {
        self.out.last().and_then(|s| s.text.chars().last())
    }

    /// Emit a binary operator, padded with spaces unless in a script or in unary position.
    fn emit_op(&mut self, op: &str, ctx: Ctx) {
        let unary = match self.last_char() {
            None => true,
            Some(c) => matches!(c, '(' | '[' | '{' | '=' | ',' | '<' | '>' | '≤' | '≥' | '±' | '×' | '·' | '→' | '⇒') || c == ' ',
        };
        if ctx.sup || ctx.sub || (unary && (op == "−" || op == "+" || op == "±" || op == "∓")) {
            self.emit(op, ctx, false);
        } else {
            self.emit(&format!(" {op} "), ctx, false);
        }
    }

    fn run(&mut self, ctx: Ctx, until_brace: bool) {
        while let Some(c) = self.peek() {
            if c == '}' && until_brace {
                self.i += 1;
                return;
            }
            self.atom(ctx);
        }
    }

    /// Parse exactly one atom: a `{group}`, a command, or a single character.
    fn atom(&mut self, ctx: Ctx) {
        let Some(c) = self.peek() else { return };
        self.i += 1;
        match c {
            '{' => self.run(ctx, true),
            '}' => {}
            '\\' => self.command(ctx),
            '^' => {
                self.skip_ws();
                let before = self.out.len();
                self.atom(Ctx { sup: true, sub: false, ..ctx });
                self.fix_degree(before, ctx);
            }
            '_' => {
                self.skip_ws();
                self.atom(Ctx { sub: true, sup: false, ..ctx });
            }
            c if c.is_whitespace() => {}
            '~' => self.emit("\u{a0}", ctx, false),
            '&' => self.emit("   ", ctx, false),
            '\'' => self.emit("′", ctx, false),
            '=' | '<' | '>' => {
                let s = c.to_string();
                self.emit_op(&s, ctx)
            }
            '+' => self.emit_op("+", ctx),
            '-' => self.emit_op("−", ctx),
            '*' => self.emit("∗", ctx, false),
            ',' => {
                let next_digit = self.peek().is_some_and(|n| n.is_ascii_digit());
                self.emit(if next_digit || ctx.sup || ctx.sub { "," } else { ", " }, ctx, false);
            }
            c if c.is_alphabetic() => {
                let italic = !ctx.upright && c.is_ascii_alphabetic() || (!ctx.upright && ('α'..='ω').contains(&c));
                self.emit(&c.to_string(), ctx, italic);
            }
            c => self.emit(&c.to_string(), ctx, false),
        }
    }

    /// `^\circ` / `^{\circ}` should read as a degree sign, not a raised raised-circle.
    fn fix_degree(&mut self, before: usize, ctx: Ctx) {
        if self.out.len() == before + 1 && self.out[before].sup && self.out[before].text == "°" {
            self.out[before].sup = ctx.sup;
            self.out[before].sub = ctx.sub;
        }
    }

    fn group_plain(&mut self, ctx: Ctx) -> Vec<Span> {
        self.skip_ws();
        let saved = std::mem::take(&mut self.out);
        self.atom(ctx);
        std::mem::replace(&mut self.out, saved)
    }

    fn raw_group(&mut self) -> String {
        self.skip_ws();
        let mut s = String::new();
        if self.peek() == Some('{') {
            self.i += 1;
            let mut depth = 1;
            while let Some(c) = self.peek() {
                self.i += 1;
                match c {
                    '{' => {
                        depth += 1;
                        s.push(c)
                    }
                    '}' => {
                        depth -= 1;
                        if depth == 0 {
                            break;
                        }
                        s.push(c)
                    }
                    '\\' if self.peek() == Some(' ') => {
                        self.i += 1;
                        s.push(' ')
                    }
                    '\\' if self.peek() == Some('%') => {}
                    _ => s.push(c),
                }
            }
        } else if let Some(c) = self.peek() {
            self.i += 1;
            s.push(c);
        }
        s
    }

    fn append_spans(&mut self, spans: Vec<Span>) {
        for s in spans {
            let t = s.text.clone();
            let _ = t;
            if let Some(last) = self.out.last_mut() {
                if last.same_style(&s) {
                    last.text.push_str(&s.text);
                    continue;
                }
            }
            self.out.push(s);
        }
    }

    fn plain_of(spans: &[Span]) -> String {
        spans.iter().map(|s| s.text.as_str()).collect()
    }

    fn command(&mut self, ctx: Ctx) {
        // name: letters, or one symbol character
        let mut name = String::new();
        while let Some(c) = self.peek() {
            if c.is_ascii_alphabetic() {
                name.push(c);
                self.i += 1;
            } else {
                break;
            }
        }
        if name.is_empty() {
            match self.peek() {
                Some(c) => {
                    self.i += 1;
                    name.push(c);
                }
                None => return,
            }
        }
        let n = name.as_str();
        if let Some(op) = spaced(n) {
            self.emit_op(op, ctx);
            return;
        }
        if let Some(s) = symbol(n) {
            let italic = !ctx.upright && n.chars().next().is_some_and(|c| c.is_ascii_lowercase()) && ('α'..='ω').contains(&s.chars().next().unwrap_or('x'));
            self.emit(s, ctx, italic);
            return;
        }
        if FUNCS.contains(&n) {
            self.emit(n, Ctx { upright: true, ..ctx }, false);
            return;
        }
        match n {
            "," | ";" | ":" | "!" | " " | "quad" | "qquad" | "enspace" | "thinspace" => {
                if n != "!" {
                    self.emit(if n == "quad" || n == "qquad" { "  " } else { " " }, ctx, false);
                }
            }
            "\\" | "cr" => self.emit("\n", ctx, false),
            "left" | "right" | "big" | "Big" | "bigg" | "Bigg" | "displaystyle" | "textstyle" | "limits" | "nolimits" | "bigl" | "bigr" => {
                if matches!(n, "left" | "right" | "big" | "Big" | "bigg" | "Bigg" | "bigl" | "bigr") {
                    if self.peek() == Some('.') {
                        self.i += 1;
                    } else if self.peek() != Some('\\') {
                        // plain delimiter: the main loop will print it
                    }
                }
            }
            "frac" | "dfrac" | "tfrac" | "cfrac" => {
                let a = self.group_plain(ctx);
                let b = self.group_plain(ctx);
                let wrap = |s: &str| s.chars().any(|c| matches!(c, '+' | '−' | '±' | '=' | ' ' | '/' | ',' | '×' | '·'));
                let (pa, pb) = (Self::plain_of(&a), Self::plain_of(&b));
                let (wa, wb) = (wrap(pa.trim()), wrap(pb.trim()));
                if wa {
                    self.emit("(", ctx, false);
                }
                self.append_spans(a);
                if wa {
                    self.emit(")", ctx, false);
                }
                self.emit("/", ctx, false);
                if wb {
                    self.emit("(", ctx, false);
                }
                self.append_spans(b);
                if wb {
                    self.emit(")", ctx, false);
                }
            }
            "sqrt" => {
                let mut index = None;
                self.skip_ws();
                if self.peek() == Some('[') {
                    self.i += 1;
                    let mut s = String::new();
                    while let Some(c) = self.peek() {
                        self.i += 1;
                        if c == ']' {
                            break;
                        }
                        s.push(c);
                    }
                    index = Some(s);
                }
                if let Some(ix) = index {
                    self.emit(&ix, Ctx { sup: true, ..ctx }, false);
                }
                let a = self.group_plain(ctx);
                let pa = Self::plain_of(&a);
                self.emit("√", ctx, false);
                let simple = pa.chars().count() <= 1;
                if !simple {
                    self.emit("(", ctx, false);
                }
                self.append_spans(a);
                if !simple {
                    self.emit(")", ctx, false);
                }
            }
            "text" | "textrm" | "mbox" | "textsf" | "textup" => {
                let s = self.raw_group();
                self.emit(&s, Ctx { upright: true, ..ctx }, false);
            }
            "textbf" => {
                let s = self.raw_group();
                self.emit(&s, Ctx { upright: true, bold: true, ..ctx }, false);
            }
            "textit" => {
                let s = self.raw_group();
                self.emit(&s, ctx, true);
            }
            "mathrm" | "operatorname" | "mathsf" | "mathtt" | "mathcal" | "mathscr" | "mathfrak" => {
                let a = self.group_plain(Ctx { upright: true, ..ctx });
                self.append_spans(a);
            }
            "mathbf" | "boldsymbol" | "bm" | "pmb" => {
                let a = self.group_plain(Ctx { bold: true, upright: true, ..ctx });
                self.append_spans(a);
            }
            "mathit" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
            }
            "mathbb" => {
                let s = self.raw_group();
                let t: String = s.chars().map(blackboard).collect();
                self.emit(&t, Ctx { upright: true, ..ctx }, false);
            }
            "vec" | "overrightarrow" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("→", Ctx { sup: true, sub: false, ..ctx }, false);
            }
            "hat" | "widehat" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("^", Ctx { sup: true, sub: false, ..ctx }, false);
            }
            "bar" | "overline" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("¯", ctx, false);
            }
            "dot" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("˙", Ctx { sup: true, sub: false, ..ctx }, false);
            }
            "ddot" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("˙˙", Ctx { sup: true, sub: false, ..ctx }, false);
            }
            "tilde" | "widetilde" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
                self.emit("~", Ctx { sup: true, sub: false, ..ctx }, false);
            }
            "underline" | "boxed" | "cancel" | "xcancel" | "bcancel" | "underbrace" | "overbrace" | "mathrel" | "mathbin" | "mathop" | "substack" => {
                let a = self.group_plain(ctx);
                self.append_spans(a);
            }
            "overset" | "underset" | "stackrel" => {
                let _ = self.group_plain(ctx);
                let b = self.group_plain(ctx);
                self.append_spans(b);
            }
            "color" | "phantom" | "hspace" | "vspace" | "tag" | "label" | "hphantom" | "vphantom" => {
                let _ = self.raw_group();
            }
            "textcolor" | "colorbox" => {
                let _ = self.raw_group();
            }
            "begin" => {
                let env = self.raw_group();
                match env.as_str() {
                    "pmatrix" => self.emit("(", ctx, false),
                    "bmatrix" => self.emit("[", ctx, false),
                    "vmatrix" => self.emit("|", ctx, false),
                    "cases" => self.emit("{ ", ctx, false),
                    "array" => {
                        let _ = self.raw_group();
                    }
                    _ => {}
                }
            }
            "end" => {
                let env = self.raw_group();
                match env.as_str() {
                    "pmatrix" => self.emit(")", ctx, false),
                    "bmatrix" => self.emit("]", ctx, false),
                    "vmatrix" => self.emit("|", ctx, false),
                    _ => {}
                }
            }
            "not" => {}
            other => {
                // Unknown command: show its name rather than silently dropping content.
                self.emit(other, Ctx { upright: true, ..ctx }, false);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn plain(s: &str) -> String {
        to_spans(s).iter().map(|x| x.text.as_str()).collect()
    }

    #[test]
    fn fractions_and_scripts() {
        assert_eq!(plain(r"\frac{\Delta Z}{Z} = p\frac{\Delta A}{A}"), "ΔZ/Z = pΔA/A");
        assert_eq!(plain(r"x^{2} + y_1"), "x2 + y1");
        let s = to_spans("x^2");
        assert!(s.iter().any(|x| x.sup && x.text == "2"));
    }

    #[test]
    fn units_and_text() {
        assert_eq!(plain(r"0.00250\ \text{m}"), "0.00250 m");
        assert_eq!(plain(r"\theta = 30^\circ"), "θ = 30°");
    }
}
