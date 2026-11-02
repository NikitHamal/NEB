//! Study content, served by the NEBians backend (`/api/content/*`) and cached on disk.
//!
//! * Syllabus / chapters are fetched lazily and stored under `<config>/cache/api`. A file is trusted while
//!   the server's content `version` (from the manifest) matches the one it was saved under; after a content
//!   release it is revalidated with `If-None-Match` and replaced only if it changed.
//! * Offline is the default fallback: if the network is down, whatever is cached is served.
//! * Figures (`/static/web/study/<hash>.svg`) are immutable and cached under `cache/assets`.
//! * Book PDFs download resumably (HTTP Range) into `cache/books`.
//! Every call here blocks: run it inside a `data::tasks::Task`.
use std::fs;
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use serde::Deserialize;

use crate::config::{api_base, VERSION};
use crate::data::models::*;
use crate::errors::{AppError, Result};

#[derive(Clone, Debug, Default, Deserialize)]
#[serde(default)]
pub struct DesktopInfo {
    pub latest: String,
    pub minimum: String,
    #[serde(rename = "downloadUrl")]
    pub download_url: String,
    pub notes: String,
}

#[derive(Clone, Debug, Default, Deserialize)]
#[serde(default)]
pub struct Manifest {
    pub version: String,
    pub subjects: u32,
    pub chapters: u32,
    pub books: u32,
    pub desktop: DesktopInfo,
}

#[derive(Clone, Debug, Default, Deserialize)]
#[serde(default)]
pub struct Book {
    pub slug: String,
    pub title: String,
    pub subject: String,
    pub track: String,
    pub grade: String,
    pub size: u64,
    #[serde(rename = "updatedAt")]
    pub updated_at: i64,
}

#[derive(Clone, Copy, Debug, Default)]
pub struct CacheStats {
    pub content_files: u64,
    pub content_bytes: u64,
    pub book_files: u64,
    pub book_bytes: u64,
}

/// Shared progress of a background download.
#[derive(Default)]
pub struct Progress {
    pub done: AtomicU64,
    pub total: AtomicU64,
    pub cancel: AtomicBool,
}

impl Progress {
    pub fn frac(&self) -> f32 {
        let t = self.total.load(Ordering::Relaxed);
        if t == 0 {
            0.0
        } else {
            (self.done.load(Ordering::Relaxed) as f32 / t as f32).clamp(0.0, 1.0)
        }
    }
}

#[derive(Clone)]
pub struct ContentRepo {
    dir: PathBuf,
    version: Arc<Mutex<String>>,
}

fn agent(read_secs: u64) -> ureq::Agent {
    ureq::AgentBuilder::new()
        .timeout_connect(Duration::from_secs(8))
        .timeout_read(Duration::from_secs(read_secs))
        .user_agent(&format!("NEBians-Desktop/{VERSION}"))
        .build()
}

static OFFLINE: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// True when the last network attempt could not reach the server (the app is then serving its cache).
pub fn is_offline() -> bool {
    OFFLINE.load(std::sync::atomic::Ordering::Relaxed)
}

fn set_offline(v: bool) {
    OFFLINE.store(v, std::sync::atomic::Ordering::Relaxed);
}

fn net_err(e: ureq::Error) -> AppError {
    set_offline(!matches!(e, ureq::Error::Status(..)));
    match e {
        ureq::Error::Status(404, _) => AppError::Content("That item isn't on the server (any more).".into()),
        ureq::Error::Status(429, _) => AppError::Network("The server is rate-limiting this device. Try again in a minute.".into()),
        ureq::Error::Status(c, _) => AppError::Network(format!("The server answered with status {c}.")),
        other => AppError::Network(format!("Could not reach NEBians. Check your connection. ({other})")),
    }
}

fn write_atomic(path: &Path, bytes: &[u8]) -> Result<()> {
    if let Some(p) = path.parent() {
        fs::create_dir_all(p)?;
    }
    let tmp = PathBuf::from(format!("{}.tmp", path.display()));
    fs::write(&tmp, bytes)?;
    fs::rename(&tmp, path)?;
    Ok(())
}

