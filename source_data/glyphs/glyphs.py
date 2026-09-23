#!/usr/bin/env python3

# Draw the PS4 and PS5 button glyphs.
#
# The retail zones carry no controller glyphs for either of these
# controllers. We do have the PS3 and Xbox 360 glyphs from the console
# game and there is no reason to redraw those, but there is nothing
# corresponding to the DualShock 4 or DualSense that we can extract and
# put here. So for these two we draw the glyphs ourselves.
#
# There are a couple of slightly non-obvious things about how this is
# done. First, we draw at four times the final size and then scale the
# result down. It may be tempting to draw straight into a 128x128 image,
# especially seeing that most of this is just simple geometry. In
# practice the thin outlines and the PlayStation symbols look fairly
# rough that way. Drawing large and filtering down gives us decent
# antialiasing without having to teach every primitive about sub-pixel
# coverage.
#
# Second, we write an uncompressed DDS with the complete mip chain.
# Perhaps we could get away with letting the game generate or otherwise
# deal with the smaller representations, but these glyphs contain thin
# strokes which become rather sensitive to how they are reduced.
# Supplying the chain here gives us one result that we can inspect and
# that the material can simply sample.
#
# The sets are:
#
#   ps4        The DualShock 4: coloured symbols on black buttons,
#              OPTIONS and SHARE, and a d-pad made from four separate
#              buttons.
#
#   ps5        The DualSense: light monochrome symbols on dark buttons,
#              OPTIONS and CREATE, and a one-piece cross d-pad.
#
#   ps5_light  The same DualSense geometry with light buttons and dark
#   symbols.
#
# The DualSense Edge uses the PS5 sets. We could perhaps add artwork for
# its extra controls, but the back paddles and Fn buttons are not keys
# that IW4 can bind, so there is currently nothing useful for such
# glyphs to represent.
#
# Usage:
#
#   glyphs.py <assets root> [preview.png]
#
# Writes:
#
#   zone_raw/iw4x_code_post_gfx_mp/images/<name>.dds
#   zone_raw/iw4x_code_post_gfx_mp/materials/<name>.json
#
# Pillow does the drawing and ImageMagick does the DDS encoding.
#

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

SIZE = 128
SCALE = 4
S = SIZE * SCALE

FONT = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"

OUTLINE_BAND = 22
RIM_WIDTH = 7

