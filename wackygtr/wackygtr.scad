/*
 * This is a parametric 3D model of the cabinet of the Wacky Gator redemption game.
 * I'm using OpenSCAD to mockup a 3D artwork layer for MAME (https://github.com/mamedev/mame)
 *
 * There's an ongoing brainstorming about it happening at:
 * https://github.com/mamedev/mame/issues/388
 *
 * And there's a video of this animated 3d scene as well as of the Wacky Gator game running on MAME
 * available here:
 * https://youtu.be/P48hQkLiNxM
 *
 * This script is licensed under the terms of the General Public License version 2
 * or (at your option) any later.
 *
 * (c)2015 Felipe Correa da Silva Sanches
 *         <juca@members.fsf.org>
 *         <http://mamedev.emulab.it/fsanches/>
 */

render_glass = false;
render_blue_metal = false;
render_clear_wood = false;
render_dark_wood = false;
render_separators = false;
render_alligator = false;

module material(name){
    if (name=="glass" && render_glass)
        color([0.7, 0.7, 0.7, 0.7])
        child(0);

    if (name=="blue metal" && render_blue_metal)
        color([0.3, 0.3, 0.6])
        child(0);

    if (name=="clear wood" && render_clear_wood)
        color([0.9, 0.8, 0.6])
        child(0);

    if (name=="dark wood" && render_dark_wood)
        color([0.3, 0.3, 0.3])
        child(0);

    if (name=="separators" && render_separators)
        color([211/255, 164/255, 65/255])
        child(0);

    if (name=="alligator" && render_alligator)
        color([136/255, 179/255, 101/255])
        child(0);
}

inches = 25.4;
glass_thickness = 2;
wood_thickness = 20;

curvature_radius = 2600;
total_height = 66 * inches;
bottom_width = 47 * inches;
bottom_height = 33 * inches;
bottom_depth = 34 * inches;
bottom_bevel = bottom_depth/5;
head_depth = 400;
head_width = 38 * inches;
head_height = total_height - bottom_height;



module wacky_gator(){
	body();

	translate([0, 0, bottom_height - wood_thickness])
	head();
}

module sidewall_2d(){
	hull(){
		square([bottom_depth - bottom_bevel, bottom_height]);
		square([bottom_depth, bottom_height - bottom_bevel + 30]);
	}
}

module sidewall(){
	material("dark wood")
	rotate([90,0,0])
	linear_extrude(height=wood_thickness) sidewall_2d();
}

module bottom_box(){
	material("blue metal")
	translate([bottom_depth - wood_thickness/2 - 80,0,2])
	cube([80, bottom_width, bottom_height - bottom_bevel]);

	material("clear wood")
	translate([0,0,bottom_height - bottom_bevel])
	cube([bottom_depth - 80, bottom_width, 1]);
}

module cover_wood(){
	material("clear wood")
	linear_extrude(height=wood_thickness){
		difference(){
			translate([0, -bottom_width/2,0])
			square([bottom_depth, bottom_width]);

			translate([curvature_radius + 500, 0])
			circle(r=curvature_radius, $fn=200);
		}
	}

	//screws:
	material("dark wood")
	for (i=[0,1]){
		for (j=[-1,1]){
			translate([40 + i*head_depth,j*((bottom_width + head_width + 2 * wood_thickness)/4), wood_thickness])
			scale([1, 1, 0.3])
			sphere(r=10);
		}
	}
}

module door_hole(){
	rotate([0,-90,0])
	linear_extrude(h=wood_thikness*2){
		hull()
		for (i=[-1,1])
			for (j=[-1,1])
				translate([i*70, j*40])
				circle(r=10, $fn=20);
	}
}

module doors(h=80){
	material("clear wood")
	difference(){
		linear_extrude(height=h){
			intersection(){
				difference(){
					translate([0, -bottom_width/2,0])
					square([bottom_depth, bottom_width]);

					translate([curvature_radius + 500, 0])
					circle(r=curvature_radius + wood_thickness, $fn=200);

				}
				translate([curvature_radius + 500, 0])
				circle(r=curvature_radius + 2*wood_thickness, $fn=200);
			}
		}

		for (i=[0:4]){
			translate([curvature_radius + 500, 0])
			rotate((i-2) * 2 * asin((bottom_width/2)/curvature_radius) / 6)
			translate([-curvature_radius, 0])
			door_hole();
		}
	}
}