fn valid_rel(rel: &str) -> bool {
    !rel.is_empty() && rel.len() < 200 && !rel.contains("..") && !rel.starts_with('/') && rel.chars().all(|c| c.is_ascii_alphanumeric() || "._-/".contains(c))
}

impl ContentRepo {
    pub fn new(config_dir: &Path) -> Self {
        let dir = config_dir.join("cache");
        let _ = fs::create_dir_all(dir.join("api"));
        let v = fs::read_to_string(dir.join("version.txt")).unwrap_or_default();
        Self { dir, version: Arc::new(Mutex::new(v.trim().to_string())) }
    }

    pub fn dir(&self) -> &Path {
        &self.dir
    }

    fn url(path: &str) -> String {
        format!("{}{}", api_base(), path.trim_start_matches('/'))
    }

    fn current_version(&self) -> String {
        self.version.lock().map(|v| v.clone()).unwrap_or_default()
    }

    fn get_bytes(&self, path: &str) -> Result<Vec<u8>> {
        let resp = agent(30).get(&Self::url(path)).set("Accept", "application/json").call().map_err(net_err)?;
        set_offline(false);
        let mut out = vec![];
        resp.into_reader().take(64 * 1024 * 1024).read_to_end(&mut out)?;
        Ok(out)
    }

    /// Always asks the server first (manifest, book list); falls back to the last good copy.
    fn live_cached(&self, rel: &str, path: &str) -> Result<Vec<u8>> {
        let file = self.dir.join("api").join(rel);
        match self.get_bytes(path) {
            Ok(b) => {
                let _ = write_atomic(&file, &b);
                Ok(b)
            }
            Err(e) => fs::read(&file).map_err(|_| e),
        }
    }

    /// Trusted while the content version matches; otherwise revalidated; stale copy if offline.
    fn api_cached(&self, rel: &str, path: &str) -> Result<Vec<u8>> {
        let file = self.dir.join("api").join(rel);
        let meta = PathBuf::from(format!("{}.meta", file.display()));
        let cur = self.current_version();
        let cached = fs::read(&file).ok();
        let meta_txt = fs::read_to_string(&meta).unwrap_or_default();
        let mut lines = meta_txt.lines();
        let (mver, metag) = (lines.next().unwrap_or("").to_string(), lines.next().unwrap_or("").to_string());
        if let Some(b) = &cached {
            if cur.is_empty() || mver == cur {
                return Ok(b.clone());
            }
        }
        let mut req = agent(30).get(&Self::url(path)).set("Accept", "application/json");
        if cached.is_some() && !metag.is_empty() {
            req = req.set("If-None-Match", &metag);
        }
        let res = req.call();
        if res.is_ok() {
            set_offline(false);
        }
        match res {
            Ok(resp) if resp.status() == 304 && cached.is_some() => {
                let _ = fs::write(&meta, format!("{cur}\n{metag}"));
                Ok(cached.unwrap_or_default())
            }
            Ok(resp) => {
                let etag = resp.header("ETag").unwrap_or("").to_string();
                let mut out = vec![];
                resp.into_reader().take(64 * 1024 * 1024).read_to_end(&mut out)?;
                write_atomic(&file, &out)?;
                let _ = fs::write(&meta, format!("{cur}\n{etag}"));
                Ok(out)
            }
            Err(ureq::Error::Status(404, r)) => Err(net_err(ureq::Error::Status(404, r))),
            Err(e) => cached.ok_or_else(|| net_err(e)),
        }
    }

    pub fn is_cached(&self, rel: &str) -> bool {
        self.dir.join("api").join(rel).is_file()
    }

    // ------------------------------------------------------------ catalogue

    pub fn manifest(&self) -> Result<Manifest> {
        let m: Manifest = serde_json::from_slice(&self.live_cached("manifest.json", "api/content/manifest/")?)?;
        if !m.version.is_empty() {
            if let Ok(mut v) = self.version.lock() {
                *v = m.version.clone();
            }
            let _ = fs::write(self.dir.join("version.txt"), &m.version);
        }
        Ok(m)
    }

