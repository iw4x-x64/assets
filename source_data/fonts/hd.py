#!/usr/bin/env python3

# Redraw the game's text fonts at three times their resolution.
#
# The retail game draws its UI and HUD text from eight bitmap fonts sharing a
# 512x1104 DXT5 atlas, sized for the displays of its day: at 4K a menu
# label's glyphs are stretched four times over and come out soft. This
# renders the same eight fonts again from the typefaces they were made from,
# Conduit ITC and Bank Gothic, at three times the resolution.
#
# Each font keeps its retail line height (the engine scales text by
# 48 / pixelHeight, so a font's pixel height only sets its resolution) and
# its retail baseline. The typeface is drawn at the size and width that fit
# the retail glyphs' ink, in the weight whose ink matches theirs, and spaced
# by its own advances with an even letter-spacing that keeps lines their
# retail length; see rebuild(). The glyph set and its order are the retail
# ones; a glyph the typeface lacks keeps the retail bitmap and metrics,
# enlarged.
#
# The console and developer fonts are left as they are.
#
# The typefaces are licensed and not part of this tree: point the script at
# a directory holding them. What it writes is a bitmap atlas, as the retail
# one is.
#
# Usage: hd.py <assets root> <retail dump dir> <typeface dir>
#
# The retail dump dir holds the Unlinker's dump of localized_code_post_gfx_mp:
# fonts/<name>.json and images/gamefonts_pc.dds (--image-format DDS). The
# typeface dir holds the files named in FONTS, in any subdirectory. Writes,
# under zone_raw/iw4x_code_post_gfx_mp:
#
#   fonts/iw4x/<name>.json                        the fonts
#   materials/fonts/iw4x_gamefonts{,_glow}.json  their materials
#   images/iw4x_gamefonts.dds                     the atlas
#
# Needs Pillow and ImageMagick.
#

import json
import subprocess
import sys
import tempfile

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# The typeface each retail font was drawn from, as its ink says.
#
FONTS = {
    "smallFont":     "Conduit ITC.otf",
    "normalFont":    "Conduit ITC Medium.otf",
    "boldFont":      "Conduit ITC ExtraBold.otf",
    "objectiveFont": "Conduit ITC Bold.otf",
    "bigFont":       "Conduit ITC Medium.otf",
    "extraBigFont":  "Conduit ITC Medium.otf",
    "hudSmallFont":  "BankGothic Md BT.ttf",
    "hudBigFont":    "BankGothic Md BT.ttf",
}

SCALE = 3 # The new resolution over the retail one.

# Fonts whose digits keep their retail advances; see rebuild().
#
RETAIL_DIGITS = ("hudSmallFont", "hudBigFont")

# The atlas is this wide and as tall as the next power of two. Between
# glyphs, so the first mips do not bleed together.
#
ATLAS_WIDTH = 4096
PAD = 8

IMAGE = "iw4x_gamefonts"
MATERIAL = "fonts/iw4x_gamefonts"
GLOW_MATERIAL = "fonts/iw4x_gamefonts_glow"

def letter(g):
    # Depending on how the font was dumped, letter can be the code point
    # or the character itself. Normalize it here so the rest of this
    # code doesn't have to care which form we got.
    #
    return g["letter"] if isinstance(g["letter"], int) else ord(g["letter"])

def ink_box(font, ch):
    # What we want here is the box around the actual ink. This is
    # slightly awkward with Pillow since getbbox() gives us useful
    # baseline-relative vertical coordinates, but horizontally its box
    # runs from the pen and includes the side bearing.
    #
    # So use getbbox() for the position relative to the baseline and the
    # mask for the actual occupied columns. Note that the mask box
    # starts at zero, hence adding l below.
    #
    l, t, r, b = font.getbbox(ch, anchor="ls")

    ink = font.getmask(ch).getbbox()

    # There are characters that have an advance but don't draw anything.
    # In that case there isn't an ink box to fit and the caller will
    # handle it as an empty glyph.
    #
    if ink is None:
        return None

    return l + ink[0], t, l + ink[2], b

