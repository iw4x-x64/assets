# `shader_bin/`

The `shader_bin/` directory holds compiled shader objects. Both pixel and
vertex shaders live here and are distinguished by the asset type in the zone
definition rather than by location.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
pixelshader,blur_apply_film.hlsl
```

is built from `shader_bin/blur_apply_film.hlsl.cso`.

Note that the extension is appended rather than replaced. The asset name
retains its `.hlsl` suffix and the file on disk carries `.cso` after it,
giving `<name>.hlsl.cso`.

If a technique names a shader whose data was never loaded, the dumper reports
that it cannot dump the shader because its data is not loaded. The remedy is
to preload the zone that provides it, which the dump script does automatically
once it has identified the provider.

The retail zones use entries such as:

```
pixelshader,blur_apply_film_color2.hlsl
pixelshader,blur_apply_film.hlsl
vertexshader,cinematic_dtex.hlsl
```

| | |
| --- | --- |
| Zone definition type | `pixelshader`, `vertexshader` |
| Extension | `.cso` |
| Retail occurrence | 103 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
