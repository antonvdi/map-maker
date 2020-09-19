# cd C:\Users\anton_mc03yx6\Documents\GitHub\map-maker
#name generation (archipelago, peninsula, strait, etc)
#auto generate terrain (perlin noise)
#1. improve render code
import pygame, os, noise
from random import randint

pygame.init()
width 		= 1280
height 		= 720
resolution	= 40
screen 		= pygame.display.set_mode((width,height))

class World:
	def __init__(self):
		#initialize the world/map-instance. The chart is 1 tile bigger than what is visible, to avoid IndexErrors when rendering.
		self.chart = [["water" for y in range(int(height/resolution+1))] for x in range(int(width/resolution+1))]
		self.current = "land"

	def render(self):
		#iterate through the map
		for x in range(0,len(self.chart)-1):
			for y in range(0,len(self.chart[x])-1):
				#make the tile water per default. 
				screen.blit(image_dict["water"], (x*resolution, y*resolution))
				if self.chart[x][y] != "water":
					#find out which tile to use by looking at the number of beaches
					beaches = 0
					if self.chart[x-1][y] == "water":
						beaches += 1
					if self.chart[x+1][y] == "water":
						beaches += 1
					if self.chart[x][y-1] == "water":
						beaches += 1
					if self.chart[x][y+1] == "water":
						beaches += 1

					#find out how to rotate the tile and print it on the screen
					if beaches == 0:
						#center
						screen.blit(image_dict["%s_center" % self.chart[x][y]], 
									(x*resolution-20, y*resolution-20))

					elif beaches == 1:
						#sides
						if self.chart[x-1][y] == "water":
							screen.blit(image_dict["%s_side" % self.chart[x][y]], 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x+1][y] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.chart[x][y]], 180), 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x][y-1] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.chart[x][y]], -90), 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x][y+1] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.chart[x][y]], 90), 
										(x*resolution-20, y*resolution-20))

					elif beaches == 2:
						#corners
						if (self.chart[x-1][y] == "water") and (self.chart[x][y-1] == "water"):
							screen.blit(image_dict["%s_corner" % self.chart[x][y]], 
										(x*resolution-20, y*resolution-20))
						elif (self.chart[x][y-1] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.chart[x][y]], -90), 
										(x*resolution-20, y*resolution-20))
						elif (self.chart[x+1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.chart[x][y]], 180), 
										(x*resolution-20, y*resolution-20))
						elif (self.chart[x-1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.chart[x][y]], 90), 
										(x*resolution-20, y*resolution-20))
						#bridges
						elif (self.chart[x-1][y] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(image_dict["%s_bridge" % self.chart[x][y]], 
										(x*resolution-20, y*resolution-20))
						elif (self.chart[x][y-1] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_bridge" % self.chart[x][y]], 90), 
										(x*resolution-20, y*resolution-20))

					elif beaches == 3:
						if self.chart[x][y+1] != "water":
							screen.blit(image_dict["%s_peninsula" % self.chart[x][y]], 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x+1][y] != "water":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.chart[x][y]], 90), 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x][y-1] != "water":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.chart[x][y]], 180), 
										(x*resolution-20, y*resolution-20))
						elif self.chart[x-1][y] != "water":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.chart[x][y]], 270), 
										(x*resolution-20, y*resolution-20))
					elif beaches == 4:
						#islands
						screen.blit(image_dict["%s_island" % self.chart[x][y]], 
									(x*resolution-20, y*resolution-20))


	def click(self, pos_x, pos_y):
		#populates the clicked position in the chart with the current land type
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = self.current

	def rightClick(self, pos_x, pos_y):
		#populates the clicked position in the chart with water
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = "water"

	def desertClick(self):
		#shuffles between the land types
		if self.current == "land":
			self.current = "desert"
		elif self.current == "desert":
			self.current = "snow"
		elif self.current == "snow":
			self.current = "land"
	def noise(self, scale, octaves, persistence, lacunarity):
		self.noisechart = [[0 for y in range(int(height/resolution+1))] for x in range(int(width/resolution+1))]
		for x in range(0,len(self.chart)-1):
			for y in range(0,len(self.chart[x])-1):
				self.noisechart[x][y] = noise.pnoise2(	x/scale,
														y/scale,
														octaves = octaves,
														persistence = persistence,
														lacunarity = lacunarity,
														repeatx = int(width/resolution+1),
														repeaty = int(height/resolution+1),
														base = randint(0,100))
				if self.noisechart[x][y] > 0.08:
					self.chart[x][y] = "land"

def main():
	done = False
	#create the world/map-instance
	chartInstance = World()
	#render the map
	chartInstance.render()

	while not done:
		for event in pygame.event.get():
			#handle the "x"/close-button
			if event.type == pygame.QUIT:
				done = True
			#handle mos click pos
			if event.type == pygame.MOUSEBUTTONDOWN:
					pos_x, pos_y = pygame.mouse.get_pos()
					#if left mouse button is pressed, create land
					if event.button == 1:
						chartInstance.click(pos_x, pos_y)
					#if right mousebutton is pressed, remove land
					elif event.button == 3:
						chartInstance.rightClick(pos_x, pos_y)
			#if space is clicked, shuffle current type
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					chartInstance.desertClick()
				if event.key == pygame.K_p:
					chartInstance.noise(100, 6, 0.5, 2.0)

		#render map and update screen
		chartInstance.render()
		pygame.display.update()

def rot_center(image, angle):
	#rotate an image while keeping its center and size
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

def load_images(path_to_directory):
	#Load images and return them as a dict.
	image_dict = {}
	for filename in os.listdir(path_to_directory):
		if filename.endswith('.png'):
			path = os.path.join(path_to_directory, filename)
			key = filename[:-4]
			image_dict[key] = pygame.image.load(path).convert_alpha()
	return image_dict

#load sprites
image_dict = load_images('sprites')
main()