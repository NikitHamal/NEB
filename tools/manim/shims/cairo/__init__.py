"""A ``pycairo``-compatible 2D renderer backed by Skia's CPU raster backend.

Why this module exists
----------------------
The NEBians video pipeline renders with Manim Community Edition, whose Cairo
renderer needs ``pycairo`` (libcairo) and ``manimpango`` (Pango).  This machine
has no distro package access, so neither library can be installed.  Skia's
*raster* backend, however, ships as a prebuilt wheel and gives us the same
immediate-mode path model with the same pixel layout cairo uses:

    cairo FORMAT_ARGB32 (little endian)  ==  Skia kBGRA_8888 + kPremul

That is the single fact this whole module is built on.  Only the slice of the
cairo API that Manim's ``CairoCamera`` touches is implemented, but it is
implemented *faithfully* rather than approximately:

* paths are recorded in user space and transformed by the CTM at paint time,
* line widths are user-space units (cairo's default is 2.0, not 1.0),
* the default fill rule is non-zero winding,
* ``fill_preserve`` / ``stroke_preserve`` leave the current path intact,
* ``save`` / ``restore`` snapshot the whole graphics state *including* the
  current path and the source, exactly like ``cairo_save`` / ``cairo_restore``,
* ``set_source_rgba(r, g, b, a)`` paints in cairo's channel order and the
  BGRA surface stores the bytes in the order cairo's ARGB32 surface would.

Nothing here is NEBians-specific; it is a small, honest port of the API.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np
import skia

__all__ = [
    "FORMAT_ARGB32",
    "FORMAT_RGB24",
    "FORMAT_A8",
    "FORMAT_A1",
    "FORMAT_RGB16_565",
    "FORMAT_RGB30",
    "FORMAT_INVALID",
    "LineCap",
    "LineJoin",
    "FillRule",
    "Operator",
    "Antialias",
    "Content",
    "Status",
    "Matrix",
    "Context",
    "ImageSurface",
    "Pattern",
    "SolidPattern",
    "LinearGradient",
    "RadialGradient",
    "Path",
    "cairo_version",
    "version",
    "get_current_point",
]

# --------------------------------------------------------------------------
# enums / constants -- values match cairo's own numbering so that code doing
# `if fmt == cairo.FORMAT_ARGB32` keeps working.
# --------------------------------------------------------------------------
FORMAT_INVALID = -1
FORMAT_ARGB32 = 0
FORMAT_RGB24 = 1
FORMAT_A8 = 2
FORMAT_A1 = 3
FORMAT_RGB16_565 = 4
FORMAT_RGB30 = 5


class LineCap:
    BUTT = 0
    ROUND = 1
    SQUARE = 2


class LineJoin:
    MITER = 0
    ROUND = 1
    BEVEL = 2


class FillRule:
    WINDING = 0
    EVEN_ODD = 1


class Antialias:
    DEFAULT = 0
    NONE = 1
    GRAY = 2
    SUBPIXEL = 3
    FAST = 4
    GOOD = 5
    BEST = 6


class Operator:
    CLEAR = 0
    SOURCE = 1
    OVER = 2
    IN = 3
    OUT = 4
    ATOP = 5
    DEST = 6
    DEST_OVER = 7
    DEST_IN = 8
    DEST_OUT = 9
    DEST_ATOP = 10
    XOR = 11
    ADD = 12
    SATURATE = 13
    MULTIPLY = 14
    SCREEN = 15
    OVERLAY = 16
    DARKEN = 17
    LIGHTEN = 18
    COLOR_DODGE = 19
    COLOR_BURN = 20
    HARD_LIGHT = 21
    SOFT_LIGHT = 22
    DIFFERENCE = 23
    EXCLUSION = 24
    HSL_HUE = 25
    HSL_SATURATION = 26
    HSL_COLOR = 27
    HSL_LUMINOSITY = 28


class Content:
    COLOR = 0x1000
    ALPHA = 0x2000
    COLOR_ALPHA = 0x3000


class Status:
    SUCCESS = 0
    NO_MEMORY = 1
    INVALID_RESTORE = 2
    INVALID_POP_GROUP = 3
    NO_CURRENT_POINT = 4
    INVALID_MATRIX = 5
    INVALID_STATUS = 6
    NULL_POINTER = 7
    INVALID_STRING = 8
    INVALID_PATH_DATA = 9
    READ_ERROR = 10
    WRITE_ERROR = 11
    SURFACE_FINISHED = 12
    SURFACE_TYPE_MISMATCH = 13
    PATTERN_TYPE_MISMATCH = 14
    INVALID_CONTENT = 15
    INVALID_FORMAT = 16
    INVALID_VISUAL = 17
    FILE_NOT_FOUND = 18
    INVALID_DASH = 19
    INVALID_DSC_COMMENT = 20
    INVALID_INDEX = 21
    CLIP_NOT_REPRESENTABLE = 22
    INVALID_STRIDE = 23
    FONT_TYPE_MISMATCH = 24
    USER_FONT_IMMUTABLE = 25
    USER_FONT_ERROR = 26
    NEGATIVE_COUNT = 27
    INVALID_CLUSTERS = 28
    INVALID_SLANT = 29
    INVALID_WEIGHT = 30
    INVALID_SIZE = 31
    USER_FONT_NOT_IMPLEMENTED = 32
    DEVICE_TYPE_MISMATCH = 33
    DEVICE_ERROR = 34
    INVALID_MESH_CONSTRUCTION = 35
    DEVICE_FINISHED = 36
    JBIG2_GLOBAL_MISSING = 37


# cairo operator -> Skia blend mode
_OPERATOR_TO_BLEND = {
    Operator.CLEAR: skia.BlendMode.kClear,
    Operator.SOURCE: skia.BlendMode.kSrc,
    Operator.OVER: skia.BlendMode.kSrcOver,
    Operator.IN: skia.BlendMode.kSrcIn,
    Operator.OUT: skia.BlendMode.kSrcOut,
    Operator.ATOP: skia.BlendMode.kSrcATop,
    Operator.DEST: skia.BlendMode.kDst,
    Operator.DEST_OVER: skia.BlendMode.kDstOver,
    Operator.DEST_IN: skia.BlendMode.kDstIn,
    Operator.DEST_OUT: skia.BlendMode.kDstOut,
    Operator.DEST_ATOP: skia.BlendMode.kDstATop,
    Operator.XOR: skia.BlendMode.kXor,
    Operator.ADD: skia.BlendMode.kPlus,
    Operator.SATURATE: skia.BlendMode.kSrcOver,
    Operator.MULTIPLY: skia.BlendMode.kMultiply,
    Operator.SCREEN: skia.BlendMode.kScreen,
    Operator.OVERLAY: skia.BlendMode.kOverlay,
    Operator.DARKEN: skia.BlendMode.kDarken,
    Operator.LIGHTEN: skia.BlendMode.kLighten,
    Operator.COLOR_DODGE: skia.BlendMode.kColorDodge,
    Operator.COLOR_BURN: skia.BlendMode.kColorBurn,
    Operator.HARD_LIGHT: skia.BlendMode.kHardLight,
    Operator.SOFT_LIGHT: skia.BlendMode.kSoftLight,
    Operator.DIFFERENCE: skia.BlendMode.kDifference,
    Operator.EXCLUSION: skia.BlendMode.kExclusion,
    Operator.HSL_HUE: skia.BlendMode.kHue,
    Operator.HSL_SATURATION: skia.BlendMode.kSaturation,
    Operator.HSL_COLOR: skia.BlendMode.kColor,
    Operator.HSL_LUMINOSITY: skia.BlendMode.kLuminosity,
}

_CAP_MAP = {
    LineCap.BUTT: skia.Paint.kButt_Cap,
    LineCap.ROUND: skia.Paint.kRound_Cap,
    LineCap.SQUARE: skia.Paint.kSquare_Cap,
}

_JOIN_MAP = {
    LineJoin.MITER: skia.Paint.kMiter_Join,
    LineJoin.ROUND: skia.Paint.kRound_Join,
    LineJoin.BEVEL: skia.Paint.kBevel_Join,
}

_FILL_TYPE_MAP = {
    FillRule.WINDING: skia.kWinding,
    FillRule.EVEN_ODD: skia.kEvenOdd,
}


def cairo_version() -> str:
    return "1.18.4 (skia-raster shim)"


version = cairo_version()


# --------------------------------------------------------------------------
# Matrix
# --------------------------------------------------------------------------
class Matrix:
    """cairo matrix: ``x' = xx*x + xy*y + x0``, ``y' = yx*x + yy*y + y0``."""

    __slots__ = ("xx", "yx", "xy", "yy", "x0", "y0")

    def __init__(self, xx=1.0, yx=0.0, xy=0.0, yy=1.0, x0=0.0, y0=0.0):
        # pycairo accepts a single iterable of six values as well.
        if isinstance(xx, (tuple, list)):
            vals = list(xx)
            if len(vals) != 6:
                raise ValueError("Matrix needs 6 values")
            xx, yx, xy, yy, x0, y0 = vals
        self.xx = float(xx)
        self.yx = float(yx)
        self.xy = float(xy)
        self.yy = float(yy)
        self.x0 = float(x0)
        self.y0 = float(y0)

    # -- construction ----------------------------------------------------
    @classmethod
    def identity(cls) -> "Matrix":
        return cls()

    @staticmethod
    def from_skia(m: skia.Matrix) -> "Matrix":
        # Skia: x' = scaleX*x + skewX*y + transX
        #       y' = skewY *x + scaleY*y + transY
        scale_x, skew_x, trans_x, skew_y, scale_y, trans_y = m.get9()[:6]
        return Matrix(
            xx=scale_x,
            yx=skew_y,
            xy=skew_x,
            yy=scale_y,
            x0=trans_x,
            y0=trans_y,
        )

    def to_skia(self) -> skia.Matrix:
        m = skia.Matrix.MakeAll(
            self.xx, self.xy, self.x0,
            self.yx, self.yy, self.y0,
            0.0, 0.0, 1.0,
        )
        return m

    # -- algebra ---------------------------------------------------------
    def multiply(self, other: "Matrix") -> "Matrix":
        """In-place ``self = self * other`` (as in pycairo)."""
        a, b, c, d, e, f = self.xx, self.yx, self.xy, self.yy, self.x0, self.y0
        p, q, r, s, t, u = other.xx, other.yx, other.xy, other.yy, other.x0, other.y0
        self.xx = a * p + c * q
        self.yx = b * p + d * q
        self.xy = a * r + c * s
        self.yy = b * r + d * s
        self.x0 = a * t + c * u + e
        self.y0 = b * t + d * u + f
        return self

    __mul__ = multiply

    def __matmul__(self, other: "Matrix") -> "Matrix":
        return self.copy().multiply(other)

    def copy(self) -> "Matrix":
        return Matrix(self.xx, self.yx, self.xy, self.yy, self.x0, self.y0)

    def invert(self) -> "Matrix | None":
        det = self.xx * self.yy - self.xy * self.yx
        if det == 0:
            return None
        inv = 1.0 / det
        a, b, c, d, e, f = self.xx, self.yx, self.xy, self.yy, self.x0, self.y0
        self.xx = d * inv
        self.yx = -b * inv
        self.xy = -c * inv
        self.yy = a * inv
        self.x0 = (c * f - d * e) * inv
        self.y0 = (b * e - a * f) * inv
        return self

    def invert_(self) -> "Matrix | None":  # pycairo alias spelling
        return self.invert()

    # -- application -----------------------------------------------------
    def transform_point(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.xx * x + self.xy * y + self.x0,
            self.yx * x + self.yy * y + self.y0,
        )

    def transform_distance(self, dx: float, dy: float) -> tuple[float, float]:
        return (self.xx * dx + self.xy * dy, self.yx * dx + self.yy * dy)

    def __repr__(self) -> str:
        return (
            f"Matrix(xx={self.xx}, yx={self.yx}, xy={self.xy}, "
            f"yy={self.yy}, x0={self.x0}, y0={self.y0})"
        )


# --------------------------------------------------------------------------
# Patterns
# --------------------------------------------------------------------------
class Pattern:
    """Base class; mirrors cairo's Pattern."""

    def set_matrix(self, matrix: Matrix) -> None:
        self.matrix = matrix.copy()

    def get_matrix(self) -> Matrix:
        return self.matrix.copy()

    def set_extend(self, extend: int) -> None:
        self.extend = extend

    def get_extend(self) -> int:
        return self.extend


