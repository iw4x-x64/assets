# `images/`

The `images/` directory holds texture data, one file per `GfxImage` asset. The
Linker looks for a `.iwi` file first and falls back to `.dds` if it is absent,
so either format may be used. `.iwi` is the format the game itself ships and
the one the IWD packer expects.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
image,example_image
```

is built from `images/example_image.iwi`.

An image name beginning with `~`, or containing `&`, denotes a generated image
whose channels are packed from several sources. Such images are ordinary
assets but are impractical to author by hand.

Note that the Unlinker writes `.dds` unless `--image-format IWI` is given. A
tree dumped with the default settings therefore round trips through the
fallback path rather than the primary one.

The retail zones use entries such as:

```
image,,$black
image,$black
```

| | |
| --- | --- |
| Zone definition type | `image` |
| Extension | `.dds` |
| Retail occurrence | 110 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
