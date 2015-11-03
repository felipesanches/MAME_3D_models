arcs_longitudinal_detail_level = 100;
arcs_circular_detail_level = 12;
render_all = true;
render_glass = false;
render_dark_black_metal = false;
render_shinny_metal = false;
render_red_panels = false;
render_static_shinny_metal = false;
render_static_golden = false;
render_static_red = false;
render_light_sphere = false;

R = 1500; //guessed
base_thickness = 400; //guessed
base_elevation = R*0.3;

//This is simply a helper sphere for
//positioning lights in the scene:
if (render_light_sphere){
	sphere(r=100, $fn=20);
}

module gforce2_super_deluxe(){
	security_stands();
	stand_strings();
	legs();
	golden_center();

	rotate(360*$t)
	translate([0,0,base_elevation]){
		sdeluxe_base();
		borders();
		speakers();
		cpu_box();
		front_arcs();
		back_arcs();
		handrail_arc();
		seat();
		joystick_panel();
		gear();
		pedals();
		coinbox();
		CRT();
	}
}

module material(name){
	if (name=="glass" && (render_glass || render_all))
		color([0.3, 0.3, 0.3, 0.7])
		child(0);

	if (name=="dark black metal" && (render_dark_black_metal || render_all))
		color([0.3, 0.3, 0.35])
		child(0);

	if (name=="shinny metal" && (render_shinny_metal || render_all))
		color([0.8, 0.8, 0.8])
		child(0);

	if (name=="static shinny metal" && (render_static_shinny_metal || render_all))
		color([0.8, 0.8, 0.8])
		child(0);

	if (name=="static red" && (render_static_red|| render_all))
		color([0.8, 0, 0])
		child(0);

	if (name=="static golden" && (render_static_golden || render_all))
		color([0.8, 0.5, 0.2])
		child(0);

	if (name=="red panels" && (render_red_panels || render_all))
		color([0.3, 0.0, 0.0, 0.7])
		child(0);
}

module golden_center(){
	material("static golden"){
		cylinder(r1=R*0.7, r2=R*0.6, h=base_elevation);
	}
}

stand_height = 1500;

module stand(){
	stand_radius = 30;
	stand_base_h = feet_height;
	stand_base_r = 250;
	stand_base_thickness = 20;

	material("static shinny metal")
	union(){
		cylinder(r=stand_radius, h=stand_height);
		hull(){
			cylinder(r=stand_base_r, h=stand_base_thickness);
			cylinder(r=stand_radius, h=stand_base_h);
		}
	}	
}

security_radius = 1.5 * R;

module stand_strings(){
	d = 2 * security_radius * sin(90/4);
	h = 300;

	for (i=[1:6]){
		rotate(90 + 45/2 + 45*i){
			translate([security_radius * cos(90/4), 0])
			stand_string(h, d);
		}
	}
}

module stand_string(h, d, top=50){
	radius = h/2 + d*d/(8*h);
	alfa = acos((radius-h)/radius);

	material("static red")
	translate([0,0,stand_height + radius-h - top])
	rotate(90)
	arc(r=10, R=radius, start = 270 - alfa, end = 270 + alfa);
}

module security_stands(){
	for (i=[1:7]){
		rotate(90 + 45*i){
			translate([security_radius, 0])
			stand();
		}
	}
}

module joystick_panel(){
	//TODO: Implement-me!
	joystick();
}

module joystick(){
	//TODO: Implement-me!
}

feet_height = 150;

module feet(){
	//TODO: Implement-me!
}

module leg_profile_2d(){
	w1 = 80;
	w2 = 120;
	h1 = 160;
	h2 = 60;
	t = 5;

	difference(){
		hull(){
			translate([-w1/2, 0])
			square([w1, h1]);

			translate([-w2/2, 0])
			square([w2, h2]);
		}

		hull(){
			translate([-w1/2+t, t])
			square([w1-2*t, h1-2*t]);

			translate([-w2/2+t, t])
			square([w2-2*t, h2-2*t]);
		}
	}
}

flash_light_h = 180;
flash_light_r = 70;

module flash_light(){
	e = 10;
	difference(){
		cylinder(r=flash_light_r, h=flash_light_h);

		translate([0,0,e])
		cylinder(r=flash_light_r-e, h=flash_light_h);
	}

	translate([0,0,flash_light_h])
	rotate([0, -70])
	cylinder(r=flash_light_r-e, h=e);

}

module foot(){
	cylinder(r=60, h=20);
	cylinder(r=20, h=feet_height);
}

//!foot();

module legs(){
	leg_length = R*1.2;