# Drawing.
#
class Canvas:
    # A glyph's drawing surface at SCALE times its eventual size. The w
    # and h arguments are in glyph sizes, so, for example, Canvas(2) is
    # twice as wide as the normal square glyph.
    #
    # It may seem simpler to expose the pixel dimensions here. But then
    # every caller would have to know about SCALE, and changing the
    # supersampling factor would mean auditing all those callers. So
    # keep that little bit of knowledge here.
    #
    def __init__(self, w=1, h=1):
        self.w, self.h = round(S * w), round(S * h)
        self.cx, self.cy = self.w / 2, self.h / 2

        # Start transparent since the texture outside the actual button
        # must remain transparent. We could perhaps create the
        # background later, once the shape is known, but almost
        # everything below is naturally expressed as painting masks onto
        # an existing image.
        #
        self.img = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))

    def mask(self, shape, inset=0):
        # Most button parts are really the same shape drawn at a
        # different inset. For example, the outer circle gives us the
        # outline and a smaller copy of that circle gives us the body.
        # So instead of having every shape know about outlines, rims,
        # and fills, ask it to draw a mask at an arbitrary inset.
        #
        # Note that this makes `inset` part of the shape interface. A
        # new shape that looks right at inset 0 but collapses strangely
        # at inset 20 will probably also produce a strange button rim.
        #
        m = Image.new("L", (self.w, self.h), 0)
        shape(ImageDraw.Draw(m), 255, inset)
        return m

    def fill(self, colour, m):
        # Paste is useful here since the L image is used directly as
        # coverage. This also means the edge pixels produced by Pillow
        # survive as alpha coverage instead of us having to combine RGBA
        # values ourselves.
        #
        self.img.paste(colour, (0, 0), m)

    def vertical(self, top, bottom, m):
        # Make the complete gradient first and clip it with the mask
        # afterwards. We could perhaps draw each scanline directly into
        # self.img, but then the loop would need to care about the shape
        # as well. Keeping the two operations separate makes the button
        # construction below much easier to follow.
        #
        g = Image.new("RGBA", (self.w, self.h))
        d = ImageDraw.Draw(g)

        for y in range(self.h):
            # Use h - 1 here so the last row really is `bottom`. With h
            # as the divisor we would stop one interpolation step short.
            # Hardly visible for these colours, perhaps, but there is no
            # reason to make the endpoints approximate.
            #
            t = y / (self.h - 1)
            d.line([(0, y), (self.w, y)], fill=mix(top, bottom, t))

        self.img.paste(g, (0, 0), m)

    def gloss(self, m, strength=110):
        # Put a broad soft highlight over the upper part of a button.
        #
        # Note that none of the current sets actually enable this.
        # Keeping it here is still useful if we want to try a glossier
        # style later, and more importantly it explains why the style
        # has a `gloss` member.
        #
        box = m.getbbox()

        # What if the shape disappeared after insetting? There is then
        # no box from which to derive the highlight. This shouldn't
        # happen for the buttons below, but treating an empty mask as
        # "nothing to gloss" is perhaps the least surprising behaviour.
        #
        if box is None:
            return

        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0

        hl = Image.new("L", (self.w, self.h), 0)

        # Derive the highlight from the mask bounds instead of from any
        # one button shape. That lets the same code work for the face
        # buttons and, say, the trigger shape without either one having
        # to tell us where its "top" is.
        #
        ImageDraw.Draw(hl).ellipse(
            [
                x0 + w * 0.16,
                y0 + h * 0.06,
                x1 - w * 0.16,
                y0 + h * 0.52,
            ],
            fill=strength,
        )

        # This is in our enlarged coordinate system. Note that using S
        # here keeps roughly the same final blur radius if SCALE
        # changes.
        #
        hl = hl.filter(ImageFilter.GaussianBlur(S * 0.03))

        # The Gaussian blur naturally spills outside the ellipse and
        # perhaps outside the button too. Clip it back to the button
        # interior before putting it onto the image.
        #
        hl = ImageChops.multiply(hl, m)
        self.img.paste((255, 255, 255, 255), (0, 0), hl)

    def draw(self):
        return ImageDraw.Draw(self.img)

    def label(self, text, size, fill, dx=0, dy=0, outline=None, stroke=0):
        d = self.draw()
        f = ImageFont.truetype(FONT, size)

        # textbbox() is a little more useful than measuring just the
        # width and height here. The font's visible bounds need not
        # begin at (0, 0), and if we ignored l/t then some labels would
        # look off-centre despite the arithmetic saying otherwise.
        #
        l, t, r, b = d.textbbox(
            (0, 0),
            text,
            font=f,
            stroke_width=stroke,
        )

        d.text(
            (
                (self.w - (r - l)) / 2 - l + dx,
                (self.h - (b - t)) / 2 - t + dy,
            ),
            text,
            font=f,
            fill=fill,
            stroke_width=stroke,
            stroke_fill=outline,
        )

    def result(self):
        # And this is where we finally leave the enlarged coordinate
        # system.
        #
        # It would be tempting to resize intermediate layers
        # individually. Doing it once, after the complete glyph has been
        # assembled, means overlapping strokes and masks all participate
        # in the same filtering operation. That seems to give the least
        # surprising edges.
        #
        return self.img.resize(
            (
                round(self.w / SCALE),
                round(self.h / SCALE),
            ),
            Image.LANCZOS,
        )

def mix(a, b, t):
    # This happens to interpolate alpha too. All current palette colours
    # are opaque, but treating RGBA uniformly means we do not have to
    # remember to revisit this helper if one of them becomes
    # translucent.
    #
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))

def dot(d, x, y, r, fill):
    # Mostly used as a round line cap. Pillow has some support for line
    # joints, but explicitly drawing the cap gives us the same result
    # for all the little symbols below.
    #
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

# Shapes.
#
# A shape here is perhaps slightly unusual: it is not an image and it
# does not even draw immediately. It is a small function with the
# interface
#
#   shape(draw, fill, inset)
#
# which knows how to draw one piece of geometry at a requested inset.
# This lets button() ask the same shape for its outer edge, body, rim,
# and so on.
#
def circle(c, r, dx=0, dy=0):
    def shape(d, fill, inset):
        x, y = c.cx + dx, c.cy + dy

        d.ellipse(
            [
                x - r + inset,
                y - r + inset,
                x + r - inset,
                y + r - inset,
            ],
            fill=fill,
        )

    return shape

def rounded(c, w, h, radius, dx=0, dy=0):
    def shape(d, fill, inset):
        x, y = c.cx + dx, c.cy + dy

        # Note that the radius has to move in with the rectangle.
        # Keeping the original radius for every inset is perhaps the
        # obvious first attempt, but the inner shape would then stop
        # following the outer one around the corners.
        #
        d.rounded_rectangle(
            [
                x - w / 2 + inset,
                y - h / 2 + inset,
                x + w / 2 - inset,
                y + h / 2 - inset,
            ],
            max(radius - inset, 1),
            fill=fill,
        )

    return shape

