# `codescripts/`

The `codescripts/` directory holds scripts the engine calls at fixed points of
its own accord, as distinct from scripts invoked by level logic.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,codescripts/example.gsc
```

is built from `codescripts/example.gsc`.

The retail zones use entries such as:

```
rawfile,codescripts/$default
rawfile,codescripts/character.gsc
rawfile,codescripts/delete.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc`, none |
| Retail occurrence | 4 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