	translate([0,0,feet_height])
	for (i=[0:3]){
		rotate(45 + 90*i){
			rotate([90,0])
			material("static shinny metal"){
				linear_extrude(height=leg_length)
				leg_profile_2d();
			}

			rotate([90,0])
			material("static red"){
				linear_extrude(height=leg_length + 600)
				scale(0.9)
				leg_profile_2d();
			}

			material("static shinny metal"){
				translate([leg_length - 30, 2*flash_light_r, flash_light_r])
				rotate([0,-70])
				flash_light();
			}

			material("static shinny metal"){
				translate([leg_length - 100, 0, -feet_height])
				foot();
			}
		}
	}
}

module borders(){
	e = 20;
	d = 500;

	material("dark black metal"){
		rotate(-6*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness]){
			back_lateral_border(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
		}
	}

	material("dark black metal"){
		rotate(-10*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness])
		mirror([0,1])
		back_lateral_border(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
	}

	material("red panels"){
		rotate(-6*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness]){
			render()
			translate([0,0,10])
			back_lateral_cover(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
		}
	}

	material("red panels"){
		rotate(-10*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness]){
			render()
			mirror([0,1])
			translate([0,0,10])
			back_lateral_cover(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
		}
	}
}

module CRT(){
	translate([R*0.4,0,base_thickness + R*0.7])
	rotate(-90)
	rotate([90-10, 0])
	CRT_glass(36);
}

module coinbox(){
	material("dark black metal")
	translate([R*0.4, -R*0.75, base_thickness])
	cube([200,300,600]);

	//TODO: metalic coin slots
}

module crt_outline_2d(w, h, r){
	hull()
	for (i=[-1,1]){
		for (j=[-1,1]){
			translate([i*w/2, j*h/2])
			circle(r=r);
		}
	}
}

module CRT_glass(inches){
	H=60;
	w=320;
	h=240;
	k=0.8;
	material("glass")
	scale(25.4*inches/w)
	intersection(){
		scale([k*w/H,k*h/H,1])
		sphere(r=H, $fn=80);

		linear_extrude(height=H)
		crt_outline_2d(w,h,10);
	}
}

module pie_slice(radius, angle, step) {
	for(theta = [0:step:angle-step]) {
		linear_extrude(height = radius*2, center=true)
		polygon(points = [[0,0], [radius * cos(theta+step), radius * sin(theta+step)], [radius * cos(theta), radius * sin(theta)]]);
	}
}

module partial_rotate_extrude(radius, start, end) {
	intersection () {
		rotate_extrude()
		translate([radius,0,0])
		child(0);

		rotate(start)
		pie_slice(radius*2, end-start, (end-start)/8);
	}
}

module arc(r, R, start=0, end=360){
	rotate([90,0])
	partial_rotate_extrude(R, start, end, $fn=arcs_longitudinal_detail_level)
	circle(r=r, $fn=arcs_circular_detail_level);
}

module arc_cut(r, R, angles, length=20, depth=10){
	N = 50;
	PI = 3.1415;
	for (angle = angles)
	rotate([0,-angle])
	translate([R,0])
	difference(){
		cylinder(r=r+1, h=length);
		cylinder(r=r-depth, h=length);
	}
}

module back_arcs(){
	back_height = R*0.8;
	back_radius = R/4;
	back_inclination = 15;

	material("shinny metal")
	rotate(90)
	translate([0, R*cos(90/4) - (back_height+back_radius)*sin(back_inclination), base_thickness])
	rotate([-back_inclination, 0]){
		translate([0, 0, back_height])
		arc(r=50, R=back_radius, start=0, end=180);

		translate([back_radius, 0, 0])
		cylinder(r=50, h=back_height, $fn=arcs_circular_detail_level);

		translate([-back_radius, 0, 0])
		cylinder(r=50, h=back_height, $fn=arcs_circular_detail_level);

		translate([0,0,back_height/2])
		rotate([0, 90])
		cylinder(r=50, h=back_radius*2, center=true, $fn=arcs_circular_detail_level);
	}
}

module handrail_arc(){
	handrail_height = 300;
	handrail_radius = R/4;

	material("shinny metal")
	translate([0, 0, base_thickness])
	rotate([0, 0, -3*90/4])
	translate([-R+handrail_radius+100, 0]){
		translate([0, 0, handrail_height])
		arc(r=60, R=handrail_radius, start=0, end=180);

		translate([handrail_radius, 0, 0])
		cylinder(r=60, h=handrail_height, $fn=arcs_circular_detail_level);

		translate([-handrail_radius, 0, 0])
		cylinder(r=60, h=handrail_height, $fn=arcs_circular_detail_level);
	}
}

module front_arcs(){
	ajustment_angle = 5.93;
	ajustment_height = 35;
	ajustment_offset = -280;
	dR = 300;

	material("shinny metal")
	rotate(90)
	translate([0, -R*sin(90/4), 160 + 1.5*base_thickness])
	arc(r=50, R=R*cos(90/4)-100, start=-20, end=200);

