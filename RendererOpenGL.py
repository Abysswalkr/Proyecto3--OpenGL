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

catModel = Model("models/cat.obj")
catModel.AddTexture("textures/cat.bmp")
catModel.AddTexture("textures/model_normal.bmp")
catModel.translation.z = -5
catModel.scale.x = 2
catModel.scale.y = 2
catModel.scale.z = 2

grandpaModel = Model("models/viejo.obj")
grandpaModel.AddTexture("textures/viejo.bmp")
grandpaModel.AddTexture("textures/moon_normal.jpg")
grandpaModel.translation.z = -5
grandpaModel.scale.x = 2
grandpaModel.scale.y = 1
grandpaModel.scale.z = 2
grandpaModel.visible = False

jake = Model("models/jake.obj")
jake.AddTexture("textures/jake.bmp")
jake.AddTexture("textures/spidey_body_normal.png")
jake.translation.z = -5
jake.scale.x = 2
jake.scale.y = 1
jake.scale.z = 2
jake.visible = False

coachModel = Model("models/Coach.obj")
coachModel.AddTexture("textures/Coach.bmp")
coachModel.AddTexture("textures/spidey_body_normal.png")
coachModel.translation.z = -5
coachModel.scale.x = 2
coachModel.scale.y = 1
coachModel.scale.z = 2
coachModel.visible = False

rend.scene.append(catModel)
rend.scene.append(grandpaModel)
rend.scene.append(jake)
rend.scene.append(coachModel)

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
				
	rend.camera.Orbit( catModel.translation, camDistance, camAngle)
	rend.camera.LookAt( catModel.translation )

	rend.Render()

	rend.time += deltaTime
	pygame.display.flip()
	
pygame.quit()
