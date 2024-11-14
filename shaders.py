
# Vertex Shaders

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;

out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;
out mat3 TBN;

uniform float time;
uniform vec3 scale;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    outPosition = modelMatrix * vec4(position, 1.0);
	gl_Position = projectionMatrix * viewMatrix * outPosition;
    
    outTexCoords = texCoords;
    outNormals = normalize(vec3(modelMatrix * vec4(normal,    0.0)));
    
    vec3 T = normalize(vec3(modelMatrix * vec4(tangent,    0.0)));
    T = normalize(T - dot(T, outNormals) * outNormals);
    vec3 B = cross(outNormals, T);
    TBN = mat3(T, B, outNormals);    
}
'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;


out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;
out mat3 TBN;

uniform float time;
uniform vec3 scale;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    vec3 blowup = mix(vec3(0,0,0), 0.5/scale, (sin(time) + 1 ) / 2);
    outPosition = modelMatrix * vec4(position + normal * blowup, 1.0);
	gl_Position = projectionMatrix * viewMatrix * outPosition;
    
    outTexCoords = texCoords;
    outNormals = normalize(vec3(modelMatrix * vec4(normal,    0.0)));
    
    vec3 T = normalize(vec3(modelMatrix * vec4(tangent,    0.0)));
    T = normalize(T - dot(T, outNormals) * outNormals);
    vec3 B = cross(outNormals, T);
    TBN = mat3(T, B, outNormals);    
}
'''

jelly_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;


out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;
out mat3 TBN;

uniform float time;
uniform vec3 scale;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    float displacement = sin(time + position.x + position.z) * 0.1;
    outPosition = modelMatrix * vec4(position + vec3(0, displacement / scale.y,0), 1.0);
	gl_Position = projectionMatrix * viewMatrix * outPosition;
    
    outTexCoords = texCoords;
    outNormals = normalize(vec3(modelMatrix * vec4(normal,    0.0)));
    
    vec3 T = normalize(vec3(modelMatrix * vec4(tangent,    0.0)));
    T = normalize(T - dot(T, outNormals) * outNormals);
    vec3 B = cross(outNormals, T);
    TBN = mat3(T, B, outNormals);    
}
'''

turbulence_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;


out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;
out mat3 TBN;

uniform float time;
uniform vec3 scale;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

