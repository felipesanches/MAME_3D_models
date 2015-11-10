STL2EGG = ../tools/stl2egg.py

MATERIALS = egg/newufo_claw_white_abs.egg \
            egg/newufo_claw_transparent_acrylic.egg

all: $(MATERIALS)

stl/newufo_%.stl: newufo.scad
	openscad $< -D render_$*=true -D render_all=false -o $@

egg/newufo_%.egg: stl/newufo_%.stl
	python $(STL2EGG) $< $@
	
clean:
	rm -f stl/*.stl
	rm -f egg/*.egg