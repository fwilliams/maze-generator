#include "textures.inc"

#declare BrickWallTex = 
  texture {
    pigment {
      brick
    }
    normal {
      brick normal{ bumps 0.3 } normal{ granite 0.3 }
    }
    finish {
      conserve_energy
      roughness 0.5
    }
    scale <0.025, 0.025, 0.025>
  }

#declare CheckerFloorTex = 
  texture { 
    pigment { 
      checker Black White
      scale 0.05
    }
    finish {
      diffuse 0.5
      specular 0.5
    }
  }

#declare WoodFloorTex = 
  texture {
    DMFWood6
    scale <0.25, 0.25, 0.25>
    
    pigment {
      turbulence 0.1
    }
  }

#macro MirrorTex(reflectivity)
  //Polished_Chrome
  finish {
    conserve_energy
    reflection reflectivity
    diffuse 0.0
    specular 0.0
  }
#end

#declare CeilingTex = 
  texture {
    pigment { 
      bozo
      turbulence 0.65
      octaves 6
      omega 0.7
      lambda 2
      color_map { 
	[0.0 0.2 color White*2 color White*2]
	[0.21 0.89 color White*1.5 color White*1.5]
	[0.90 1.0 color White color White]
      }
      scale 1.5
    }
    finish { conserve_energy ambient 0.00 diffuse 1.0 }
  }