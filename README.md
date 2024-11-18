# Proyecto: Diorama 3D en OpenGL

## Descripción del Proyecto

Este proyecto presenta un **Diorama 3D** desarrollado en **Python** utilizando **OpenGL** y **pygame**. El objetivo es demostrar los conocimientos adquiridos en la materia mediante la creación de una escena tridimensional interactiva con modelos, texturas, shaders personalizados, cámara dinámica y elementos visuales atractivos. El diorama incluye personajes, un piso y una pared texturizada, todo ambientado con un skybox y música de fondo para una experiencia inmersiva.

## Características

- **Modelos 3D cargados**:
  - Cuatro modelos diferentes posicionados dentro de la escena: un gato, un abuelo, un personaje estilo caricatura y un entrenador.
  - Pared y piso como base del diorama con texturas detalladas.
- **Cámara Dinámica**:
  - Movimiento orbital, zoom, y desplazamiento vertical mediante teclado y mouse.
  - Cambio de enfoque entre modelos visibles.
- **Shaders Personalizados**:
  - Uso creativo de vertex y fragment shaders para deformaciones, animaciones y efectos visuales complejos.
- **Skybox**:
  - Entorno inmersivo con texturas personalizadas.
- **Música de Fondo**:
  - Pista en bucle que mejora la ambientación del diorama.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Abysswalkr/Proyecto3--OpenGL.git
   ```

2. Instalar las dependencias necesarias:
   ```bash
   pip install pygame PyGLM
   ```

3. Colocar las texturas y modelos en las carpetas correspondientes dentro del proyecto.

4. Ejecutar el proyecto:
   ```bash
   python RendererOpenGL.py
   ```

## Estructura del Proyecto

- **gl.py**: Configuración base del renderizador, manejo de proyección y luces.
- **model.py**: Clase para cargar y renderizar modelos 3D desde archivos `.obj` con texturas.
- **obj.py**: Parser para cargar y procesar modelos en formato OBJ.
- **shaders.py**: Definición de shaders personalizados, tanto para vértices como para fragmentos.
- **RendererOpenGL.py**: Archivo principal que configura la escena, los modelos, la cámara, y el renderizado.
- **camera.py**: Implementación de la cámara para manejar los movimientos en la escena.
- **skybox.py**: Clase para crear un entorno cúbico inmersivo alrededor de la escena.
- **buffer.py**: Manejo eficiente de buffers para el renderizado en OpenGL.

## Uso

### Controles de Cámara
- **Teclado**:
  - `W/S`: Acercar/Alejar la cámara.
  - `A/D`: Rotar horizontalmente alrededor de la escena.
  - `Q/E`: Mover la cámara hacia arriba o hacia abajo.
- **Mouse**:
  - Mantén presionado el botón izquierdo para rotar la cámara.
  - Usa la rueda para hacer zoom.
- **Cambio de Modelos**:
  - Haz clic derecho para alternar entre los modelos visibles.

### Cambiar Shaders
- **Vertex Shaders**:
  - Presiona `1-4` para alternar entre diferentes efectos de vértices.
- **Fragment Shaders**:
  - Presiona `5-9` para cambiar entre distintos efectos visuales.

## Modelos y Posiciones

1. **CatModel**: Modelo de un gato, posicionado a la izquierda de la pared.
2. **JakeModel**: Personaje animado estilo caricatura, colocado al frente.
3. **GrandpaModel**: Abuelo modelado con un estilo detallado, a la derecha.
4. **CoachModel**: Entrenador musculoso, en la parte trasera de la escena.
5. **Pared**: Pared texturizada al fondo del escenario con un diseño graffiti.
6. **Piso**: Plano inferior con textura de madera que sirve como base del diorama.

## Iluminación

- Fuente de luz puntual colocada estratégicamente para iluminar los modelos y el escenario de manera uniforme.
- Iluminación dinámica ajustable mediante teclas (`Arrow keys` para mover la luz en el espacio).

## Música

- Pista en bucle configurada con **pygame.mixer** para mejorar la experiencia del usuario.

## Ejemplo de Código: Añadir un Modelo con Textura

```python
newModel = Model("models/tree.obj")
newModel.AddTexture("textures/tree_texture.jpg")
newModel.translation = glm.vec3(2, 0, -4)
newModel.scale = glm.vec3(0.5, 0.5, 0.5)
newModel.visible = True
rend.scene.append(newModel)
```

## Capturas de Pantalla

Captura de la escena con los modelos visibles y shaders aplicados:

![Captura de pantalla 2024-11-18 123304](https://github.com/user-attachments/assets/fa77bee8-3b6b-43a2-917c-18182a15377a)
![Captura de pantalla 2024-11-18 123250](https://github.com/user-attachments/assets/9c95e82b-db37-457d-a349-9e2e1e4e835c)
![Captura de pantalla 2024-11-18 123245](https://github.com/user-attachments/assets/75566df2-1db9-434f-b092-38396f12c813)
![Captura de pantalla 2024-11-18 123234](https://github.com/user-attachments/assets/380d0f10-7e1b-47b1-86da-898a2feb176c)
![Captura de pantalla 2024-11-18 123224](https://github.com/user-attachments/assets/f0d4f210-cbc3-4ef0-a9cd-94127daabf9d)

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias, abre un issue o envía un pull request. 😊