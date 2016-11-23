inches = 2.54;
LCD_largura = 78 * inches;
LCD_altura = 55 * inches;
LCD_espessura = 1;
CRT_profundidade = 40 * inches;

fundo_largura=60;
fundo_altura=40;
arredondamento = 8;
R = 20;


module strut_2d(){
    translate([-(LCD_largura - fundo_largura)/2 + R, -(CRT_profundidade - 2*R)])
  difference(){
    square([(LCD_largura - fundo_largura)/2 - R, CRT_profundidade - 2*R]);

    scale([((LCD_largura - fundo_largura)/2 - R)/(CRT_profundidade - 2*R),1])
    circle(r=(CRT_profundidade - 2*R));
  }
}

module strut(){
  translate([0, 0, CRT_profundidade*0.8 - R + arredondamento/2])
  rotate([90, 0])
  minkowski(){
    linear_extrude(height=1)
    strut_2d();

    sphere($fn=8, r=arredondamento/3);
  }
}

module LCD(){
  translate([-LCD_largura/2, -LCD_altura/2, CRT_profundidade])

  minkowski(){
    cube([LCD_largura, LCD_altura, LCD_espessura]);
    cube(5, center = true);
  }
}

module strut_pair(){
  translate([-fundo_largura*0.6, 0]) strut();
  mirror() translate([-fundo_largura*0.6, 0]) strut();
}

module caixa(){

  for (i=[0,1])
    translate([0,20*i, 0])
      strut_pair();

  hull(){
    for (i=[-1,1])
      for (j=[-1,1])
        translate([i*(LCD_largura/2 - R), j*(LCD_altura*0.4 - R), CRT_profundidade - R]) sphere(r=R);


    translate([-LCD_largura/2, -LCD_altura/2, CRT_profundidade])
    cube([LCD_largura, LCD_altura, LCD_espessura]);
  }

  hull(){
    translate([-fundo_largura/2, -fundo_altura/2])
    cube([fundo_largura, fundo_altura, 1]);

    for (i=[-1,1])
      for (j=[-1,1])
        translate([i*fundo_largura/2, j*fundo_altura/2]) sphere(r=arredondamento);


    translate([-LCD_largura/4, -LCD_altura/8, CRT_profundidade])
    cube([LCD_largura/2, LCD_altura/4, LCD_espessura]);
  }

  hull(){
    for (i=[-1,1])
      for (j=[-1,1])
        translate([i*(fundo_largura + LCD_largura/2)/4, j*fundo_altura, CRT_profundidade/2]) sphere(r=arredondamento/2);


    translate([-LCD_largura/4, -LCD_altura/2, CRT_profundidade])
    cube([LCD_largura/2, LCD_altura, LCD_espessura]);
  }

  for (i=[-1,1]){
    hull(){
      for (j=[-1,1])
        translate([i*fundo_largura/2, j*fundo_altura/2]) sphere(r=arredondamento);

      translate([i*LCD_largura/4, 0, CRT_profundidade])
      cube([LCD_espessura, LCD_altura, LCD_espessura], center=true);
    }
  }
}


rotate([90-15,0])
{
 caixa();
 LCD();
}