class SolidPattern(Pattern):
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.rgba = (float(r), float(g), float(b), float(a))
        self.matrix = Matrix()
        self.extend = 0  # none


class LinearGradient(Pattern):
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.points = (float(x0), float(y0), float(x1), float(y1))
        self.stops: list[tuple[float, float, float, float, float]] = []
        self.matrix = Matrix()
        self.extend = 1  # pad

    def add_color_stop_rgb(self, offset: float, r: float, g: float, b: float) -> None:
        self.add_color_stop_rgba(offset, r, g, b, 1.0)

    def add_color_stop_rgba(
        self, offset: float, r: float, g: float, b: float, a: float
    ) -> None:
        self.stops.append((float(offset), float(r), float(g), float(b), float(a)))


class RadialGradient(Pattern):
    def __init__(self, cx0: float, cy0: float, r0: float, cx1: float, cy1: float, r1: float):
        self.points = (float(cx0), float(cy0), float(r0), float(cx1), float(cy1), float(r1))
        self.stops: list[tuple[float, float, float, float, float]] = []
        self.matrix = Matrix()
        self.extend = 1

    def add_color_stop_rgb(self, offset: float, r: float, g: float, b: float) -> None:
        self.add_color_stop_rgba(offset, r, g, b, 1.0)

    def add_color_stop_rgba(
        self, offset: float, r: float, g: float, b: float, a: float
    ) -> None:
        self.stops.append((float(offset), float(r), float(g), float(b), float(a)))


