//! Search is done by the server (`/api/content/search/`): subjects, units, topics and full chapter text.
use serde::Deserialize;

use crate::config::{api_base, VERSION};
use crate::data::models::*;
use crate::errors::{AppError, Result};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum HitKind {
    Subject,
    Unit,
    Topic,
    Text,
}

#[derive(Clone, Debug)]
pub struct SearchHit {
    pub kind: HitKind,
    pub track: String,
    pub subject: String,
    pub subject_name: String,
    pub track_label: String,
    pub color: String,
    pub chapter: Option<ChapterRef>,
    pub title: String,
    pub snippet: String,
    #[allow(dead_code)]
    pub score: i32,
}

#[derive(Deserialize)]
struct Resp {
    hits: Vec<Raw>,
}

#[derive(Deserialize, Default)]
#[serde(default)]
struct Raw {
    kind: String,
    track: String,
    subject: String,
    #[serde(rename = "subjectName")]
    subject_name: String,
    #[serde(rename = "trackLabel")]
    track_label: String,
    color: String,
    #[serde(rename = "chapterKind")]
    chapter_kind: Option<String>,
    no: u32,
    title: String,
    snippet: String,
    score: i32,
}

pub fn remote(query: &str) -> Result<Vec<SearchHit>> {
    let resp = ureq::AgentBuilder::new()
        .timeout(std::time::Duration::from_secs(15))
        .user_agent(&format!("NEBians-Desktop/{VERSION}"))
        .build()
        .get(&format!("{}api/content/search/", api_base()))
        .query("q", query)
        .query("limit", "60")
        .call()
        .map_err(|e| match e {
            ureq::Error::Status(429, _) => AppError::Network("Searching too fast — wait a moment.".into()),
            other => AppError::Network(format!("Search needs a connection. ({other})")),
        })?;
    let parsed: Resp = resp.into_json().map_err(|e| AppError::Network(format!("Unexpected search reply: {e}")))?;
    Ok(parsed
        .hits
        .into_iter()
        .map(|h| {
            let kind = match h.kind.as_str() {
                "subject" => HitKind::Subject,
                "unit" => HitKind::Unit,
                "topic" => HitKind::Topic,
                _ => HitKind::Text,
            };
            let ck = match h.chapter_kind.as_deref() {
                Some("unit") => Some(ChapterKind::Unit),
                Some("bank") => Some(ChapterKind::Bank),
                Some("guide") => Some(ChapterKind::Guide),
                _ => None,
            };
            let chapter = ck.map(|k| ChapterRef::new(&h.track, &h.subject, k, h.no));
            SearchHit { kind, track: h.track, subject: h.subject, subject_name: h.subject_name, track_label: h.track_label, color: h.color, chapter, title: h.title, snippet: h.snippet, score: h.score }
        })
        .collect())
}