def polygon(c, points):
    # A convex polygon whose points are relative to the centre of the
    # canvas.
    #
    def shape(d, fill, inset):
        pts = [(c.cx + x, c.cy + y) for x, y in points]

        # Now, how do we inset a polygon? Moving each point towards the
        # centre is tempting and for a regular polygon it may even look
        # convincing. It does not keep a constant distance from each
        # edge, though, which shows up rather quickly once we use the
        # result as a narrow border.
        #
        # So for polygons we move the edges instead and recover the new
        # vertices from their intersections.
        #
        if inset:
            pts = inset_polygon(pts, inset)

        d.polygon(pts, fill=fill)

    return shape

def inset_polygon(pts, inset):
    n = len(pts)
    lines = []

    # Build the inset edge lines first. It may be possible to combine
    # this with the intersection loop below, but keeping the
    # intermediate lines around makes the construction rather easier to
    # reason about: first move every edge inward, then join neighbouring
    # moved edges.
    #
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]

        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)

        # Rotating the edge gives us a normal. Which normal, though?
        # Depending on the order in which the caller listed the vertices
        # this may point into the polygon or away from it. We could
        # perhaps require one winding order from every caller, but that
        # is a fairly easy condition to forget when adding another
        # shape.
        #
        nx, ny = -dy / length, dx / length

        # For the convex polygons used here the average of the vertices
        # gives us a point on the inside. Take the edge midpoint and see
        # if our candidate normal points in the direction of that point.
        # Flip it if not.
        #
        # Note that "convex" matters here. If we ever feed this function
        # a concave polygon then this little test is no longer a
        # sufficient definition of an inset.
        #
        cx = sum(p[0] for p in pts) / n
        cy = sum(p[1] for p in pts) / n
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2

        if (cx - mx) * nx + (cy - my) * ny < 0:
            nx, ny = -nx, -ny

        lines.append(
            (
                (
                    x0 + nx * inset,
                    y0 + ny * inset,
                ),
                (
                    x1 + nx * inset,
                    y1 + ny * inset,
                ),
            )
        )

    out = []

    # Each new vertex is where two neighbouring inset edges meet. Using
    # i - 1 here also gives us the last/first pair for i == 0, which
    # saves a special case for closing the polygon.
    #
    for i in range(n):
        (a, b), (c_, d_) = lines[i - 1], lines[i]
        out.append(intersect(a, b, c_, d_))

    return out

def intersect(p1, p2, p3, p4):
    # Intersection of two infinite lines.
    #
    # Note that treating these as segments would be wrong for the inset
    # construction. The new corner may lie past the endpoint of either
    # little offset segment we happened to construct above.
    #
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # Parallel neighbouring edges should perhaps be treated as an error
    # since the polygons below are meant to be well-formed. Still,
    # returning the existing corner is a more useful failure mode for
    # hand-tuned artwork than producing a huge coordinate after dividing
    # by something very close to zero.
    #
    if abs(den) < 1e-9:
        return p2

    t = (
        (x1 - x3) * (y3 - y4)
        - (y1 - y3) * (x3 - x4)
    ) / den

    return (
        x1 + t * (x2 - x1),
        y1 + t * (y2 - y1),
    )

def trigger_shape(c, w, h, dy=10):
    # A trigger is perhaps the first shape here that is easier to
    # describe than to draw with one Pillow primitive. It has a shallow
    # dome at the top and rounded corners at the bottom, so construct
    # the perimeter ourselves.
    #
    def shape(d, fill, inset):
        x0 = c.cx - w / 2 + inset
        x1 = c.cx + w / 2 - inset
        y0 = c.cy - h / 2 + dy + inset
        y1 = c.cy + h / 2 + dy - inset

        rx = (x1 - x0) / 2
        ry = rx * 0.6

        # Move the bottom corner radius with the inset. This is the same
        # idea as rounded(): the nested shape should keep looking like
        # the same trigger instead of acquiring larger and larger
        # corners.
        #
        corner = max(44 - inset, 1)

        pts = []

        # The top is half an ellipse. Ninety segments is probably more
        # than we strictly need at the final texture size, but remember
        # that this is the 4x drawing surface. It is cheap and keeps the
        # later downsampling from exposing the polygon.
        #
        for i in range(91):
            a = math.pi + math.pi * i / 90
            pts.append(
                (
                    c.cx + rx * math.cos(a),
                    y0 + ry + ry * math.sin(a),
                )
            )

        # Then come around the lower-right corner.
        #
        for i in range(31):
            a = (math.pi / 2) * i / 30
            pts.append(
                (
                    x1 - corner + corner * math.cos(a),
                    y1 - corner + corner * math.sin(a),
                )
            )

        # And back around the lower-left. polygon() will close the
        # remaining side for us.
        #
        for i in range(31):
            a = math.pi / 2 + (math.pi / 2) * i / 30
            pts.append(
                (
                    x0 + corner + corner * math.cos(a),
                    y1 - corner + corner * math.sin(a),
                )
            )

        d.polygon(pts, fill=fill)

    return shape