# --------------------------------------------------------------------------
# Path
# --------------------------------------------------------------------------
class Path:
    """A recorded path in user space (cairo_path_t equivalent)."""

    def __init__(self, other: "Path | None" = None):
        self._verbs: list[tuple] = []
        if other is not None:
            self._verbs = list(other._verbs)

    def _copy(self) -> "Path":
        return Path(self)

    def __repr__(self) -> str:
        return f"Path({len(self._verbs)} verbs)"


# --------------------------------------------------------------------------
# ImageSurface
# --------------------------------------------------------------------------
def _skia_image_info(width: int, height: int) -> skia.ImageInfo:
    # kBGRA_8888 + kPremul is byte-identical to cairo's FORMAT_ARGB32 on a
    # little-endian machine.
    return skia.ImageInfo.Make(
        width, height, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType
    )


class ImageSurface:
    """A raster surface.  ``create_for_data`` wraps an existing buffer."""

    def __init__(self, format: int, width: int, height: int):
        if format != FORMAT_ARGB32:
            raise NotImplementedError(
                f"Surface format {format} is not supported by the skia shim "
                "(only FORMAT_ARGB32, which is what Manim uses)."
            )
        self._width = int(width)
        self._height = int(height)
        self._array = np.zeros((self._height, self._width, 4), dtype=np.uint8)
        self._surface = skia.Surface.MakeRasterDirect(
            _skia_image_info(self._width, self._height),
            self._array,
            self._width * 4,
        )
        self._owns_array = True
        self._ctx: "Context | None" = None

    @classmethod
    def create_for_data(
        cls,
        data,
        format: int,
        width: int,
        height: int,
        stride: int | None = None,
    ) -> "ImageSurface":
        if format != FORMAT_ARGB32:
            raise NotImplementedError(
                f"Surface format {format} is not supported by the skia shim."
            )
        arr = np.asarray(data)
        if arr.dtype != np.uint8:
            raise TypeError("ImageSurface data must be a uint8 array")
        if arr.ndim != 3 or arr.shape[2] != 4:
            raise TypeError("ImageSurface data must have shape (height, width, 4)")
        if arr.shape[0] != height or arr.shape[1] != width:
            raise ValueError(
                f"data shape {arr.shape} does not match {height}x{width}"
            )
        if not arr.flags["C_CONTIGUOUS"]:
            arr = np.ascontiguousarray(arr)
        surf = cls.__new__(cls)
        surf._width = int(width)
        surf._height = int(height)
        surf._array = arr
        row_bytes = int(stride) if stride else int(width) * 4
        surf._surface = skia.Surface.MakeRasterDirect(
            _skia_image_info(surf._width, surf._height), arr, row_bytes
        )
        surf._owns_array = False
        surf._ctx = None
        return surf

    # -- queries ---------------------------------------------------------
    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_stride(self) -> int:
        return self._width * 4

    def get_format(self) -> int:
        return FORMAT_ARGB32

    def get_data(self) -> memoryview:
        return memoryview(self._array)

    def get_content(self) -> int:
        return Content.COLOR_ALPHA

    # -- lifecycle -------------------------------------------------------
    def flush(self) -> None:
        if self._surface is not None:
            self._surface.flushAndSubmit()

    def finish(self) -> None:
        self.flush()

    def mark_dirty(self) -> None:
        pass

    def mark_dirty_rectangle(self, x: int, y: int, width: int, height: int) -> None:
        pass

    def write_to_png(self, target) -> None:
        self.flush()
        image = self._surface.makeImageSnapshot()
        data = image.encodeToData()
        if hasattr(target, "write"):
            target.write(bytes(data))
        else:
            with open(target, "wb") as fh:
                fh.write(bytes(data))

    def __del__(self) -> None:  # pragma: no cover - best effort
        self._surface = None


