//! Search: an in-memory structural index (subjects, units, topics — instant)
//! plus a cancellable full-text scan over every chapter on disk (background).
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

use crate::data::content::ContentRoot;
use crate::data::models::*;

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
    pub score: i32,
}

pub struct SearchIndex {
    entries: Vec<SearchHit>,
    hay: Vec<String>,
}

impl SearchIndex {
    pub fn build(root: &ContentRoot, tracks: &[Track]) -> Self {
        let mut entries = vec![];
        let mut hay = vec![];
        for t in tracks {
            for s in &t.subjects {
                let base = |kind, title: String, snippet: String, chapter| SearchHit {
                    kind,
                    track: t.grade.clone(),
                    subject: s.subject.clone(),
                    subject_name: s.name.clone(),
                    track_label: t.short.clone(),
                    color: s.color.clone(),
                    chapter,
                    title,
                    snippet,
                    score: 0,
                };
                entries.push(base(HitKind::Subject, s.name.clone(), format!("{} · {} units · {}", t.label, s.unit_count, t.exam), None));
                hay.push(format!("{} {} {} {}", s.name, s.name_ne, t.short, t.label).to_lowercase());
                let Ok(syl) = root.syllabus(&t.grade, &s.subject) else { continue };
                for u in &syl.units {
                    let cref = Some(ChapterRef::new(&t.grade, &s.subject, ChapterKind::Unit, u.no));
                    entries.push(base(HitKind::Unit, format!("Unit {} · {}", u.no, u.title), format!("{} · {} · {}", s.name, t.short, u.area), cref.clone()));
                    hay.push(format!("{} {} {} {} {}", u.title, u.area, s.name, t.short, u.topics.join(" ")).to_lowercase());
                    for topic in &u.topics {
                        entries.push(base(HitKind::Topic, topic.clone(), format!("Unit {} · {} — {} · {}", u.no, u.title, s.name, t.short), cref.clone()));
                        hay.push(format!("{} {} {} {}", topic, u.title, s.name, t.short).to_lowercase());
                    }
                }
            }
        }
        Self { entries, hay }
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn query(&self, q: &str) -> Vec<SearchHit> {
        let toks: Vec<String> = q.to_lowercase().split_whitespace().map(str::to_owned).collect();
        if toks.is_empty() {
            return vec![];
        }
        let mut out: Vec<SearchHit> = vec![];
        for (e, h) in self.entries.iter().zip(&self.hay) {
            if !toks.iter().all(|t| h.contains(t.as_str())) {
                continue;
            }
            let title = e.title.to_lowercase();
            let mut score = match e.kind {
                HitKind::Subject => 40,
                HitKind::Unit => 30,
                HitKind::Topic => 20,
                HitKind::Text => 0,
            };
            for t in &toks {
                if title.contains(t.as_str()) {
                    score += 25;
                }
                if title.starts_with(t.as_str()) {
                    score += 10;
                }
            }
            let mut hit = e.clone();
            hit.score = score;
            out.push(hit);
        }
        out.sort_by(|a, b| b.score.cmp(&a.score).then(a.title.cmp(&b.title)));
        out.truncate(80);
        out
    }
}

/// Context for the full-text scan: which folder maps to which subject.
#[derive(Clone)]
pub struct DirInfo {
    pub dir: String,
    pub track: String,
    pub subject: String,
    pub subject_name: String,
    pub track_label: String,
    pub color: String,
}

pub fn dir_infos(tracks: &[Track]) -> Vec<DirInfo> {
    tracks
        .iter()
        .flat_map(|t| {
            t.subjects.iter().map(move |s| DirInfo {
                dir: format!("{}-{}", t.grade, s.subject),
                track: t.grade.clone(),
                subject: s.subject.clone(),
                subject_name: s.name.clone(),
                track_label: t.short.clone(),
                color: s.color.clone(),
            })
        })
        .collect()
}

/// Strip tags and decode the handful of entities the exporter emits.
pub fn html_to_text(html: &str) -> String {
    let mut out = String::with_capacity(html.len() / 2);
    let mut in_tag = false;
    for c in html.chars() {
        match c {
            '<' => {
                in_tag = true;
                out.push(' ');
            }
            '>' => in_tag = false,
            _ if !in_tag => out.push(c),
            _ => {}
        }
    }
    out.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&#39;", "'").replace("&nbsp;", " ")
}

pub fn fulltext(root: &ContentRoot, infos: &[DirInfo], q: &str, cancel: Arc<AtomicBool>) -> Vec<SearchHit> {
    let needle = q.to_lowercase();
    if needle.chars().count() < 3 {
        return vec![];
    }
    let mut hits: Vec<SearchHit> = vec![];
    for info in infos {
        let dir = root.study_dir().join(&info.dir);
        let Ok(rd) = std::fs::read_dir(&dir) else { continue };
        let mut files: Vec<_> = rd.flatten().map(|e| e.path()).collect();
        files.sort();
        for path in files {
            if cancel.load(Ordering::Relaxed) {
                return vec![];
            }
            let name = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            let (kind, no) = if name == "guide.json" {
                (ChapterKind::Guide, 0)
            } else if let Some(n) = name.strip_prefix("unit-").and_then(|n| n.strip_suffix(".json")) {
                (ChapterKind::Unit, n.parse().unwrap_or(0))
            } else if let Some(n) = name.strip_prefix("bank-").and_then(|n| n.strip_suffix(".json")) {
                (ChapterKind::Bank, n.parse().unwrap_or(0))
            } else {
                continue;
            };
            let Ok(txt) = std::fs::read_to_string(&path) else { continue };
            let Ok(ch) = serde_json::from_str::<Chapter>(&txt) else { continue };
            let plain = html_to_text(&ch.html);
            let lower = plain.to_lowercase();
            let count = lower.matches(&needle).count();
            if count == 0 {
                continue;
            }
            let first = lower.find(&needle).unwrap_or(0);
            // `lower` may differ in byte length from `plain` for exotic characters; clamp on char boundaries.
            let start = floor_boundary(&plain, first.saturating_sub(70));
            let end = floor_boundary(&plain, (first + needle.len() + 110).min(plain.len()));
            let mut snippet = plain[start..end].split_whitespace().collect::<Vec<_>>().join(" ");
            if start > 0 {
                snippet.insert(0, '…');
            }
            if end < plain.len() {
                snippet.push('…');
            }
            let label = match kind {
                ChapterKind::Unit => format!("Unit {} · {}", ch.no, ch.title),
                _ => ch.title.clone(),
            };
            hits.push(SearchHit {
                kind: HitKind::Text,
                track: info.track.clone(),
                subject: info.subject.clone(),
                subject_name: info.subject_name.clone(),
                track_label: info.track_label.clone(),
                color: info.color.clone(),
                chapter: Some(ChapterRef::new(&info.track, &info.subject, kind, no)),
                title: label,
                snippet: format!("{} · {} — {}", info.subject_name, info.track_label, snippet),
                score: count as i32,
            });
        }
    }
    hits.sort_by(|a, b| b.score.cmp(&a.score));
    hits.truncate(60);
    hits
}

fn floor_boundary(s: &str, mut i: usize) -> usize {
    i = i.min(s.len());
    while i > 0 && !s.is_char_boundary(i) {
        i -= 1;
    }
    i
}
