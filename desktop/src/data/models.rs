//! Serde models for the content the website and the Android app already read:
//! `data/syllabus/*.json` and `data/study/<track>-<subject>/*.json`.
//! Deserialisation is deliberately lenient (numbers may be strings, nulls appear).
#![allow(dead_code)] // wire/icon sets mirror the server and Material font in full
use serde::{Deserialize, Deserializer, Serialize};
use serde_json::Value;

fn de_string<'de, D: Deserializer<'de>>(d: D) -> Result<String, D::Error> {
    Ok(match Value::deserialize(d)? {
        Value::String(s) => s,
        Value::Number(n) => n.to_string(),
        _ => String::new(),
    })
}

fn de_opt_u32<'de, D: Deserializer<'de>>(d: D) -> Result<Option<u32>, D::Error> {
    Ok(match Value::deserialize(d)? {
        Value::Number(n) => n.as_u64().map(|x| x as u32),
        Value::String(s) => s.trim().parse().ok(),
        _ => None,
    })
}

fn de_u32<'de, D: Deserializer<'de>>(d: D) -> Result<u32, D::Error> {
    Ok(de_opt_u32(d)?.unwrap_or(0))
}

/// A top-level category: Class 8/10/11/12, CEE, IOE.
#[derive(Clone, Debug, Deserialize, Default)]
pub struct Track {
    #[serde(default, deserialize_with = "de_string")]
    pub label: String,
    #[serde(default, deserialize_with = "de_string")]
    pub label_ne: String,
    #[serde(default, deserialize_with = "de_string")]
    pub exam: String,
    #[serde(default, deserialize_with = "de_string")]
    pub short: String,
    #[serde(default, deserialize_with = "de_string")]
    pub kind: String,
    #[serde(default, deserialize_with = "de_string")]
    pub grade: String,
    #[serde(default)]
    pub subjects: Vec<SubjectSummary>,
}

