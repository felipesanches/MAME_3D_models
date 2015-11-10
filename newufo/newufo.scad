$fn=80;

//These global parameters are all based on guessed dimentions.
//It should all be verified by measuring the real equipment.
claw_radius = 200;
claw_opening_angle = 0;
claw_thickness = 40;
feet_height = 50;
cabinet_width = 2200;
cabinet_depth = 1000;
cabinet_height = 2400;
base_height = 800;
cabinet_rounding = 50;

pink_metal = [1, 0.9, 0.9, 1];

//spacing between the cabinet top and the maximum z coordinate of the ufo claw:
top_margin = 500;
bottom_margin = 300; //to the bottom of the cage
width_margin = 300; //to the sides
depth_margin = 300; //to front and to back

render_all = true;
render_claw_white_abs = false;
render_claw_transparent_acrylic = false;

claw_white_abs = [1, 1, 0.95, 1];
claw_transparent_acrylic = [0.8, 0.8, 0.9, 0.5];

if (render_claw_transparent_acrylic){
	material("claw_transparent_acrylic")
	rotate([0, claw_opening_angle, 0])
	claw_finger();
}

module material(name){
    if (name=="claw_transparent_acrylic" && (render_claw_transparent_acrylic || render_all))
        color(claw_transparent_acrylic)
        child(0);

    if (name=="claw_white_abs" && (render_claw_white_abs || render_all))
        color(claw_white_abs)
        child(0);
}

module claw(){
	claw_body();

	if (render_all){
		color(claw_transparent_acrylic){
			rotate([0, claw_opening_angle, 0])
			claw_finger();

			mirror([1,0])
			rotate([0, claw_opening_angle, 0])
			claw_finger();
		}
	}
}

module claw_finger_2d(border = [0,0]){

	nodes = [
		[[40,0], [30,10]],
		[[180,-150], [30,10]],
		[[180,-180], [30,10]],
		[[50,-320], [10,10]]
	];

	for (i=[0:2]){
		assign(p1 = nodes[i][0], s1 = nodes[i][1], p2 = nodes[i+1][0], s2 = nodes[i+1][1]){
			hull(){
				translate(p1) square(s1 - border, center=true);
				translate(p2) square(s2 - border, center=true);
			}
		}
	}
}

module claw_finger(){
	render()
	difference(){
		rotate([90,0])
		linear_extrude(height=claw_thickness, center=true)
		claw_finger_2d();

		rotate([90,0])
		translate([0,0,2*claw_thickness/3])
		linear_extrude(height=claw_thickness, center=true)
		claw_finger_2d(border=[9,9]);

		rotate([90,0])
		mirror([0,0,1])
		translate([0,0,2*claw_thickness/3])
		linear_extrude(height=claw_thickness, center=true)
		claw_finger_2d(border=[9,9]);
	}
}

module claw_body(){
	material("claw_white_abs")
	difference(){
		claw_body_main();
		for (i=[0,1]){
			mirror([i,0])
			translate([claw_radius/2, -claw_thickness, -claw_radius])
			cube([claw_radius, 2*claw_thickness, claw_radius]);
		}
	}
}

module claw_body_main(){
	extra = 10;

	scale([1, 1, 0.6])
	sphere(r=claw_radius);

	cylinder(center=true, h=50, r=claw_radius + extra/2);

	scale([1, 1, 0.6])
	hull(){
		intersection(){
			rotate([90,0])
			cylinder(r=claw_radius * 0.6, h=2*(claw_radius + extra), center=true);

			sphere(r=claw_radius + extra);
		}

		intersection(){
			rotate([90,0])
			cylinder(r=claw_radius * 0.6 + extra, h=2*(claw_radius + extra), center=true);

			sphere(r=claw_radius);
		}
	}
}

module rounded_square(s, r){
    hull()
    for (i=[-1:1]){
        for (j=[-1:1]){
            translate([i*(s[0]/2 - r), j*(s[1]/2 - r)])
            circle(r=r, $fn=20);
        }
    }
}

module cabinet_front_panel(){
    //TODO: Implement-me!
}

module cabinet_base_body(){
    //TODO: Implement-me!
    color(pink_metal)
    linear_extrude(height=base_height)
    rounded_square([cabinet_width, cabinet_depth], r=cabinet_rounding);
}

module cabinet_windows(){
    //TODO: Implement-me!
}

module cabinet_feet(){
    //TODO: Implement-me!
}

//coordinates for the claws of each of the 2 players
claw_x = [0, 0];
claw_y = [0, 0];
claw_z = [0, 0];

module     claw_mechanisms(){
    //TODO: Implement-me!
    for (p = [0, 1]){
        translate([ -cabinet_width/2 * (1-p) + width_margin + claw_x[p] * (cabinet_width/2 - 2*width_margin),
                    -cabinet_depth/2 + depth_margin + claw_y[p] * (cabinet_depth - 2*depth_margin),
                     base_height + bottom_margin +
                      claw_z[p] * (cabinet_height - base_height - top_margin)])
        claw();
    }
}

module newufo(){
    cabinet_feet();
    translate([0, 0, feet_height]){
        cabinet_front_panel();
        cabinet_base_body();
        cabinet_windows();
        claw_mechanisms();
    }
}

newufo();