vec3 mod289(vec3 x)
{
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 mod289(vec4 x)
{
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 permute(vec4 x)
{
  return mod289(((x*34.0)+10.0)*x);
}

vec4 taylorInvSqrt(vec4 r)
{
  return 1.79284291400159 - 0.85373472095314 * r;
}

vec3 fade(vec3 t) {
  return t*t*t*(t*(t*6.0-15.0)+10.0);
}

// Classic Perlin noise
float cnoise(vec3 P)
{
  vec3 Pi0 = floor(P); // Integer part for indexing
  vec3 Pi1 = Pi0 + vec3(1.0); // Integer part + 1
  Pi0 = mod289(Pi0);
  Pi1 = mod289(Pi1);
  vec3 Pf0 = fract(P); // Fractional part for interpolation
  vec3 Pf1 = Pf0 - vec3(1.0); // Fractional part - 1.0
  vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
  vec4 iy = vec4(Pi0.yy, Pi1.yy);
  vec4 iz0 = Pi0.zzzz;
  vec4 iz1 = Pi1.zzzz;

  vec4 ixy = permute(permute(ix) + iy);
  vec4 ixy0 = permute(ixy + iz0);
  vec4 ixy1 = permute(ixy + iz1);

  vec4 gx0 = ixy0 * (1.0 / 7.0);
  vec4 gy0 = fract(floor(gx0) * (1.0 / 7.0)) - 0.5;
  gx0 = fract(gx0);
  vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
  vec4 sz0 = step(gz0, vec4(0.0));
  gx0 -= sz0 * (step(0.0, gx0) - 0.5);
  gy0 -= sz0 * (step(0.0, gy0) - 0.5);

  vec4 gx1 = ixy1 * (1.0 / 7.0);
  vec4 gy1 = fract(floor(gx1) * (1.0 / 7.0)) - 0.5;
  gx1 = fract(gx1);
  vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
  vec4 sz1 = step(gz1, vec4(0.0));
  gx1 -= sz1 * (step(0.0, gx1) - 0.5);
  gy1 -= sz1 * (step(0.0, gy1) - 0.5);

  vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
  vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
  vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
  vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
  vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
  vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
  vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
  vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

  vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
  g000 *= norm0.x;
  g010 *= norm0.y;
  g100 *= norm0.z;
  g110 *= norm0.w;
  vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
  g001 *= norm1.x;
  g011 *= norm1.y;
  g101 *= norm1.z;
  g111 *= norm1.w;

  float n000 = dot(g000, Pf0);
  float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
  float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
  float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
  float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
  float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
  float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
  float n111 = dot(g111, Pf1);

  vec3 fade_xyz = fade(Pf0);
  vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
  vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
  float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x); 
  return 2.2 * n_xyz;
}

// Classic Perlin noise, periodic variant
float pnoise(vec3 P, vec3 rep)
{
  vec3 Pi0 = mod(floor(P), rep); // Integer part, modulo period
  vec3 Pi1 = mod(Pi0 + vec3(1.0), rep); // Integer part + 1, mod period
  Pi0 = mod289(Pi0);
  Pi1 = mod289(Pi1);
  vec3 Pf0 = fract(P); // Fractional part for interpolation
  vec3 Pf1 = Pf0 - vec3(1.0); // Fractional part - 1.0
  vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
  vec4 iy = vec4(Pi0.yy, Pi1.yy);
  vec4 iz0 = Pi0.zzzz;
  vec4 iz1 = Pi1.zzzz;

  vec4 ixy = permute(permute(ix) + iy);
  vec4 ixy0 = permute(ixy + iz0);
  vec4 ixy1 = permute(ixy + iz1);

  vec4 gx0 = ixy0 * (1.0 / 7.0);
  vec4 gy0 = fract(floor(gx0) * (1.0 / 7.0)) - 0.5;
  gx0 = fract(gx0);
  vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
  vec4 sz0 = step(gz0, vec4(0.0));
  gx0 -= sz0 * (step(0.0, gx0) - 0.5);
  gy0 -= sz0 * (step(0.0, gy0) - 0.5);

  vec4 gx1 = ixy1 * (1.0 / 7.0);
  vec4 gy1 = fract(floor(gx1) * (1.0 / 7.0)) - 0.5;
  gx1 = fract(gx1);
  vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
  vec4 sz1 = step(gz1, vec4(0.0));
  gx1 -= sz1 * (step(0.0, gx1) - 0.5);
  gy1 -= sz1 * (step(0.0, gy1) - 0.5);

  vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
  vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
  vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
  vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
  vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
  vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
  vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
  vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

  vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
  g000 *= norm0.x;
  g010 *= norm0.y;
  g100 *= norm0.z;
  g110 *= norm0.w;
  vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
  g001 *= norm1.x;
  g011 *= norm1.y;
  g101 *= norm1.z;
  g111 *= norm1.w;

  float n000 = dot(g000, Pf0);
  float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
  float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
  float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
  float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
  float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
  float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
  float n111 = dot(g111, Pf1);

  vec3 fade_xyz = fade(Pf0);
  vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
  vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
  float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x); 
  return 2.2 * n_xyz;
}

float turbulence( vec3 p ) {

  float w = 100.0;
  float t = -.5;

  for (float f = 1.0 ; f <= 10.0 ; f++ ){
    float power = pow( 2.0, f );
    t += abs( pnoise( vec3( power * p ), vec3( 10.0, 10.0, 10.0 ) ) / power );
  }

  return t;

}

