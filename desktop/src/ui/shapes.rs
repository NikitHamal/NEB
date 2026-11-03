//! M3 Expressive shapes. Nine polygons with ONE point count (generated from the website's
//! `m3x/shapes.css`) so any shape morphs into any other by lerping points. All are star-shaped
//! around the centre, which lets a triangle fan fill them without a tessellator.
use egui::{epaint::Vertex, pos2, Color32, Mesh, Painter, Pos2, Rect, Shape as PShape, Stroke};

use super::shapes_data as d;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    Circle,
    Cookie,
    Sunny,
    Flower,
    Clover,
    Burst,
    Squircle,
    Gem,
    Pebble,
}

impl Kind {
    pub fn points(self) -> &'static [[f32; 2]; 120] {
        match self {
            Kind::Circle => &d::CIRCLE,
            Kind::Cookie => &d::COOKIE,
            Kind::Sunny => &d::SUNNY,
            Kind::Flower => &d::FLOWER,
            Kind::Clover => &d::CLOVER,
            Kind::Burst => &d::BURST,
            Kind::Squircle => &d::SQUIRCLE,
            Kind::Gem => &d::GEM,
            Kind::Pebble => &d::PEBBLE,
        }
    }
}

/// Paint `from` morphing into `to` (t = 0..1, may overshoot slightly with a spring), filling `rect`.
/// `rot` is radians about the centre. The fan is filled as a mesh and outlined with a 1px
/// anti-aliased line of the same colour so the edge is smooth.
pub fn paint_morph(p: &Painter, rect: Rect, from: Kind, to: Kind, t: f32, rot: f32, color: Color32) {
    let (a, b) = (from.points(), to.points());
    let c = rect.center();
    let (s, co) = rot.sin_cos();
    let pts: Vec<Pos2> = (0..120)
        .map(|i| {
            let x = (a[i][0] + (b[i][0] - a[i][0]) * t) / 100.0 - 0.5;
            let y = (a[i][1] + (b[i][1] - a[i][1]) * t) / 100.0 - 0.5;
            let (x, y) = (x * rect.width(), y * rect.height());
            pos2(c.x + x * co - y * s, c.y + x * s + y * co)
        })
        .collect();
    let mut mesh = Mesh::default();
    mesh.vertices.push(Vertex { pos: c, uv: egui::epaint::WHITE_UV, color });
    for q in &pts {
        mesh.vertices.push(Vertex { pos: *q, uv: egui::epaint::WHITE_UV, color });
    }
    for i in 0..120u32 {
        mesh.indices.extend_from_slice(&[0, 1 + i, 1 + (i + 1) % 120]);
    }
    p.add(PShape::mesh(mesh));
    p.add(PShape::closed_line(pts, Stroke::new(1.0, color)));
}

pub fn paint(p: &Painter, rect: Rect, kind: Kind, color: Color32) {
    paint_morph(p, rect, kind, kind, 0.0, 0.0, color);
}
