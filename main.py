# cd C:\Users\anton_mc03yx6\Documents\GitHub\map-maker
#name generation (archipelago, peninsula, strait, etc)
#auto generate terrain
import pygame, os

pygame.init()
width 		= 1280
height 		= 720
resolution	= 40
screen 		= pygame.display.set_mode((width,height))

class World:
	def __init__(self):
		#initialize the world/map-instance
		self.chart = [["water" for y in range(int(height/resolution+1))] for x in range(int(width/resolution+1))]
		self.current = 'land'

	def update(self):
		#loop through the map and update the colors
		for x in range(0,len(self.chart)):
			for y in range(0,len(self.chart[x])):
				screen.blit(image_dict["water"], (x*resolution, y*resolution))

				if self.chart[x][y] == "land":
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
						screen.blit(image_dict["%s_center" % self.current], (x*resolution, y*resolution))

					elif beaches == 1:
						#sides
						if self.chart[x-1][y] == "water":
							screen.blit(image_dict["%s_side" % self.current], (x*resolution, y*resolution))
						elif self.chart[x+1][y] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.current], 180), (x*resolution, y*resolution))
						elif self.chart[x][y-1] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.current], -90), (x*resolution, y*resolution))
						elif self.chart[x][y+1] == "water":
							screen.blit(rot_center(image_dict["%s_side" % self.current], 90), (x*resolution, y*resolution))

					elif beaches == 2:
						#corners
						if (self.chart[x-1][y] == "water") and (self.chart[x][y-1] == "water"):
							screen.blit(image_dict["%s_corner" % self.current], (x*resolution, y*resolution))
						elif (self.chart[x][y-1] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.current], -90), (x*resolution, y*resolution))
						elif (self.chart[x+1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.current], 180), (x*resolution, y*resolution))
						elif (self.chart[x-1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_corner" % self.current], 90), (x*resolution, y*resolution))
						#bridges
						elif (self.chart[x-1][y] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(image_dict["%s_bridge" % self.current], (x*resolution, y*resolution))
						elif (self.chart[x][y-1] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(image_dict["%s_bridge" % self.current], 90), (x*resolution, y*resolution))

					elif beaches == 3:
						if self.chart[x][y+1] == "land":
							screen.blit(image_dict["%s_peninsula" % self.current], (x*resolution, y*resolution))
						elif self.chart[x+1][y] == "land":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.current], 90), (x*resolution, y*resolution))
						elif self.chart[x][y-1] == "land":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.current], 180), (x*resolution, y*resolution))
						elif self.chart[x-1][y] == "land":
							screen.blit(rot_center(image_dict["%s_peninsula" % self.current], 270), (x*resolution, y*resolution))
					elif beaches == 4:
						#islands
						screen.blit(image_dict["%s_island" % self.current], (x*resolution, y*resolution))

	def click(self, pos_x, pos_y):
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = self.current

	def rightClick(self, pos_x, pos_y):
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = "water"

	def desertClick(self):
		self.current = "desert"

def main():
	done = False
	#create the world/map-instance
	chartInstance = World()
	chartInstance.update()

	while not done:
		for event in pygame.event.get():
			#handle the "x"/close-button
			if event.type == pygame.QUIT:
				done = True
			#handle mos click pos
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos_x, pos_y = pygame.mouse.get_pos()
				if event.button == 1:
					chartInstance.click(pos_x, pos_y)
				elif event.button == 3:
					chartInstance.rightClick(pos_x, pos_y)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					chartInstance.desertClick()

		chartInstance.update()
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

image_dict = load_images('sprites')
main()