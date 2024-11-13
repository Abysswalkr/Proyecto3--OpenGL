import pygame
from pygame.locals import *

from gl import Renderer
from model import Model
from shaders import *


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

faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.AddTexture("textures/model_normal.bmp")
faceModel.translation.z = -5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2

moonModel = Model("models/sphere.obj")
moonModel.AddTexture("textures/moon_diffuse.jpg")
moonModel.AddTexture("textures/moon_normal.jpg")
moonModel.translation.z = -5
moonModel.scale.x = 0.005
moonModel.scale.y = 0.005
moonModel.scale.z = 0.005
moonModel.visible = False

spidey = Model("models/spidey.obj")
spidey.AddTexture("textures/spidey_body_diff.png")
spidey.AddTexture("textures/spidey_body_normal.png")
spidey.translation.z = -5
spidey.rotation.y = 180
spidey.scale.x = 0.03
spidey.scale.y = 0.03
spidey.scale.z = 0.03
spidey.visible = False

rend.scene.append(faceModel)
rend.scene.append(moonModel)
rend.scene.append(spidey)

vShader = vertex_shader
fShader = fragment_shader

camDistance = 5
camAngle = 0
camAngleY = 0


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
				
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[2]:
				modelIndex += 1
				modelIndex %= len(rend.scene)
				for i in range(len(rend.scene)):
					rend.scene[i].visible = i == modelIndex
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_SPACE:
				rend.ToggleFilledMode()
				
			# Vertex Shaders
			elif event.key == pygame.K_1:
				vShader = vertex_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_2:
				vShader = fat_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_3:
				vShader = jelly_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_4:
				vShader = turbulence_shader
				rend.SetShaders(vShader, fShader)
				
			# Fragment Shaders
			elif event.key == pygame.K_5:
				fShader = fragment_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_6:
				fShader = toon_shader
				rend.SetShaders(vShader, fShader)			
				
			elif event.key == pygame.K_7:
				fShader = negative_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_8:
				fShader = mirror_shader
				rend.SetShaders(vShader, fShader)
				
			elif event.key == pygame.K_9:
				fShader = sapphire_shader
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
				
	rend.camera.Orbit( faceModel.translation, camDistance, camAngle)
	rend.camera.LookAt( faceModel.translation )

	rend.Render()

	rend.time += deltaTime
	pygame.display.flip()
	
pygame.quit()
