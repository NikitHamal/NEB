//! Locates and loads the NEBians study content that already lives in the repo.
//!
//! Two layouts are understood (see docs/ARCHITECTURE.md):
//!   1. a repo checkout:  `<dir>/backend_python/web/{data,static/web}` + `<dir>/notes/pdf`
//!   2. a bundled folder: `<dir>/{data,static/web,pdf}` (what `scripts/bundle-content.sh` makes)
use std::path::{Path, PathBuf};

use crate::data::models::*;
use crate::errors::{AppError, Result};

#[derive(Clone, Debug)]
pub struct ContentRoot {
    /// Folder the user pointed us at (shown in Settings).
    pub base: PathBuf,
    /// `.../data` — contains `syllabus/` and `study/`.
    pub data: PathBuf,
    /// `.../static/web` — figures referenced as `/static/web/study/<hash>.svg`.
    pub assets: PathBuf,
    /// Optional folder with the built book PDFs.
    pub pdf: Option<PathBuf>,
}

#[derive(Clone, Debug)]
pub struct PdfEntry {
    pub name: String,
    pub path: PathBuf,
    pub size: u64,
}

impl ContentRoot {
    pub fn from_dir(dir: &Path) -> Option<Self> {
        let repo = dir.join("backend_python/web");
        if repo.join("data/syllabus/index.json").is_file() {
            let pdf = dir.join("notes/pdf");
            return Some(Self {
                base: dir.to_path_buf(),
                data: repo.join("data"),
                assets: repo.join("static/web"),
                pdf: pdf.is_dir().then_some(pdf),
            });
        }
        if dir.join("data/syllabus/index.json").is_file() {
            let pdf = dir.join("pdf");
            return Some(Self {
                base: dir.to_path_buf(),
                data: dir.join("data"),
                assets: dir.join("static/web"),
                pdf: pdf.is_dir().then_some(pdf),
            });
        }
        None
    }

    /// Resolution order: explicit path → saved path → next to the executable
    /// (`content/`) → any ancestor of the executable or working directory
    /// (so `cargo run` inside a repo checkout just works).
    pub fn detect(explicit: Option<&Path>, saved: Option<&Path>) -> Option<Self> {
        for p in [explicit, saved].into_iter().flatten() {
            if let Some(r) = Self::from_dir(p) {
                return Some(r);
            }
        }
        let mut starts: Vec<PathBuf> = vec![];
        if let Ok(exe) = std::env::current_exe() {
            if let Some(d) = exe.parent() {
                starts.push(d.to_path_buf());
            }
        }
        if let Ok(cwd) = std::env::current_dir() {
            starts.push(cwd);
        }
        for s in starts {
            for anc in s.ancestors().take(8) {
                if let Some(r) = Self::from_dir(&anc.join("content")).or_else(|| Self::from_dir(anc)) {
                    return Some(r);
                }
            }
        }
        None
    }

    pub fn tracks(&self) -> Result<Vec<Track>> {
        #[derive(serde::Deserialize)]
        struct Index {
            grades: Vec<Track>,
        }
        let txt = std::fs::read_to_string(self.data.join("syllabus/index.json"))?;
        Ok(serde_json::from_str::<Index>(&txt)?.grades)
    }

    pub fn syllabus(&self, track: &str, subject: &str) -> Result<Syllabus> {
        let p = self.data.join(format!("syllabus/{track}-{subject}.json"));
        Ok(serde_json::from_str(&std::fs::read_to_string(p)?)?)
    }

    pub fn study_index(&self, track: &str, subject: &str) -> Result<StudyIndex> {
        let p = self.data.join(format!("study/{track}-{subject}/index.json"));
        Ok(serde_json::from_str(&std::fs::read_to_string(p)?)?)
    }

    pub fn chapter(&self, r: &ChapterRef) -> Result<Chapter> {
        let p = self.data.join("study").join(r.dir()).join(r.kind.file_name(r.no));
        let txt = std::fs::read_to_string(&p)
            .map_err(|e| AppError::Content(format!("Could not open {}: {e}", p.display())))?;
        Ok(serde_json::from_str(&txt)?)
    }

    /// Map `/static/web/study/abc.svg` (as written in the chapter HTML) to a `file://` URI.
    pub fn asset_uri(&self, src: &str) -> Option<String> {
        let rel = src.strip_prefix("/static/web/").or_else(|| src.strip_prefix("static/web/")).unwrap_or(src.trim_start_matches('/'));
        let p = self.assets.join(rel);
        p.is_file().then(|| format!("file://{}", p.display()))
    }

    pub fn study_dir(&self) -> PathBuf {
        self.data.join("study")
    }

    pub fn list_pdfs(&self) -> Vec<PdfEntry> {
        let Some(dir) = &self.pdf else { return vec![] };
        let mut out: Vec<PdfEntry> = std::fs::read_dir(dir)
            .into_iter()
            .flatten()
            .flatten()
            .filter(|e| e.path().extension().is_some_and(|x| x.eq_ignore_ascii_case("pdf")))
            .map(|e| PdfEntry {
                name: e.path().file_stem().map(|s| s.to_string_lossy().into_owned()).unwrap_or_default(),
                size: e.metadata().map(|m| m.len()).unwrap_or(0),
                path: e.path(),
            })
            .collect();
        out.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));
        out
    }

    /// Total bytes of syllabus + study JSON and figures (for the Offline screen).
    pub fn footprint(&self) -> (u64, u64) {
        fn walk(p: &Path, files: &mut u64, bytes: &mut u64) {
            if let Ok(rd) = std::fs::read_dir(p) {
                for e in rd.flatten() {
                    let path = e.path();
                    if path.is_dir() {
                        walk(&path, files, bytes);
                    } else if let Ok(m) = e.metadata() {
                        *files += 1;
                        *bytes += m.len();
                    }
                }
            }
        }
        let (mut files, mut bytes) = (0, 0);
        walk(&self.data, &mut files, &mut bytes);
        walk(&self.assets.join("study"), &mut files, &mut bytes);
        (files, bytes)
    }
}
