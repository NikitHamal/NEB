//! Vector icons drawn with the egui painter on a 24×24 grid (no icon font needed,
//! crisp at any DPI, recoloured by the theme).
use egui::{pos2, vec2, Color32, Painter, Pos2, Rect, Shape, Stroke};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Icon {
    Home,
    Library,
    Search,
    Bookmark,
    BookmarkFilled,
    Download,
    Settings,
    Back,
    Forward,
    ChevronRight,
    ChevronDown,
    Check,
    Close,
    Plus,
    Minus,
    User,
    Info,
    Clock,
    Contrast,
    External,
    Folder,
    Trash,
    Eye,
    Keyboard,
    Globe,
    Lock,
    Bolt,
    File,
    Menu,
    Play,
    School,
    Edit,
    Mail,
    Logout,
    List,
}

pub fn paint(p: &Painter, r: Rect, icon: Icon, color: Color32) {
    let k = r.width().min(r.height()) / 24.0;
    let o = r.center() - vec2(12.0 * k, 12.0 * k);
    let pt = |x: f32, y: f32| pos2(o.x + x * k, o.y + y * k);
    let sw = (1.9 * k).max(1.3);
    let st = Stroke::new(sw, color);
    let line = |pts: &[(f32, f32)]| {
        let v: Vec<Pos2> = pts.iter().map(|&(x, y)| pt(x, y)).collect();
        p.add(Shape::line(v, st));
    };
    let closed = |pts: &[(f32, f32)]| {
        let v: Vec<Pos2> = pts.iter().map(|&(x, y)| pt(x, y)).collect();
        p.add(Shape::closed_line(v, st));
    };
    let circle = |x: f32, y: f32, rad: f32| {
        p.circle_stroke(pt(x, y), rad * k, st);
    };
    let dot = |x: f32, y: f32, rad: f32| {
        p.circle_filled(pt(x, y), rad * k, color);
    };
    let arc = |cx: f32, cy: f32, rad: f32, a0: f32, a1: f32| -> Vec<(f32, f32)> {
        (0..=16)
            .map(|i| {
                let a = (a0 + (a1 - a0) * i as f32 / 16.0).to_radians();
                (cx + rad * a.cos(), cy + rad * a.sin())
            })
            .collect()
    };
    match icon {
        Icon::Home => {
            line(&[(3.0, 11.0), (12.0, 3.5), (21.0, 11.0)]);
            line(&[(5.5, 9.5), (5.5, 20.0), (10.0, 20.0), (10.0, 14.0), (14.0, 14.0), (14.0, 20.0), (18.5, 20.0), (18.5, 9.5)]);
        }
        Icon::Library => {
            line(&[(12.0, 6.5), (12.0, 20.0)]);
            line(&[(12.0, 6.5), (7.5, 4.5), (3.0, 5.5), (3.0, 18.0), (7.5, 17.0), (12.0, 20.0)]);
            line(&[(12.0, 6.5), (16.5, 4.5), (21.0, 5.5), (21.0, 18.0), (16.5, 17.0), (12.0, 20.0)]);
        }
        Icon::Search => {
            circle(10.5, 10.5, 6.5);
            line(&[(15.3, 15.3), (21.0, 21.0)]);
        }
        Icon::Bookmark => closed(&[(6.0, 3.0), (18.0, 3.0), (18.0, 21.0), (12.0, 16.5), (6.0, 21.0)]),
        Icon::BookmarkFilled => {
            p.rect_filled(Rect::from_two_pos(pt(6.0, 3.0), pt(18.0, 16.5)), 0.0, color);
            p.add(Shape::convex_polygon(vec![pt(6.0, 16.5), pt(12.0, 16.5), pt(6.0, 21.0)], color, Stroke::NONE));
            p.add(Shape::convex_polygon(vec![pt(12.0, 16.5), pt(18.0, 16.5), pt(18.0, 21.0)], color, Stroke::NONE));
        }
        Icon::Download => {
            line(&[(12.0, 3.5), (12.0, 15.0)]);
            line(&[(7.0, 10.5), (12.0, 15.5), (17.0, 10.5)]);
            line(&[(4.0, 16.0), (4.0, 20.0), (20.0, 20.0), (20.0, 16.0)]);
        }
        Icon::Settings => {
            for (x, y) in [(8.5, 6.0), (16.0, 12.0), (9.5, 18.0)] {
                line(&[(3.0, y), (x - 3.0, y)]);
                line(&[(x + 3.0, y), (21.0, y)]);
                circle(x, y, 2.7);
            }
        }
        Icon::Back => {
            line(&[(20.0, 12.0), (4.5, 12.0)]);
            line(&[(10.5, 5.5), (4.0, 12.0), (10.5, 18.5)]);
        }
        Icon::Forward => {
            line(&[(4.0, 12.0), (19.5, 12.0)]);
            line(&[(13.5, 5.5), (20.0, 12.0), (13.5, 18.5)]);
        }
        Icon::ChevronRight => line(&[(9.0, 5.0), (16.0, 12.0), (9.0, 19.0)]),
        Icon::ChevronDown => line(&[(5.0, 9.0), (12.0, 16.0), (19.0, 9.0)]),
        Icon::Check => line(&[(4.0, 12.5), (9.5, 18.0), (20.0, 6.5)]),
        Icon::Close => {
            line(&[(5.5, 5.5), (18.5, 18.5)]);
            line(&[(18.5, 5.5), (5.5, 18.5)]);
        }
        Icon::Plus => {
            line(&[(12.0, 4.5), (12.0, 19.5)]);
            line(&[(4.5, 12.0), (19.5, 12.0)]);
        }
        Icon::Minus => line(&[(4.5, 12.0), (19.5, 12.0)]),
        Icon::User => {
            circle(12.0, 8.0, 4.2);
            line(&arc(12.0, 21.0, 8.5, 180.0, 360.0));
        }
        Icon::Info => {
            circle(12.0, 12.0, 9.0);
            line(&[(12.0, 11.0), (12.0, 17.0)]);
            dot(12.0, 7.6, 1.2);
        }
        Icon::Clock => {
            circle(12.0, 12.0, 9.0);
            line(&[(12.0, 7.0), (12.0, 12.0), (15.8, 14.2)]);
        }
        Icon::Contrast => {
            circle(12.0, 12.0, 9.0);
            let mut pts: Vec<Pos2> = arc(12.0, 12.0, 9.0, 90.0, 270.0).into_iter().map(|(x, y)| pt(x, y)).collect();
            pts.push(pt(12.0, 3.0));
            p.add(Shape::convex_polygon(pts, color, Stroke::NONE));
        }
        Icon::External => {
            line(&[(14.0, 4.0), (20.0, 4.0), (20.0, 10.0)]);
            line(&[(20.0, 4.0), (11.0, 13.0)]);
            line(&[(18.0, 14.5), (18.0, 20.0), (4.0, 20.0), (4.0, 6.0), (9.5, 6.0)]);
        }
        Icon::Folder => closed(&[(3.0, 6.0), (10.0, 6.0), (12.0, 8.5), (21.0, 8.5), (21.0, 19.0), (3.0, 19.0)]),
        Icon::Trash => {
            line(&[(4.0, 7.0), (20.0, 7.0)]);
            line(&[(9.0, 7.0), (9.0, 4.0), (15.0, 4.0), (15.0, 7.0)]);
            line(&[(6.0, 7.0), (7.0, 20.0), (17.0, 20.0), (18.0, 7.0)]);
        }
        Icon::Eye => {
            let top = arc(12.0, 18.0, 9.0, 235.0, 305.0);
            let bot = arc(12.0, 6.0, 9.0, 55.0, 125.0);
            let mut pts = top;
            pts.extend(bot);
            let v: Vec<Pos2> = pts.into_iter().map(|(x, y)| pt(x, y)).collect();
            p.add(Shape::closed_line(v, st));
            circle(12.0, 12.0, 3.0);
        }
        Icon::Keyboard => {
            p.rect_stroke(Rect::from_two_pos(pt(2.5, 6.0), pt(21.5, 18.0)), 2.5 * k, st);
            for (x, y) in [(6.5, 10.0), (10.0, 10.0), (13.5, 10.0), (17.0, 10.0)] {
                dot(x, y, 0.9);
            }
            line(&[(7.0, 14.5), (17.0, 14.5)]);
        }
        Icon::Globe => {
            circle(12.0, 12.0, 9.0);
            line(&[(3.0, 12.0), (21.0, 12.0)]);
            let e: Vec<(f32, f32)> = (0..=24).map(|i| {
                let a = (i as f32 / 24.0 * 360.0).to_radians();
                (12.0 + 4.0 * a.cos(), 12.0 + 9.0 * a.sin())
            }).collect();
            line(&e);
        }
        Icon::Lock => {
            p.rect_stroke(Rect::from_two_pos(pt(5.0, 11.0), pt(19.0, 21.0)), 2.0 * k, st);
            line(&arc(12.0, 11.0, 4.5, 180.0, 360.0));
        }
        Icon::Bolt => closed(&[(13.0, 2.5), (5.0, 13.0), (11.0, 13.0), (10.0, 21.5), (19.0, 10.0), (13.0, 10.0)]),
        Icon::File => {
            line(&[(14.0, 3.0), (6.0, 3.0), (6.0, 21.0), (19.0, 21.0), (19.0, 8.0), (14.0, 3.0), (14.0, 8.0), (19.0, 8.0)]);
            line(&[(9.0, 13.0), (16.0, 13.0)]);
            line(&[(9.0, 17.0), (16.0, 17.0)]);
        }
        Icon::Menu => {
            line(&[(4.0, 7.0), (20.0, 7.0)]);
            line(&[(4.0, 12.0), (20.0, 12.0)]);
            line(&[(4.0, 17.0), (20.0, 17.0)]);
        }
        Icon::Play => {
            p.add(Shape::convex_polygon(vec![pt(8.0, 5.0), pt(19.0, 12.0), pt(8.0, 19.0)], color, Stroke::NONE));
        }
        Icon::School => {
            closed(&[(2.0, 9.0), (12.0, 4.0), (22.0, 9.0), (12.0, 14.0)]);
            line(&[(6.0, 11.5), (6.0, 16.0), (12.0, 19.0), (18.0, 16.0), (18.0, 11.5)]);
            line(&[(22.0, 9.0), (22.0, 15.0)]);
        }
        Icon::Edit => closed(&[(4.0, 20.0), (5.0, 15.0), (16.0, 4.0), (20.0, 8.0), (9.0, 19.0)]),
        Icon::Mail => {
            p.rect_stroke(Rect::from_two_pos(pt(3.0, 5.5), pt(21.0, 18.5)), 2.5 * k, st);
            line(&[(3.5, 7.0), (12.0, 13.5), (20.5, 7.0)]);
        }
        Icon::Logout => {
            line(&[(10.0, 4.0), (4.5, 4.0), (4.5, 20.0), (10.0, 20.0)]);
            line(&[(9.0, 12.0), (20.0, 12.0)]);
            line(&[(15.5, 7.5), (20.0, 12.0), (15.5, 16.5)]);
        }
        Icon::List => {
            for y in [7.0, 12.0, 17.0] {
                dot(4.5, y, 1.1);
                line(&[(8.5, y), (20.0, y)]);
            }
        }
    }
}