	material("shinny metal")
	translate([0, -R*sin(90/4), 1.5*base_thickness + ajustment_height])
	translate([R + ajustment_offset,0])
	rotate(-ajustment_angle)
	translate([-R,0])
	difference(){
		arc(r=50, R=(R+dR)*cos(90/4)-100, start=-10, end=133);
		arc_cut(r=50, R=(R+dR)*cos(90/4)-100, angles=[61, 128]);
	}

	material("shinny metal")
	translate([0, R*sin(90/4), 1.5*base_thickness + ajustment_height])
	translate([R + ajustment_offset,0])
	rotate(ajustment_angle)
	translate([-R,0])
	difference(){
		arc(r=50, R=(R+dR)*cos(90/4)-100, start=-10, end=133);
		arc_cut(r=50, R=(R+dR)*cos(90/4)-100, angles=[61, 128]);
	}

}

module back_lateral_cover_2d(l, h, d, e){
	translate([4*e, -l/2 + e])
	square([d - 4*e, l - 2*e]);

	translate([d/3 + 4*e, -l/2 - 80 + e])
	square([2*d/3 - 4*e, l + 160 - 2*e]);
}

module back_lateral_cover(l1, l2, h, d, e, tip_length){
	intersection(){
		back_lateral_border(l1, l2, h, d, e, tip_length, cut=false);

		linear_extrude(height=h)
		back_lateral_cover_2d(l1, h, d, e);
	}
}

module back_lateral_border(l1=200, l2=400, h=200, d=300, e=10, tip_length = 50, cut=true){

	render()
	difference(){
		union(){
			hull(){
				translate([0, -l1/2])
				cube([e, l1, h]);

				linear_extrude(height=e){
					hull(){
						translate([0,-l1/2])
						square([d, l1]);

						translate([d, -l2/2 + tip_length])
						square([e, l2 - tip_length]);
					}
				}
			}

			hull(){
				cube([e, l1/2, h]);

				linear_extrude(height=e){
					hull(){
						square([d, l1/2]);

						translate([d, -l2/2])
						square([e, l2]);
					}
				}
			}
		}

		if (cut){
			translate([0,0,e]){
				linear_extrude(height=h)
				back_lateral_cover_2d(l1, h, d, e);
			}
		}
	}
}

step_height = base_thickness*0.8;

module grid_pattern_2d(){
	thickness = 2*R*sin(45/2)/50;
	height = base_thickness*0.4;
	for (x=[-1:1]){
		for (y=[-1,1]){
			for (i=[-3:3]){
				translate([(x*15 + i*2)*thickness, y*(height + thickness)/2])
				square([thickness, height], center=true);
			}
		}
	}
}

module grid_pattern2_2d(){
	thickness = step_height/11;
	width  = (2*R*sin(45/2)/2 - 4*thickness)/3;
	spacing = thickness;
	height = base_thickness*0.4;
	for (x=[-1:1]){
		for (y=[-2:2]){
			translate([x*(width + spacing), y*(thickness + spacing)])
			square([width, thickness], center=true);
		}
	}
}

module grid_pattern(){
	//grids on the sides
	for (i=[1:7]){
		rotate(i*360/8)
		translate([0,R, base_thickness/2]){
			rotate([90,0])
			linear_extrude(height=200)
			grid_pattern_2d();
		}
	}

	//grid on the step
	translate([0,R, base_thickness - step_height/2]){
		rotate([90,0])
		linear_extrude(height=800)
		grid_pattern2_2d();
	}
}

module sdeluxe_base(){
	material("dark black metal")
	render()
	{
		difference(){
			rotate(360/16)
			cylinder($fn=8, r=R, h=base_thickness);

			translate([0, 1.6*R, base_thickness/5])
			scale([0.5, 1])
			rotate(360/16)
			cylinder($fn=8, r=R, h=base_thickness);

			grid_pattern();

		    //This is not strictly necessary.
            //I am removing this portion of the base only
            //for aestethical purposes (to make the floor visible
            //though the grid
			difference(){
				translate([0,0,-1])
				rotate(360/16)
				cylinder(r=R-10, h=base_thickness, $fn=8);

				translate([0, 1.6*R, -1])
				scale([0.5 + 0.01, 1 + 0.01])
				rotate(360/16)
				cylinder($fn=8, r=R+1, h=base_thickness);
			}
		}

		difference(){
			translate([0,0,base_thickness])
			rotate(360/16)
			cylinder($fn=8, r1=R-200, r2=R-400, h=base_thickness);

			translate([-R, -R])
			cube([R+R*0.4, 2*R, 3*base_thickness]);
		}
	}
}

gforce2_super_deluxe();