//function aligator_position(i) = states[i]/5;
function aligator_position(i) = (1 + sin((15*$t+i/5)*360))/2;

module body(){
	translate([0, -bottom_width/2, 0])
	sidewall();

	translate([0, bottom_width/2 + wood_thickness, 0])
	sidewall();

	translate([0, -bottom_width/2, 0])
	bottom_box();

	translate([bottom_depth/3 + 200, 0, bottom_height - bottom_bevel]){
		for (i=[0:5]){
			translate([curvature_radius, 0])
			rotate((i-2.5) * 2 * asin((bottom_width/2)/curvature_radius) / 6)
			translate([-curvature_radius, 0])
			wall();
		}

		for (i=[0:4]){
			translate([curvature_radius, 0])
			rotate((i-2) * 2 * asin((bottom_width/2)/curvature_radius) / 6)
			translate([-curvature_radius - 200 + 200 * aligator_position(i), 0])
			alligator();
		}
	}

	translate([0, 0, bottom_height - 2*wood_thickness])
	cover_wood();

	translate([0, 0, bottom_height - bottom_bevel])
	doors(h=bottom_bevel - 2*wood_thickness);
}

module half_pill_2d(r, l){
	hull(){
		translate([l,0])
		circle(r=r);
		square([0.1, 2*r], center=true);
	}
}

skew = [ [ 1,  0, -0.4,  0 ],
         [ 0,  1,    0,  0 ],
         [ 0,  0,    1,  0 ],
         [ 0,  0,    0,  1 ] ]; 

module wall(h=40, l=160){
	material("separators")
	intersection(){
		union(){
			multmatrix(skew)
			linear_extrude(height=h)
			half_pill_2d(r=40, l=l);

			translate([0,0,h])
			multmatrix(skew)
			linear_extrude(height=h)
			half_pill_2d(r=32, l=l-20);

			translate([0,0,2*h])
			multmatrix(skew)
			linear_extrude(height=h)
			half_pill_2d(r=25, l=l-40);
		}
		translate([0,-60])
		cube([250,120,3*h]);
	}
}

module rounded_block(x, y, z, r=20){
	hull(){
		for (i=[0,1]){
			for (j=[0,1]){
				for (k=[0,1]){
					translate([i*x, j*y, k*z])
					sphere(r=r);
				}
			}
		}
	}
}

module alligator(){
	material("alligator")
	translate([0,-25, 20])
	rounded_block(200, 50,30);
}

//-------------------------------------------------------

head_bevel = 100;
module head_sidepanel_2d(){
	square([head_depth, head_height]);

	translate([head_depth, 0])
	polygon([[0,0], [0,head_bevel], [head_bevel,0]]);
}

module head_sidepanel(){
	material("dark wood")
	rotate([90,0])
	linear_extrude(height=wood_thickness)
	head_sidepanel_2d();
}

module top_wood(){
	material("dark wood")
	cube([head_depth - wood_thickness, head_width, wood_thickness]);
}

module back_glass(){
	material("glass")
	cube([ glass_thickness, head_width, head_height - head_bevel - 2*wood_thickness]);
}

module marquee(){
	material("glass")
	cube([ glass_thickness, head_width, head_bevel*sqrt(2) ]);
}

module head(){
	translate([0, -head_width/2])
	head_sidepanel();

	translate([0, head_width/2 + wood_thickness])
	head_sidepanel();

	translate([0, -head_width/2, head_height - 2*wood_thickness])
	top_wood();

	translate([head_depth - wood_thickness, -head_width/2, head_bevel])
	back_glass();

	translate([head_depth - wood_thickness + head_bevel, -head_width/2, 0])
	rotate([0, -45])
	marquee();
}

rotate(20*sin($t*360))
wacky_gator();