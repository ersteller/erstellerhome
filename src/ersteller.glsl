#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

#define GRID vec2(15,15)
#define BITS 1.

// only 1D arrays but at least with constructor ;(
const int[] aiErsteller = int[] (
      0,0,0,0,0,0,0,
	  0,0,0,1,0,0,0,
	  0,0,1,1,1,0,0,
	  0,0,0,1,0,0,0,
	  0,0,0,0,0,0,0,
	  1,1,1,1,1,1,1,
	  1,0,1,1,1,0,1,
	  1,0,1,1,1,0,1,
      0,0,1,1,1,0,0,
	  0,0,1,1,1,0,0,
	  0,0,1,0,1,0,0,
	  0,0,1,0,1,0,0,
	  0,0,1,0,1,0,0,
	  0,1,1,0,1,1,0,
      0,0,0,0,0,0,0
);

const vec2 bitmap_size = vec2(7, 15);


float random(float co){
    return fract(sin(co)*33333.);
}

vec3 getRandomGridColor( in vec2 uv , in vec2 grid_size, float bits ){
    int frac = int(fract(iTime)*4095.);
    vec2 fetch_pos = vec2( uv * grid_size);
    int idx = int(fetch_pos.x) + ( int(grid_size.y) - 1 - int(fetch_pos.y)) * int(grid_size.x);
    float seed = float( frac + idx);
    return vec3( floor(random(3. * seed)* (bits+1.))  / bits ,
        floor(random(11. * seed)* (bits+1.)) / bits ,
        floor(random(13. * seed)* (bits+1.)) / bits );
}

// input 0 to 1
vec3 getValueXY( in vec2 uv  )
{
	float value = 1.;
    vec3 col ;
    // transform to grid pos
    vec2 fetch_pos = vec2( uv * bitmap_size.y );
    // check if in array range
	if( fetch_pos.x >= 0.  && fetch_pos.y >= 0.
		&& fetch_pos.x < bitmap_size.x  && fetch_pos.y < bitmap_size.y  )
	{
        // convert x y to index 
		int idx = int(fetch_pos.x) + ( int(bitmap_size.y) - 1 - int(fetch_pos.y)) * int(bitmap_size.x);
		value = float(1 - aiErsteller[idx]); // invert color value of 1 means black
        
	} else value = 1.;  // outer color;
	return vec3(value);
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // normalize coord (and force square grid aspect ratio)
    vec2 uv = vec2(fragCoord.x /iResolution.y,fragCoord.y/iResolution.y);
    // shift to center
    uv.x = uv.x-0.6;
    uv.y = uv.y-0.;
    
    // emulate VHS-Tape pause artifact
    float amp = sin((uv.y + iTime*0.5)*5.) - 0.95;
    if (amp > 0.){
        uv.x -= amp*.5*sin((- uv.y*10.+ iTime)*5.)*0.5;
    }

    vec3 col = getValueXY(uv); // get color value from array
    
    // random color noise on the artifact
    if (amp > 0. && col.x == 0.){
        col = getRandomGridColor(uv, GRID, BITS);
    }

    fragColor = vec4(col, 1.0);
}
