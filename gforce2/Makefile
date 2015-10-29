MATERIALS = egg/gforce2_glass.egg \
            egg/gforce2_dark_black_metal.egg \
            egg/gforce2_shinny_metal.egg

all: $(MATERIALS)

stl/gforce2_%.stl: gforce2.scad
	openscad $< -D render_$*=true -o $@

egg/gforce2_%.egg: stl/gforce2_%.stl
	python stl2egg.py $< $@