def cross_shape(c, arm, reach):
    # The DualSense d-pad looks like one cross, so perhaps the natural
    # representation would be a polygon containing all twelve-ish
    # corners. Two rounded rectangles are simpler and their overlap is
    # exactly the centre of the cross that we want filled anyway.
    #
    def shape(d, fill, inset):
        a = arm - inset
        r = reach - inset
        rr = max(46 - inset, 1)

        d.rounded_rectangle(
            [
                c.cx - a,
                c.cy - r,
                c.cx + a,
                c.cy + r,
            ],
            rr,
            fill=fill,
        )

        d.rounded_rectangle(
            [
                c.cx - r,
                c.cy - a,
                c.cx + r,
                c.cy + a,
            ],
            rr,
            fill=fill,
        )

    return shape

def arrow_points(direction, near=60, far=244, half=116, tip=26):
    # Start with one d-pad button pointing up and rotate it for the
    # other three directions. Apart from avoiding four copies of these
    # numbers, this means an adjustment to the shape cannot accidentally
    # make, say, the left button subtly different from the right one.
    #
    base = [
        (-half, -far),
        (half, -far),
        (half, -near - tip),
        (0, -near),
        (-half, -near - tip),
    ]

    a = math.radians(
        {
            "up": 0,
            "right": 90,
            "down": 180,
            "left": 270,
        }[direction]
    )

    return [
        (
            x * math.cos(a) - y * math.sin(a),
            x * math.sin(a) + y * math.cos(a),
        )
        for x, y in base
    ]


# Buttons: one shape used to derive the outline, body, and rim.
#
def button(c, shape, top, bottom, outline, rim, gloss=0, band=OUTLINE_BAND):
    # Paint from the outside in. First the complete shape becomes the
    # outline. We then put the body over a smaller version of it. So
    # whatever survives between inset 0 and `band` is our outline.
    #
    # This may look a bit backwards compared with drawing a body and
    # then stroking its edge, but Pillow's stroke behaviour varies
    # between the primitives we use. Nested masks give all the shapes
    # the same border construction.
    #
    c.fill(outline, c.mask(shape, 0))

    body = c.mask(shape, band)
    c.vertical(top, bottom, body)

    if rim is not None:
        # The rim is another ring cut from two copies of the same shape.
        #
        # Perhaps the obvious way to write this is to ask Pillow to
        # outline the inner shape. The mask subtraction keeps its
        # thickness tied to our geometric inset instead, which is what
        # we want for the odd trigger and d-pad shapes too.
        #
        r = c.mask(shape, band)
        r.paste(
            0,
            (0, 0),
            c.mask(shape, band + RIM_WIDTH),
        )

        c.fill(rim, r)

    if gloss:
        # Note that the gloss begins inside the rim. Passing the larger
        # body mask here would let the blur wash over the rim that we
        # just drew.
        #
        c.gloss(
            c.mask(shape, band + RIM_WIDTH),
            gloss,
        )


def symbol(c, kind, colour, w=34, scale=1.0, dy=0):
    d = c.draw()
    x, y = c.cx, c.cy + dy

    if kind == "cross":
        a = 88 * scale

        d.line(
            [x - a, y - a, x + a, y + a],
            fill=colour,
            width=w,
        )

        d.line(
            [x - a, y + a, x + a, y - a],
            fill=colour,
            width=w,
        )

        # Pillow leaves us with line caps that are a little too obvious
        # here. Put a circle with radius w/2 at every exposed end. One
        # could perhaps use a more elaborate path primitive, but for two
        # crossing strokes this is both clearer and gives us the shape
        # we want.
        #
        for px, py in (
            (x - a, y - a),
            (x + a, y + a),
            (x - a, y + a),
            (x + a, y - a),
        ):
            dot(d, px, py, w / 2, colour)

    elif kind == "circle":
        r = 96 * scale

        d.ellipse(
            [x - r, y - r, x + r, y + r],
            outline=colour,
            width=w,
        )

    elif kind == "square":
        a = 84 * scale

        # A completely square corner looks surprisingly harsh once this
        # is reduced to the size used in the HUD. A small radius here is
        # perhaps technically less geometric, but visually it is much
        # closer to the controller symbol.
        #
        d.rounded_rectangle(
            [x - a, y - a, x + a, y + a],
            10,
            outline=colour,
            width=w,
        )

    elif kind == "triangle":
        r = 112 * scale

        # The +14 is an optical correction. A triangle centred by its
        # bounding circle looks a little high next to the other three
        # symbols. We could derive its centroid and centre that exactly,
        # but what matters here is where the outlined shape appears to
        # sit after reduction.
        #
        pts = [
            (
                x + r * math.cos(math.radians(-90 + 120 * i)),
                y
                + 14 * scale
                + r * math.sin(math.radians(-90 + 120 * i)),
            )
            for i in range(3)
        ]

        # Repeat the first couple of points so Pillow gets a curved
        # joint at the closing corner too. Without that, that corner can
        # end up looking a little different from the other two.
        #
        d.line(
            pts + [pts[0], pts[1]],
            fill=colour,
            width=w,
            joint="curve",
        )

