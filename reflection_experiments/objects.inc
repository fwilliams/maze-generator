#include "shapes.inc"
#include "reflection_experiments/textures.inc"

#declare Lightbulb = 
  union {
    merge {
      sphere { <0,0,0>, 1 }
      
      cylinder {
	<0,0,1>, <0,0,0>, 1
	scale <0.35, 0.35, 1.0>
	translate  0.5*z
      }
      
      texture {
      pigment { color White transmit 0.9 }
	finish { conserve_energy diffuse .01 specular 0.8 }
      }
      
      interior { ior 1.2 }
    }
    
    cylinder {
      <0,0,1>, <0,0,0>, 1
      scale <0.4, 0.4, 0.5>
      texture { Brass_Texture }
      translate  1.5*z
    }
  
    rotate -90*x
    scale .2
  }


#declare Wall = 
  #local A = <-0.5,  0.5, -0.5>;
  #local B = <-0.5, -0.5, -0.5>;
  #local C = < 0.5, -0.5, -0.5>;
  #local D = < 0.5,  0.5, -0.5>;
  merge { Quad(A, B, C, D) }


#declare Floor = 
  object {
    #local A = <-0.5, -0.5,  0.5>;
    #local B = < 0.5, -0.5,  0.5>;
    #local C = < 0.5, -0.5, -0.5>;
    #local D = <-0.5, -0.5, -0.5>;
    
    merge { Quad(A, B, C, D) }
  }

#declare Ceiling = object {
  #local A = <-0.5, 0.5,  0.5>;
  #local B = < 0.5, 0.5,  0.5>;
  #local C = < 0.5, 0.5, -0.5>;
  #local D = <-0.5, 0.5, -0.5>;
  
  merge { Quad(A, B, C, D) }
  
  texture{ 
    CeilingTex
    scale 0.25
  }
}

#macro CardboardBox(sz)
  box {
    -(sz / 2.0), (sz / 2.0)
    
    pigment {
      uv_mapping
      image_map {
	png "reflection_experiments/assets/textures/box_uv.png"
	map_type 0
      }
    }
    
    finish {
      conserve_energy
      diffuse 0.6
      roughness 0.4
    }
  }
#end


#macro ShinySphere(clr,  rad)
  sphere {
    <0, 0, 0>, rad

    interior { ior 2.5 }
    
    pigment { clr }
    
    finish {
      ambient 0.0
      diffuse 0.3
      specular 0.7
      roughness 0.1
      
      reflection {
	0.5
	fresnel on
      }
    }
  }
  
#end

#declare LightbulbSource = 
  light_source {
    <0, 0.45, 0>
    
    color <0.8, 0.8, 0.5>
    
    fade_distance 5.0
    fade_power 2.0
    
    area_light 
    0.5*z, 0.5*x, 2, 2
    
    circular orient
    
    photons {
      reflection on
      refraction on
      area_light
    }
    
    looks_like { Lightbulb }
  }