void main()
{
    float noise = turbulence( .5 * normal + time );
    float b = pnoise( 0.05 * position + vec3( 2.0 * time ), vec3( 100.0 ) );
    float displacement = (-noise + b) / 10;
    
    
    outPosition = modelMatrix * vec4(position + normal * displacement / scale, 1.0);
	gl_Position = projectionMatrix * viewMatrix * outPosition;
    
    outTexCoords = texCoords;
    outNormals = normalize(vec3(modelMatrix * vec4(normal,    0.0)));
    
    vec3 T = normalize(vec3(modelMatrix * vec4(tangent,    0.0)));
    T = normalize(T - dot(T, outNormals) * outNormals);
    vec3 B = cross(outNormals, T);
    TBN = mat3(T, B, outNormals);    
}
'''

# Fragment Shaders

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(outNormals, lightDir) , 0) + ambientLight;
	fragColor = texture(tex0, outTexCoords) * intensity;
}
'''

toon_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;

uniform sampler2D tex0;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = dot(outNormals, lightDir);
    
    if (intensity < 0.33)
		intensity = 0.2;
    else if (intensity < 0.66)
		intensity = 0.6;
    else
		intensity = 1.0;
        
	fragColor = texture(tex0, outTexCoords) * intensity;
}
'''

negative_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;

uniform sampler2D tex0;

out vec4 fragColor;

void main()
{
	fragColor = 1 - texture(tex0, outTexCoords);
}
'''

mirror_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;

uniform vec3 pointLight;
uniform vec3 cameraPos;
uniform samplerCube skybox;

out vec4 fragColor;

void main()
{          
    vec3 L = normalize(pointLight - outPosition.xyz);
    vec3 V = normalize(cameraPos - outPosition.xyz);
    vec3 H = normalize(V+L);
    float spec = pow(max(dot(H, outNormals), 0.0), 32.0);
    
    vec3 I = normalize(outPosition.xyz - cameraPos);
    vec3 R = reflect(I, normalize(outNormals));
    fragColor = vec4(texture(skybox, R).rgb, 1.0) + spec;
}
'''

sapphire_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;

uniform vec3 pointLight;
uniform vec3 cameraPos;
uniform samplerCube skybox;

out vec4 fragColor;

vec3 fresnelSchlick(float cosTheta, vec3 F0)
{
    return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}

void main()
{   
    vec3 L = normalize(pointLight - outPosition.xyz);
    vec3 V = normalize(cameraPos - outPosition.xyz);
    vec3 H = normalize(V+L);
    float spec = pow(max(dot(H, outNormals), 0.0), 32.0);  
    
    
    float ratio = 1.00 / 1.757;
    vec3 I = normalize(outPosition.xyz - cameraPos);
    vec3 reflectVector = reflect(I, normalize(outNormals));
    vec3 refractVector = refract(I, normalize(outNormals), ratio);
    
    float Kr = fresnelSchlick( dot(V, outNormals), vec3(0.08))[0];
    
    vec4 reflectColor = (vec4(texture(skybox, reflectVector).rgb, 1.0) + spec) * Kr;
    vec4 refractColor = vec4(texture(skybox, refractVector).rgb, 1.0) * (1 - Kr);
    
    fragColor = vec4(0.06, 0.32, 0.72,1.0) * (reflectColor + refractColor);
}  
'''

normal_mapping_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;
in mat3 TBN;

uniform sampler2D tex0;
uniform sampler2D tex1;

uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main()
{
    vec3 normal = texture(tex1, outTexCoords).rgb;
    normal = normal * 2.0 - 1.0;
    normal = normalize(TBN * normal);

    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(normal, lightDir) , 0) + ambientLight;
	fragColor = texture(tex0, outTexCoords) * intensity;
}
'''

### Nuevos Shaders ###

animated_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec3 FragPos;  // Pasamos la posición del fragmento en espacio mundo

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Animación del vértice
    vec3 animatedPosition = position;
    animatedPosition.y += sin(position.x * 5.0 + time) * 0.1;

    // Calcular FragPos en espacio mundo (solo con modelMatrix)
    FragPos = vec3(modelMatrix * vec4(animatedPosition, 1.0)); 

    // Pasar normales al espacio mundo
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;

    // Pasar coordenadas de textura
    outTexCoords = texCoords;

    // Calcular la posición final del vértice
    gl_Position = projectionMatrix * viewMatrix * vec4(FragPos, 1.0);
}
'''