# The PlayStation sets.
#
# Keep geometry out of these descriptions. The useful thing about the
# style dictionaries is that a PS5 light button follows exactly the same
# drawing path as a normal PS5 button. If the geometry needs fixing,
# there should probably be one place to fix it.
#
PS_OUTLINE = (12, 12, 14, 255)
PS_RIM = (98, 101, 110, 255)
PS_UNLIT = (70, 72, 79, 255)
LIGHT = (236, 238, 242, 255)

PS_COLOURS = {
    "cross": (124, 160, 232, 255),
    "circle": (240, 96, 104, 255),
    "square": (226, 146, 206, 255),
    "triangle": (72, 206, 170, 255),
}

PS4 = {
    "top": (46, 47, 52, 255),
    "bottom": (18, 18, 21, 255),
    "outline": PS_OUTLINE,
    "rim": PS_RIM,
    "gloss": 0,
    "symbols": PS_COLOURS,
    "text": LIGHT,
    "unlit": PS_UNLIT,
    "lit": LIGHT,
}

PS5 = {
    "top": (60, 62, 68, 255),
    "bottom": (30, 31, 35, 255),
    "outline": PS_OUTLINE,
    "rim": PS_RIM,
    "gloss": 0,
    "symbols": {k: LIGHT for k in PS_COLOURS},
    "text": LIGHT,
    "unlit": PS_UNLIT,
    "lit": LIGHT,
}

PS5_LIGHT = {
    "top": (250, 250, 252, 255),
    "bottom": (214, 216, 222, 255),
    "outline": (40, 41, 46, 255),
    "rim": (255, 255, 255, 255),
    "gloss": 0,
    "symbols": {k: (34, 35, 40, 255) for k in PS_COLOURS},
    "text": (34, 35, 40, 255),
    "unlit": (186, 189, 196, 255),
    "lit": (34, 35, 40, 255),
}

def ps_button(c, style, shape):
    # This is mostly a convenience wrapper, but it gives us one place
    # where a PlayStation style becomes the generic button parameters.
    # Perhaps useful if another generation later wants one extra common
    # treatment.
    #
    button(
        c,
        shape,
        style["top"],
        style["bottom"],
        style["outline"],
        style["rim"],
        gloss=style["gloss"],
    )

def ps_face(style, kind):
    c = Canvas()

    # Nothing controller-specific about the geometry of the four face
    # buttons; use one circle and let `kind` select the artwork in its
    # centre.
    #
    ps_button(c, style, circle(c, 248))
    symbol(c, kind, style["symbols"][kind])

    return c.result()

def ps_shoulder(style, text):
    c = Canvas()

    # L1/R1 are perhaps better thought of as a wide pill than as a tiny
    # representation of the physical bumper. At HUD size the readable
    # label matters more than reproducing the controller's perspective.
    #
    ps_button(c, style, rounded(c, 480, 280, 110))
    c.label(text, 190, style["text"])

    return c.result()

def ps_trigger(style, text):
    c = Canvas()

    ps_button(c, style, trigger_shape(c, 400, 440))

    # The trigger body is deliberately lower than the canvas centre.
    # Move its label with it. Putting this adjustment into label() would
    # make the normal centred labels wrong.
    #
    c.label(text, 180, style["text"], dy=40)

    return c.result()

def ps_click_stick(style, text):
    c = Canvas()

    ps_button(c, style, circle(c, 248))

    # Add the inner ring after the generic button has been drawn. We
    # could perhaps express the ring as another pair of masks, but here
    # it really is just a line and treating it as such makes its
    # intended width obvious.
    #
    d = c.draw()
    r = 172

    d.ellipse(
        [
            c.cx - r,
            c.cy - r,
            c.cx + r,
            c.cy + r,
        ],
        outline=style["rim"],
        width=10,
    )

    c.label(text, 150, style["text"])

    return c.result()

def ps_pill(style):
    # OPTIONS, SHARE, and CREATE all start from this same narrow button.
    # Return the Canvas instead of the final image since the caller
    # still has to draw the actual mark on it.
    #
    c = Canvas()
    ps_button(c, style, rounded(c, 300, 460, 120))
    return c

