# `scriptdebugger/`

The `scriptdebugger/` directory holds data supporting the script debugger.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,scriptdebugger/example.txt
```

is built from `scriptdebugger/example.txt`.

The retail zones use entries such as:

```
rawfile,scriptdebugger/help.txt
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.txt` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
