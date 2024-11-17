import pygame
import glm
from pygame.locals import *

from gl import Renderer
from model import Model
from shaders import *

def GetSceneCenter(scene):
    center = glm.vec3(0, 0, 0)
    visibleModels = 0

    for model in scene:
        if model.visible:  # Solo consideramos los modelos visibles
            center += model.translation
            visibleModels += 1

    if visibleModels > 0:
        center /= visibleModels  # Calcula el promedio de las posiciones visibles

    return center

width = 1280
height = 720

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF )
clock = pygame.time.Clock()

rend = Renderer(screen)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures)

# Gato
catModel = Model("models/cat.obj")
catModel.AddTexture("textures/cat.bmp")
catModel.AddTexture("textures/model_normal.bmp")
catModel.translation.x = -2.5
catModel.translation.y = 0
catModel.translation.z = -5.3
catModel.rotation.x = 0
catModel.rotation.y = 30
catModel.rotation.z = 0
catModel.scale.x = 1
catModel.scale.y = 1
catModel.scale.z = 1
catModel.visible = False

# Jake
jake = Model("models/jake.obj")
jake.AddTexture("textures/jake.bmp")
jake.AddTexture("textures/spidey_body_normal.png")
jake.translation.x = -2.2
jake.translation.y = 0
jake.translation.z = -3.8
jake.rotation.x = 0
jake.rotation.y = 30
jake.rotation.z = 0
jake.scale.x = 0.4
jake.scale.y = 0.4
jake.scale.z = 0.4
jake.visible = False

# Abuelo
grandpaModel = Model("models/viejo.obj")
grandpaModel.AddTexture("textures/viejo.bmp")
grandpaModel.AddTexture("textures/moon_normal.jpg")
grandpaModel.translation.x = 1
grandpaModel.translation.y = 0
grandpaModel.translation.z = -4
grandpaModel.rotation.x = 0
grandpaModel.rotation.y = -20
grandpaModel.rotation.z = 0
grandpaModel.scale.x = 2
grandpaModel.scale.y = 1
grandpaModel.scale.z = 2
grandpaModel.visible = False



# Coach
coachModel = Model("models/Coach.obj")
coachModel.AddTexture("textures/Coach.bmp")
coachModel.AddTexture("textures/spidey_body_normal.png")
coachModel.translation.x = 0
coachModel.translation.y = 0
coachModel.translation.z = -1
coachModel.rotation.x = 0
coachModel.rotation.y = -140
coachModel.rotation.z = 0
coachModel.scale.x = 2
coachModel.scale.y = 1
coachModel.scale.z = 2
coachModel.visible = False


plane = Model("models/plane.obj")
plane.AddTexture("textures/muro.jpg")
plane.translation.x = 0
plane.translation.y = 1
plane.translation.z = -6
plane.rotation.y = 0
plane.rotation.x = 90
plane.rotation.z = 180
plane.scale.x = 5
plane.scale.y = 5
plane.scale.z = 2
plane.visible = True
plane.InvertNormals()

floor = Model("models/plane.obj")
floor.AddTexture("textures/vias.jpg")
floor.translation.x = 0
floor.translation.y = 0
floor.translation.z = -3
floor.rotation.y = 0
floor.rotation.x = 0
floor.rotation.z = 180
floor.scale.x = 5
floor.scale.y = 5
floor.scale.z = 7
floor.visible = True
floor.InvertNormals()

rend.scene.append(floor)
rend.scene.append(catModel)
rend.scene.append(grandpaModel)
rend.scene.append(jake)
rend.scene.append(coachModel)
rend.scene.append(plane)

vShader = vertex_shader
fShader = fragment_shader

camDistance = 7
camAngle = -30
camAngleY = 10


modelIndex = 0

rend.SetShaders(vShader, fShader)

isRunning = True

while isRunning:
	
	deltaTime = clock.tick(60) / 1000
	
	keys = pygame.key.get_pressed()
	mouseVel = pygame.mouse.get_rel()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
			
		elif event.type == pygame.MOUSEWHEEL:

			if event.y < 0 and camDistance < 10:
				camDistance -= event.y * deltaTime * 10

			if event.y > 0 and camDistance > 2:
				camDistance -= event.y * deltaTime * 10

		# Modificación en la lógica de cambio de modelo
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[2]:
				modelIndex += 1
				modelIndex %= (len(rend.scene) + 1)  # Añadir un estado adicional para mostrar todos los modelos

				if modelIndex == len(rend.scene):
					# Mostrar todos los modelos
					for model in rend.scene:
						model.visible = True
				else:
					# Mostrar solo el modelo seleccionado
					for i in range(len(rend.scene)):
						rend.scene[i].visible = (i == modelIndex)
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_SPACE:
				rend.ToggleFilledMode()
				
			# Vertex Shaders
			elif event.key == pygame.K_1:
				vShader = animated_vertex_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_2:
				vShader = wave_vertex_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_3:
				vShader = pulsating_vertex_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_4:
				vShader = explosion_vertex_shader
				rend.SetShaders(vShader, fShader)
				
			# Fragment Shaders
			elif event.key == pygame.K_5:
				fShader = fire_fragment_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_6:
				fShader = pulsating_fragment_shader
				rend.SetShaders(vShader, fShader)			
				
			elif event.key == pygame.K_7:
				fShader = glass_fragment_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_8:
				fShader = high_fragment_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_9:
				fShader = scaner_fragment_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_0:
				fShader = normal_mapping_shader
				rend.SetShaders(vShader, fShader)
				

	if keys[K_LEFT]:
		rend.pointLight.x -= 1 * deltaTime
		
	if keys[K_RIGHT]:
		rend.pointLight.x += 1 * deltaTime
		
	if keys[K_UP]:
		rend.pointLight.z -= 1 * deltaTime
		
	if keys[K_DOWN]:
		rend.pointLight.z += 1 * deltaTime
		
	if keys[K_PAGEUP]:
		rend.pointLight.y += 1 * deltaTime
		
	if keys[K_PAGEDOWN]:
		rend.pointLight.y -= 1 * deltaTime
		

	if keys[K_a]:
		camAngle -= 45 * deltaTime
		
	if keys[K_d]:
		camAngle += 45 * deltaTime
		
	if keys[K_w]:
		if camDistance > 2:
			camDistance -= 2 * deltaTime
		
	if keys[K_s]:
		if camDistance < 10:
			camDistance += 2 * deltaTime
			
	if keys[K_q]:
		if rend.camera.position.y < 2:
			rend.camera.position.y += 5 * deltaTime
		
	if keys[K_e]:
		if rend.camera.position.y > -2:
			rend.camera.position.y -= 5 * deltaTime
			

	if pygame.mouse.get_pressed()[0]:
		camAngle -= mouseVel[0] * deltaTime * 5
		
		if mouseVel[1] > 0 and rend.camera.position.y < 2:
			rend.camera.position.y += mouseVel[1] * deltaTime
			
		if mouseVel[1] < 0 and rend.camera.position.y > -2:
			rend.camera.position.y += mouseVel[1] * deltaTime

	if modelIndex < len(rend.scene):
		targetModel = rend.scene[modelIndex]  # Selecciona el modelo visible
		rend.camera.Orbit(targetModel.translation, camDistance, camAngle)
		rend.camera.LookAt(targetModel.translation)
	else:
		sceneCenter = GetSceneCenter(rend.scene)  # Calcula el centro dinámico
		rend.camera.Orbit(sceneCenter, camDistance, camAngle)
		rend.camera.LookAt(sceneCenter)

	rend.Render()

	rend.time += deltaTime
	pygame.display.flip()
	
pygame.quit()
