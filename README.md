# pyassp
Lightweight python wrapper around libassp, using the R package wrassp as reference.

# Installation
To install the libassp binaries:
```
cd libassp-1.1
./configure
make
```

# Progress/todo:
Three functions required to recreate wrassp usage in MDAi:
- computeFMT (forest) - largely complete
  - note that the output buffer contains a lot more data than we're currently retrieving - what is it?
  - DOBJ.maxbufrecs * DOBJ.recordsize items are present
- rmsana - todo
- ksvf0 - todo

Also need to recreate calculation of formant plot from the results of the above.

## Usage with pyodide
Requires that this package can be built using pypa/build - i.e.: requires a setup.py
May require conversion from autotools make to cmake, as pyodide may not support autotools, but not yet sure.
