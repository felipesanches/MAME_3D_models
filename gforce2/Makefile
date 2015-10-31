STL2EGG = ../tools/stl2egg.py

MATERIALS = egg/gforce2_glass.egg \
            egg/gforce2_dark_black_metal.egg \
            egg/gforce2_shinny_metal.egg \
            egg/gforce2_static_shinny_metal.egg \
            egg/gforce2_static_red.egg \
            egg/gforce2_static_golden.egg

all: $(MATERIALS)

stl/gforce2_%.stl: gforce2.scad
	openscad $< -D render_$*=true -D render_all=false -o $@

egg/gforce2_%.egg: stl/gforce2_%.stl
	python $(STL2EGG) $< $@
	
clean:
	rm -f stl/gforce2_*.stl
	rm -f egg/gforce2_*.egg