def ps_options(style):
    c = ps_pill(style)
    d = c.draw()

    # Three horizontal strokes with round ends. It is tempting to use a
    # text glyph here, perhaps U+2630 or something similar, but then the
    # result depends on the font and tends to look like a menu icon
    # instead of the controller's OPTIONS mark.
    #
    for dy in (-70, 0, 70):
        d.line(
            [
                c.cx - 70,
                c.cy + dy,
                c.cx + 70,
                c.cy + dy,
            ],
            fill=style["text"],
            width=28,
        )

        for x in (c.cx - 70, c.cx + 70):
            dot(d, x, c.cy + dy, 14, style["text"])

    return c.result()

def ps_create(style):
    # The CREATE symbol is three short strokes fanning upwards. There
    # may be a nicer way to describe this as one path, but the three
    # rays are easier to tune independently this way and the final
    # symbol is small enough that there is little value in making the
    # geometry clever.
    #
    c = ps_pill(style)
    d = c.draw()

    ox, oy = c.cx, c.cy + 110

    for angle, near, far in (
        (-125, 80, 190),
        (-90, 70, 220),
        (-55, 80, 190),
    ):
        a = math.radians(angle)

        x0 = ox + near * math.cos(a)
        y0 = oy + near * math.sin(a)
        x1 = ox + far * math.cos(a)
        y1 = oy + far * math.sin(a)

        d.line(
            [x0, y0, x1, y1],
            fill=style["text"],
            width=30,
        )

        # As with the cross symbol above, put our own caps on these
        # strokes.
        #
        dot(d, x0, y0, 15, style["text"])
        dot(d, x1, y1, 15, style["text"])

    return c.result()

def ps_share(style):
    # An arrow rising out of an open box.
    #
    # This is another one where perhaps using an existing icon would
    # save some code. Then we would have to match somebody else's stroke
    # weight and proportions to the rest of this set, so a few lines of
    # geometry seem preferable.
    #
    c = ps_pill(style)
    d = c.draw()

    x, y, w = c.cx, c.cy, 26
    colour = style["text"]

    # Shaft and head.
    #
    d.line(
        [x, y + 40, x, y - 120],
        fill=colour,
        width=w,
    )

    d.line(
        [
            x - 60,
            y - 60,
            x,
            y - 120,
            x + 60,
            y - 60,
        ],
        fill=colour,
        width=w,
        joint="curve",
    )

    # And the open box. Note that the two little horizontal pieces stop
    # before the arrow shaft; closing the top here would turn this into
    # a rather different-looking symbol after scaling down.
    #
    d.line(
        [
            x - 40,
            y - 10,
            x - 80,
            y - 10,
            x - 80,
            y + 130,
            x + 80,
            y + 130,
            x + 80,
            y - 10,
            x + 40,
            y - 10,
        ],
        fill=colour,
        width=w,
        joint="curve",
    )

    return c.result()

def ps_dpad_arrows(style, lit):
    c = Canvas()

    # The DS4 d-pad really is four separate buttons, so draw four
    # independent button shapes. `arrow_points()` starts from the same
    # geometry each time and rotates it for us.
    #
    for direction in ("up", "down", "left", "right"):
        shape = polygon(c, arrow_points(direction))
        ps_button(c, style, shape)

        if direction == lit:
            # What exactly should become bright here? Filling the
            # complete button would lose the outline and make the active
            # direction look like a different shape. So go past the
            # outline and rim, plus a small extra margin, and light the
            # face of the button.
            #
            c.fill(
                style["lit"],
                c.mask(
                    shape,
                    OUTLINE_BAND + RIM_WIDTH + 18,
                ),
            )

    return c.result()

def ps_dpad_cross(style, lit):
    c = Canvas()

    # The DualSense d-pad is the opposite case: one physical cross with
    # four directional faces on it.
    #
    ps_button(c, style, cross_shape(c, 150, 244))

    d = c.draw()

    # Leave a small gap around the centre. Perhaps filling all the way
    # through would be a more literal model of a cross, but at glyph
    # size the separation helps the selected direction read as one arm
    # instead of as a highlight bleeding into its neighbours.
    #
    a, r, g = 110, 200, 60
    x, y = c.cx, c.cy

    arms = {
        "up": [x - a, y - r, x + a, y - g],
        "down": [x - a, y + g, x + a, y + r],
        "left": [x - r, y - a, x - g, y + a],
        "right": [x + g, y - a, x + r, y + a],
    }

    for name, box in arms.items():
        d.rounded_rectangle(
            box,
            30,
            fill=style["lit"] if name == lit else style["unlit"],
        )

    return c.result()

