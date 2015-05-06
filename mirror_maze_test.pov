#version 3.7;

#include "colors.inc"
#include "rad_def.inc"

#include "reflection_experiments/objects.inc"
#include "mirrormaze.inc"

#declare EnablePhotonMapping = true;

global_settings {
  assumed_gamma 1.0
  max_trace_level 30

  #if (EnablePhotonMapping)
    photons {
      spacing 0.01
      save_file "mirrormaze.map"
    }
  #end
}

#default{ finish { conserve_energy ambient 0.0 diffuse 0.7 specular 0.0 } }


#declare ScaleParam = 5.0;

#declare WallTex = MirrorTex(0.9)
//#declare WallTex = BrickWallTex;

object {
  union {
  Maze(WallTex, true)

  object {
    #local BoxDims = <0.2, 0.2, 0.2>;
    CardboardBox(BoxDims)
    
    rotate 45.0 * y
    translate <MazeWidth/2.0 + 0.2, -0.4, MazeHeight/2.0>
  }
  }
  translate <-MazeWidth/2.0 + 0.5, 0.0, -MazeHeight/2.0 + 0.5>
  scale ScaleParam  
  
  

}

light_source {
  LightbulbSource
  
  translate <-MazeWidth/2.0 + 0.5, 0.4, -MazeHeight/2.0 + 0.5> * ScaleParam
}

light_source {
  LightbulbSource
  
  translate <0.0, 0.0, 0.0> * ScaleParam
}

camera { 
  // View 1
  location <0.1, 0.1, 0.1>
  look_at  <1.0, 0.0, 1.0>
  right    <1.0, 0.0, 0.0>
  angle 90
  
  focal_point <4.0, 0.0, 4.0>
  blur_samples 100
  aperture 0.05
  confidence 0.9
  variance 1/10000
}