gradient_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec3 FragPos;

out vec4 fragColor;

uniform sampler2D tex;

void main()
{
    // Usamos la coordenada Y de FragPos (en espacio mundo) para determinar el color
    float height = FragPos.y;
    vec3 color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), height);

    // Combinar el color del degradado con la textura
    fragColor = vec4(color, 1.0) * texture(tex, outTexCoords);
}
'''

pulsating_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec3 FragPos;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Efecto de pulsación usando seno del tiempo
    float scale = 1.0 + 0.1 * sin(time * 2.0);
    vec3 pulsatingPosition = position * scale;

    // Calcular FragPos en espacio mundo
    FragPos = vec3(modelMatrix * vec4(pulsatingPosition, 1.0));

    // Pasar normales al espacio mundo
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;

    // Pasar coordenadas de textura
    outTexCoords = texCoords;

    // Calcular la posición final del vértice
    gl_Position = projectionMatrix * viewMatrix * vec4(FragPos, 1.0);
}
'''

pulsating_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec3 FragPos;

out vec4 fragColor;

uniform sampler2D tex;
uniform float time;

void main()
{
    // Cambiar el color entre azul y amarillo usando el tiempo
    vec3 color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 1.0, 0.0), (sin(time * 2.0) + 1.0) / 2.0);

    // Combinar el color del pulsado con la textura
    fragColor = vec4(color, 1.0) * texture(tex, outTexCoords);
}
'''

scan_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 FragPos;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    FragPos = vec3(modelMatrix * vec4(position, 1.0));
    outTexCoords = texCoords;

    // Transformación final de la posición del vértice
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
}
'''

scan_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 FragPos;

out vec4 fragColor;

uniform sampler2D tex;
uniform float time;

void main()
{
    // Efecto de escaneo basado en la coordenada Y y el tiempo
    float frequency = 5.0; // Ajusta la frecuencia de la franja de escaneo
    float scanLine = sin(time + FragPos.y * frequency) * 0.5 + 0.5;

    // Color de escaneo (blanco brillante) y mezcla con el color de la textura
    vec3 scanColor = mix(texture(tex, outTexCoords).rgb, vec3(1.0, 1.0, 1.0), scanLine);

    // Color final del fragmento
    fragColor = vec4(scanColor, 1.0);
}
'''

# Se usa con vertex_shader
high_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec3 FragPos;

out vec4 fragColor;

uniform sampler2D tex;

void main()
{
    // Usa la posición Y de FragPos para generar el degradado
    float height = FragPos.y;
    vec3 color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), height);

    // Combina el color del degradado con la textura
    fragColor = vec4(color, 1.0) * texture(tex, outTexCoords);
}
'''

scaner_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 FragPos;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    FragPos = vec3(modelMatrix * vec4(position, 1.0));
    outTexCoords = texCoords;

    // Transformación final de la posición del vértice
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
}
'''

scaner_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 FragPos;

out vec4 fragColor;

uniform sampler2D tex;
uniform float time;

void main()
{
    // Efecto de escaneo basado en la coordenada Y y el tiempo
    float frequency = 5.0; // Ajusta la frecuencia de la franja de escaneo
    float scanLine = sin(time + FragPos.y * frequency) * 0.5 + 0.5;

    // Color de escaneo (blanco brillante) y mezcla con el color de la textura
    vec3 scanColor = mix(texture(tex, outTexCoords).rgb, vec3(1.0, 1.0, 1.0), scanLine);

    // Color final del fragmento
    fragColor = vec4(scanColor, 1.0);
}
'''