# The glyphs, by name. Store drawing functions here instead of rendered
# images so importing this module does not immediately render the
# complete set.
#
DIRECTIONS = ("up", "down", "left", "right")

def ps_family(prefix, style, back, back_draw, start_draw, dpad_draw):
    g = {}

    # There is a Python closure trap hiding in these loops. It is
    # tempting to write:
    #
    #   lambda: ps_face(style, kind)
    #
    # But `kind` would be looked up when that lambda is eventually
    # called, at which point the loop has finished and all four lambdas
    # would see "triangle". Bind the current value through the outer
    # lambda instead.
    #
    # Perhaps functools.partial would make this less surprising. The
    # little closure here keeps the table entries consistently as
    # zero-argument functions and avoids introducing another form just
    # for this case.
    #
    for kind in ("cross", "circle", "square", "triangle"):
        g[f"button_{prefix}_{kind}"] = (
            lambda k: lambda: ps_face(style, k)
        )(kind)

    for text in ("L1", "R1"):
        g[f"button_{prefix}_{text.lower()}"] = (
            lambda t: lambda: ps_shoulder(style, t)
        )(text)

    for text in ("L2", "R2"):
        g[f"button_{prefix}_{text.lower()}"] = (
            lambda t: lambda: ps_trigger(style, t)
        )(text)

    for text in ("L3", "R3"):
        g[f"button_{prefix}_{text.lower()}"] = (
            lambda t: lambda: ps_click_stick(style, t)
        )(text)

    # `start_draw` contains the name too since the button traditionally
    # called Start changed its printed name to OPTIONS. The "back" side
    # similarly differs between SHARE and CREATE, though in that case
    # the caller already supplies the name separately.
    #
    # Maybe these could both be represented by (name, draw) pairs for
    # symmetry. There are just two entries and the current form keeps
    # the call sites fairly readable, so leave the distinction visible
    # for now.
    #
    g[f"button_{prefix}_{start_draw[0]}"] = start_draw[1]
    g[f"button_{prefix}_{back}"] = back_draw

    for d in DIRECTIONS:
        # Same late-binding issue as the face-button loop above.
        #
        g[f"dpad_{prefix}_{d}"] = (
            lambda dd: lambda: dpad_draw(style, dd)
        )(d)

    return g

GLYPHS = {
    **ps_family(
        "ps4",
        PS4,
        "share",
        lambda: ps_share(PS4),
        ("options", lambda: ps_options(PS4)),
        ps_dpad_arrows,
    ),

    **ps_family(
        "ps5",
        PS5,
        "create",
        lambda: ps_create(PS5),
        ("options", lambda: ps_options(PS5)),
        ps_dpad_cross,
    ),

    **ps_family(
        "ps5_light",
        PS5_LIGHT,
        "create",
        lambda: ps_create(PS5_LIGHT),
        ("options", lambda: ps_options(PS5_LIGHT)),
        ps_dpad_cross,
    ),
}

def material(image):
    # This is the material state used by the console game's PS3 glyph
    # set, with mip-mapping enabled for our generated image.
    #
    # There is perhaps some temptation to trim this down to the fields
    # we think matter to the PC renderer. Keeping the known console
    # material state here gives us a much better reference point,
    # especially for the less obvious stateBitsEntry layout.
    #
    return {
        "$schema": "http://openassettools.dev/schema/material.v1.json",
        "_game": "iw4",
        "_type": "material",
        "_version": 1,
        "cameraRegion": "none",
        "constants": [],
        "gameFlags": [],
        "sortKey": 47,
        "stateBits": [
            {
                "alphaTest": "gt0",
                "blendOpAlpha": "disabled",
                "blendOpRgb": "add",
                "colorWriteAlpha": True,
                "colorWriteRgb": True,
                "cullFace": "back",
                "depthTest": "disabled",
                "depthWrite": False,
                "dstBlendAlpha": "zero",
                "dstBlendRgb": "invsrcalpha",
                "gammaWrite": False,
                "polygonOffset": "offset0",
                "polymodeLine": False,
                "srcBlendAlpha": "one",
                "srcBlendRgb": "srcalpha",
            }
        ],

        # Note that this has 48 entries. The one real state block above
        # is used in slot four and every other slot is absent.
        # Expressing the runs this way makes that fact rather more
        # apparent than a long row of -1's.
        #
        "stateBitsEntry": [-1] * 4 + [0] + [-1] * 43,

        "stateFlags": 3,
        "surfaceTypeBits": 0,
        "techniqueSet": "2d",
        "textureAtlas": {
            "columns": 1,
            "rows": 1,
        },
        "textures": [
            {
                "image": image,
                "name": "colorMap",
                "samplerState": {
                    "clampU": True,
                    "clampV": True,
                    "clampW": True,
                    "filter": "linear",
                    "mipMap": "linear",
                },
                "semantic": "2D",
            }
        ],
    }