    /// The categories and their subjects. Also learns the server's content version (best effort).
    pub fn bootstrap(&self) -> Result<(Vec<Track>, Option<Manifest>)> {
        #[derive(Deserialize)]
        struct Index {
            grades: Vec<Track>,
        }
        let manifest = self.manifest().ok();
        let raw = self.api_cached("index.json", "api/content/index/")?;
        Ok((serde_json::from_slice::<Index>(&raw)?.grades, manifest))
    }

    pub fn syllabus(&self, track: &str, subject: &str) -> Result<Syllabus> {
        let key = format!("{track}-{subject}");
        Ok(serde_json::from_slice(&self.api_cached(&format!("syllabus/{key}.json"), &format!("api/content/syllabus/{key}/"))?)?)
    }

    pub fn study_index(&self, track: &str, subject: &str) -> Result<StudyIndex> {
        let key = format!("{track}-{subject}");
        Ok(serde_json::from_slice(&self.api_cached(&format!("study/{key}/index.json"), &format!("api/content/study/{key}/index/"))?)?)
    }

    pub fn chapter(&self, r: &ChapterRef) -> Result<Chapter> {
        let file = r.kind.file_name(r.no);
        let stem = file.trim_end_matches(".json");
        let dir = r.dir();
        let raw = self.api_cached(&format!("study/{dir}/{file}"), &format!("api/content/study/{dir}/{stem}/"))?;
        Ok(serde_json::from_slice(&raw)?)
    }

    pub fn chapter_cached(&self, r: &ChapterRef) -> bool {
        self.is_cached(&format!("study/{}/{}", r.dir(), r.kind.file_name(r.no)))
    }

    pub fn books(&self) -> Result<Vec<Book>> {
        #[derive(Deserialize)]
        struct B {
            books: Vec<Book>,
        }
        Ok(serde_json::from_slice::<B>(&self.live_cached("books.json", "api/content/books/")?)?.books)
    }

    // --------------------------------------------------------------- figures

    fn asset_rel(src: &str) -> Option<&str> {
        let rel = src.strip_prefix("/static/web/").or_else(|| src.strip_prefix("static/web/"))?;
        valid_rel(rel).then_some(rel)
    }

    pub fn asset_uri(&self, src: &str) -> Option<String> {
        let p = self.dir.join("assets").join(Self::asset_rel(src)?);
        p.is_file().then(|| format!("file://{}", p.display()))
    }

    pub fn fetch_asset(&self, src: &str) -> Result<()> {
        let rel = Self::asset_rel(src).ok_or_else(|| AppError::Content("Unsupported figure address".into()))?;
        let file = self.dir.join("assets").join(rel);
        if file.is_file() {
            return Ok(());
        }
        let resp = agent(30).get(&Self::url(&format!("static/web/{rel}"))).call().map_err(net_err)?;
        let mut out = vec![];
        resp.into_reader().take(32 * 1024 * 1024).read_to_end(&mut out)?;
        write_atomic(&file, &out)
    }

    /// Every `/static/web/…` address mentioned in a chapter's HTML.
    pub fn asset_refs(html: &str) -> Vec<String> {
        let mut out: Vec<String> = vec![];
        let mut rest = html;
        while let Some(i) = rest.find("/static/web/") {
            let tail = &rest[i..];
            let end = tail.find(|c: char| c == '"' || c == '\'' || c == ')' || c == '<' || c.is_whitespace()).unwrap_or(tail.len());
            let s = tail[..end].split(['?', '#']).next().unwrap_or("").to_string();
            if !out.contains(&s) {
                out.push(s);
            }
            rest = &tail[end..];
        }
        out
    }

    /// Download all figures of a chapter in parallel (so the reader can paint them immediately).
    pub fn prefetch_assets(&self, html: &str) {
        let refs: Vec<String> = Self::asset_refs(html).into_iter().filter(|s| self.asset_uri(s).is_none()).collect();
        for chunk in refs.chunks(6) {
            std::thread::scope(|sc| {
                for s in chunk {
                    sc.spawn(move || {
                        let _ = self.fetch_asset(s);
                    });
                }
            });
        }
    }

    // ----------------------------------------------------- offline subjects