def retail_ink(retail_atlas, g):
    # We could just compare pixelWidth/pixelHeight with the new glyph
    # here. The problem with doing that is that the retail rectangle
    # includes the antialiasing fringe around the glyph. At these font
    # sizes one pixel of fringe is quite a lot and ends up noticeably
    # skewing the fit.
    #
    # Instead let's recover the part that looks like actual ink from the
    # alpha channel. We first enlarge it so that the half-coverage edge
    # can land at something finer than a retail pixel, then threshold at
    # 50% and measure the resulting box.
    #
    W, H = retail_atlas.size

    x = int(g["s0"] * W)
    y = int(g["t0"] * H)

    bm = retail_atlas.crop(
        (x, y, x + g["pixelWidth"], y + g["pixelHeight"])
    )

    # Eight is somewhat arbitrary here. We only need enough resolution
    # that quantizing the threshold back to the retail size doesn't
    # dominate the measurement.
    #
    up = 8

    big = bm.resize(
        (bm.width * up, bm.height * up),
        Image.BICUBIC
    )

    box = big.point(
        lambda v: 255 if v >= 128 else 0
    ).getbbox()

    # An empty bitmap tells us nothing about the size of the face, so
    # leave it out of the fit.
    #
    if box is None:
        return None

    return (
        (box[2] - box[0]) / up,
        (box[3] - box[1]) / up
    )

def fitted_size(face, glyphs, retail_atlas):
    # There are really two things we need to recover from the retail
    # font: the size at which the face was drawn and how much it was
    # condensed horizontally. Trying combinations until one looks close
    # works, but there is no need to do that here since both
    # measurements scale linearly enough for what we are doing.
    #
    # Draw the source face at 1000 pixels, measure its ink, and fit that
    # to the retail ink with a least-squares scale through zero. For a
    # source measurement x and retail measurement y this gives:
    #
    #                sum(x * y)
    #          s =  ------------
    #                sum(x * x)
    #
    # We do that independently for height and width. The height fit
    # gives us the font size. The width fit divided by that size gives
    # us the horizontal scale to apply after rasterization.
    #
    f = ImageFont.truetype(str(face), 1000)

    nw = dw = nh = dh = 0.0

    for g in glyphs:
        cp = letter(g)

        # Stick to printable ASCII here. It gives us plenty of samples
        # common to all these fonts and avoids fitting against one of
        # the odd retail glyphs that the source face may represent
        # differently.
        #
        # Note that a glyph with no retail bitmap is of no use here
        # either.
        #
        if not g["pixelWidth"] or not 32 < cp < 127 or not has_glyph(f, cp):
            continue

        box = ink_box(f, chr(cp))
        ink = retail_ink(retail_atlas, g)

        if box is None or ink is None:
            continue

        l, t, r, b = box

        # Since f was loaded at size 1000, dividing these measurements
        # by 1000 gives us the amount of ink per pixel of font size.
        # That means the result of the fit below is directly the font
        # size we are after.
        #
        w = (r - l) / 1000
        h = (b - t) / 1000

        nw += w * ink[0]
        dw += w * w

        nh += h * ink[1]
        dh += h * h

    by_height = nh / dh

    # nw/dw is what the font size would have been if we fitted width
    # alone. We already picked the size from height, so what remains
    # after dividing by it is the horizontal scale.
    #
    return by_height, (nw / dw) / by_height

def has_glyph(font, cp):
    # Pillow doesn't seem to have a useful query for this at the level
    # we are using it. Asking FreeType to draw a missing character gives
    # us .notdef, though, so use an unassigned code point to get that
    # bitmap and compare.
    #
    # Check the pixels too. Just comparing the mask size would mistake a
    # real glyph for .notdef if the two happened to have the same
    # dimensions.
    #
    notdef = font.getmask(chr(0x10FFFD))
    mask = font.getmask(chr(cp))

    return not (
        mask.size == notdef.size and
        bytes(mask) == bytes(notdef)
    )

