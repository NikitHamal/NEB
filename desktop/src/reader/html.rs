//! HTML (the subset the NEBians exporter emits) → `Block`s.
//! Handles: headings, paragraphs, callout boxes (`div.box.*`), lists, tables,
//! figures, code, quotes, `<details>` answers, display maths (`div.dm`) and
//! the interactive MCQ markup (`ol.mcq > li[data-key] .opts .opt`).
use scraper::{ElementRef, Html, Node};

use super::math;
use super::model::*;

#[derive(Clone, Default)]
struct Style {
    bold: bool,
    italic: bool,
    code: bool,
    sup: bool,
    sub: bool,
    underline: bool,
    link: Option<String>,
}

#[derive(Clone, Copy)]
enum Skip<'a> {
    Nothing,
    Class(&'a str),
    Tag(&'a str),
}

#[derive(Default)]
struct Parser {
    mcq_keys: Vec<char>,
}

pub fn parse(html: &str) -> Doc {
    let frag = Html::parse_fragment(html);
    let mut p = Parser::default();
    let blocks = p.blocks(frag.root_element(), Skip::Nothing);
    Doc { blocks, mcq_keys: p.mcq_keys }
}

fn has_class(el: &ElementRef, c: &str) -> bool {
    el.value().classes().any(|x| x == c)
}

fn text_of(el: &ElementRef) -> String {
    el.text().collect::<Vec<_>>().concat()
}

fn is_inline(el: &ElementRef) -> bool {
    matches!(
        el.value().name(),
        "span" | "strong" | "b" | "em" | "i" | "code" | "sub" | "sup" | "u" | "a" | "br" | "small" | "mark" | "s" | "del" | "abbr" | "kbd"
    )
}

fn push_text(out: &mut Vec<Span>, raw: &str, st: &Style) {
    // collapse whitespace like a browser
    let mut t = String::with_capacity(raw.len());
    let mut prev_space = false;
    for c in raw.chars() {
        if c.is_whitespace() {
            if !prev_space {
                t.push(' ');
            }
            prev_space = true;
        } else {
            t.push(c);
            prev_space = false;
        }
    }
    if t.is_empty() {
        return;
    }
    if let Some(last) = out.last() {
        if last.text.ends_with(' ') && t.starts_with(' ') {
            t.remove(0);
        }
    }
    if t.is_empty() {
        return;
    }
    push_span(
        out,
        Span { text: t, bold: st.bold, italic: st.italic, code: st.code, sup: st.sup, sub: st.sub, underline: st.underline, link: st.link.clone(), ..Default::default() },
    );
}

fn push_span(out: &mut Vec<Span>, s: Span) {
    if let Some(last) = out.last_mut() {
        if last.same_style(&s) {
            last.text.push_str(&s.text);
            return;
        }
    }
    out.push(s);
}

fn trim_spans(spans: &mut Vec<Span>) {
    if let Some(f) = spans.first_mut() {
        f.text = f.text.trim_start().to_string();
    }
    if let Some(l) = spans.last_mut() {
        l.text = l.text.trim_end().to_string();
    }
    spans.retain(|s| !s.text.is_empty());
}

impl Parser {
    fn inline(&mut self, el: ElementRef, mut st: Style, out: &mut Vec<Span>) {
        match el.value().name() {
            "br" => {
                push_span(out, Span::plain("\n"));
                return;
            }
            "strong" | "b" => st.bold = true,
            "em" | "i" => st.italic = true,
            "code" | "kbd" => st.code = true,
            "sub" => st.sub = true,
            "sup" => st.sup = true,
            "u" => st.underline = true,
            "a" => st.link = el.value().attr("href").map(str::to_owned),
            "span" => {
                if has_class(&el, "m") {
                    for mut s in math::to_spans(&text_of(&el)) {
                        s.bold |= st.bold;
                        out.push(s);
                    }
                    return;
                }
                if has_class(&el, "marks") {
                    push_span(out, Span { text: text_of(&el), marks: true, ..Default::default() });
                    return;
                }
            }
            _ => {}
        }
        for child in el.children() {
            match child.value() {
                Node::Text(t) => push_text(out, t, &st),
                Node::Element(_) => {
                    if let Some(e) = ElementRef::wrap(child) {
                        self.inline(e, st.clone(), out);
                    }
                }
                _ => {}
            }
        }
    }

    fn spans_of(&mut self, el: ElementRef) -> Vec<Span> {
        let mut out = vec![];
        self.inline(el, Style::default(), &mut out);
        trim_spans(&mut out);
        out
    }

    fn blocks(&mut self, parent: ElementRef, skip: Skip) -> Vec<Block> {
        let mut out: Vec<Block> = vec![];
        let mut run: Vec<Span> = vec![];
        let flush = |run: &mut Vec<Span>, out: &mut Vec<Block>| {
            trim_spans(run);
            if !run.is_empty() {
                out.push(Block::Para(std::mem::take(run)));
            }
            run.clear();
        };
        for child in parent.children() {
            match child.value() {
                Node::Text(t) => push_text(&mut run, t, &Style::default()),
                Node::Element(_) => {
                    let Some(el) = ElementRef::wrap(child) else { continue };
                    match skip {
                        Skip::Class(c) if has_class(&el, c) => continue,
                        Skip::Tag(t) if el.value().name() == t => continue,
                        _ => {}
                    }
                    if is_inline(&el) && !(el.value().name() == "span" && has_class(&el, "m") && has_class(&el, "d")) {
                        self.inline(el, Style::default(), &mut run);
                    } else {
                        flush(&mut run, &mut out);
                        if let Some(b) = self.block(el) {
                            out.push(b);
                        }
                    }
                }
                _ => {}
            }
        }
        flush(&mut run, &mut out);
        out
    }

    fn one_or_group(mut v: Vec<Block>) -> Option<Block> {
        match v.len() {
            0 => None,
            1 => v.pop(),
            _ => Some(Block::Group(v)),
        }
    }

    fn block(&mut self, el: ElementRef) -> Option<Block> {
        let name = el.value().name();
        match name {
            "script" | "style" | "img" | "figcaption" | "summary" => None,
            "h1" | "h2" | "h3" | "h4" | "h5" | "h6" => {
                let level = name[1..].parse().unwrap_or(3);
                let spans = self.spans_of(el);
                (!spans.is_empty()).then(|| Block::Heading { level, id: el.value().attr("id").unwrap_or("").to_string(), spans })
            }
            "p" | "section" => Self::one_or_group(self.blocks(el, Skip::Nothing)),
            "div" => {
                if has_class(&el, "dm") {
                    let spans = math::to_display_spans(&text_of(&el));
                    return (!spans.is_empty()).then_some(Block::Math(spans));
                }
                if has_class(&el, "bt") {
                    return None;
                }
                if has_class(&el, "box") {
                    let kind = el.value().classes().find(|c| *c != "box" && *c != "ans" && *c != "nobreak").unwrap_or("note").to_string();
                    let title = el
                        .children()
                        .filter_map(ElementRef::wrap)
                        .find(|c| has_class(c, "bt"))
                        .map(|t| self.spans_of(t))
                        .filter(|t| !t.is_empty());
                    let blocks = self.blocks(el, Skip::Class("bt"));
                    return Some(Block::Box { kind, title, blocks });
                }
                Self::one_or_group(self.blocks(el, Skip::Nothing))
            }
            "ul" | "ol" => {
                if name == "ol" && has_class(&el, "mcq") {
                    return Some(self.mcq(el));
                }
                let items: Vec<Vec<Block>> = el
                    .children()
                    .filter_map(ElementRef::wrap)
                    .filter(|c| c.value().name() == "li")
                    .map(|li| self.blocks(li, Skip::Nothing))
                    .collect();
                (!items.is_empty()).then_some(Block::List { ordered: name == "ol", items })
            }
            "table" => Some(self.table(el)),
            "figure" => {
                let img = el.descendants().filter_map(ElementRef::wrap).find(|c| c.value().name() == "img")?;
                let src = img.value().attr("src")?.to_string();
                let width_pct = img
                    .value()
                    .attr("style")
                    .and_then(|s| s.split("width:").nth(1))
                    .and_then(|s| s.trim().trim_end_matches(';').trim_end_matches('%').trim().parse::<f32>().ok());
                let caption = el
                    .descendants()
                    .filter_map(ElementRef::wrap)
                    .find(|c| c.value().name() == "figcaption")
                    .map(|c| self.spans_of(c))
                    .unwrap_or_default();
                Some(Block::Figure { src, caption, width_pct })
            }
            "pre" => {
                let code = el.descendants().filter_map(ElementRef::wrap).find(|c| c.value().name() == "code");
                let lang = code
                    .and_then(|c| c.value().classes().find_map(|k| k.strip_prefix("language-")))
                    .unwrap_or("text")
                    .to_string();
                Some(Block::Code { lang, text: text_of(&code.unwrap_or(el)).trim_end().to_string() })
            }
            "blockquote" => Self::one_or_group(self.blocks(el, Skip::Nothing)).map(|b| Block::Quote(vec![b])),
            "hr" => Some(Block::Rule),
            "details" => {
                let summary = el
                    .children()
                    .filter_map(ElementRef::wrap)
                    .find(|c| c.value().name() == "summary")
                    .map(|s| self.spans_of(s))
                    .unwrap_or_default();
                let blocks = self.blocks(el, Skip::Tag("summary"));
                Some(Block::Details { summary, blocks })
            }
            _ => Self::one_or_group(self.blocks(el, Skip::Nothing)),
        }
    }

    fn table(&mut self, el: ElementRef) -> Block {
        let mut head = vec![];
        let mut rows = vec![];
        for tr in el.descendants().filter_map(ElementRef::wrap).filter(|c| c.value().name() == "tr") {
            let cells: Vec<ElementRef> = tr.children().filter_map(ElementRef::wrap).filter(|c| matches!(c.value().name(), "td" | "th")).collect();
            let is_head = cells.iter().all(|c| c.value().name() == "th") && !cells.is_empty();
            let row: Vec<Vec<Span>> = cells.into_iter().map(|c| self.spans_of(c)).collect();
            if is_head && head.is_empty() && rows.is_empty() {
                head = row;
            } else {
                rows.push(row);
            }
        }
        Block::Table { head, rows }
    }

    fn mcq(&mut self, ol: ElementRef) -> Block {
        let mut items = vec![];
        for li in ol.children().filter_map(ElementRef::wrap).filter(|c| c.value().name() == "li") {
            let key = li.value().attr("data-key").and_then(|k| k.chars().next()).unwrap_or('a');
            let mut question: Vec<Span> = vec![];
            let mut marks = None;
            let mut options = vec![];
            let mut cols = 1;
            for child in li.children() {
                match child.value() {
                    Node::Text(t) => push_text(&mut question, t, &Style::default()),
                    Node::Element(_) => {
                        let Some(e) = ElementRef::wrap(child) else { continue };
                        if has_class(&e, "opts") {
                            cols = e.value().classes().find_map(|c| c.strip_prefix('c').and_then(|n| n.parse().ok())).unwrap_or(1);
                            for o in e.children().filter_map(ElementRef::wrap).filter(|c| has_class(c, "opt")) {
                                let label = o
                                    .children()
                                    .filter_map(ElementRef::wrap)
                                    .find(|c| c.value().name() == "i")
                                    .map(|i| text_of(&i).trim().chars().next().unwrap_or('?'))
                                    .unwrap_or('?');
                                let mut spans = vec![];
                                for oc in o.children() {
                                    match oc.value() {
                                        Node::Text(t) => push_text(&mut spans, t, &Style::default()),
                                        Node::Element(_) => {
                                            if let Some(oe) = ElementRef::wrap(oc) {
                                                if oe.value().name() == "i" && text_of(&oe).trim().chars().count() == 1 && spans.is_empty() {
                                                    continue; // the option letter
                                                }
                                                self.inline(oe, Style::default(), &mut spans);
                                            }
                                        }
                                        _ => {}
                                    }
                                }
                                trim_spans(&mut spans);
                                options.push((label, spans));
                            }
                        } else if has_class(&e, "marks") {
                            marks = Some(text_of(&e).trim().to_string());
                        } else {
                            self.inline(e, Style::default(), &mut question);
                        }
                    }
                    _ => {}
                }
            }
            trim_spans(&mut question);
            self.mcq_keys.push(key);
            items.push(McqItem { key, question, marks, options, cols });
        }
        Block::Mcq(items)
    }
}
