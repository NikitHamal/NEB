//! A keyed cache of values loaded on a background thread: `get` returns immediately with
//! `Loading`, `Ready` or `Failed`, and the UI repaints when a load lands.
use std::collections::HashMap;
use std::sync::Arc;

use crate::data::tasks::Task;
use crate::errors::Result;

pub enum Slot<T> {
    Loading(Task<Result<T>>),
    Ready(Arc<T>),
    Failed(String),
}

pub struct Lazy<T> {
    slots: HashMap<String, Slot<T>>,
}

impl<T> Default for Lazy<T> {
    fn default() -> Self {
        Self { slots: HashMap::new() }
    }
}

pub enum View<T> {
    Loading,
    Ready(Arc<T>),
    Failed(String),
}

impl<T: Send + 'static> Lazy<T> {
    pub fn get(&mut self, ctx: &egui::Context, key: &str, load: impl FnOnce() -> Result<T> + Send + 'static) -> View<T> {
        if !self.slots.contains_key(key) {
            self.slots.insert(key.to_string(), Slot::Loading(Task::spawn(ctx, load)));
        }
        if let Some(Slot::Loading(t)) = self.slots.get_mut(key) {
            if let Some(res) = t.poll() {
                let slot = match res {
                    Ok(v) => Slot::Ready(Arc::new(v)),
                    Err(e) => Slot::Failed(e.to_string()),
                };
                self.slots.insert(key.to_string(), slot);
            }
        }
        match self.slots.get(key) {
            Some(Slot::Ready(v)) => View::Ready(v.clone()),
            Some(Slot::Failed(m)) => View::Failed(m.clone()),
            _ => View::Loading,
        }
    }

    pub fn peek(&self, key: &str) -> Option<Arc<T>> {
        match self.slots.get(key) {
            Some(Slot::Ready(v)) => Some(v.clone()),
            _ => None,
        }
    }

    pub fn forget(&mut self, key: &str) {
        self.slots.remove(key);
    }

    pub fn clear(&mut self) {
        self.slots.clear();
    }

    pub fn retry_failed(&mut self) {
        self.slots.retain(|_, s| !matches!(s, Slot::Failed(_)));
    }
}