def rebuild(name, dump, retail_atlas, faces):
    j = json.loads(
        (dump / "fonts" / f"{name}.json").read_text()
    )

    W, H = retail_atlas.size

    face = faces[FONTS[name]]

    # Fit at the retail resolution first. The result tells us what
    # source font best explains the retail rasterization. Only after we
    # have that do we multiply the size by SCALE and draw the new
    # version.
    #
    # Doing the fit on the already enlarged target would make SCALE part
    # of the fitting problem for no useful reason.
    #
    size, condense = fitted_size(
        face,
        j["glyphs"],
        retail_atlas
    )

    size *= SCALE

    font = ImageFont.truetype(
        str(face),
        round(size)
    )

    # Now for the slightly non-obvious y coordinates.
    #
    # Pillow places a glyph relative to the baseline. IW4 doesn't store
    # that baseline directly; y0 is relative to its line coordinate
    # system. The bottom of the retail H gives us the baseline in that
    # system since H doesn't descend below it.
    #
    # So remember that position and add it to Pillow's baseline-relative
    # y coordinate when we build each new glyph below.
    #
    H_retail = next(
        g
        for g in j["glyphs"]
        if letter(g) == ord("H")
    )

    baseline = (
        H_retail["y0"] +
        H_retail["pixelHeight"]
    ) * SCALE

    # We use the original glyphs again later for spacing. Index them now
    # since looking them up repeatedly in the list below would obscure
    # what the spacing code is actually doing.
    #
    retail = {
        letter(g): g
        for g in j["glyphs"]
    }

    glyphs = []
    missing = []

    for g in j["glyphs"]:
        cp = letter(g)

        pw = g["pixelWidth"]
        ph = g["pixelHeight"]

        # Start with the retail metrics enlarged exactly by SCALE. This
        # is our fallback representation and means a glyph we cannot
        # redraw already has the right metrics before we get to that
        # case.
        #
        # bitmap is temporary state used by the packer. It doesn't
        # become part of the font JSON.
        #
        new = {
            "letter": cp,
            "dx": g["dx"] * SCALE,
            "x0": g["x0"] * SCALE,
            "y0": g["y0"] * SCALE,
            "pixelWidth": pw * SCALE,
            "pixelHeight": ph * SCALE,
            "bitmap": None,
        }

        glyphs.append(new)

        # Nothing to rasterize or pack in this case. Keep the metrics we
        # just copied and move on.
        #
        if not pw or not ph:
            continue

        if has_glyph(font, cp):
            box = ink_box(font, chr(cp))

            # A character can exist in the face and still draw no
            # pixels. Space is the obvious example, though the retail
            # font has a few entries where treating this case explicitly
            # is useful. Keep the face's advance and represent it as an
            # empty glyph.
            #
            l, t, r, b = (
                box
                if box is not None
                else (0, 0, 0, 0)
            )

            w = r - l
            h = b - t

            if w <= 0 or h <= 0:
                new.update(
                    dx=round(
                        font.getlength(chr(cp)) *
                        condense
                    ),
                    x0=0,
                    y0=0,
                    pixelWidth=0,
                    pixelHeight=0
                )

                continue

            # ink_box() is relative to the pen. Draw at the negated
            # origin so the ink begins at (0, 0) in this little bitmap.
            # This gives us a tight rectangle to put into the atlas
            # instead of carrying the side bearings around as empty
            # texture space.
            #
            bm = Image.new(
                "L",
                (w, h),
                0
            )

            ImageDraw.Draw(bm).text(
                (-l, -t),
                chr(cp),
                font=font,
                fill=255,
                anchor="ls"
            )

            # The point size came from fitting height. Apply the
            # independent width fit now to both the bitmap and the
            # horizontal metrics.
            #
            # Bail out of rounding-to-zero by keeping at least one
            # column for a glyph that really has ink.
            #
            cw = max(
                1,
                round(w * condense)
            )

            bm = bm.resize(
                (cw, h),
                Image.LANCZOS
            )

            new.update(
                dx=round(
                    font.getlength(chr(cp)) *
                    condense
                ),
                x0=round(l * condense),
                y0=t + baseline,
                pixelWidth=cw,
                pixelHeight=h,
                bitmap=bm
            )

        else:
            # There are a few glyphs in the retail set that aren't
            # present in the source face. We don't want rebuilding the
            # common characters to quietly remove those from the game,
            # so keep their retail bitmap and enlarge it.
            #
            # s0/t0 point at texel centres. Multiplying by the atlas
            # dimensions gets us back to the first column/row closely
            # enough that taking the integer part gives the stored
            # rectangle.
            #
            x = int(g["s0"] * W)
            y = int(g["t0"] * H)

            new["bitmap"] = retail_atlas.crop(
                (x, y, x + pw, y + ph)
            ).resize(
                (pw * SCALE, ph * SCALE),
                Image.BICUBIC
            )

            missing.append(chr(cp))

    # There is one more wrinkle with advances.
    #
    # It is tempting to take the retail dx for every glyph and multiply
    # it by SCALE, just like we did for the fallback metrics above. That
    # keeps line lengths exactly the same, but it carries the spacing
    # from a 27-42 pixel rasterization into a font drawn three times
    # larger. Those advances have whole-pixel rounding and hinting baked
    # into them, which is quite visible around narrow glyphs such as I
    # and l.
    #
    # So let the source face provide the relative spacing and add one
    # constant tracking value that makes its average advance agree with
    # retail. This keeps long strings at roughly the same length without
    # throwing away the spacing information we gained by redrawing the
    # font at the larger size.
    #
    by_letter = {
        g["letter"]: g
        for g in glyphs
    }

    drawn = [
        c
        for c in range(33, 127)
        if (
            chr(c).isalnum() and
            c in by_letter and
            chr(c) not in missing
        )
    ]

    tracking = round(
        sum(
            retail[c]["dx"] * SCALE -
            by_letter[c]["dx"]
            for c in drawn
        ) /
        len(drawn)
    )

    for g in glyphs:
        # Missing characters are still using their retail metrics, so
        # they have already got the spacing correction, so to speak.
        #
        if (
            chr(g["letter"]) not in missing and
            g["dx"] > 0
        ):
            g["dx"] += tracking

    # Space has no ink and was consequently absent from the fit above.
    # There isn't anything useful to infer for it from the new
    # rasterization anyway, so keep the retail word spacing exactly.
    #
    by_letter[ord(" ")]["dx"] = (
        retail[ord(" ")]["dx"] *
        SCALE
    )

    # Bank Gothic gives us tabular digits. That sounds attractive for a
    # HUD until you compare it with what the retail font actually did:
    # its digits use their own, tighter advances. Leaving the typeface
    # advances here makes counters look conspicuously loose.
    #
    # For these two fonts put each digit back into its retail-width cell
    # and centre the newly drawn bitmap in it. We still get the
    # higher-resolution shape so this just keeps the old HUD spacing.
    #
    if name in RETAIL_DIGITS:
        for c in "0123456789":
            g = by_letter[ord(c)]

            if (
                g["bitmap"] is not None and
                c not in missing
            ):
                g["dx"] = (
                    retail[ord(c)]["dx"] *
                    SCALE
                )

                g["x0"] = round(
                    (
                        g["dx"] -
                        g["pixelWidth"]
                    ) /
                    2
                )

    # dx is a byte in the IW4 font asset. Do this last so none of the
    # fitting or spacing arithmetic has to pretend that wider
    # intermediate values are impossible.
    #
    for g in glyphs:
        g["dx"] = min(
            max(g["dx"], 0),
            255
        )

    print(
        f"{name}: {FONTS[name]} at {size:.1f} px, drawn at "
        f"{condense:.0%} width, tracking {tracking:+d}"
    )

    if missing:
        print(
            f"{name}: {FONTS[name]} lacks {''.join(missing)!r}; "
            "those keep the retail bitmap"
        )

    return (
        j["pixelHeight"] * SCALE,
        glyphs
    )


