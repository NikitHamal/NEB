//! Community — the forum feed from the live API (`api/posts/`), a thread view with replies,
//! likes, bookmarks, and a composer. Guests can read; signing in unlocks writing.
use egui::{vec2, Align, Align2, Layout, RichText, Rounding, Sense, Stroke, Ui};
use serde_json::{json, Value};

use super::common::*;
use crate::actions::Action;
use crate::data::api::{b, n, s};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::avatar::avatar;
use crate::ui::icons::{self, Icon};
use crate::ui::widgets::{self, BtnKind};

pub const CATEGORIES: [&str; 5] = ["General", "Science", "Math", "Exam Prep", "Entrance Exams"];

#[derive(Clone, Default)]
pub struct Post {
    pub id: String,
    pub title: String,
    pub content: String,
    pub author: String,
    pub category: String,
    pub likes: i64,
    pub replies: i64,
    pub views: i64,
    pub liked: bool,
    pub bookmarked: bool,
    pub anonymous: bool,
    pub owner: bool,
    pub created: i64,
}

#[derive(Clone, Default)]
pub struct Reply {
    pub id: String,
    pub author: String,
    pub content: String,
    pub likes: i64,
    pub liked: bool,
    pub created: i64,
}

fn parse_post(v: &Value) -> Post {
    Post {
        id: s(v, "id"),
        title: s(v, "title"),
        content: s(v, "content"),
        author: if b(v, "isAnonymous") { "Anonymous".into() } else { s(v, "authorName") },
        category: s(v, "category"),
        likes: n(v, "thumbsUpCount"),
        replies: n(v, "replyCount"),
        views: n(v, "viewCount"),
        liked: b(v, "isThumbedUp"),
        bookmarked: b(v, "isBookmarked"),
        anonymous: b(v, "isAnonymous"),
        owner: b(v, "isOwner"),
        created: n(v, "createdAt"),
    }
}

fn parse_reply(v: &Value) -> Reply {
    Reply {
        id: s(v, "id"),
        author: if b(v, "isAnonymous") { "Anonymous".into() } else { s(v, "authorName") },
        content: s(v, "content"),
        likes: n(v, "thumbsUpCount"),
        liked: b(v, "isThumbedUp"),
        created: n(v, "createdAt"),
    }
}

/// `results` array of a paginated reply, or a bare array.
fn results(v: &Value) -> Vec<Value> {
    v.get("results").and_then(Value::as_array).cloned().or_else(|| v.as_array().cloned()).unwrap_or_default()
}

pub fn time_ago(ms: i64) -> String {
    let now = crate::util::now_secs() as i64;
    let d = (now - ms / 1000).max(0);
    match d {
        0..=59 => "just now".into(),
        60..=3599 => format!("{}m ago", d / 60),
        3600..=86399 => format!("{}h ago", d / 3600),
        86400..=2591999 => format!("{}d ago", d / 86400),
        _ => format!("{}mo ago", d / 2592000),
    }
}

/// Strip the most common markdown so previews read as plain prose.
fn plain(md: &str) -> String {
    md.lines()
        .map(|l| l.trim_start_matches('#').trim().replace("**", "").replace('`', "").replace("__", ""))
        .filter(|l| !l.is_empty() && l != "---")
        .collect::<Vec<_>>()
        .join(" ")
}

#[derive(Default)]
struct Composer {
    title: String,
    body: String,
    category: usize,
    anon: bool,
    send: Option<Task<Result<Value>>>,
    error: Option<String>,
}

#[derive(Default)]
struct Thread {
    id: String,
    post: Option<Post>,
    replies: Vec<Reply>,
    load: Option<Task<Result<(Post, Vec<Reply>)>>>,
    reply_text: String,
    send: Option<Task<Result<Value>>>,
    error: Option<String>,
}

#[derive(Default)]
pub struct CommunityState {
    category: Option<usize>,
    posts: Vec<Post>,
    loaded: bool,
    page: u32,
    has_more: bool,
    load: Option<Task<Result<(Vec<Post>, bool, u32)>>>,
    error: Option<String>,
    likes: Vec<(String, bool, Task<Result<Value>>)>,
    composer: Option<Composer>,
    thread: Thread,
}