def main():
    root = Path(sys.argv[1])

    # The argument is the assets tree, not iw4x_code_post_gfx_mp itself.
    # Keep the knowledge of where this generated set lives here so the
    # rest of the code can work with the two actual output directories.
    #
    zone = root / "zone_raw" / "iw4x_code_post_gfx_mp"
    images = zone / "images"
    materials = zone / "materials"

    # Save the rendered Pillow images too. We do not need them after
    # producing the DDS files in the normal case, but what if a preview
    # was requested? Re-rendering every glyph at the end would work,
    # though it would mean the preview is no longer literally made from
    # the images from this generation pass. Keeping these small images
    # around is cheap.
    #
    rendered = {}

    # ImageMagick wants a file for the conversion. The PNG is just that
    # interchange file, so put it in a temporary directory instead of
    # leaving a second representation beside every DDS in the assets
    # tree.
    #
    with tempfile.TemporaryDirectory() as tmp:
        for image, draw in GLYPHS.items():
            glyph = draw()
            rendered[image] = glyph

            png = Path(tmp) / f"{image}.png"
            glyph.save(png)

            # How many mip levels do we ask ImageMagick to write?
            # Starting with the longest dimension, each level halves it
            # until we get to one texel. floor(log2(n)) + 1 is exactly
            # that count including the original level.
            #
            # Note that max() is intentional here. The current glyphs
            # happen to be square, but Canvas can represent a wide glyph
            # and nothing in this conversion needs to assume otherwise.
            #
            mips = int(math.log2(max(glyph.size))) + 1

            # Use the already filtered PNG as the top level and let
            # ImageMagick write the DDS mip chain.
            #
            # We deliberately ask for no DDS compression. These images
            # are tiny, so the saving would be small, and compression
            # artefacts are quite easy to see around the thin
            # high-contrast outlines. Maybe this is worth revisiting if
            # this grows into a much larger texture set; for a few
            # controller glyphs the uncompressed result is the useful
            # trade.
            #
            subprocess.run(
                [
                    "magick",
                    str(png),
                    "-define",
                    "dds:compression=none",
                    "-define",
                    f"dds:mipmaps={mips}",
                    str(images / f"{image}.dds"),
                ],
                check=True,
            )

            # The image and material deliberately share the same name.
            # Apart from being convenient in the zone, this means GLYPHS
            # is the one list of assets we maintain; there is no second
            # material table that can quietly get out of sync.
            #
            (materials / f"{image}.json").write_text(
                json.dumps(material(image), indent=4) + "\n"
            )

    if len(sys.argv) > 2:
        # Build a quick contact sheet when requested. This is meant for
        # a human checking the set, so arrange it by controller family
        # instead of by filename.
        #
        rows = []

        for p in ("ps4", "ps5", "ps5_light"):
            # There is a mildly annoying naming detail here: "_ps5_" is
            # also a substring of "_ps5_light_". A simple membership
            # test would put the light set in the ps5 row too.
            #
            # We could perhaps parse the names more formally. These
            # names are generated just above and have a fixed form, so
            # excluding the one overlapping prefix is enough and keeps
            # this preview code small.
            #
            rows.append(
                [
                    k
                    for k in rendered
                    if (
                        (f"_{p}_" in k)
                        and not (
                            p == "ps5"
                            and "_ps5_light_" in k
                        )
                    )
                ]
            )

        # Leave four pixels around each glyph. SIZE + 8 then gives us
        # the row stride for the normal square glyphs.
        #
        cell = SIZE + 8

        # Do not assume all glyphs are SIZE pixels wide here. Canvas
        # already supports wide images and the preview should probably
        # keep working if one turns up later.
        #
        width = max(
            sum(rendered[k].size[0] + 8 for k in r)
            for r in rows
        )

        # A middling background is useful for this preview since the set
        # contains both very dark and very light buttons. The somewhat
        # odd brown colour is intentional: transparent fringes and
        # colour bleeding tend to be easier to notice against it than
        # against black or white.
        #
        sheet = Image.new(
            "RGBA",
            (width, cell * len(rows)),
            (150, 120, 70, 255),
        )

        for j, r in enumerate(rows):
            x = 4

            for k in r:
                sheet.alpha_composite(
                    rendered[k],
                    (x, j * cell + 4),
                )

                # Again use the rendered width here instead of SIZE.
                # Perhaps everything stays square forever, but there is
                # no useful reason for the contact-sheet code to depend
                # on that.
                #
                x += rendered[k].size[0] + 8

        sheet.save(sys.argv[2])

if __name__ == "__main__":
    main()