    pub fn subject_chapters(&self, track: &str, subject: &str) -> Result<Vec<ChapterRef>> {
        let idx = self.study_index(track, subject)?;
        let mut v: Vec<ChapterRef> = idx.units.iter().map(|u| ChapterRef::new(track, subject, ChapterKind::Unit, u.no)).collect();
        v.extend(idx.banks.iter().map(|b| ChapterRef::new(track, subject, ChapterKind::Bank, b.no)));
        if !idx.guide.is_empty() {
            v.push(ChapterRef::new(track, subject, ChapterKind::Guide, 0));
        }
        Ok(v)
    }

    /// True when the syllabus, the index and every chapter of the subject are on disk.
    pub fn subject_offline(&self, track: &str, subject: &str) -> bool {
        let key = format!("{track}-{subject}");
        if !self.is_cached(&format!("study/{key}/index.json")) {
            return false;
        }
        match self.study_index(track, subject).ok().and_then(|_| self.subject_chapters(track, subject).ok()) {
            Some(list) => !list.is_empty() && list.iter().all(|c| self.chapter_cached(c)),
            None => false,
        }
    }

    pub fn download_subject(&self, track: &str, subject: &str, p: &Progress) -> Result<()> {
        self.syllabus(track, subject)?;
        let list = self.subject_chapters(track, subject)?;
        p.total.store(list.len() as u64, Ordering::Relaxed);
        for c in list {
            if p.cancel.load(Ordering::Relaxed) {
                return Err(AppError::Gone("Download cancelled".into()));
            }
            let ch = self.chapter(&c)?;
            self.prefetch_assets(&ch.html);
            p.done.fetch_add(1, Ordering::Relaxed);
        }
        Ok(())
    }

    pub fn remove_subject(&self, track: &str, subject: &str) {
        let key = format!("{track}-{subject}");
        let _ = fs::remove_dir_all(self.dir.join("api/study").join(&key));
        let _ = fs::remove_file(self.dir.join(format!("api/syllabus/{key}.json")));
    }

    // ----------------------------------------------------------------- books

    pub fn book_file(&self, slug: &str) -> Option<PathBuf> {
        valid_rel(slug).then(|| self.dir.join("books").join(format!("{slug}.pdf"))).filter(|p| p.is_file())
    }

    /// PDFs already on disk: (slug, path, bytes), newest first.
    pub fn downloaded_books(&self) -> Vec<(String, PathBuf, u64)> {
        let mut v: Vec<(String, PathBuf, u64, std::time::SystemTime)> = fs::read_dir(self.dir.join("books"))
            .into_iter()
            .flatten()
            .flatten()
            .filter(|e| e.path().extension().is_some_and(|x| x == "pdf"))
            .filter_map(|e| {
                let m = e.metadata().ok()?;
                let slug = e.path().file_stem()?.to_string_lossy().into_owned();
                Some((slug, e.path(), m.len(), m.modified().unwrap_or(std::time::UNIX_EPOCH)))
            })
            .collect();
        v.sort_by(|a, b| b.3.cmp(&a.3));
        v.into_iter().map(|(a, b, c, _)| (a, b, c)).collect()
    }

    pub fn delete_book(&self, slug: &str) {
        if valid_rel(slug) {
            let _ = fs::remove_file(self.dir.join("books").join(format!("{slug}.pdf")));
            let _ = fs::remove_file(self.dir.join("books").join(format!("{slug}.pdf.part")));
        }
    }

