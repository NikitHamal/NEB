//! Background downloads: whole subjects for offline reading and book PDFs. One job per key; the UI reads
//! progress from `Downloads::job` and the finished set from `offline` / `repo.book_file`.
use std::collections::HashSet;
use std::path::PathBuf;
use std::sync::atomic::Ordering;
use std::sync::Arc;

use crate::data::content::{ContentRepo, Progress};
use crate::data::models::Track;
use crate::data::tasks::Task;
use crate::errors::Result;

pub struct Job {
    pub key: String,
    pub title: String,
    pub progress: Arc<Progress>,
    task: Task<Result<Option<PathBuf>>>,
}

#[derive(Default)]
pub struct Downloads {
    pub jobs: Vec<Job>,
    pub offline: HashSet<String>,
    pub failed: Vec<(String, String)>,
    scan: Option<Task<HashSet<String>>>,
}

pub fn subject_key(track: &str, subject: &str) -> String {
    format!("subj:{track}-{subject}")
}

pub fn book_key(slug: &str) -> String {
    format!("book:{slug}")
}

impl Downloads {
    pub fn scan(&mut self, ctx: &egui::Context, repo: &ContentRepo, tracks: &[Track]) {
        let repo = repo.clone();
        let pairs: Vec<(String, String)> = tracks.iter().flat_map(|t| t.subjects.iter().map(|s| (t.grade.clone(), s.subject.clone()))).collect();
        self.scan = Some(Task::spawn(ctx, move || pairs.into_iter().filter(|(t, s)| repo.subject_offline(t, s)).map(|(t, s)| subject_key(&t, &s)).collect()));
    }

    pub fn job(&self, key: &str) -> Option<&Job> {
        self.jobs.iter().find(|j| j.key == key)
    }

    pub fn is_offline(&self, track: &str, subject: &str) -> bool {
        self.offline.contains(&subject_key(track, subject))
    }

    pub fn start_subject(&mut self, ctx: &egui::Context, repo: &ContentRepo, track: &str, subject: &str, title: &str) {
        let key = subject_key(track, subject);
        if self.job(&key).is_some() {
            return;
        }
        self.failed.retain(|(k, _)| *k != key);
        let (repo, p, t, s) = (repo.clone(), Arc::new(Progress::default()), track.to_string(), subject.to_string());
        let p2 = p.clone();
        let task = Task::spawn(ctx, move || repo.download_subject(&t, &s, &p2).map(|_| None));
        self.jobs.push(Job { key, title: title.to_string(), progress: p, task });
    }

    pub fn start_book(&mut self, ctx: &egui::Context, repo: &ContentRepo, slug: &str, title: &str) {
        let key = book_key(slug);
        if self.job(&key).is_some() {
            return;
        }
        self.failed.retain(|(k, _)| *k != key);
        let (repo, p, sl) = (repo.clone(), Arc::new(Progress::default()), slug.to_string());
        let p2 = p.clone();
        let task = Task::spawn(ctx, move || repo.download_book(&sl, &p2).map(Some));
        self.jobs.push(Job { key, title: title.to_string(), progress: p, task });
    }

    pub fn cancel(&mut self, key: &str) {
        if let Some(j) = self.job(key) {
            j.progress.cancel.store(true, Ordering::Relaxed);
        }
    }

    pub fn remove_subject(&mut self, repo: &ContentRepo, track: &str, subject: &str) {
        repo.remove_subject(track, subject);
        self.offline.remove(&subject_key(track, subject));
    }

    /// Returns toast messages for jobs that finished this frame.
    pub fn poll(&mut self) -> Vec<String> {
        let mut msgs = vec![];
        if let Some(t) = self.scan.as_mut() {
            if let Some(set) = t.poll() {
                self.offline.extend(set);
                self.scan = None;
            }
        }
        let mut i = 0;
        while i < self.jobs.len() {
            if let Some(res) = self.jobs[i].task.poll() {
                let j = self.jobs.remove(i);
                match res {
                    Ok(_) => {
                        if j.key.starts_with("subj:") {
                            self.offline.insert(j.key.clone());
                        }
                        msgs.push(format!("{} is ready offline", j.title));
                    }
                    Err(e) => {
                        let cancelled = j.progress.cancel.load(Ordering::Relaxed);
                        if !cancelled {
                            msgs.push(format!("Couldn't finish {} — {e}", j.title));
                            self.failed.push((j.key, e.to_string()));
                        }
                    }
                }
            } else {
                i += 1;
            }
        }
        msgs
    }
}
