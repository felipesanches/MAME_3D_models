# MAME_3D_models
3D models for usage as artwork in MAME (this is an on-going experiment / mockup for a future feature that is being discussed at: https://github.com/mamedev/mame/issues/388)

# Some thoughs...
The EGG files are provided in this repository, even though they are actually generated from STL files. And these STLs are generated from SCAD source code.

There's a Makefile in each artwork directory for generating these, but one needs to have OpenSCAD installed in order to build it.

With the purpose of making it easier for MAME developers and contributors to try this technology demo, I am storing the EGG files in the git repository. If you change the SCAD source, you can run **make** in order to update the EGG files.

There's also a python script in this repository for converting STL files to EGG files.