fn fetch_page(env: &Env, st: &mut CommunityState, page: u32) {
    let api = env.api();
    let cat = st.category.map(|i| CATEGORIES[i].to_string()).unwrap_or_default();
    st.load = Some(Task::spawn(&env.ctx, move || {
        let p = page.to_string();
        let mut q: Vec<(&str, &str)> = vec![("page", &p), ("page_size", "20")];
        if !cat.is_empty() {
            q.push(("category", &cat));
        }
        let v = api.get("api/posts/", &q)?;
        let has_more = v.get("next").map(|x| !x.is_null()).unwrap_or(false);
        Ok((results(&v).iter().map(parse_post).collect(), has_more, page))
    }));
}

fn drive_feed(env: &mut Env, st: &mut CommunityState) {
    if !st.loaded && st.load.is_none() && !env.demo {
        fetch_page(env, st, 1);
    }
    if let Some(t) = st.load.as_mut() {
        if let Some(r) = t.poll() {
            st.load = None;
            match r {
                Ok((posts, more, page)) => {
                    if page == 1 {
                        st.posts = posts;
                    } else {
                        st.posts.extend(posts);
                    }
                    st.has_more = more;
                    st.page = page;
                    st.loaded = true;
                    st.error = None;
                }
                Err(e) => {
                    st.loaded = true;
                    if !env.handle_api_error(&e) {
                        st.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    let mut finished: Vec<(String, bool, Result<Value>)> = vec![];
    st.likes.retain_mut(|(id, was, t)| match t.poll() {
        Some(r) => {
            finished.push((id.clone(), *was, r));
            false
        }
        None => true,
    });
    for (id, was, r) in finished {
        if let Err(e) = r {
            // roll the optimistic toggle back
            for p in st.posts.iter_mut().chain(st.thread.post.iter_mut()).filter(|p| p.id == id) {
                p.liked = was;
                p.likes += if was { 1 } else { -1 };
            }
            if !env.handle_api_error(&e) {
                env.toast(format!("Could not update like: {e}"));
            }
        }
    }
    if let Some(c) = st.composer.as_mut() {
        if let Some(t) = c.send.as_mut() {
            if let Some(r) = t.poll() {
                c.send = None;
                match r {
                    Ok(_) => {
                        st.composer = None;
                        st.loaded = false;
                        st.posts.clear();
                        env.toast("Posted to the community");
                    }
                    Err(e) => {
                        if !env.handle_api_error(&e) {
                            c.error = Some(e.to_string());
                        }
                    }
                }
            }
        }
    }
}

fn toggle_like(env: &mut Env, st: &mut CommunityState, id: &str) {
    if !env.signed_in() {
        env.toast("Sign in to like posts");
        return;
    }
    let mut was = false;
    for p in st.posts.iter_mut().chain(st.thread.post.iter_mut()).filter(|p| p.id == id) {
        was = p.liked;
        p.liked = !p.liked;
        p.likes += if p.liked { 1 } else { -1 };
    }
    let api = env.api();
    let pid = id.to_string();
    st.likes.push((id.to_string(), was, Task::spawn(&env.ctx, move || api.post(&format!("api/posts/{pid}/like/"), json!({})))));
}

fn toggle_bookmark(env: &mut Env, st: &mut CommunityState, id: &str) {
    if !env.signed_in() {
        env.toast("Sign in to save posts");
        return;
    }
    let mut now = false;
    for p in st.posts.iter_mut().chain(st.thread.post.iter_mut()).filter(|p| p.id == id) {
        p.bookmarked = !p.bookmarked;
        now = p.bookmarked;
    }
    env.toast(if now { "Saved to your bookmarks" } else { "Removed from bookmarks" });
    let api = env.api();
    let pid = id.to_string();
    std::thread::spawn(move || {
        let _ = api.post("api/bookmarks/toggle/", json!({ "targetType": "post", "targetId": pid, "target_type": "post", "target_id": pid }));
    });
}

fn pill(ui: &mut Ui, env: &Env, icon: Icon, label: &str, active: bool) -> egui::Response {
    let th = &env.theme;
    let g = ui.painter().layout_no_wrap(label.to_owned(), fonts::medium(13.0), th.p.ink);
    let w = 44.0 + g.size().x;
    let (rect, resp) = ui.allocate_exact_size(vec2(w.max(48.0), 36.0), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
    let fg = if active { th.p.accent } else { th.p.ink_muted };
    if active {
        ui.painter().rect_filled(rect, Rounding::same(18.0), th.p.accent_soft);
    }
    ui.painter().rect_filled(rect, Rounding::same(18.0), th.p.ink.gamma_multiply(0.07 * hover));
    icons::paint(ui.painter(), egui::Rect::from_center_size(egui::pos2(rect.min.x + 22.0, rect.center().y), vec2(20.0, 20.0)), icon, fg);
    if !label.is_empty() {
        ui.painter().text(egui::pos2(rect.min.x + 38.0, rect.center().y), Align2::LEFT_CENTER, label, fonts::medium(13.0), fg);
    }
    if resp.hovered() {
        ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
    }
    resp
}

fn author_row(ui: &mut Ui, env: &Env, name: &str, meta: &str, tone: usize) {
    let th = &env.theme;
    ui.horizontal(|ui| {
        ui.spacing_mut().item_spacing.x = 12.0;
        avatar(ui, th, name, tone, 38.0);
        ui.vertical(|ui| {
            ui.spacing_mut().item_spacing.y = 0.0;
            widgets::label(ui, RichText::new(name).font(fonts::medium(14.0)).color(th.p.ink));
            widgets::label(ui, RichText::new(meta).font(fonts::regular(12.0)).color(th.p.ink_faint));
        });
    });
}

fn post_card(ui: &mut Ui, env: &mut Env, st: &mut CommunityState, p: &Post, w: f32) {
    let th = env.theme.clone();
    let mut open = false;
    let mut like = false;
    let mut mark = false;
    egui::Frame::none()
        .fill(th.p.card)
        .stroke(Stroke::new(1.0, th.p.hairline))
        .rounding(Rounding::same(crate::theme::spacing::CARD_RADIUS))
        .inner_margin(egui::Margin::symmetric(20.0, 16.0))
        .show(ui, |ui| {
            ui.set_width(w - 42.0);
            ui.horizontal(|ui| {
                author_row(ui, env, &p.author, &time_ago(p.created), p.author.len());
                ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                    widgets::badge(ui, &p.category, th.p.on_secondary_container, th.p.secondary_container);
                });
            });
            ui.add_space(10.0);
            let t = ui.add(egui::Label::new(RichText::new(&p.title).font(fonts::bold(18.0)).color(th.p.ink)).selectable(false).sense(Sense::click()));
            if t.hovered() {
                ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
            }
            open |= t.clicked();
            ui.add_space(4.0);
            let body = crate::util::truncate(&plain(&p.content), 260);
            ui.add(egui::Label::new(RichText::new(body).font(fonts::regular(14.5)).color(th.p.ink_muted)).selectable(false));
            ui.add_space(10.0);
            ui.horizontal(|ui| {
                ui.spacing_mut().item_spacing.x = 4.0;
                like |= pill(ui, env, if p.liked { Icon::ThumbUpFilled } else { Icon::ThumbUp }, &p.likes.to_string(), p.liked).clicked();
                open |= pill(ui, env, Icon::Chat, &p.replies.to_string(), false).clicked();
                let _ = pill(ui, env, Icon::Eye, &p.views.to_string(), false);
                ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                    mark |= pill(ui, env, if p.bookmarked { Icon::BookmarkFilled } else { Icon::Bookmark }, "", p.bookmarked).on_hover_text("Save").clicked();
                });
            });
        });
    if open {
        env.go(Route::Post(p.id.clone()));
    }
    if like {
        toggle_like(env, st, &p.id);
    }
    if mark {
        toggle_bookmark(env, st, &p.id);
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut CommunityState) {
    drive_feed(env, st);
    scroll_page(ui, env, "community", |ui, env| {
        let th = env.theme.clone();
        let w = ui.available_width();
        ui.horizontal(|ui| {
            ui.vertical(|ui| {
                widgets::heading(ui, &th, "Community", 30.0);
                widgets::muted(ui, &th, "Questions, answers and study talk from learners across Nepal.");
            });
            right(ui, |ui| {
                ui.add_enabled_ui(true, |ui| {
                    if widgets::button(ui, &th, "New post", BtnKind::Primary, Some(Icon::Compose), None).clicked() {
                        if env.signed_in() {
                            st.composer = Some(Composer::default());
                        } else {
                            env.toast("Sign in to post in the community");
                        }
                    }
                });
                if widgets::icon_button(ui, &th, Icon::Refresh, "Refresh", false).clicked() {
                    st.loaded = false;
                    st.posts.clear();
                }
            });
        });
        ui.add_space(14.0);
        if !env.signed_in() {
            guest_banner(ui, env, w);
            ui.add_space(14.0);
        }
        ui.horizontal_wrapped(|ui| {
            if widgets::chip(ui, &th, "All", st.category.is_none()).clicked() && st.category.is_some() {
                st.category = None;
                st.loaded = false;
                st.posts.clear();
            }
            for (i, c) in CATEGORIES.iter().enumerate() {
                if widgets::chip(ui, &th, c, st.category == Some(i)).clicked() && st.category != Some(i) {
                    st.category = Some(i);
                    st.loaded = false;
                    st.posts.clear();
                }
            }
        });
        ui.add_space(16.0);
        if let Some(e) = st.error.clone() {
            crate::screens::login::error_banner(ui, &th, &e, w);
            ui.add_space(10.0);
            if widgets::button(ui, &th, "Try again", BtnKind::Tonal, Some(Icon::Refresh), None).clicked() {
                st.error = None;
                st.loaded = false;
            }
        } else if st.load.is_some() && st.posts.is_empty() {
            for _ in 0..3 {
                skeleton(ui, &th, w);
                ui.add_space(12.0);
            }
        } else if st.loaded && st.posts.is_empty() {
            widgets::empty_state(ui, &th, Icon::Forum, "Nothing here yet", "Be the first to start a conversation in this category.");
        }
        let posts = st.posts.clone();
        for p in &posts {
            post_card(ui, env, st, p, w);
            ui.add_space(12.0);
        }
        if st.has_more && st.load.is_none() {
            ui.vertical_centered(|ui| {
                if widgets::button(ui, &th, "Load more", BtnKind::Tonal, Some(Icon::ChevronDown), None).clicked() {
                    let next = st.page + 1;
                    fetch_page(env, st, next);
                }
            });
        } else if st.load.is_some() && !st.posts.is_empty() {
            ui.vertical_centered(|ui| ui.add(egui::Spinner::new().color(th.p.accent)));
        }
        ui.add_space(30.0);
    });
    composer_window(ui.ctx(), env, st);
}

fn skeleton(ui: &mut Ui, th: &crate::theme::Theme, w: f32) {
    let (rect, _) = ui.allocate_exact_size(vec2(w, 138.0), Sense::hover());
    let t = (ui.input(|i| i.time) * 1.6).sin() as f32 * 0.5 + 0.5;
    ui.ctx().request_repaint();
    let c = crate::theme::mix(th.p.field, th.p.card, t * 0.5);
    ui.painter().rect_filled(rect, Rounding::same(20.0), th.p.card);
    ui.painter().rect_stroke(rect, Rounding::same(20.0), Stroke::new(1.0, th.p.hairline));
    ui.painter().circle_filled(rect.min + vec2(38.0, 36.0), 18.0, c);
    for (i, f) in [0.35, 0.8, 0.6].iter().enumerate() {
        ui.painter().rect_filled(egui::Rect::from_min_size(rect.min + vec2(68.0 - if i > 0 { 50.0 } else { 0.0 }, 28.0 + i as f32 * 28.0), vec2((w - 100.0) * f, 12.0)), Rounding::same(6.0), c);
    }
}

fn guest_banner(ui: &mut Ui, env: &mut Env, w: f32) {
    let th = env.theme.clone();
    egui::Frame::none().fill(th.p.accent_soft).rounding(Rounding::same(24.0)).inner_margin(egui::Margin::symmetric(18.0, 14.0)).show(ui, |ui| {
        ui.set_width(w - 38.0);
        ui.horizontal(|ui| {
            let r = ui.allocate_exact_size(vec2(26.0, 26.0), Sense::hover()).0;
            icons::paint(ui.painter(), r, Icon::Person, th.p.on_accent_soft);
            ui.vertical(|ui| {
                widgets::label(ui, RichText::new("You're browsing as a guest").font(fonts::bold(14.5)).color(th.p.on_accent_soft));
                widgets::label(ui, RichText::new("Sign in to like, reply and post.").font(fonts::regular(13.0)).color(th.p.on_accent_soft));
            });
            right(ui, |ui| {
                if widgets::button_sized(ui, &th, "Sign in", BtnKind::Primary, None, None, 40.0).clicked() {
                    env.act(Action::Replace(Route::Login));
                }
            });
        });
    });
}

fn composer_window(ctx: &egui::Context, env: &mut Env, st: &mut CommunityState) {
    if st.composer.is_none() {
        return;
    }
    let th = env.theme.clone();
    let mut close = false;
    let mut submit = false;
    egui::Window::new("New post")
        .title_bar(false)
        .collapsible(false)
        .resizable(false)
        .anchor(Align2::CENTER_CENTER, [0.0, 0.0])
        .fixed_size([ctx.screen_rect().width().min(620.0) - 40.0, 0.0])
        .frame(egui::Frame::none().fill(th.p.card).rounding(Rounding::same(28.0)).stroke(Stroke::new(1.0, th.p.hairline)).shadow(ctx.style().visuals.window_shadow).inner_margin(egui::Margin::same(24.0)))
        .show(ctx, |ui| {
            let c = st.composer.as_mut().unwrap();
            let w = ui.available_width();
            ui.horizontal(|ui| {
                widgets::heading(ui, &th, "New post", 22.0);
                right(ui, |ui| {
                    if widgets::icon_button(ui, &th, Icon::Close, "Close (Esc)", false).clicked() {
                        close = true;
                    }
                });
            });
            ui.add_space(14.0);
            widgets::field(ui, &th, &mut c.title, "Title", Some(Icon::Article), w, false, false);
            ui.add_space(10.0);
            widgets::text_area(ui, &th, &mut c.body, "What would you like to discuss or ask?", w, 6);
            ui.add_space(12.0);
            ui.horizontal_wrapped(|ui| {
                for (i, name) in CATEGORIES.iter().enumerate() {
                    if widgets::chip(ui, &th, name, c.category == i).clicked() {
                        c.category = i;
                    }
                }
            });
            ui.add_space(8.0);
            if widgets::chip(ui, &th, "Post anonymously", c.anon).clicked() {
                c.anon = !c.anon;
            }
            if let Some(e) = c.error.clone() {
                ui.add_space(10.0);
                crate::screens::login::error_banner(ui, &th, &e, w);
            }
            ui.add_space(16.0);
            let busy = c.send.is_some();
            let ready = c.title.trim().len() >= 3 && c.body.trim().len() >= 3;
            ui.horizontal(|ui| {
                right(ui, |ui| {
                    ui.add_enabled_ui(ready && !busy, |ui| {
                        if widgets::button(ui, &th, if busy { "Posting…" } else { "Post" }, BtnKind::Primary, Some(Icon::Send), None).clicked() {
                            submit = true;
                        }
                    });
                    if widgets::button(ui, &th, "Cancel", BtnKind::Ghost, None, None).clicked() {
                        close = true;
                    }
                });
            });
        });
    if ctx.input(|i| i.key_pressed(egui::Key::Escape)) {
        close = true;
    }
    if submit {
        let c = st.composer.as_mut().unwrap();
        let body = json!({ "title": c.title.trim(), "content": c.body.trim(), "category": CATEGORIES[c.category], "isAnonymous": c.anon, "image_urls": [] });
        let api = env.api();
        c.error = None;
        c.send = Some(Task::spawn(ctx, move || api.post("api/posts/", body)));
    }
    if close {
        st.composer = None;
    }
}

// ---------------------------------------------------------------- thread

fn load_thread(env: &Env, st: &mut CommunityState, id: &str) {
    st.thread = Thread { id: id.to_string(), ..Default::default() };
    let api = env.api();
    let pid = id.to_string();
    st.thread.load = Some(Task::spawn(&env.ctx, move || {
        let post = parse_post(&api.get(&format!("api/posts/{pid}/"), &[])?);
        let replies = api.get(&format!("api/posts/{pid}/replies/"), &[]).map(|v| results(&v).iter().map(parse_reply).collect()).unwrap_or_default();
        let _ = api.post(&format!("api/posts/{pid}/view/"), json!({}));
        Ok((post, replies))
    }));
}

pub fn show_post(ui: &mut Ui, env: &mut Env, st: &mut CommunityState, id: &str) {
    if st.thread.id != id {
        if env.demo {
            st.demo_thread(id);
        } else {
            load_thread(env, st, id);
        }
    }
    drive_feed(env, st);
    if let Some(t) = st.thread.load.as_mut() {
        if let Some(r) = t.poll() {
            st.thread.load = None;
            match r {
                Ok((p, rs)) => {
                    st.thread.post = Some(p);
                    st.thread.replies = rs;
                }
                Err(e) => {
                    if !env.handle_api_error(&e) {
                        st.thread.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    let mut reload = false;
    if let Some(t) = st.thread.send.as_mut() {
        if let Some(r) = t.poll() {
            st.thread.send = None;
            match r {
                Ok(_) => {
                    st.thread.reply_text.clear();
                    reload = true;
                    env.toast("Reply posted");
                }
                Err(e) => {
                    if !env.handle_api_error(&e) {
                        st.thread.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    if reload {
        st.loaded = false;
        let keep = st.thread.id.clone();
        load_thread(env, st, &keep);
    }
    scroll_page(ui, env, "post", |ui, env| {
        let th = env.theme.clone();
        let w = ui.available_width();
        ui.horizontal(|ui| {
            if widgets::icon_button(ui, &th, Icon::Back, "Back (Esc)", false).clicked() {
                env.act(Action::Back);
            }
            widgets::heading(ui, &th, "Discussion", 24.0);
        });
        ui.add_space(12.0);
        if let Some(e) = st.thread.error.clone() {
            crate::screens::login::error_banner(ui, &th, &e, w);
            return;
        }
        let Some(p) = st.thread.post.clone() else {
            ui.vertical_centered(|ui| {
                ui.add_space(40.0);
                ui.add(egui::Spinner::new().size(28.0).color(th.p.accent));
            });
            return;
        };
        egui::Frame::none().fill(th.p.card).stroke(Stroke::new(1.0, th.p.hairline)).rounding(Rounding::same(28.0)).inner_margin(egui::Margin::same(24.0)).show(ui, |ui| {
            ui.set_width(w - 50.0);
            ui.horizontal(|ui| {
                author_row(ui, env, &p.author, &time_ago(p.created), p.author.len());
                right(ui, |ui| widgets::badge(ui, &p.category, th.p.on_secondary_container, th.p.secondary_container));
            });
            ui.add_space(14.0);
            ui.add(egui::Label::new(RichText::new(&p.title).font(fonts::bold(26.0)).color(th.p.ink)));
            ui.add_space(10.0);
            for line in p.content.lines() {
                let t = line.trim();
                if t.is_empty() {
                    ui.add_space(6.0);
                } else if t.starts_with('#') {
                    ui.add(egui::Label::new(RichText::new(t.trim_start_matches('#').trim().replace("**", "")).font(fonts::bold(18.0)).color(th.p.ink)));
                } else {
                    ui.add(egui::Label::new(RichText::new(t.replace("**", "").replace('`', "")).font(fonts::regular(15.5)).color(th.p.ink)));
                }
            }
            ui.add_space(14.0);
            let (mut like, mut mark) = (false, false);
            ui.horizontal(|ui| {
                like = pill(ui, env, if p.liked { Icon::ThumbUpFilled } else { Icon::ThumbUp }, &p.likes.to_string(), p.liked).clicked();
                let _ = pill(ui, env, Icon::Chat, &st.thread.replies.len().to_string(), false);
                right(ui, |ui| {
                    mark = pill(ui, env, if p.bookmarked { Icon::BookmarkFilled } else { Icon::Bookmark }, "", p.bookmarked).clicked();
                });
            });
            if like {
                toggle_like(env, st, &p.id);
            }
            if mark {
                toggle_bookmark(env, st, &p.id);
            }
        });
        ui.add_space(18.0);
        widgets::heading(ui, &th, &format!("Replies · {}", st.thread.replies.len()), 19.0);
        ui.add_space(10.0);
        if env.signed_in() {
            let busy = st.thread.send.is_some();
            widgets::text_area(ui, &th, &mut st.thread.reply_text, "Write a reply…", w, 3);
            ui.add_space(8.0);
            ui.horizontal(|ui| {
                right(ui, |ui| {
                    ui.add_enabled_ui(!busy && st.thread.reply_text.trim().len() >= 2, |ui| {
                        if widgets::button(ui, &th, if busy { "Sending…" } else { "Reply" }, BtnKind::Primary, Some(Icon::Send), None).clicked() {
                            let api = env.api();
                            let pid = p.id.clone();
                            let body = json!({ "content": st.thread.reply_text.trim() });
                            st.thread.send = Some(Task::spawn(&env.ctx, move || api.post(&format!("api/posts/{pid}/replies/"), body)));
                        }
                    });
                });
            });
        } else {
            guest_banner(ui, env, w);
        }
        ui.add_space(14.0);
        if st.thread.replies.is_empty() {
            widgets::empty_state(ui, &th, Icon::Chat, "No replies yet", "Start the conversation.");
        }
        for r in st.thread.replies.clone() {
            egui::Frame::none().fill(th.p.card).stroke(Stroke::new(1.0, th.p.hairline)).rounding(Rounding::same(20.0)).inner_margin(egui::Margin::symmetric(18.0, 14.0)).show(ui, |ui| {
                ui.set_width(w - 38.0);
                author_row(ui, env, &r.author, &time_ago(r.created), r.author.len());
                ui.add_space(8.0);
                ui.add(egui::Label::new(RichText::new(plain(&r.content)).font(fonts::regular(15.0)).color(th.p.ink)));
            });
            ui.add_space(10.0);
        }
        ui.add_space(30.0);
    });
}

// ------------------------------------------------------------ sample data (screenshot tour only)

impl CommunityState {
    /// Bundled sample posts used by `--screenshots` so signed-in screens can be photographed
    /// without a live account. Never reachable in normal use (`Env::demo` is false).
    pub fn demo(&mut self) {
        let now = crate::util::now_secs() as i64 * 1000;
        let mk = |id: &str, title: &str, body: &str, who: &str, cat: &str, likes: i64, replies: i64, views: i64, ago_min: i64, liked: bool| Post {
            id: id.into(),
            title: title.into(),
            content: body.into(),
            author: who.into(),
            category: cat.into(),
            likes,
            replies,
            views,
            liked,
            created: now - ago_min * 60_000,
            ..Default::default()
        };
        self.posts = vec![
            mk("d1", "How do you approach projectile-motion MCQs in IOE?", "I keep losing marks on the range and time-of-flight questions when the launch angle is not given. Is there a quick way to decide which formula to use before I start calculating?", "Sita Rai", "Entrance Exams", 18, 6, 214, 42, true),
            mk("d2", "Organic chemistry: how to remember named reactions", "Preparing for CEE and the named reactions are the part I forget fastest. What worked for you — flashcards, writing the mechanism, or past papers?", "Anish Karki", "Science", 11, 4, 143, 190, false),
            mk("d3", "Weekly study group for Class 12 Mathematics (Lalitpur)", "We meet on Saturdays to work through integration and probability. Reply here if you would like to join — all levels welcome.", "Prabin Shrestha", "Math", 27, 12, 388, 1500, false),
            mk("d4", "Model question: why does the Hall voltage reverse for p-type?", "Chapter 'Current electricity' — I understand the n-type case but cannot see why the sign flips for holes as majority carriers.", "Anonymous", "Exam Prep", 6, 3, 97, 4300, false),
        ];
        self.loaded = true;
    }

    fn demo_thread(&mut self, id: &str) {
        if self.posts.is_empty() {
            self.demo();
        }
        let now = crate::util::now_secs() as i64 * 1000;
        self.thread = Thread { id: id.to_string(), post: self.posts.first().cloned(), ..Default::default() };
        self.thread.replies = vec![
            Reply { id: "r1".into(), author: "Anish Karki".into(), content: "First check what is given: if the launch angle is missing, the question almost always hands you either the range and the maximum height, or the time of flight. Use their ratio to get the angle, then everything else follows.".into(), likes: 9, liked: false, created: now - 30 * 60_000 },
            Reply { id: "r2".into(), author: "Prabin Shrestha".into(), content: "Write the three standard results (T, R, H) on one line at the top of the page before you start. It saves time and stops you mixing them up.".into(), likes: 4, liked: true, created: now - 12 * 60_000 },
        ];
    }
}
