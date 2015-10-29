STL2EGG = ../tools/stl2egg.py

MATERIALS = egg/wackygtr_glass.egg \
            egg/wackygtr_blue_metal.egg \
            egg/wackygtr_clear_wood.egg \
            egg/wackygtr_dark_wood.egg \
            egg/wackygtr_separators.egg \
            egg/wackygtr_alligator.egg

all: $(MATERIALS)

stl/wackygtr_%.stl: wackygtr.scad
	openscad $< -D render_$*=true -o $@

egg/wackygtr_%.egg: stl/wackygtr_%.stl
	python $(STL2EGG) $< $@

clean:
	rm -f stl/wackygtr_*.stl
	rm -f egg/wackygtr_*.egg