    pub fn download_book(&self, slug: &str, p: &Progress) -> Result<PathBuf> {
        if !valid_rel(slug) || slug.contains('/') {
            return Err(AppError::Content("Bad book name".into()));
        }
        fs::create_dir_all(self.dir.join("books"))?;
        let final_path = self.dir.join("books").join(format!("{slug}.pdf"));
        let part = self.dir.join("books").join(format!("{slug}.pdf.part"));
        let have = fs::metadata(&part).map(|m| m.len()).unwrap_or(0);
        let mut req = agent(60).get(&Self::url(&format!("api/content/books/{slug}/file/")));
        if have > 0 {
            req = req.set("Range", &format!("bytes={have}-"));
        }
        let resp = req.call().map_err(net_err)?;
        let resumed = resp.status() == 206;
        let len: u64 = resp.header("Content-Length").and_then(|v| v.parse().ok()).unwrap_or(0);
        let start = if resumed { have } else { 0 };
        p.total.store(start + len, Ordering::Relaxed);
        p.done.store(start, Ordering::Relaxed);
        let mut file = fs::OpenOptions::new().create(true).write(true).append(resumed).truncate(!resumed).open(&part)?;
        let mut reader = resp.into_reader();
        let mut buf = vec![0u8; 64 * 1024];
        loop {
            if p.cancel.load(Ordering::Relaxed) {
                return Err(AppError::Gone("Download paused".into()));
            }
            let n = reader.read(&mut buf).map_err(|e| AppError::Network(format!("Connection interrupted ({e}). Retry to resume.")))?;
            if n == 0 {
                break;
            }
            file.write_all(&buf[..n])?;
            p.done.fetch_add(n as u64, Ordering::Relaxed);
        }
        file.flush()?;
        drop(file);
        if fs::metadata(&part)?.len() < 8 {
            return Err(AppError::Network("The download came back empty.".into()));
        }
        fs::rename(&part, &final_path)?;
        Ok(final_path)
    }

    // ----------------------------------------------------------------- cache

    pub fn stats(&self) -> CacheStats {
        fn walk(p: &Path, files: &mut u64, bytes: &mut u64) {
            if let Ok(rd) = fs::read_dir(p) {
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
        let mut s = CacheStats::default();
        walk(&self.dir.join("api"), &mut s.content_files, &mut s.content_bytes);
        walk(&self.dir.join("assets"), &mut s.content_files, &mut s.content_bytes);
        walk(&self.dir.join("books"), &mut s.book_files, &mut s.book_bytes);
        s
    }

    pub fn clear_content(&self) {
        let _ = fs::remove_dir_all(self.dir.join("api"));
        let _ = fs::remove_dir_all(self.dir.join("assets"));
        let _ = fs::remove_dir_all(self.dir.join("images"));
        let _ = fs::create_dir_all(self.dir.join("api"));
    }

    pub fn clear_books(&self) {
        let _ = fs::remove_dir_all(self.dir.join("books"));
    }

    // ---------------------------------------------------------- remote images

    /// Avatars and other server images, cached by URL hash. `url` may be site-relative (`/avatar/x/`).
    pub fn image_bytes(&self, url: &str) -> Result<Vec<u8>> {
        use sha2::{Digest, Sha256};
        let abs = if url.starts_with("http://") || url.starts_with("https://") {
            url.to_string()
        } else {
            Self::url(url)
        };
        let host_ok = abs.starts_with("https://") || abs.starts_with(&api_base()) || abs.starts_with("http://127.0.0.1") || abs.starts_with("http://localhost");
        if !host_ok {
            return Err(AppError::Content("Refusing to load an image over plain http".into()));
        }
        let hash: String = Sha256::digest(abs.as_bytes()).iter().take(12).map(|b| format!("{b:02x}")).collect();
        let file = self.dir.join("images").join(&hash);
        // Fresh for a day; after that try the server again but fall back to the stale copy (offline-first).
        let cached = fs::read(&file).ok().filter(|b| !b.is_empty());
        let fresh = fs::metadata(&file).and_then(|m| m.modified()).ok().and_then(|m| m.elapsed().ok()).map(|e| e.as_secs() < 86_400).unwrap_or(false);
        if let (Some(b), true) = (&cached, fresh) {
            return Ok(b.clone());
        }
        let fetched = agent(20).get(&abs).call().map_err(net_err).and_then(|resp| {
            let mut out = vec![];
            resp.into_reader().take(6 * 1024 * 1024).read_to_end(&mut out)?;
            Ok(out)
        });
        match fetched {
            Ok(out) if !out.is_empty() => {
                set_offline(false);
                let _ = write_atomic(&file, &out);
                Ok(out)
            }
            Ok(_) => cached.ok_or_else(|| AppError::Content("Empty image".into())),
            Err(e) => cached.ok_or(e),
        }
    }
}