def pack(fonts):
    # There aren't enough glyphs here to warrant anything clever. Put
    # them on shelves, tallest first. Sorting by height keeps
    # similarly-sized glyphs together, which avoids wasting too much of
    # each shelf.
    #
    # Note that the exact packing is otherwise uninteresting. The
    # generated UVs follow it, so we care more about this being simple
    # and deterministic than squeezing the last few rows out of the
    # atlas.
    #
    items = [
        g
        for _, glyphs in fonts.values()
        for g in glyphs
        if g["bitmap"]
    ]

    items.sort(
        key=lambda g: -g["pixelHeight"]
    )

    x = y = PAD
    shelf = 0

    for g in items:
        w = g["pixelWidth"]
        h = g["pixelHeight"]

        if x + w + PAD > ATLAS_WIDTH:
            x = PAD
            y += shelf + PAD
            shelf = 0

        g["pos"] = (x, y)

        x += w + PAD
        shelf = max(shelf, h)

    height = y + shelf + PAD

    # Round the used height up to a power of two. ImageMagick is going
    # to generate the complete DDS mip chain and we want each level to
    # halve cleanly all the way down.
    #
    return 1 << (height - 1).bit_length()


def material(glow):
    # These are the retail gamefonts_pc materials with the image
    # replaced by our atlas and mipmapping enabled. Keep the two
    # variants together here since the few differing blend values are
    # easier to see this way than in two almost identical JSON literals.
    #
    return {
        "$schema": "http://openassettools.dev/schema/material.v1.json",
        "_game": "iw4",
        "_type": "material",
        "_version": 1,
        "cameraRegion": "none",
        "constants": [],
        "gameFlags": [],
        "sortKey": 34 if glow else 47,
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
                "dstBlendAlpha": "one" if glow else "zero",
                "dstBlendRgb": "one" if glow else "invsrcalpha",
                "gammaWrite": False,
                "polygonOffset": "offset0",
                "polymodeLine": False,
                "srcBlendAlpha": "one",
                "srcBlendRgb": "srcalpha",
            }
        ],
        "stateBitsEntry": [-1] * 4 + [0] + [-1] * 43,
        "stateFlags": 3,
        "surfaceTypeBits": 0,
        "techniqueSet": "2d",
        "textureAtlas": {
            "columns": 1,
            "rows": 1
        },
        "textures": [
            {
                "image": IMAGE,
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
    dump = Path(sys.argv[2])
    typefaces = Path(sys.argv[3])

    zone = (
        root /
        "zone_raw" /
        "iw4x_code_post_gfx_mp"
    )

    # The face names above are filenames, not paths. Search below the
    # supplied directory so somebody can point this at their normal font
    # collection without arranging it into a special layout for this
    # script.
    #
    # Bail out if one is missing. Silently substituting another weight
    # would produce perfectly usable output that is simply the wrong
    # font, which is a particularly annoying failure mode for this sort
    # of generator.
    #
    faces = {}

    for want in set(FONTS.values()):
        found = [
            p
            for p in typefaces.rglob("*")
            if p.name == want
        ]

        if not found:
            sys.exit(
                f"{want} is not under {typefaces}"
            )

        faces[want] = found[0]

    # All the information we use from the retail atlas is its coverage.
    # Strip it down to alpha here so the fitting and fallback code works
    # with plain grayscale bitmaps from this point on.
    #
    retail_atlas = Image.open(
        dump / "images" / "gamefonts_pc.dds"
    ).convert("RGBA").split()[3]

    # Rebuild all fonts before packing since they share one atlas.
    # rebuild() leaves each bitmap attached to its glyph for pack() and
    # the assembly below; those temporary fields never make it into the
    # output JSON.
    #
    fonts = {
        name: rebuild(
            name,
            dump,
            retail_atlas,
            faces
        )
        for name in FONTS
    }

    height = pack(fonts)

    atlas = Image.new(
        "L",
        (ATLAS_WIDTH, height),
        0
    )

    for _, glyphs in fonts.values():
        for g in glyphs:
            if g["bitmap"]:
                atlas.paste(
                    g["bitmap"],
                    g["pos"]
                )

    (zone / "fonts" / "iw4x").mkdir(
        parents=True,
        exist_ok=True
    )

    for name, (px, glyphs) in fonts.items():
        out = []

        for g in glyphs:
            # pack() worked in texels since that is the convenient unit
            # for fitting rectangles together. The font asset wants
            # normalized coordinates, and only now do we know the final
            # atlas height, so convert them here.
            #
            if g["bitmap"]:
                x, y = g["pos"]

                s0 = x / ATLAS_WIDTH
                t0 = y / height

                s1 = (
                    x + g["pixelWidth"]
                ) / ATLAS_WIDTH

                t1 = (
                    y + g["pixelHeight"]
                ) / height
            else:
                # There is no texture lookup for an empty glyph. Zero
                # all four coordinates instead of leaving meaningless
                # values from the retail asset around.
                #
                s0 = t0 = s1 = t1 = 0.0

            out.append({
                "letter": g["letter"],
                "x0": g["x0"],
                "y0": g["y0"],
                "dx": g["dx"],
                "pixelWidth": g["pixelWidth"],
                "pixelHeight": g["pixelHeight"],
                "s0": s0,
                "t0": t0,
                "s1": s1,
                "t1": t1,
            })

        (
            zone /
            "fonts" /
            "iw4x" /
            f"{name}.json"
        ).write_text(
            json.dumps(
                {
                    "$schema": "http://openassettools.dev/schema/font.v1.json",
                    "_type": "font",
                    "_version": 1,
                    "_game": "iw4",
                    "pixelHeight": px,
                    "material": MATERIAL,
                    "glowMaterial": GLOW_MATERIAL,
                    "glyphs": out,
                },
                indent=4
            ) + "\n"
        )

    (zone / "materials" / "fonts").mkdir(
        parents=True,
        exist_ok=True
    )

    (
        zone /
        "materials" /
        "fonts" /
        "iw4x_gamefonts.json"
    ).write_text(
        json.dumps(
            material(False),
            indent=4
        ) + "\n"
    )

    (
        zone /
        "materials" /
        "fonts" /
        "iw4x_gamefonts_glow.json"
    ).write_text(
        json.dumps(
            material(True),
            indent=4
        ) + "\n"
    )

    # gamefonts_pc is white with the glyph coverage in alpha. Our
    # working atlas has only that coverage, so fill the three colour
    # channels with white and use the atlas as alpha.
    #
    white = Image.new(
        "L",
        atlas.size,
        255
    )

    rgba = Image.merge(
        "RGBA",
        (white, white, white, atlas)
    )

    # Pillow has done all the interesting image work by this point. Use
    # ImageMagick for the final encoding since we need a DXT5 DDS
    # containing the complete mip chain expected by the Linker.
    #
    # Since both atlas dimensions are powers of two, bit_length() on the
    # largest one gives us the number of levels including the original
    # image and the final 1x1 level.
    #
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "atlas.png"

        rgba.save(png)

        subprocess.run(
            [
                "magick",
                str(png),
                "-define",
                "dds:compression=dxt5",
                "-define",
                f"dds:mipmaps={max(atlas.size).bit_length()}",
                str(
                    zone /
                    "images" /
                    f"{IMAGE}.dds"
                ),
            ],
            check=True
        )

    print(
        f"atlas {ATLAS_WIDTH}x{height}"
    )

    for name, (px, glyphs) in fonts.items():
        print(
            f"{name}: {px} px, {len(glyphs)} glyphs"
        )

if __name__ == "__main__":
    main()
