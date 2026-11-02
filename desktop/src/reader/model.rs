//! Block / inline model produced from chapter HTML.

#[derive(Clone, Debug, Default, PartialEq)]
pub struct Span {
    pub text: String,
    pub bold: bool,
    pub italic: bool,
    pub code: bool,
    pub sup: bool,
    pub sub: bool,
    pub math: bool,
    pub underline: bool,
    pub marks: bool,
    pub link: Option<String>,
}

impl Span {
    pub fn plain(t: impl Into<String>) -> Self {
        Self { text: t.into(), ..Default::default() }
    }

    pub fn same_style(&self, o: &Span) -> bool {
        self.bold == o.bold
            && self.italic == o.italic
            && self.code == o.code
            && self.sup == o.sup
            && self.sub == o.sub
            && self.math == o.math
            && self.underline == o.underline
            && self.marks == o.marks
            && self.link == o.link
    }
}

pub fn plain_text(spans: &[Span]) -> String {
    spans.iter().map(|s| s.text.as_str()).collect()
}

#[derive(Clone, Debug)]
pub struct McqItem {
    pub key: char,
    pub question: Vec<Span>,
    pub marks: Option<String>,
    pub options: Vec<(char, Vec<Span>)>,
    pub cols: usize,
}

#[derive(Clone, Debug)]
pub enum Block {
    Heading { level: u8, id: String, spans: Vec<Span> },
    Para(Vec<Span>),
    /// Display-mode equation (may contain `\n` for multi-line environments).
    Math(Vec<Span>),
    Box { kind: String, title: Option<Vec<Span>>, blocks: Vec<Block> },
    List { ordered: bool, items: Vec<Vec<Block>> },
    Table { head: Vec<Vec<Span>>, rows: Vec<Vec<Vec<Span>>> },
    Figure { src: String, caption: Vec<Span>, width_pct: Option<f32> },
    Code { lang: String, text: String },
    Quote(Vec<Block>),
    Rule,
    Details { summary: Vec<Span>, blocks: Vec<Block> },
    Mcq(Vec<McqItem>),
    Group(Vec<Block>),
}

/// A parsed chapter, ready to render.
#[derive(Clone, Debug, Default)]
pub struct Doc {
    pub blocks: Vec<Block>,
    /// Correct answer key of every MCQ in reading order (drives the score).
    pub mcq_keys: Vec<char>,
}
