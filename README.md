# MAME_3D_models
3D models for usage as artwork in MAME (this is an on-going experiment / mockup for a future feature that is being discussed at: https://github.com/mamedev/mame/issues/388)

# Some thoughs...
The EGG files are provided in this repository, even though they are actually generated from STL files. And these STLs are generated from SCAD source code.

There's a Makefile in each artwork directory for generating these, but one needs to have OpenSCAD installed in order to build it.

With the purpose of making it easier for MAME developers and contributors to try this technology demo, I am storing the EGG files in the git repository. If you change the SCAD source, you can run **make** in order to update the EGG files.

There's also a python script in this repository for converting STL files to EGG files.

# keyboard commands

**TAB** key alternates between the default orbiting camera and any other camera that may have been declared in the 3d artwork layout XML file.

**ESC** key exists the program.

**H** and **G** keys are used to control the motion relative to the first **motion** tag found in an XML file. For Galaxy Force II Super Deluxe, it controls the rotation of the cabinet.

**F** key toggles fullscreen mode.

# Tips

If you run this system with the gforce2 3d artwork and then you run MAME with the Power Drift driver, you'll be able to see the 3d model move in sync with the gameplay. Including the blinking of the light in the start button.
