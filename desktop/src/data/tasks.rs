//! Tiny background-task helper: run a closure on a thread, poll for the result
//! from the UI thread, and wake the UI when it lands.
use std::sync::mpsc::{channel, Receiver, TryRecvError};

pub struct Task<T> {
    rx: Receiver<T>,
    finished: bool,
}

impl<T: Send + 'static> Task<T> {
    pub fn spawn(ctx: &egui::Context, f: impl FnOnce() -> T + Send + 'static) -> Self {
        let (tx, rx) = channel();
        let ctx = ctx.clone();
        std::thread::spawn(move || {
            let v = f();
            let _ = tx.send(v);
            ctx.request_repaint();
        });
        Self { rx, finished: false }
    }

    pub fn poll(&mut self) -> Option<T> {
        if self.finished {
            return None;
        }
        match self.rx.try_recv() {
            Ok(v) => {
                self.finished = true;
                Some(v)
            }
            Err(TryRecvError::Empty) => None,
            Err(TryRecvError::Disconnected) => {
                self.finished = true;
                None
            }
        }
    }

    pub fn is_running(&self) -> bool {
        !self.finished
    }
}
