render_glass = false;
render_dark_black_metal = false;
render_shinny_metal = false;

R = 1500; //guessed
base_thickness = 400; //guessed

module gforce2_super_deluxe(){
	sdeluxe_base();
	borders();
	CRT();
	front_arcs();
	back_arcs();
	handrail_arc();
	seat();
	joystick();
	coinbox();
}

module material(name){
	if (name=="glass" && render_glass)
		color([0.7, 0.7, 0.7, 0.7])
		child(0);

	if (name=="dark black metal" && render_dark_black_metal)
		color([0.3, 0.3, 0.35])
		child(0);

	if (name=="shinny metal" && render_shinny_metal)
		color([0.8, 0.8, 0.8])
		child(0);
}

module borders(){
	e = 20;
	d = 500;

	material("dark black metal"){
		rotate(-6*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness])
		back_lateral_border(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
	}

	material("dark black metal"){
		rotate(-10*90/4)
		translate([R*cos(90/4)-d-e, 0, base_thickness])
		mirror([0,1])
		back_lateral_border(l1=2*(R-2*d)*sin(90/4), l2=2*R*sin(90/4), h=300, d=d, e=e, tip_length=200);
	}
}

module CRT(){
	translate([R*0.4,0,base_thickness + R*0.7])
	rotate(-90)
	rotate([90-10, 0])
	CRT_glass(29);
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

module arc(r, R, start=0, end=360){
	N = 50;
	PI = 3.1415;
	for (i=[0:N-1]){
		hull(){
			rotate([0,-(start + i*(end-start)/N)])
			translate([R,0])
			cylinder(r=r, h=0.1);

			rotate([0,-(start + (i+1)*(end-start)/N)])
			translate([R,0])
			cylinder(r=r, h=0.1);
		}
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
		cylinder(r=50, h=back_height);

		translate([-back_radius, 0, 0])
		cylinder(r=50, h=back_height);

		translate([0,0,back_height/2])
		rotate([0, 90])
		cylinder(r=50, h=back_radius*2, center=true);
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
		cylinder(r=60, h=handrail_height);

		translate([-handrail_radius, 0, 0])
		cylinder(r=60, h=handrail_height);
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
	arc(r=50, R=(R+dR)*cos(90/4)-100, start=-10, end=133);

	material("shinny metal")
	translate([0, R*sin(90/4), 1.5*base_thickness + ajustment_height])
	translate([R + ajustment_offset,0])
	rotate(ajustment_angle)
	translate([-R,0])
	arc(r=50, R=(R+dR)*cos(90/4)-100, start=-10, end=133);
}

module back_lateral_border(l1=200, l2=400, h=200, d=300, e=10, tip_length = 50){

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

rotate(360*$t)
gforce2_super_deluxe();