impl Track {
    pub fn is_entrance(&self) -> bool {
        self.kind == "entrance"
    }
    pub fn chapter_total(&self) -> u32 {
        self.subjects.iter().map(|s| s.unit_count).sum()
    }
    pub fn ready_total(&self) -> u32 {
        self.subjects.iter().map(|s| s.notes_ready).sum()
    }
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct SubjectSummary {
    #[serde(default, deserialize_with = "de_string")]
    pub subject: String,
    #[serde(default, deserialize_with = "de_string")]
    pub name: String,
    #[serde(default, deserialize_with = "de_string")]
    pub name_ne: String,
    #[serde(default, deserialize_with = "de_string")]
    pub icon: String,
    #[serde(default, deserialize_with = "de_string")]
    pub group: String,
    #[serde(default, deserialize_with = "de_string")]
    pub color: String,
    #[serde(default, deserialize_with = "de_string")]
    pub lang: String,
    #[serde(default, deserialize_with = "de_opt_u32")]
    pub hours: Option<u32>,
    #[serde(default, deserialize_with = "de_u32")]
    pub unit_count: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub topic_count: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub notes_ready: u32,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct Syllabus {
    #[serde(default, deserialize_with = "de_string")]
    pub grade: String,
    #[serde(default, deserialize_with = "de_string")]
    pub grade_label: String,
    #[serde(default, deserialize_with = "de_string")]
    pub subject: String,
    #[serde(default, deserialize_with = "de_string")]
    pub name: String,
    #[serde(default, deserialize_with = "de_string")]
    pub name_ne: String,
    #[serde(default, deserialize_with = "de_string")]
    pub color: String,
    #[serde(default, deserialize_with = "de_string")]
    pub lang: String,
    #[serde(default, deserialize_with = "de_string")]
    pub code: String,
    #[serde(default, deserialize_with = "de_opt_u32")]
    pub hours: Option<u32>,
    #[serde(default, deserialize_with = "de_string")]
    pub exam: String,
    #[serde(default)]
    pub areas: Vec<String>,
    #[serde(default)]
    pub units: Vec<SyllabusUnit>,
    #[serde(default, deserialize_with = "de_u32")]
    pub unit_count: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub topic_count: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub notes_ready: u32,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct SyllabusUnit {
    #[serde(default, deserialize_with = "de_u32")]
    pub no: u32,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
    #[serde(default, deserialize_with = "de_opt_u32")]
    pub hours: Option<u32>,
    #[serde(default, deserialize_with = "de_string")]
    pub area: String,
    #[serde(default)]
    pub topics: Vec<String>,
    #[serde(default)]
    pub sections: Vec<SectionRef>,
    #[serde(default)]
    pub summary: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct SectionRef {
    #[serde(default, deserialize_with = "de_string")]
    pub no: String,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
}

/// `data/study/<dir>/index.json`
#[derive(Clone, Debug, Deserialize, Default)]
pub struct StudyIndex {
    #[serde(default)]
    pub units: Vec<UnitMeta>,
    #[serde(default)]
    pub banks: Vec<BankMeta>,
    #[serde(default, deserialize_with = "de_string")]
    pub guide: String,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct UnitMeta {
    #[serde(default, deserialize_with = "de_u32")]
    pub no: u32,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
    #[serde(default, deserialize_with = "de_string")]
    pub area: String,
    #[serde(default, deserialize_with = "de_u32")]
    pub words: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub read_min: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub figures: u32,
    #[serde(default)]
    pub has_questions: bool,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct BankMeta {
    #[serde(default, deserialize_with = "de_u32")]
    pub no: u32,
    #[serde(default, deserialize_with = "de_string")]
    pub kind: String,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
    #[serde(default, deserialize_with = "de_u32")]
    pub words: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub read_min: u32,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct TocItem {
    #[serde(default, deserialize_with = "de_string")]
    pub id: String,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
    #[serde(default, deserialize_with = "de_string")]
    pub kind: String,
}

#[derive(Clone, Debug, Deserialize, Default)]
pub struct ExamMeta {
    #[serde(default, deserialize_with = "de_u32")]
    pub minutes: u32,
    #[serde(default)]
    pub negative: f64,
}

/// One reader chapter (`unit-NN.json`, `bank-NN.json`, `guide.json`).
#[derive(Clone, Debug, Deserialize, Default)]
pub struct Chapter {
    #[serde(default, deserialize_with = "de_u32")]
    pub no: u32,
    #[serde(default, deserialize_with = "de_string")]
    pub title: String,
    #[serde(default, deserialize_with = "de_string")]
    pub area: String,
    #[serde(default, deserialize_with = "de_string")]
    pub lang: String,
    #[serde(default, deserialize_with = "de_u32")]
    pub words: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub read_min: u32,
    #[serde(default, deserialize_with = "de_u32")]
    pub figures: u32,
    #[serde(default)]
    pub toc: Vec<TocItem>,
    #[serde(default)]
    pub html: String,
    #[serde(default)]
    pub exam: Option<ExamMeta>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ChapterKind {
    Unit,
    Bank,
    Guide,
}

impl ChapterKind {
    pub fn file_name(self, no: u32) -> String {
        match self {
            ChapterKind::Unit => format!("unit-{no:02}.json"),
            ChapterKind::Bank => format!("bank-{no:02}.json"),
            ChapterKind::Guide => "guide.json".to_string(),
        }
    }
    pub fn label(self) -> &'static str {
        match self {
            ChapterKind::Unit => "Unit",
            ChapterKind::Bank => "Question bank",
            ChapterKind::Guide => "Exam guide",
        }
    }
}

/// Stable address of a chapter — used by routes, bookmarks, progress.
#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ChapterRef {
    pub track: String,
    pub subject: String,
    pub kind: ChapterKind,
    pub no: u32,
}

impl ChapterRef {
    pub fn new(track: &str, subject: &str, kind: ChapterKind, no: u32) -> Self {
        Self { track: track.into(), subject: subject.into(), kind, no }
    }
    pub fn key(&self) -> String {
        format!("{}-{}/{}", self.track, self.subject, self.kind.file_name(self.no))
    }
    pub fn dir(&self) -> String {
        format!("{}-{}", self.track, self.subject)
    }
}