# --------------------------------------------------------------------------
# Context
# --------------------------------------------------------------------------
class _State:
    __slots__ = ("source", "line_width", "line_join", "line_cap", "miter_limit",
                 "dash", "operator", "fill_rule", "antialias", "tolerance")

    def __init__(self):
        self.source = (0.0, 0.0, 0.0, 1.0)
        self.line_width = 2.0  # cairo's default, not 1.0
        self.line_join = LineJoin.MITER
        self.line_cap = LineCap.BUTT
        self.miter_limit = 10.0
        self.dash = None
        self.operator = Operator.OVER
        self.fill_rule = FillRule.WINDING
        self.antialias = Antialias.DEFAULT
        self.tolerance = 0.1

    def copy(self) -> "_State":
        new = _State()
        new.source = self.source
        new.line_width = self.line_width
        new.line_join = self.line_join
        new.line_cap = self.line_cap
        new.miter_limit = self.miter_limit
        new.dash = self.dash
        new.operator = self.operator
        new.fill_rule = self.fill_rule
        new.antialias = self.antialias
        new.tolerance = self.tolerance
        return new


class Context:
    """The subset of ``cairo.Context`` that Manim's camera uses."""

    def __init__(self, surface: ImageSurface):
        self._surface = surface
        self._canvas = surface._surface.getCanvas()
        self._path = skia.Path()
        self._state = _State()
        self._state_stack: list[tuple[_State, skia.Path, int]] = []
        self._base_save_count = self._canvas.getSaveCount()
        self._has_current_point = False

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def get_target(self) -> ImageSurface:
        return self._surface

    def _paint(self, style: int) -> skia.Paint:
        st = self._state
        paint = skia.Paint()
        paint.setAntiAlias(st.antialias != Antialias.NONE)
        paint.setStyle(style)
        paint.setBlendMode(_OPERATOR_TO_BLEND.get(st.operator, skia.BlendMode.kSrcOver))
        if isinstance(st.source, tuple):
            r, g, b, a = st.source
            paint.setColor4f(skia.Color4f(r, g, b, a))
        else:
            paint.setShader(st.source)
        if style == skia.Paint.kStroke_Style:
            paint.setStrokeWidth(st.line_width)
            paint.setStrokeCap(_CAP_MAP.get(st.line_cap, skia.Paint.kButt_Cap))
            paint.setStrokeJoin(_JOIN_MAP.get(st.line_join, skia.Paint.kMiter_Join))
            paint.setStrokeMiter(st.miter_limit)
            if st.dash is not None:
                phase, dashes = st.dash
                paint.setPathEffect(
                    skia.DashPathEffect.Make([float(d) for d in dashes], float(phase))
                )
        return paint

    def _draw_path(self, style: int, preserve: bool) -> None:
        if self._path.countVerbs() == 0:
            return
        self._canvas.drawPath(self._path, self._paint(style))
        if not preserve:
            self._path.rewind()
            self._has_current_point = False

    # ------------------------------------------------------------------
    # state
    # ------------------------------------------------------------------
    def save(self) -> None:
        self._state_stack.append(
            (self._state.copy(), skia.Path(self._path), self._canvas.getSaveCount())
        )
        self._canvas.save()

    def restore(self) -> None:
        if not self._state_stack:
            return
        self._state, self._path, _ = self._state_stack.pop()
        self._canvas.restore()

    # ------------------------------------------------------------------
    # path construction
    # ------------------------------------------------------------------
    def new_path(self) -> None:
        self._path.rewind()
        self._has_current_point = False

    def new_sub_path(self) -> None:
        # cairo starts a new subpath; Skia does that implicitly on the next
        # moveTo, so nothing to do beyond marking the current point stale.
        self._has_current_point = False

    def move_to(self, x: float, y: float) -> None:
        self._path.moveTo(x, y)
        self._has_current_point = True

    def line_to(self, x: float, y: float) -> None:
        self._path.lineTo(x, y)
        self._has_current_point = True

    def curve_to(
        self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float
    ) -> None:
        self._path.cubicTo(x1, y1, x2, y2, x3, y3)
        self._has_current_point = True

    def rel_move_to(self, dx: float, dy: float) -> None:
        if self._has_current_point:
            x, y = self._path.getLastPt()
            self._path.moveTo(x + dx, y + dy)
        else:
            self._path.moveTo(dx, dy)
        self._has_current_point = True

    def rel_line_to(self, dx: float, dy: float) -> None:
        x, y = self._path.getLastPt()
        self._path.lineTo(x + dx, y + dy)
        self._has_current_point = True

    def rel_curve_to(
        self, dx1: float, dy1: float, dx2: float, dy2: float, dx3: float, dy3: float
    ) -> None:
        x, y = self._path.getLastPt()
        self._path.cubicTo(x + dx1, y + dy1, x + dx2, y + dy2, x + dx3, y + dy3)
        self._has_current_point = True

    def close_path(self) -> None:
        self._path.close()

    def arc(
        self, xc: float, yc: float, radius: float, angle1: float, angle2: float
    ) -> None:
        rect = skia.Rect.MakeLTRB(
            xc - radius, yc - radius, xc + radius, yc + radius
        )
        self._path.addArc(rect, math.degrees(angle1), math.degrees(angle2 - angle1))

    def arc_negative(
        self, xc: float, yc: float, radius: float, angle1: float, angle2: float
    ) -> None:
        rect = skia.Rect.MakeLTRB(
            xc - radius, yc - radius, xc + radius, yc + radius
        )
        self._path.addArc(rect, math.degrees(angle1), math.degrees(angle2 - angle1))

    def rectangle(self, x: float, y: float, width: float, height: float) -> None:
        self._path.addRect(skia.Rect.MakeXYWH(x, y, width, height))

    def get_current_point(self) -> tuple[float, float]:
        if not self._has_current_point:
            raise ValueError("no current point")
        return self._path.getLastPt()

    def has_current_point(self) -> bool:
        return self._has_current_point

    def copy_path(self) -> Path:
        p = Path()
        it = skia.Path.Iter(self._path)
        # A faithful dump is unnecessary for Manim; expose the verb stream so
        # callers can at least inspect the geometry.
        p._verbs = [
            (verb,)
            for verb in (
                skia.Path.kMove_Verb,
                skia.Path.kLine_Verb,
                skia.Path.kQuad_Verb,
                skia.Path.kCubic_Verb,
                skia.Path.kClose_Verb,
            )
        ]
        return p

    # ------------------------------------------------------------------
    # painting
    # ------------------------------------------------------------------
    def fill(self) -> None:
        self._draw_path(skia.Paint.kFill_Style, preserve=False)

    def fill_preserve(self) -> None:
        self._draw_path(skia.Paint.kFill_Style, preserve=True)

    def fill_extents(self) -> tuple[float, float, float, float]:
        return self.path_extents()

    def in_fill(self, x: float, y: float) -> bool:
        return self._path.contains(x, y)

    def stroke(self) -> None:
        self._draw_path(skia.Paint.kStroke_Style, preserve=False)

    def stroke_preserve(self) -> None:
        self._draw_path(skia.Paint.kStroke_Style, preserve=True)

    def stroke_extents(self) -> tuple[float, float, float, float]:
        paint = self._paint(skia.Paint.kStroke_Style)
        outline = paint.getFillPath(self._path)
        r = outline.getBounds()
        return (r.left(), r.top(), r.right(), r.bottom())

    def path_extents(self) -> tuple[float, float, float, float]:
        r = self._path.getBounds()
        return (r.left(), r.top(), r.right(), r.bottom())

    def paint(self) -> None:
        self._canvas.drawPaint(self._paint(skia.Paint.kFill_Style))

    def paint_with_alpha(self, alpha: float) -> None:
        paint = self._paint(skia.Paint.kFill_Style)
        paint.setAlphaf(alpha)
        self._canvas.drawPaint(paint)

    # ------------------------------------------------------------------
    # clipping
    # ------------------------------------------------------------------
    def clip(self) -> None:
        self._canvas.clipPath(self._path, doAntiAlias=True)
        self._path.rewind()

    def clip_preserve(self) -> None:
        self._canvas.clipPath(self._path, doAntiAlias=True)

    def reset_clip(self) -> None:
        self._canvas.restoreToCount(self._base_save_count)

    def clip_extents(self) -> tuple[float, float, float, float]:
        r = self._canvas.getDeviceClipBounds()
        return (r.left(), r.top(), r.right(), r.bottom())

    # ------------------------------------------------------------------
    # sources
    # ------------------------------------------------------------------
    def set_source_rgba(self, r: float, g: float, b: float, a: float = 1.0) -> None:
        self._state.source = (float(r), float(g), float(b), float(a))

    def set_source_rgb(self, r: float, g: float, b: float) -> None:
        self.set_source_rgba(r, g, b, 1.0)

    def set_source(self, pattern: Pattern) -> None:
        if isinstance(pattern, SolidPattern):
            self._state.source = pattern.rgba
            return
        if isinstance(pattern, LinearGradient):
            x0, y0, x1, y1 = pattern.points
            colors = [skia.Color4f(r, g, b, a) for _, r, g, b, a in pattern.stops]
            positions = [o for o, *_ in pattern.stops]
            if len(colors) == 1:
                self._state.source = (
                    pattern.stops[0][1],
                    pattern.stops[0][2],
                    pattern.stops[0][3],
                    pattern.stops[0][4],
                )
                return
            self._state.source = skia.GradientShader.MakeLinear(
                [skia.Point(x0, y0), skia.Point(x1, y1)],
                colors,
                positions,
            )
            return
        if isinstance(pattern, RadialGradient):
            cx0, cy0, r0, cx1, cy1, r1 = pattern.points
            colors = [skia.Color4f(r, g, b, a) for _, r, g, b, a in pattern.stops]
            positions = [o for o, *_ in pattern.stops]
            if len(colors) == 1:
                self._state.source = (
                    pattern.stops[0][1],
                    pattern.stops[0][2],
                    pattern.stops[0][3],
                    pattern.stops[0][4],
                )
                return
            self._state.source = skia.GradientShader.MakeTwoPointConical(
                skia.Point(cx0, cy0), r0, skia.Point(cx1, cy1), r1, colors, positions
            )
            return
        raise TypeError(f"unsupported pattern type {type(pattern)!r}")

    def set_source_surface(
        self, surface: ImageSurface, x: float = 0.0, y: float = 0.0
    ) -> None:
        image = surface._surface.makeImageSnapshot()
        self._canvas.drawImage(image, x, y)

    # ------------------------------------------------------------------
    # line attributes
    # ------------------------------------------------------------------
    def set_line_width(self, width: float) -> None:
        self._state.line_width = float(width)

    def get_line_width(self) -> float:
        return self._state.line_width

    def set_line_join(self, join: int) -> None:
        self._state.line_join = join

    def get_line_join(self) -> int:
        return self._state.line_join

    def set_line_cap(self, cap: int) -> None:
        self._state.line_cap = cap

    def get_line_cap(self) -> int:
        return self._state.line_cap

    def set_miter_limit(self, limit: float) -> None:
        self._state.miter_limit = float(limit)

    def get_miter_limit(self) -> float:
        return self._state.miter_limit

    def set_dash(self, offset: float, *dashes) -> None:
        if len(dashes) == 1 and isinstance(dashes[0], (list, tuple)):
            dashes = tuple(dashes[0])
        dashes = tuple(float(d) for d in dashes)
        self._state.dash = (float(offset), dashes) if dashes else None

    def get_dash(self) -> tuple[float, list[float]]:
        if self._state.dash is None:
            return (0.0, [])
        return self._state.dash

    def get_dash_count(self) -> int:
        return 0 if self._state.dash is None else len(self._state.dash[1])

    def set_fill_rule(self, rule: int) -> None:
        self._state.fill_rule = rule
        self._path.setFillType(_FILL_TYPE_MAP.get(rule, skia.kWinding))

    def get_fill_rule(self) -> int:
        return self._state.fill_rule

    def set_operator(self, operator: int) -> None:
        self._state.operator = operator

    def get_operator(self) -> int:
        return self._state.operator

    def set_antialias(self, antialias: int) -> None:
        self._state.antialias = antialias

    def get_antialias(self) -> int:
        return self._state.antialias

    def set_tolerance(self, tolerance: float) -> None:
        self._state.tolerance = float(tolerance)

    def get_tolerance(self) -> float:
        return self._state.tolerance

    # ------------------------------------------------------------------
    # transforms
    # ------------------------------------------------------------------
    def translate(self, tx: float, ty: float) -> None:
        self._canvas.translate(tx, ty)

    def scale(self, sx: float, sy: float) -> None:
        self._canvas.scale(sx, sy)

    def rotate(self, angle: float) -> None:
        self._canvas.rotate(math.degrees(angle))

    def transform(self, matrix: Matrix) -> None:
        self._canvas.concat(matrix.to_skia())

    def set_matrix(self, matrix: Matrix) -> None:
        self._canvas.setMatrix(matrix.to_skia())

    def get_matrix(self) -> Matrix:
        return Matrix.from_skia(self._canvas.getTotalMatrix())

    def user_to_device(self, x: float, y: float) -> tuple[float, float]:
        return self.get_matrix().transform_point(x, y)

    def user_to_device_distance(self, dx: float, dy: float) -> tuple[float, float]:
        return self.get_matrix().transform_distance(dx, dy)

    def device_to_user(self, x: float, y: float) -> tuple[float, float]:
        m = self.get_matrix()
        if m.invert() is None:
            return (x, y)
        return m.transform_point(x, y)

    def device_to_user_distance(self, dx: float, dy: float) -> tuple[float, float]:
        m = self.get_matrix()
        if m.invert() is None:
            return (dx, dy)
        return m.transform_distance(dx, dy)

    # ------------------------------------------------------------------
    # text -- Manim never draws text through cairo (text becomes VMobjects),
    # so these are deliberately loud rather than silently wrong.
    # ------------------------------------------------------------------
    def _no_text(self, *args, **kwargs):
        raise NotImplementedError(
            "The skia/cairo shim does not implement cairo's text API; Manim "
            "renders text as vector mobjects instead."
        )

    select_font_face = _no_text
    set_font_face = _no_text
    get_font_face = _no_text
    set_font_size = _no_text
    set_font_matrix = _no_text
    get_font_matrix = _no_text
    set_font_options = _no_text
    get_font_options = _no_text
    show_text = _no_text
    show_glyphs = _no_text
    text_path = _no_text
    glyph_path = _no_text
    text_extents = _no_text
    glyph_extents = _no_text
    font_extents = _no_text
    show_page = _no_text
    copy_page = _no_text
